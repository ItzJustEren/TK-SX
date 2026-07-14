# relay.py - هندلر WebSocket با Sing-box
import asyncio
import secrets
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
from speed_limit import throttle
RELAY_BUF = 256*1024

def _ws_client_ip(ws): return ws.headers.get("x-forwarded-for", "").split(",")[0].strip() or ws.headers.get("x-real-ip", "").strip() or (ws.client.host if ws.client else "نامشخص")

async def handle_websocket(ws: WebSocket, uuid: str, connections: dict, LINKS: dict, LINKS_LOCK: asyncio.Lock, stats: dict, error_logs: list, hourly_traffic: dict, logger):
    await ws.accept()
    async with LINKS_LOCK: link = LINKS.get(uuid)
    if not link or not link.get("active", True): await ws.close(code=1008, reason="not authorized"); return
    ip = _ws_client_ip(ws)
    from main import is_ip_allowed, is_link_expired
    if not is_ip_allowed(link, uuid, ip): await ws.close(code=1008, reason="ip limit"); return
    if is_link_expired(link): await ws.close(code=1008, reason="expired"); return
    conn_id = secrets.token_urlsafe(6)
    connections[conn_id] = {"uuid": uuid, "ip": ip, "transport": "singbox-ws", "connected_at": datetime.now().isoformat(), "bytes": 0}
    logger.info(f"WS [{conn_id}] uuid={uuid[:8]} ip={ip}")
    try:
        first_msg = await asyncio.wait_for(ws.receive(), timeout=15.0)
        if first_msg["type"] == "websocket.disconnect": return
        first_chunk = first_msg.get("bytes") or (first_msg.get("text") or "").encode()
        if not first_chunk: return
        from relay_vless import parse_vless_header
        try:
            command, address, port, payload = await parse_vless_header(first_chunk)
        except: await ws.close(code=1003, reason="invalid header"); return
        reader, writer = await asyncio.wait_for(asyncio.open_connection(address, port), timeout=10.0)
        if payload: writer.write(payload); await writer.drain()
        async def relay_ws_to_tcp():
            try:
                while True:
                    msg = await ws.receive()
                    if msg["type"] == "websocket.disconnect": break
                    data = msg.get("bytes") or (msg.get("text") or "").encode()
                    if not data: continue
                    if link.get("limit_bytes", 0) > 0 and link.get("used_bytes", 0) + len(data) > link["limit_bytes"]: break
                    link["used_bytes"] = link.get("used_bytes", 0) + len(data)
                    stats["total_bytes"] += len(data); stats["total_requests"] += 1
                    connections[conn_id]["bytes"] += len(data)
                    await throttle(uuid, len(data))
                    writer.write(data)
                    if writer.transport.get_write_buffer_size() > RELAY_BUF: await writer.drain()
            except: pass
        async def relay_tcp_to_ws():
            try:
                first = True
                while True:
                    data = await reader.read(RELAY_BUF)
                    if not data: break
                    if link.get("limit_bytes", 0) > 0 and link.get("used_bytes", 0) + len(data) > link["limit_bytes"]: break
                    link["used_bytes"] = link.get("used_bytes", 0) + len(data)
                    connections[conn_id]["bytes"] += len(data)
                    payload = (b"\x00\x00" + data) if first else data
                    first = False
                    await ws.send_bytes(payload)
            except: pass
        done, pending = await asyncio.wait({asyncio.create_task(relay_ws_to_tcp()), asyncio.create_task(relay_tcp_to_ws())}, return_when=asyncio.FIRST_COMPLETED)
        for t in pending: t.cancel()
        writer.close(); await writer.wait_closed()
    except WebSocketDisconnect: pass
    except asyncio.TimeoutError: stats["total_errors"] += 1; error_logs.append({"error": "timeout", "time": datetime.now().isoformat()})
    except Exception as exc: stats["total_errors"] += 1; error_logs.append({"error": str(exc), "time": datetime.now().isoformat()})
    finally: connections.pop(conn_id, None); logger.info(f"WS closed [{conn_id}]")
