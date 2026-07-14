# xhttp.py
# XHTTP Ultra با Sing-box - پشتیبانی از packet-up و stream-up

import asyncio
import secrets
import time
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from speed_limit import throttle

router = APIRouter()

XHTTP_BUF = 512 * 1024
SESSION_IDLE_TIMEOUT = 30
REAPER_INTERVAL = 10
TCP_CONNECT_TIMEOUT = 10.0

xhttp_sessions: dict = {}
XHTTP_LOCK = asyncio.Lock()

def _ws_client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return "نامشخص"

@router.get("/xhttp-siz10/{mode}/{uuid}/{session_id}")
async def xhttp_downlink(mode: str, uuid: str, session_id: str, request: Request):
    """دانلینک XHTTP"""
    if mode not in ("packet-up", "stream-up"):
        raise HTTPException(status_code=404, detail="unknown mode")
    
    from main import LINKS, LINKS_LOCK, is_link_allowed, is_ip_allowed
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    if not is_link_allowed(link):
        raise HTTPException(status_code=403, detail="not allowed")
    
    ip = _ws_client_ip(request)
    if not is_ip_allowed(link, uuid, ip):
        raise HTTPException(status_code=403, detail="ip limit reached")
    
    async with XHTTP_LOCK:
        sess = xhttp_sessions.get(session_id)
        if sess is None:
            sess = {
                "uuid": uuid,
                "mode": mode,
                "writer": None,
                "down_q": asyncio.Queue(),
                "last_seen": time.time(),
                "closed": False,
                "conn_id": secrets.token_urlsafe(6),
                "addr": None,
                "port": None,
            }
            xhttp_sessions[session_id] = sess
    
    headers = {"content-type": "application/octet-stream", "cache-control": "no-store"}
    return StreamingResponse(_downstream_gen(sess), headers=headers)

async def _downstream_gen(sess: dict):
    try:
        while True:
            chunk = await sess["down_q"].get()
            if chunk is None:
                break
            sess["last_seen"] = time.time()
            yield chunk
    finally:
        pass

@router.post("/xhttp-siz10/packet-up/{uuid}/{session_id}/{seq}")
async def packet_up_upload(uuid: str, session_id: str, seq: int, request: Request):
    """آپلینک packet-up"""
    from main import LINKS, LINKS_LOCK
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    if not link or not link.get("active", True):
        raise HTTPException(status_code=403, detail="inactive")
    
    body = await request.body()
    if not body:
        return {"ok": True}
    
    if link.get("limit_bytes", 0) > 0:
        if link.get("used_bytes", 0) + len(body) > link["limit_bytes"]:
            raise HTTPException(status_code=403, detail="quota exceeded")
    link["used_bytes"] = link.get("used_bytes", 0) + len(body)
    await throttle(uuid, len(body))
    
    async with XHTTP_LOCK:
        sess = xhttp_sessions.get(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="session not found")
    
    if sess["writer"] is None:
        from relay_vless import parse_vless_header
        try:
            command, address, port, payload = await parse_vless_header(body)
            sess["addr"] = address
            sess["port"] = port
        except Exception as e:
            raise HTTPException(status_code=400, detail="invalid header")
        
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(address, port),
            timeout=TCP_CONNECT_TIMEOUT
        )
        sess["writer"] = writer
        if payload:
            writer.write(payload)
            await writer.drain()
        asyncio.create_task(_pump_downlink(session_id, sess, reader))
        return {"ok": True, "connected": True}
    
    try:
        sess["writer"].write(body)
        if sess["writer"].transport.get_write_buffer_size() > XHTTP_BUF:
            await sess["writer"].drain()
    except Exception as e:
        raise HTTPException(status_code=502, detail="write failed")
    
    return {"ok": True}

@router.post("/xhttp-siz10/stream-up/{uuid}/{session_id}")
async def stream_up_upload(uuid: str, session_id: str, request: Request):
    """آپلینک stream-up"""
    from main import LINKS, LINKS_LOCK
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    if not link or not link.get("active", True):
        raise HTTPException(status_code=403, detail="inactive")
    
    async with XHTTP_LOCK:
        sess = xhttp_sessions.get(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="session not found")
    
    first_chunk = True
    try:
        async for chunk in request.stream():
            if not chunk:
                continue
            
            if link.get("limit_bytes", 0) > 0:
                if link.get("used_bytes", 0) + len(chunk) > link["limit_bytes"]:
                    raise HTTPException(status_code=403, detail="quota exceeded")
            link["used_bytes"] = link.get("used_bytes", 0) + len(chunk)
            await throttle(uuid, len(chunk))
            
            if sess["writer"] is None and first_chunk:
                from relay_vless import parse_vless_header
                try:
                    command, address, port, payload = await parse_vless_header(chunk)
                    sess["addr"] = address
                    sess["port"] = port
                except Exception as e:
                    raise HTTPException(status_code=400, detail="invalid header")
                
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(address, port),
                    timeout=TCP_CONNECT_TIMEOUT
                )
                sess["writer"] = writer
                if payload:
                    writer.write(payload)
                    await writer.drain()
                asyncio.create_task(_pump_downlink(session_id, sess, reader))
                first_chunk = False
                continue
            
            try:
                sess["writer"].write(chunk)
                if sess["writer"].transport.get_write_buffer_size() > XHTTP_BUF:
                    await sess["writer"].drain()
            except Exception as e:
                raise HTTPException(status_code=502, detail="write failed")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"ok": True}

async def _pump_downlink(session_id: str, sess: dict, reader):
    """پمپ دانلینک از TCP به WebSocket"""
    try:
        while True:
            data = await reader.read(XHTTP_BUF)
            if not data:
                break
            await sess["down_q"].put(data)
    except Exception as e:
        pass
    finally:
        await sess["down_q"].put(None)
        sess["closed"] = True
