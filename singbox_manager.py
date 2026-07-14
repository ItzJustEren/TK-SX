# singbox_manager.py
# مدیریت Sing-box با پشتیبانی کامل از UDP over TCP

import json
import os
import subprocess
import asyncio
import secrets
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger("TK-SX")

PROTOCOLS = {
    "vless": {"name": "VLESS", "icon": "ti-link", "tcp": True},
    "vmess": {"name": "VMess", "icon": "ti-shield", "tcp": True},
    "trojan": {"name": "Trojan", "icon": "ti-shield-lock", "tcp": True},
    "shadowsocks": {"name": "Shadowsocks", "icon": "ti-lock", "tcp": True},
    "socks5": {"name": "SOCKS5", "icon": "ti-sock", "tcp": True},
    "http": {"name": "HTTP", "icon": "ti-world", "tcp": True},
    "wireguard": {"name": "WireGuard", "icon": "ti-vpn", "tcp": False, "udp_over_tcp": True},
    "hysteria2": {"name": "Hysteria2", "icon": "ti-rocket", "tcp": False, "udp_over_tcp": True},
    "tun": {"name": "TUN", "icon": "ti-device-desktop", "tcp": False},
    "dokodemo": {"name": "Dokodemo-door", "icon": "ti-door", "tcp": True},
    "snell": {"name": "Snell", "icon": "ti-snail", "tcp": True},
}

SINGBOX_CONFIG_PATH = Path("/app/singbox_config.json")
SINGBOX_BIN = os.environ.get("SINGBOX_BIN", "sing-box")
_singbox_process: Optional[asyncio.subprocess.Process] = None

def generate_link_url(uuid: str, link: dict, host: str) -> str:
    """تولید لینک اتصال با پشتیبانی از UDP over TCP"""
    from urllib.parse import quote
    protocol = link.get("protocol", "vless")
    port = link.get("port", 443)
    
    if protocol == "vless":
        return f"vless://{uuid}@{host}:{port}?encryption=none&security=tls&sni={host}&fp=chrome&type=ws&host={host}&path=/ws/{uuid}#{quote(link.get('label','TK-SX'))}"
    elif protocol == "vmess":
        vmess = {"v":"2","ps":link.get('label','TK-SX'),"add":host,"port":port,"id":uuid,"aid":"0","net":"ws","type":"none","host":host,"path":f"/ws/{uuid}","tls":"tls","sni":host,"fp":"chrome"}
        return f"vmess://{quote(json.dumps(vmess, separators=(',',':')), safe='')}"
    elif protocol == "trojan":
        return f"trojan://{uuid}@{host}:{port}?security=tls&sni={host}&fp=chrome&type=ws&host={host}&path=/ws/{uuid}#{quote(link.get('label','TK-SX'))}"
    elif protocol == "shadowsocks":
        method = link.get("method", "aes-256-gcm")
        password = link.get("password", secrets.token_urlsafe(16))
        return f"ss://{quote(f'{method}:{password}')}@{host}:{port}#{quote(link.get('label','TK-SX'))}"
    elif protocol == "socks5":
        return f"socks5://{host}:{port}#{quote(link.get('label','TK-SX'))}"
    elif protocol == "http":
        return f"http://{host}:{port}#{quote(link.get('label','TK-SX'))}"
    elif protocol == "wireguard":
        private_key = link.get("private_key", secrets.token_urlsafe(32))
        public_key = link.get("public_key", secrets.token_urlsafe(32))
        address = link.get("address", "10.0.0.2/32")
        return f"wireguard://{private_key}@{host}:{port}?public_key={public_key}&address={address}&udp_over_tcp=true#{quote(link.get('label','TK-SX'))}"
    elif protocol == "hysteria2":
        return f"hysteria2://{uuid}@{host}:{port}?sni={host}&insecure=0&udp_over_tcp=true#{quote(link.get('label','TK-SX'))}"
    elif protocol == "tun":
        return f"tun://{host}:{port}#{quote(link.get('label','TK-SX'))}"
    elif protocol == "dokodemo":
        return f"dokodemo://{host}:{port}#{quote(link.get('label','TK-SX'))}"
    elif protocol == "snell":
        psk = link.get("psk", secrets.token_urlsafe(16))
        return f"snell://{uuid}@{host}:{port}?psk={psk}#{quote(link.get('label','TK-SX'))}"
    return f"vless://{uuid}@{host}:{port}?encryption=none&security=tls&sni={host}#{quote(link.get('label','TK-SX'))}"

