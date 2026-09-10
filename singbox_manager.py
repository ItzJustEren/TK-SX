# singbox_manager.py
# مدیریت Sing-box با پشتیبانی کامل از UDP over TCP

import json
import os
import asyncio
import secrets
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
from urllib.parse import quote
import logging

logger = logging.getLogger("TK-SX")

PROTOCOLS = {
    "vless": {"name": "VLESS", "icon": "ti-link", "tcp": True, "udp_over_tcp": True},
    "vmess": {"name": "VMess", "icon": "ti-shield", "tcp": True, "udp_over_tcp": True},
    "trojan": {"name": "Trojan", "icon": "ti-shield-lock", "tcp": True, "udp_over_tcp": True},
    "shadowsocks": {"name": "Shadowsocks", "icon": "ti-lock", "tcp": True},
    "socks5": {"name": "SOCKS5", "icon": "ti-sock", "tcp": True},
    "http": {"name": "HTTP", "icon": "ti-world", "tcp": True},
    "wireguard": {"name": "WireGuard", "icon": "ti-vpn", "tcp": False, "udp_over_tcp": True},
    "hysteria2": {"name": "Hysteria2", "icon": "ti-rocket", "tcp": False},
    "tun": {"name": "TUN", "icon": "ti-device-desktop", "tcp": False},
    "dokodemo": {"name": "Dokodemo-door", "icon": "ti-door", "tcp": True},
    "snell": {"name": "Snell", "icon": "ti-snail", "tcp": True},
}

SINGBOX_CONFIG_PATH = Path("/app/singbox_config.json")
SINGBOX_BIN = os.environ.get("SINGBOX_BIN", "sing-box")
SINGBOX_INTERNAL_PORT = int(os.environ.get("SINGBOX_INTERNAL_PORT", "8443"))

_singbox_process: Optional[asyncio.subprocess.Process] = None
_config_lock = asyncio.Lock()


# ── Helpers ──────────────────────────────────────────────────────────────────
def is_link_expired(link: dict) -> bool:
    exp = link.get("expires_at")
    if not exp:
        return False
    try:
        return datetime.now() > datetime.fromisoformat(exp)
    except Exception:
        return False


def is_link_allowed(link: dict) -> bool:
    if not link.get("active", True):
        return False
    if is_link_expired(link):
        return False
    lb = link.get("limit_bytes", 0)
    if lb > 0 and link.get("used_bytes", 0) >= lb:
        return False
    return True


# ── Link generator ───────────────────────────────────────────────────────────
def generate_link_url(uuid: str, link: dict, host: str) -> str:
    """تولید لینک اتصال با پشتیبانی UDP over TCP"""
    protocol = link.get("protocol", "vless")
    port = link.get("port", 443)
    label = quote(link.get("label", "TK-SX"))

    if protocol == "vless":
        # VLESS + WS + TLS — UDP به‌طور خودکار در WS تونل میشه
        return (
            f"vless://{uuid}@{host}:{port}"
            f"?encryption=none"
            f"&security=tls"
            f"&sni={host}"
            f"&fp=chrome"
            f"&alpn=http%2F1.1"
            f"&type=ws"
            f"&host={host}"
            f"&path=%2Fws"
            f"#{label}"
        )
    elif protocol == "vmess":
        vmess = {
            "v": "2", "ps": link.get("label", "TK-SX"),
            "add": host, "port": port, "id": uuid, "aid": "0",
            "scy": "auto", "net": "ws", "type": "none",
            "host": host, "path": "/ws", "tls": "tls",
            "sni": host, "fp": "chrome"
        }
        return f"vmess://{quote(json.dumps(vmess, separators=(',', ':')), safe='')}"
    elif protocol == "trojan":
        return (
            f"trojan://{uuid}@{host}:{port}"
            f"?security=tls&sni={host}&fp=chrome"
            f"&type=ws&host={host}&path=%2Fws"
            f"#{label}"
        )
    elif protocol == "shadowsocks":
        method = link.get("method", "aes-256-gcm")
        password = link.get("password", secrets.token_urlsafe(16))
        userinfo = quote(f"{method}:{password}", safe="")
        return f"ss://{userinfo}@{host}:{port}#{label}"
    elif protocol == "socks5":
        return f"socks5://{host}:{port}#{label}"
    elif protocol == "http":
        return f"http://{host}:{port}#{label}"
    elif protocol == "wireguard":
        private_key = link.get("private_key", secrets.token_urlsafe(32))
        public_key = link.get("public_key", secrets.token_urlsafe(32))
        address = link.get("address", "10.0.0.2/32")
        return (
            f"wireguard://{private_key}@{host}:{port}"
            f"?public_key={public_key}&address={address}"
            f"&udp_over_tcp=true#{label}"
        )
    elif protocol == "hysteria2":
        return f"hysteria2://{uuid}@{host}:{port}?sni={host}&insecure=0#{label}"
    elif protocol == "tun":
        return f"tun://{host}:{port}#{label}"
    elif protocol == "dokodemo":
        return f"dokodemo://{host}:{port}#{label}"
    elif protocol == "snell":
        psk = link.get("psk", secrets.token_urlsafe(16))
        return f"snell://{uuid}@{host}:{port}?psk={psk}#{label}"

    return f"vless://{uuid}@{host}:{port}?encryption=none&security=tls&sni={host}&type=ws&path=%2Fws#{label}"


