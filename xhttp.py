# xhttp.py
# XHTTP Ultra با Sing-box — packet-up و stream-up
# پشتیبانی TCP و UDP (command 1 و 2)

import asyncio
import secrets
import time
from typing import Optional

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse

try:
    from speed_limit import throttle
except ImportError:
    async def throttle(uuid: str, size: int):
        return

from relay_vless import parse_vless_header

router = APIRouter()

XHTTP_BUF = 512 * 1024
SESSION_IDLE_TIMEOUT = 30
REAPER_INTERVAL = 10
TCP_CONNECT_TIMEOUT = 10.0

xhttp_sessions: dict = {}
XHTTP_LOCK = asyncio.Lock()
_reaper_task: Optional[asyncio.Task] = None


def _client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    real = request.headers.get("x-real-ip")
    if real:
        return real.strip()
    return request.client.host if request.client else "نامشخص"


# ── Reaper: پاک‌سازی سشن‌های idle ────────────────────────────────────────────
async def _reaper_loop():
    while True:
        try:
            await asyncio.sleep(REAPER_INTERVAL)
            now = time.time()
            dead = []
            async with XHTTP_LOCK:
                for sid, sess in list(xhttp_sessions.items()):
                    if now - sess.get("last_seen", 0) > SESSION_IDLE_TIMEOUT:
                        dead.append(sid)
            for sid in dead:
                await _close_session(sid)
        except asyncio.CancelledError:
            break
        except Exception:
            continue


def _ensure_reaper():
    global _reaper_task
    if _reaper_task is None or _reaper_task.done():
        try:
            _reaper_task = asyncio.create_task(_reaper_loop())
        except RuntimeError:
            pass


async def _close_session(session_id: str):
    async with XHTTP_LOCK:
        sess = xhttp_sessions.pop(session_id, None)
    if not sess:
        return
    sess["closed"] = True
    # بستن TCP writer
    w = sess.get("writer")
    if w is not None:
        try:
            w.close()
            await w.wait_closed()
        except Exception:
            pass
    # بستن UDP transport
    ut = sess.get("udp_transport")
    if ut is not None:
        try:
            ut.close()
        except Exception:
            pass
    # آنلاک کردن downstream
    try:
        sess["down_q"].put_nowait(None)
    except Exception:
        pass


# ── Downlink (SSE-like streaming) ────────────────────────────────────────────
@router.get("/xhttp-siz10/{mode}/{uuid}/{session_id}")
async def xhttp_downlink(mode: str, uuid: str, session_id: str, request: Request):
    if mode not in ("packet-up", "stream-up"):
        raise HTTPException(status_code=404, detail="unknown mode")

    from main import LINKS, LINKS_LOCK, is_link_allowed, is_ip_allowed
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    if not is_link_allowed(link):
        raise HTTPException(status_code=403, detail="not allowed")

    ip = _client_ip(request)
    if not is_ip_allowed(link, uuid, ip):
        raise HTTPException(status_code=403, detail="ip limit reached")

    _ensure_reaper()

    async with XHTTP_LOCK:
        sess = xhttp_sessions.get(session_id)
        if sess is None:
            sess = {
                "uuid": uuid,
                "mode": mode,
                "writer": None,
                "udp_transport": None,
                "udp_target": None,
                "down_q": asyncio.Queue(maxsize=256),
                "last_seen": time.time(),
                "closed": False,
                "conn_id": secrets.token_urlsafe(6),
                "first_response": True,
            }
            xhttp_sessions[session_id] = sess
        else:
            sess["last_seen"] = time.time()

    headers = {
        "content-type": "application/octet-stream",
        "cache-control": "no-store, no-cache",
        "x-accel-buffering": "no",
    }
    return StreamingResponse(_downstream_gen(sess), headers=headers)


async def _downstream_gen(sess: dict):
    try:
        while not sess.get("closed"):
            try:
                chunk = await asyncio.wait_for(sess["down_q"].get(), timeout=SESSION_IDLE_TIMEOUT)
            except asyncio.TimeoutError:
                break
            if chunk is None:
                break
            sess["last_seen"] = time.time()
            yield chunk
    finally:
        sess["closed"] = True