def create_singbox_config(links: Dict[str, dict], host: str) -> dict:
    """تولید کانفیگ سرور Sing-box با UDP over TCP"""
    config = {
        "log": {"level": "error", "output": "/app/singbox.log"},
        "dns": {"servers": [{"tag": "default", "address": "8.8.8.8"}]},
        "inbounds": [],
        "outbounds": [{"type": "direct", "tag": "direct"}, {"type": "block", "tag": "block"}],
    }
    
    for uuid, link in links.items():
        if not link.get("active", True):
            continue
        if is_link_expired(link):
            continue
        protocol = link.get("protocol", "vless")
        port = link.get("port", 443)
        
        inbound = {"type": protocol, "tag": f"in-{uuid[:8]}", "listen": "0.0.0.0", "listen_port": port}
        
        if protocol == "vless":
            inbound["uuid"] = uuid
            inbound["flow"] = "xtls-rprx-vision"
            inbound["transport"] = {"type": "ws", "path": f"/ws/{uuid}"}
        elif protocol == "vmess":
            inbound["uuid"] = uuid
            inbound["security"] = "auto"
            inbound["transport"] = {"type": "ws", "path": f"/ws/{uuid}"}
        elif protocol == "trojan":
            inbound["password"] = uuid
            inbound["transport"] = {"type": "ws", "path": f"/ws/{uuid}"}
        elif protocol == "shadowsocks":
            inbound["method"] = link.get("method", "aes-256-gcm")
            inbound["password"] = link.get("password", secrets.token_urlsafe(16))
        elif protocol == "socks5":
            inbound["users"] = [{"username": uuid, "password": secrets.token_urlsafe(16)}]
        elif protocol == "http":
            inbound["users"] = [{"username": uuid, "password": secrets.token_urlsafe(16)}]
        elif protocol == "wireguard":
            inbound["private_key"] = link.get("private_key", secrets.token_urlsafe(32))
            inbound["peers"] = [{"public_key": link.get("public_key", secrets.token_urlsafe(32)), "allowed_ips": [link.get("address", "10.0.0.2/32")]}]
            inbound["udp_over_tcp"] = {"enabled": True, "version": 2}
        elif protocol == "hysteria2":
            inbound["password"] = uuid
            inbound["tls"] = {"enabled": True, "certificate": "/app/cert.pem", "key": "/app/key.pem"}
            inbound["udp_over_tcp"] = {"enabled": True, "version": 2}
        elif protocol == "tun":
            inbound["inet4_address"] = "172.19.0.1/30"
            inbound["inet6_address"] = "fdfe:dcba:9876::1/126"
        elif protocol == "dokodemo":
            inbound["address"] = "0.0.0.0"
            inbound["port"] = 0
            inbound["follow_redirect"] = True
        elif protocol == "snell":
            inbound["psk"] = link.get("psk", secrets.token_urlsafe(16))
        
        config["inbounds"].append(inbound)
    
    return config

def is_link_expired(link: dict) -> bool:
    from datetime import datetime
    exp = link.get("expires_at")
    if not exp:
        return False
    try:
        return datetime.now() > datetime.fromisoformat(exp)
    except Exception:
        return False

async def singbox_start():
    global _singbox_process
    try:
        await singbox_stop()
        from main import LINKS, LINKS_LOCK, CONFIG
        async with LINKS_LOCK:
            links = dict(LINKS)
        host = CONFIG.get("host", "localhost")
        config = create_singbox_config(links, host)
        with open(SINGBOX_CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
        cmd = [SINGBOX_BIN, "run", "-c", str(SINGBOX_CONFIG_PATH)]
        _singbox_process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        logger.info(f"Sing-box started with PID {_singbox_process.pid}")
        return True
    except Exception as e:
        logger.error(f"Failed to start Sing-box: {e}")
        return False

async def singbox_stop():
    global _singbox_process
    if _singbox_process:
        try:
            _singbox_process.terminate()
            await asyncio.sleep(2)
            if _singbox_process.returncode is None:
                _singbox_process.kill()
            await _singbox_process.wait()
            logger.info("Sing-box stopped")
        except Exception as e:
            logger.error(f"Error stopping Sing-box: {e}")
        finally:
            _singbox_process = None
    return True

async def singbox_restart():
    await singbox_stop()
    await asyncio.sleep(1)
    return await singbox_start()

def singbox_status() -> dict:
    if _singbox_process and _singbox_process.returncode is None:
        return {"running": True, "pid": _singbox_process.pid}
    return {"running": False, "pid": None}