# ── Config builder ───────────────────────────────────────────────────────────
def create_singbox_config(links: Dict[str, dict], host: str) -> dict:
    """
    تولید کانفیگ Sing-box.
    نکته‌ی مهم: برای هر پروتکل فقط یک inbound ساخته میشه
    (چون همه‌ی کاربران یک path مشترک دارند و با UUID/auth از هم جدا میشن).
    """
    config = {
        "log": {"level": "warn", "output": "/app/singbox.log"},
        "dns": {
            "servers": [
                {"tag": "google", "address": "8.8.8.8"},
                {"tag": "cloudflare", "address": "1.1.1.1"}
            ],
            "strategy": "prefer_ipv4"
        },
        "inbounds": [],
        "outbounds": [
            {"type": "direct", "tag": "direct"},
            {"type": "block", "tag": "block"}
        ]
    }

    vless_users = []
    vmess_users = []
    trojan_users = []
    ss_users = []

    for uuid, link in links.items():
        if not is_link_allowed(link):
            continue
        protocol = link.get("protocol", "vless")

        if protocol == "vless":
            vless_users.append({
                "uuid": uuid,
                "flow": ""  # برای WebSocket خالی باید باشه
            })
        elif protocol == "vmess":
            vmess_users.append({"uuid": uuid, "alterId": 0})
        elif protocol == "trojan":
            trojan_users.append({"password": uuid})
        elif protocol == "shadowsocks":
            ss_users.append({
                "method": link.get("method", "aes-256-gcm"),
                "password": link.get("password", secrets.token_urlsafe(16)),
                "tag": f"ss-{uuid[:8]}"
            })

    # ── VLESS (main) ──
    if vless_users:
        config["inbounds"].append({
            "type": "vless",
            "tag": "vless-in",
            "listen": "0.0.0.0",
            "listen_port": SINGBOX_INTERNAL_PORT,
            "users": vless_users,
            "transport": {
                "type": "ws",
                "path": "/ws",
                "max_early_data": 2048,
                "early_data_header_name": "Sec-WebSocket-Protocol"
            },
            "sniff": True,
            "sniff_override_destination": True,
            "domain_strategy": "prefer_ipv4"
        })

    # ── VMess ──
    if vmess_users:
        config["inbounds"].append({
            "type": "vmess",
            "tag": "vmess-in",
            "listen": "0.0.0.0",
            "listen_port": SINGBOX_INTERNAL_PORT + 1,
            "users": vmess_users,
            "transport": {
                "type": "ws",
                "path": "/ws",
                "max_early_data": 2048,
                "early_data_header_name": "Sec-WebSocket-Protocol"
            },
            "sniff": True,
            "sniff_override_destination": True,
            "domain_strategy": "prefer_ipv4"
        })

    # ── Trojan ──
    if trojan_users:
        config["inbounds"].append({
            "type": "trojan",
            "tag": "trojan-in",
            "listen": "0.0.0.0",
            "listen_port": SINGBOX_INTERNAL_PORT + 2,
            "users": trojan_users,
            "transport": {
                "type": "ws",
                "path": "/ws",
                "max_early_data": 2048,
                "early_data_header_name": "Sec-WebSocket-Protocol"
            },
            "sniff": True,
            "sniff_override_destination": True,
            "domain_strategy": "prefer_ipv4"
        })

    # ── Shadowsocks ──
    for ss in ss_users:
        config["inbounds"].append({
            "type": "shadowsocks",
            "tag": ss["tag"],
            "listen": "0.0.0.0",
            "listen_port": SINGBOX_INTERNAL_PORT + 10,
            "method": ss["method"],
            "password": ss["password"],
            "sniff": True,
            "sniff_override_destination": True
        })

    return config


# ── Lifecycle ────────────────────────────────────────────────────────────────
async def _stop_internal():
    global _singbox_process
    if _singbox_process:
        try:
            _singbox_process.terminate()
            try:
                await asyncio.wait_for(_singbox_process.wait(), timeout=3)
            except asyncio.TimeoutError:
                _singbox_process.kill()
                await _singbox_process.wait()
        except Exception as e:
            logger.error(f"Error stopping Sing-box: {e}")
        finally:
            _singbox_process = None


async def _start_internal() -> bool:
    global _singbox_process
    try:
        from main import LINKS, LINKS_LOCK, CONFIG
        async with LINKS_LOCK:
            links = dict(LINKS)
        host = CONFIG.get("host", "localhost")
        config = create_singbox_config(links, host)

        with open(SINGBOX_CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)

        # بررسی صحت کانفیگ قبل از اجرا
        check = await asyncio.create_subprocess_exec(
            SINGBOX_BIN, "check", "-c", str(SINGBOX_CONFIG_PATH),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        _, check_err = await check.communicate()
        if check.returncode != 0:
            logger.error(f"Sing-box config invalid: {check_err.decode(errors='ignore')}")
            return False

        cmd = [SINGBOX_BIN, "run", "-c", str(SINGBOX_CONFIG_PATH)]
        _singbox_process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        logger.info(f"Sing-box started with PID {_singbox_process.pid}")
        return True
    except Exception as e:
        logger.error(f"Failed to start Sing-box: {e}")
        return False


async def singbox_start() -> bool:
    async with _config_lock:
        await _stop_internal()
        return await _start_internal()


async def singbox_stop() -> bool:
    async with _config_lock:
        await _stop_internal()
    logger.info("Sing-box stopped")
    return True


async def singbox_restart() -> bool:
    async with _config_lock:
        await _stop_internal()
        await asyncio.sleep(0.5)
        return await _start_internal()


def singbox_status() -> dict:
    if _singbox_process and _singbox_process.returncode is None:
        return {"running": True, "pid": _singbox_process.pid}
    return {"running": False, "pid": None}