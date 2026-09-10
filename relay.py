# relay.py - هندلر WebSocket با Sing-box (TCP + UDP over TCP)

import asyncio
import secrets
import socket
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect

from relay_vless import parse_vless_header
from speed_limit import throttle

RELAY_BUF = 256 * 1024
HEADER_TIMEOUT = 15.0
CONNECT_TIMEOUT = 10.0


def _ws_client_ip(ws: WebSocket) -> str:
    fwd = ws.headers.get("x-forwarded-for", "")
    if fwd:
        return fwd.split(",")[0].strip()
    real = ws.headers.get("x-real-ip", "")
    if real:
        return real.strip()
    return ws.client.host if ws.client else "نامشخص"


def _bump_usage(link: dict, conn: dict, stats: dict, size: int) -> bool:
    """
    افزایش شمارنده مصرف.
    True برگردون اگه هنوز مجاز باشه، False اگه به سقف رسیده.
    """
    lb = link.get("limit_bytes", 0)
    used = link.get("used_bytes", 0)
    if lb > 0 and used + size > lb:
        return False
    link["used_bytes"] = used + size
    if conn is not None:
        conn["bytes"] = conn.get("bytes", 0) + size
    stats["total_bytes"] = stats.get("total_bytes", 0) + size
    stats["total_requests"] = stats.get("total_requests", 0) + 1
    return True


# ── UDP Protocol برای command=2 ──────────────────────────────────────────────
class _UdpRelayProtocol(asyncio.DatagramProtocol):
    """UDP relay بین WebSocket و مقصد."""

    def __init__(self, ws: WebSocket, link: dict, conn: dict, stats: dict, logger, conn_id: str):
        self.ws = ws
        self.link = link
        self.conn = conn
        self.stats = stats
        self.logger = logger
        self.conn_id = conn_id
        self.transport = None
        self.first_response = True
        self._closed = False

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data: bytes, addr):
        """پاسخ از مقصد UDP → ارسال به کلاینت از طریق WS."""
        if self._closed:
            return
        if not _bump_usage(self.link, self.conn, self.stats, len(data)):
            self._close_ws()
            return
        payload = (b"\x00\x00" + data) if self.first_response else data
        self.first_response = False
        asyncio.create_task(self._safe_send(payload))

    async def _safe_send(self, payload: bytes):
        try:
            await self.ws.send_bytes(payload)
        except Exception:
            self._close_ws()

    def error_received(self, exc):
        self.logger.warning(f"UDP relay error [{self.conn_id}]: {exc}")

    def connection_lost(self, exc):
        self._closed = True

    def _close_ws(self):
        self._closed = True
        try:
            self.transport.close()
        except Exception:
            pass