# ── اتصال به مقصد (TCP یا UDP) ───────────────────────────────────────────────
async def _connect_target(sess: dict, body: bytes, link: dict, session_id: str):
    """پارسر هدر و اتصال به مقصد. payload اولیه رو هم می‌فرسته."""
    try:
        command, address, port, payload = await parse_vless_header(body)
    except Exception:
        raise HTTPException(status_code=400, detail="invalid header")

    if command == 2:
        # UDP
        loop = asyncio.get_event_loop()
        udp_remote_q: asyncio.Queue = sess["down_q"]

        class _Proto(asyncio.DatagramProtocol):
            def __init__(self):
                self.transport = None

            def connection_made(self, transport):
                self.transport = transport

            def datagram_received(self, data, addr):
                # هدر VLESS در اولین پاسخ
                out = (b"\x00\x00" + data) if sess.get("first_response", True) else data
                sess["first_response"] = False
                try:
                    udp_remote_q.put_nowait(out)
                except asyncio.QueueFull:
                    pass

            def error_received(self, exc):
                pass

            def connection_lost(self, exc):
                try:
                    udp_remote_q.put_nowait(None)
                except Exception:
                    pass

        try:
            transport, proto = await asyncio.wait_for(
                loop.create_datagram_endpoint(_Proto, remote_addr=(address, port)),
                timeout=TCP_CONNECT_TIMEOUT,
            )
        except Exception:
            raise HTTPException(status_code=502, detail="udp connect failed")

        sess["udp_transport"] = transport
        sess["udp_target"] = (address, port)
        if payload:
            transport.sendto(payload)
            link["used_bytes"] = link.get("used_bytes", 0) + len(payload)
    else:
        # TCP
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(address, port),
                timeout=TCP_CONNECT_TIMEOUT,
            )
        except Exception:
            raise HTTPException(status_code=502, detail="tcp connect failed")

        sess["writer"] = writer
        if payload:
            writer.write(payload)
            await writer.drain()
            link["used_bytes"] = link.get("used_bytes", 0) + len(payload)

        # پمپ دانلینک از TCP به queue
        asyncio.create_task(_pump_tcp_downlink(session_id, sess, reader, link))


async def _pump_tcp_downlink(session_id: str, sess: dict, reader, link: dict):
    try:
        first = True
        while True:
            data = await reader.read(XHTTP_BUF)
            if not data:
                break
            lb = link.get("limit_bytes", 0)
            if lb > 0 and link.get("used_bytes", 0) + len(data) > lb:
                break
            link["used_bytes"] = link.get("used_bytes", 0) + len(data)
            out = (b"\x00\x00" + data) if first else data
            first = False
            try:
                await sess["down_q"].put(out)
            except Exception:
                break
    except Exception:
        pass
    finally:
        try:
            sess["down_q"].put_nowait(None)
        except Exception:
            pass


# ── Upload (packet-up) ───────────────────────────────────────────────────────
@router.post("/xhttp-siz10/packet-up/{uuid}/{session_id}/{seq}")
async def packet_up_upload(uuid: str, session_id: str, seq: int, request: Request):
    from main import LINKS, LINKS_LOCK
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    if not link or not link.get("active", True):
        raise HTTPException(status_code=403, detail="inactive")

    body = await request.body()
    if not body:
        return {"ok": True}

    lb = link.get("limit_bytes", 0)
    if lb > 0 and link.get("used_bytes", 0) + len(body) > lb:
        raise HTTPException(status_code=403, detail="quota exceeded")
    await throttle(uuid, len(body))

    async with XHTTP_LOCK:
        sess = xhttp_sessions.get(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="session not found")

    sess["last_seen"] = time.time()

    # اگه هنوز به مقصد وصل نشده، هدر رو پارس کن و وصل شو
    if sess["writer"] is None and sess.get("udp_transport") is None:
        await _connect_target(sess, body, link, session_id)
        return {"ok": True, "connected": True}

    # وگرنه، data رو بفرست به مقصد
    link["used_bytes"] = link.get("used_bytes", 0) + len(body)
    if sess.get("udp_transport") is not None:
        try:
            sess["udp_transport"].sendto(body)
        except Exception:
            raise HTTPException(status_code=502, detail="udp write failed")
    else:
        try:
            sess["writer"].write(body)
            if sess["writer"].transport.get_write_buffer_size() > XHTTP_BUF:
                await sess["writer"].drain()
        except Exception:
            raise HTTPException(status_code=502, detail="write failed")

    return {"ok": True}


# ── Upload (stream-up) ───────────────────────────────────────────────────────
@router.post("/xhttp-siz10/stream-up/{uuid}/{session_id}")
async def stream_up_upload(uuid: str, session_id: str, request: Request):
    from main import LINKS, LINKS_LOCK
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    if not link or not link.get("active", True):
        raise HTTPException(status_code=403, detail="inactive")

    async with XHTTP_LOCK:
        sess = xhttp_sessions.get(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="session not found")

    sess["last_seen"] = time.time()
    first = True

    try:
        async for chunk in request.stream():
            if not chunk:
                continue

            lb = link.get("limit_bytes", 0)
            if lb > 0 and link.get("used_bytes", 0) + len(chunk) > lb:
                raise HTTPException(status_code=403, detail="quota exceeded")
            await throttle(uuid, len(chunk))

            # اگه اولین چانکه و هنوز وصل نشده
            if first and sess["writer"] is None and sess.get("udp_transport") is None:
                await _connect_target(sess, chunk, link, session_id)
                first = False
                continue

            first = False
            link["used_bytes"] = link.get("used_bytes", 0) + len(chunk)

            if sess.get("udp_transport") is not None:
                try:
                    sess["udp_transport"].sendto(chunk)
                except Exception:
                    raise HTTPException(status_code=502, detail="udp write failed")
            else:
                try:
                    sess["writer"].write(chunk)
                    if sess["writer"].transport.get_write_buffer_size() > XHTTP_BUF:
                        await sess["writer"].drain()
                except Exception:
                    raise HTTPException(status_code=502, detail="write failed")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"ok": True}