# ── هندلر اصلی ───────────────────────────────────────────────────────────────
async def handle_websocket(
    ws: WebSocket,
    uuid: str,
    connections: dict,
    LINKS: dict,
    LINKS_LOCK: asyncio.Lock,
    stats: dict,
    error_logs: list,
    hourly_traffic: dict,
    logger,
):
    await ws.accept()

    # ── اعتبارسنجی لینک ──
    async with LINKS_LOCK:
        link = LINKS.get(uuid)

    if not link or not link.get("active", True):
        await ws.close(code=1008, reason="not authorized")
        return

    from main import is_ip_allowed, is_link_expired

    ip = _ws_client_ip(ws)

    if not is_ip_allowed(link, uuid, ip):
        await ws.close(code=1008, reason="ip limit")
        return

    if is_link_expired(link):
        await ws.close(code=1008, reason="expired")
        return

    # ── ثبت اتصال ──
    conn_id = secrets.token_urlsafe(6)
    connections[conn_id] = {
        "uuid": uuid,
        "ip": ip,
        "transport": "vless-ws",
        "connected_at": datetime.now().isoformat(),
        "bytes": 0,
    }
    logger.info(f"WS [{conn_id}] uuid={uuid[:8]} ip={ip}")

    writer = None
    udp_protocol = None
    udp_transport = None

    try:
        # ── دریافت اولین چانک (هدر VLESS) ──
        first_msg = await asyncio.wait_for(ws.receive(), timeout=HEADER_TIMEOUT)
        if first_msg.get("type") == "websocket.disconnect":
            return

        first_chunk = first_msg.get("bytes") or (first_msg.get("text") or "").encode()
        if not first_chunk:
            await ws.close(code=1002, reason="empty header")
            return

        # ── پارس هدر ──
        try:
            command, address, port, payload = await parse_vless_header(first_chunk)
        except Exception as e:
            logger.warning(f"WS [{conn_id}] invalid header: {e}")
            await ws.close(code=1003, reason="invalid header")
            return

        logger.info(f"WS [{conn_id}] cmd={command} target={address}:{port}")

        # ═══════════════════════════════════════════════════════════
        # حالت UDP (command=2)
        # ═══════════════════════════════════════════════════════════
        if command == 2:
            loop = asyncio.get_event_loop()
            try:
                transport, protocol = await asyncio.wait_for(
                    loop.create_datagram_endpoint(
                        lambda: _UdpRelayProtocol(ws, link, connections[conn_id], stats, logger, conn_id),
                        remote_addr=(address, port),
                    ),
                    timeout=CONNECT_TIMEOUT,
                )
                udp_transport = transport
                udp_protocol = protocol
            except Exception as e:
                logger.warning(f"WS [{conn_id}] UDP connect failed to {address}:{port}: {e}")
                await ws.close(code=1011, reason="upstream failed")
                return

            # ارسال payload اولیه (اگه بود)
            if payload:
                transport.sendto(payload)
                _bump_usage(link, connections[conn_id], stats, len(payload))

            # حلقه دریافت از WS و ارسال به UDP
            try:
                while True:
                    msg = await ws.receive()
                    if msg.get("type") == "websocket.disconnect":
                        break
                    data = msg.get("bytes") or (msg.get("text") or "").encode()
                    if not data:
                        continue
                    if not _bump_usage(link, connections[conn_id], stats, len(data)):
                        break
                    await throttle(uuid, len(data))
                    transport.sendto(data)
            except WebSocketDisconnect:
                pass
            except Exception as e:
                logger.debug(f"UDP ws loop ended [{conn_id}]: {e}")
            finally:
                try:
                    transport.close()
                except Exception:
                    pass
            return

        # ═══════════════════════════════════════════════════════════
        # حالت TCP (command=1 یا هر چیز دیگه)
        # ═══════════════════════════════════════════════════════════
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(address, port),
                timeout=CONNECT_TIMEOUT,
            )
        except Exception as e:
            logger.warning(f"WS [{conn_id}] TCP connect failed to {address}:{port}: {e}")
            await ws.close(code=1011, reason="upstream failed")
            return

        # ارسال payload اولیه
        if payload:
            writer.write(payload)
            await writer.drain()
            _bump_usage(link, connections[conn_id], stats, len(payload))

        async def relay_ws_to_tcp():
            """کلاینت → سرور مقصد"""
            try:
                while True:
                    msg = await ws.receive()
                    if msg.get("type") == "websocket.disconnect":
                        break
                    data = msg.get("bytes") or (msg.get("text") or "").encode()
                    if not data:
                        continue
                    if not _bump_usage(link, connections[conn_id], stats, len(data)):
                        break
                    await throttle(uuid, len(data))
                    writer.write(data)
                    if writer.transport.get_write_buffer_size() > RELAY_BUF:
                        await writer.drain()
            except Exception:
                pass

        async def relay_tcp_to_ws():
            """سرور مقصد → کلاینت (با هدر VLESS در اولین بایت)"""
            try:
                first = True
                while True:
                    data = await reader.read(RELAY_BUF)
                    if not data:
                        break
                    if not _bump_usage(link, connections[conn_id], stats, len(data)):
                        break
                    payload_out = (b"\x00\x00" + data) if first else data
                    first = False
                    await ws.send_bytes(payload_out)
            except Exception:
                pass

        t1 = asyncio.create_task(relay_ws_to_tcp())
        t2 = asyncio.create_task(relay_tcp_to_ws())
        done, pending = await asyncio.wait(
            {t1, t2},
            return_when=asyncio.FIRST_COMPLETED,
        )
        for t in pending:
            t.cancel()
            try:
                await t
            except Exception:
                pass

    except WebSocketDisconnect:
        pass
    except asyncio.TimeoutError:
        stats["total_errors"] += 1
        error_logs.append({"error": "timeout", "time": datetime.now().isoformat()})
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "time": datetime.now().isoformat()})
        logger.debug(f"WS handler error [{conn_id}]: {exc}")
    finally:
        # بستن TCP
        if writer is not None:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        # بستن UDP
        if udp_transport is not None:
            try:
                udp_transport.close()
            except Exception:
                pass
        connections.pop(conn_id, None)
        logger.info(f"WS closed [{conn_id}]")