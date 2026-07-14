# main.py
# TK-SX v3.0 - هسته اصلی با Sing-box، کیف پول، کارت، معرفی، تخفیف، قرعه‌کشی
# پشتیبانی از: VLESS, VMess, Trojan, Shadowsocks, SOCKS5, HTTP, WireGuard, Hysteria2, TUN, Dokodemo-door, Snell
# UDP over TCP فعال برای WireGuard و Hysteria2

import asyncio
import json
import os
import hashlib
import secrets
import time
import aiofiles
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import quote
from collections import deque, defaultdict
from pathlib import Path
from typing import Optional, Dict, Any

from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import Response, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx
import logging

from singbox_manager import (
    singbox_start, singbox_stop, singbox_restart, singbox_status,
    generate_link_url, PROTOCOLS, create_singbox_config
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("TK-SX")

IRAN_TZ = ZoneInfo("Asia/Tehran")

app = FastAPI(title="TK-SX", docs_url=None, redoc_url=None)

# ── Persistence ───────────────────────────────────────────────────────────────
DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))
DATA_FILE = DATA_DIR / "tksx_state.json"
SECRET_FILE = DATA_DIR / "tksx_secret.key"
SAVE_LOCK = asyncio.Lock()

def _load_or_create_secret() -> str:
    env_secret = os.environ.get("SECRET_KEY")
    if env_secret:
        return env_secret
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if SECRET_FILE.exists():
            existing = SECRET_FILE.read_text(encoding="utf-8").strip()
            if existing:
                return existing
        new_secret = secrets.token_urlsafe(32)
        SECRET_FILE.write_text(new_secret, encoding="utf-8")
        return new_secret
    except Exception as e:
        logger.warning(f"Could not persist SECRET_KEY: {e}")
        return secrets.token_urlsafe(32)

CONFIG = {
    "port": int(os.environ.get("PORT", 8000)),
    "secret": _load_or_create_secret(),
    "host": os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost"),
    "bot_username": os.environ.get("BOT_USERNAME", "CyrusBot"),
    "stars_rate": int(os.environ.get("STARS_RATE", 1000)),
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── State ────────────────────────────────────────────────────────────────────
LINKS: Dict[str, dict] = {}
LINKS_LOCK = asyncio.Lock()
SUBS: Dict[str, dict] = {}
SUBS_LOCK = asyncio.Lock()
PRODUCTS: Dict[str, dict] = {}
PRODUCTS_LOCK = asyncio.Lock()
ORDERS: Dict[str, dict] = {}
ORDERS_LOCK = asyncio.Lock()
TEST_USERS: Dict[int, dict] = {}
USER_CODES: Dict[int, dict] = {}
FEEDBACKS: list = []
REYMIT_LINKS: list = ["https://reymit.ir/itzjusteren"]
TUTORIAL_CHANNEL: str = "@TaaKaaOrg"
ADMIN_IDS = set()
OWNER_ID = None
CARD_NUMBER = os.environ.get("CARD_NUMBER", "6037-9910-1234-5678")
CARD_OWNER_NAME = os.environ.get("CARD_OWNER_NAME", "نام صاحب کارت")
PRICE_PER_GB = float(os.environ.get("PRICE_PER_GB", "6"))
ADMIN_GROUP_ID = int(os.environ.get("ADMIN_GROUP_ID", 0)) or None

# ===== سیستم‌های جدید (کیف پول، کارت، معرفی، تخفیف، قرعه‌کشی) =====
WALLETS: Dict[int, dict] = {}  # user_id -> {"balance": int, "frozen": int}
WALLETS_LOCK = asyncio.Lock()
TRANSACTIONS: list = []

USER_CARDS: Dict[int, dict] = {}  # user_id -> {"card_number": str, "full_name": str, "status": str, ...}
CARDS_LOCK = asyncio.Lock()

REFERRALS: Dict[int, dict] = {}  # user_id -> {"code": str, "referred_by": int, "earnings": int, "referred_users": list}
REFERRALS_LOCK = asyncio.Lock()

DISCOUNT_CODES: Dict[str, dict] = {}  # code -> {"percent": int, "max_uses": int, "used_count": int, "expires_at": str}
DISCOUNT_LOCK = asyncio.Lock()

LOTTERY: dict = {
    "active": False,
    "prize": "۵۰ گیگ کانفیگ رایگان",
    "participants": {},
    "winner": None,
    "started_at": None,
    "ended_at": None,
}
LOTTERY_LOCK = asyncio.Lock()

connections: dict = {}
stats = {"total_bytes": 0, "total_requests": 0, "total_errors": 0, "start_time": time.time()}
error_logs: deque = deque(maxlen=50)
activity_logs: deque = deque(maxlen=200)
hourly_traffic: dict = defaultdict(int)
http_client: httpx.AsyncClient | None = None

# ── Auth ──────────────────────────────────────────────────────────────────────
SESSION_COOKIE = "tksx_session"
SESSION_TTL = 60 * 60 * 24 * 365

def hash_password(pw: str) -> str:
    return hashlib.sha256(f"{pw}{CONFIG['secret']}".encode()).hexdigest()

AUTH = {"password_hash": hash_password(os.environ.get("ADMIN_PASSWORD", "taakaa"))}
SESSIONS: dict = {}
SESSIONS_LOCK = asyncio.Lock()

async def create_session() -> str:
    token = secrets.token_urlsafe(32)
    async with SESSIONS_LOCK:
        SESSIONS[token] = time.time() + SESSION_TTL
    return token

async def is_valid_session(token: str | None) -> bool:
    if not token:
        return False
    async with SESSIONS_LOCK:
        exp = SESSIONS.get(token)
        if exp is None:
            return False
        if exp < time.time():
            SESSIONS.pop(token, None)
            return False
        return True

async def destroy_session(token: str | None):
    if not token:
        return
    async with SESSIONS_LOCK:
        SESSIONS.pop(token, None)

async def require_auth(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    if not await is_valid_session(token):
        raise HTTPException(status_code=401, detail="unauthorized")
    return token

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_host(request: Request | None = None) -> str:
    if request is not None:
        h = request.headers.get("x-forwarded-host") or request.headers.get("host")
        if h:
            h = h.split(":")[0]
            CONFIG["host"] = h
            return h
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", CONFIG["host"])

def generate_uuid() -> str:
    h = secrets.token_hex(16)
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[20:32]}"

def now_ir() -> datetime:
    return datetime.now(IRAN_TZ)

def fmt_bytes(b: int) -> str:
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.1f} KB"
    if b < 1024**3: return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"

def generate_user_code() -> str:
    import string
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def calculate_user_level(user_id: int) -> int:
    confirmed = [o for o in ORDERS.values() if o["user_id"] == user_id and o["status"] == "confirmed"]
    total = len(confirmed)
    if total >= 10: return 10
    elif total >= 5: return 5
    elif total >= 3: return 3
    elif total >= 1: return 1
    return 0

def log_activity(kind: str, message: str, level: str = "info"):
    activity_logs.append({"kind": kind, "level": level, "message": message, "time": datetime.now().isoformat()})

def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return request.client.host if request.client else "نامشخص"

def is_link_expired(link: dict) -> bool:
    exp = link.get("expires_at")
    if not exp:
        return False
    try:
        return datetime.now() > datetime.fromisoformat(exp)
    except Exception:
        return False

def is_link_allowed(link: dict | None) -> bool:
    if link is None:
        return False
    if not link.get("active", True):
        return False
    if is_link_expired(link):
        return False
    lb = link.get("limit_bytes", 0)
    if lb > 0 and link.get("used_bytes", 0) >= lb:
        return False
    return True

def unique_ips_for_uuid(uuid: str) -> set:
    return {c.get("ip") for c in connections.values() if c.get("uuid") == uuid and c.get("ip")}

def is_ip_allowed(link: dict | None, uuid: str, ip: str) -> bool:
    if link is None:
        return False
    limit = int(link.get("ip_limit", 0) or 0)
    if limit <= 0:
        return True
    ips = unique_ips_for_uuid(uuid)
    if ip in ips:
        return True
    return len(ips) < limit

# ── سیستم کیف پول ────────────────────────────────────────────────────────────
async def get_balance(user_id: int) -> int:
    return WALLETS.get(user_id, {}).get("balance", 0)

async def add_balance(user_id: int, amount: int, description: str, admin_id: int = None) -> int:
    async with WALLETS_LOCK:
        if user_id not in WALLETS:
            WALLETS[user_id] = {"balance": 0, "frozen": 0}
        WALLETS[user_id]["balance"] += amount
        TRANSACTIONS.append({
            "user_id": user_id,
            "amount": amount,
            "description": description,
            "admin_id": admin_id,
            "created_at": datetime.now().isoformat()
        })
    await save_state()
    return WALLETS[user_id]["balance"]

async def deduct_balance(user_id: int, amount: int, description: str) -> bool:
    async with WALLETS_LOCK:
        if user_id not in WALLETS:
            return False
        if WALLETS[user_id]["balance"] < amount:
            return False
        WALLETS[user_id]["balance"] -= amount
        TRANSACTIONS.append({
            "user_id": user_id,
            "amount": -amount,
            "description": description,
            "admin_id": None,
            "created_at": datetime.now().isoformat()
        })
    await save_state()
    return True

# ── سیستم کارت ──────────────────────────────────────────────────────────────
async def register_card(user_id: int, card_number: str, full_name: str) -> dict:
    async with CARDS_LOCK:
        USER_CARDS[user_id] = {
            "card_number": card_number,
            "full_name": full_name,
            "status": "pending",
            "submitted_at": datetime.now().isoformat(),
            "approved_at": None,
        }
    await save_state()
    return USER_CARDS[user_id]

async def get_card_status(user_id: int) -> Optional[dict]:
    return USER_CARDS.get(user_id)

# ── سیستم معرفی ──────────────────────────────────────────────────────────────
async def generate_referral_code(user_id: int) -> str:
    code = secrets.token_hex(4).upper()
    async with REFERRALS_LOCK:
        REFERRALS[user_id] = {
            "code": code,
            "referred_by": None,
            "earnings": 0,
            "referred_users": [],
        }
    await save_state()
    return code

async def get_referral_info(user_id: int) -> Optional[dict]:
    return REFERRALS.get(user_id)

async def add_referral_earning(user_id: int, amount: int):
    async with REFERRALS_LOCK:
        if user_id in REFERRALS:
            REFERRALS[user_id]["earnings"] += amount
    await save_state()

# ── سیستم تخفیف ──────────────────────────────────────────────────────────────
async def create_discount_code(code: str, percent: int, max_uses: int, expires_at: str, created_by: int) -> bool:
    async with DISCOUNT_LOCK:
        if code in DISCOUNT_CODES:
            return False
        DISCOUNT_CODES[code] = {
            "percent": percent,
            "max_uses": max_uses,
            "used_count": 0,
            "expires_at": expires_at,
            "created_by": created_by,
        }
    await save_state()
    return True

async def use_discount_code(code: str) -> Optional[int]:
    async with DISCOUNT_LOCK:
        if code not in DISCOUNT_CODES:
            return None
        d = DISCOUNT_CODES[code]
        if d["used_count"] >= d["max_uses"]:
            return None
        if datetime.now() > datetime.fromisoformat(d["expires_at"]):
            return None
        d["used_count"] += 1
    await save_state()
    return d["percent"]

# ── لینک‌ها با Sing-box ────────────────────────────────────────────────────
async def make_link(
    label: str = "لینک جدید",
    limit_bytes: int = 0,
    expires_at: str | None = None,
    note: str = "",
    sub_id: str | None = None,
    protocol: str = "vless",
    port: int = 443,
    ip_limit: int = 0,
    speed_limit_bytes: int = 0,
    **kwargs
) -> tuple[str, dict]:
    uid = generate_uuid()
    config = {
        "label": label[:60],
        "limit_bytes": max(0, limit_bytes),
        "used_bytes": 0,
        "created_at": datetime.now().isoformat(),
        "active": True,
        "expires_at": expires_at,
        "note": (note or "").strip()[:200],
        "sub_id": sub_id,
        "protocol": protocol,
        "port": port,
        "ip_limit": max(0, ip_limit),
        "speed_limit_bytes": max(0, speed_limit_bytes),
        "is_default": False,
    }
    for k, v in kwargs.items():
        if v:
            config[k] = v
    
    async with LINKS_LOCK:
        LINKS[uid] = config
    
    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                ids = SUBS[sub_id].setdefault("link_ids", [])
                if uid not in ids:
                    ids.append(uid)
    
    await save_state()
    log_activity("link", f"کانفیگ «{label}» ساخته شد ({protocol})", "ok")
    return uid, config

async def remove_link(uid: str) -> str | None:
    async with LINKS_LOCK:
        if uid not in LINKS:
            return None
        label = LINKS[uid].get("label", uid)
        sub_id = LINKS[uid].get("sub_id")
        del LINKS[uid]
    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                ids = SUBS[sub_id].get("link_ids", [])
                if uid in ids:
                    ids.remove(uid)
    await save_state()
    log_activity("link", f"کانفیگ «{label}» حذف شد", "warn")
    return label

# ── State persistence ────────────────────────────────────────────────────────
async def load_state():
    global LINKS, SUBS, PRODUCTS, ORDERS, TEST_USERS, USER_CODES, FEEDBACKS, REYMIT_LINKS, TUTORIAL_CHANNEL
    global CARD_NUMBER, CARD_OWNER_NAME, PRICE_PER_GB, ADMIN_IDS, OWNER_ID
    global WALLETS, TRANSACTIONS, USER_CARDS, REFERRALS, DISCOUNT_CODES, LOTTERY
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if DATA_FILE.exists():
            async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
                raw = await f.read()
            data = json.loads(raw)
            LINKS.update(data.get("links", {}))
            SUBS.update(data.get("subs", {}))
            PRODUCTS.update(data.get("products", {}))
            ORDERS.update(data.get("orders", {}))
            TEST_USERS.update(data.get("test_users", {}))
            USER_CODES.update(data.get("user_codes", {}))
            REYMIT_LINKS = data.get("reymit_links", ["https://reymit.ir/itzjusteren"])
            FEEDBACKS = data.get("feedbacks", [])
            TUTORIAL_CHANNEL = data.get("tutorial_channel", "@TaaKaaOrg")
            if "password_hash" in data:
                AUTH["password_hash"] = data["password_hash"]
            if "card_number" in data:
                CARD_NUMBER = data["card_number"]
            if "card_owner_name" in data:
                CARD_OWNER_NAME = data["card_owner_name"]
            if "price_per_gb" in data:
                PRICE_PER_GB = data["price_per_gb"]
            if "admin_ids" in data:
                ADMIN_IDS = set(data["admin_ids"])
            if "owner_id" in data:
                OWNER_ID = data["owner_id"]
            WALLETS.update(data.get("wallets", {}))
            TRANSACTIONS.extend(data.get("transactions", []))
            USER_CARDS.update(data.get("user_cards", {}))
            REFERRALS.update(data.get("referrals", {}))
            DISCOUNT_CODES.update(data.get("discount_codes", {}))
            if "lottery" in data:
                LOTTERY.update(data["lottery"])
            logger.info(f"State loaded: {len(LINKS)} links, {len(WALLETS)} wallets, {len(USER_CARDS)} cards")
    except Exception as e:
        logger.warning(f"Could not load state: {e}")

async def save_state():
    async with SAVE_LOCK:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            data = {
                "links": dict(LINKS),
                "subs": dict(SUBS),
                "products": dict(PRODUCTS),
                "orders": dict(ORDERS),
                "test_users": dict(TEST_USERS),
                "user_codes": dict(USER_CODES),
                "reymit_links": REYMIT_LINKS,
                "feedbacks": FEEDBACKS,
                "tutorial_channel": TUTORIAL_CHANNEL,
                "password_hash": AUTH["password_hash"],
                "card_number": CARD_NUMBER,
                "card_owner_name": CARD_OWNER_NAME,
                "price_per_gb": PRICE_PER_GB,
                "admin_ids": list(ADMIN_IDS),
                "owner_id": OWNER_ID,
                "wallets": WALLETS,
                "transactions": TRANSACTIONS,
                "user_cards": USER_CARDS,
                "referrals": REFERRALS,
                "discount_codes": DISCOUNT_CODES,
                "lottery": LOTTERY,
                "saved_at": datetime.now().isoformat(),
            }
            tmp = DATA_FILE.with_suffix(".tmp")
            async with aiofiles.open(tmp, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
            tmp.replace(DATA_FILE)
        except Exception as e:
            logger.warning(f"Could not save state: {e}")

# ── Startup / Shutdown ────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    global http_client
    limits = httpx.Limits(max_connections=500, max_keepalive_connections=100)
    timeout = httpx.Timeout(30.0, connect=10.0)
    http_client = httpx.AsyncClient(limits=limits, timeout=timeout, follow_redirects=True)
    await load_state()
    await singbox_start()
    await _tg_start_bot()
    log_activity("system", "TK-SX سرور راه‌اندازی شد", "ok")
    logger.info(f"TK-SX v3.0 started on port {CONFIG['port']}")

@app.on_event("shutdown")
async def shutdown():
    await save_state()
    await singbox_stop()
    await _tg_stop_bot()
    if http_client:
        await http_client.aclose()

# ── Auth endpoints ────────────────────────────────────────────────────────────
@app.post("/api/login")
async def api_login(request: Request):
    body = await request.json()
    ip = client_ip(request)
    if hash_password(str(body.get("password", ""))) != AUTH["password_hash"]:
        log_activity("auth", f"تلاش ورود ناموفق از {ip}", "err")
        raise HTTPException(status_code=401, detail="رمز عبور اشتباه است")
    token = await create_session()
    log_activity("auth", f"ورود موفق به پنل از {ip}", "ok")
    resp = JSONResponse({"ok": True})
    resp.set_cookie(SESSION_COOKIE, token, max_age=SESSION_TTL, httponly=True, samesite="lax", path="/")
    return resp

@app.post("/api/logout")
async def api_logout(request: Request):
    await destroy_session(request.cookies.get(SESSION_COOKIE))
    resp = JSONResponse({"ok": True})
    resp.delete_cookie(SESSION_COOKIE, path="/")
    return resp

@app.get("/api/me")
async def api_me(request: Request):
    return {"authenticated": await is_valid_session(request.cookies.get(SESSION_COOKIE))}

@app.post("/api/change-password")
async def api_change_password(request: Request, token=Depends(require_auth)):
    body = await request.json()
    if hash_password(str(body.get("current_password", ""))) != AUTH["password_hash"]:
        raise HTTPException(status_code=400, detail="رمز فعلی اشتباه است")
    new = str(body.get("new_password", ""))
    if len(new) < 4:
        raise HTTPException(status_code=400, detail="رمز جدید باید حداقل ۴ کاراکتر باشد")
    AUTH["password_hash"] = hash_password(new)
    async with SESSIONS_LOCK:
        SESSIONS.clear()
        SESSIONS[token] = time.time() + SESSION_TTL
    await save_state()
    log_activity("auth", "رمز عبور پنل تغییر کرد", "ok")
    return {"ok": True}

# ── Link Management API ──────────────────────────────────────────────────────
@app.post("/api/links")
async def create_link(request: Request, _=Depends(require_auth)):
    body = await request.json()
    lv = float(body.get("limit_value") or 0)
    lu = body.get("limit_unit") or "GB"
    limit_bytes = 0 if lv <= 0 else parse_size_to_bytes(lv, lu)
    exp_days = int(body.get("expires_days") or 0)
    expires_at = (datetime.now() + timedelta(days=exp_days)).isoformat() if exp_days > 0 else None
    port = int(body.get("port") or 443)
    ip_limit = int(body.get("ip_limit") or 0)
    sv = float(body.get("speed_limit_value") or 0)
    su = body.get("speed_limit_unit") or "MBIT"
    speed_limit_bytes = 0 if sv <= 0 else parse_speed_to_bytes(sv, su)
    protocol = body.get("protocol") or "vless"
    
    extra = {}
    if protocol == "shadowsocks":
        extra["method"] = body.get("method", "aes-256-gcm")
        extra["password"] = body.get("password", secrets.token_urlsafe(16))
    elif protocol == "wireguard":
        extra["private_key"] = body.get("private_key", secrets.token_urlsafe(32))
        extra["public_key"] = body.get("public_key", secrets.token_urlsafe(32))
        extra["address"] = body.get("address", "10.0.0.2/32")
    elif protocol == "snell":
        extra["psk"] = body.get("psk", secrets.token_urlsafe(16))
    
    uid, link = await make_link(
        label=body.get("label") or "لینک جدید",
        limit_bytes=limit_bytes,
        expires_at=expires_at,
        note=body.get("note") or "",
        sub_id=body.get("sub_id") or None,
        protocol=protocol,
        port=port,
        ip_limit=ip_limit,
        speed_limit_bytes=speed_limit_bytes,
        **extra
    )
    
    host = get_host(request)
    link_url = generate_link_url(uid, link, host)
    
    return {
        "uuid": uid,
        **link,
        "expired": False,
        "link_url": link_url,
        "sub_url": f"https://{host}/sub/{uid}",
    }

@app.get("/api/links")
async def list_links(request: Request, _=Depends(require_auth)):
    host = get_host(request)
    async with LINKS_LOCK:
        snap = dict(LINKS)
    result = []
    for uid, d in snap.items():
        result.append({
            "uuid": uid,
            **d,
            "expired": is_link_expired(d),
            "link_url": generate_link_url(uid, d, host),
            "sub_url": f"https://{host}/sub/{uid}",
            "connected_ips": len(unique_ips_for_uuid(uid)),
        })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"links": result}

@app.patch("/api/links/{uid}")
async def update_link(uid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        link = LINKS[uid]
        if "active" in body:
            link["active"] = bool(body["active"])
        if "label" in body:
            link["label"] = str(body["label"])[:60]
        if "note" in body:
            link["note"] = str(body["note"])[:200]
        if "reset_usage" in body and body["reset_usage"]:
            link["used_bytes"] = 0
        if "limit_value" in body:
            lv = float(body.get("limit_value") or 0)
            lu = body.get("limit_unit") or "GB"
            link["limit_bytes"] = 0 if lv <= 0 else parse_size_to_bytes(lv, lu)
        if "expires_days" in body:
            ed = int(body["expires_days"] or 0)
            link["expires_at"] = (datetime.now() + timedelta(days=ed)).isoformat() if ed > 0 else None
        if "port" in body:
            link["port"] = int(body.get("port") or 443)
        if "ip_limit" in body:
            link["ip_limit"] = max(0, int(body.get("ip_limit") or 0))
        if "speed_limit_value" in body:
            sv = float(body.get("speed_limit_value") or 0)
            su = body.get("speed_limit_unit") or "MBIT"
            link["speed_limit_bytes"] = 0 if sv <= 0 else parse_speed_to_bytes(sv, su)
            from speed_limit import reset_bucket
            reset_bucket(uid)
    await save_state()
    return {"ok": True}

@app.delete("/api/links/{uid}")
async def delete_link(uid: str, _=Depends(require_auth)):
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        label = LINKS[uid].get("label", uid)
        sub_id = LINKS[uid].get("sub_id")
        del LINKS[uid]
    if sub_id:
        async with SUBS_LOCK:
            if sub_id in SUBS:
                ids = SUBS[sub_id].get("link_ids", [])
                if uid in ids:
                    ids.remove(uid)
    await save_state()
    return {"ok": True, "deleted": uid}

@app.get("/sub/{uuid}")
async def subscription_single(uuid: str, request: Request):
    import base64
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    if not link or not is_link_allowed(link):
        raise HTTPException(status_code=404, detail="not found or inactive")
    host = get_host(request)
    link_url = generate_link_url(uuid, link, host)
    content = base64.b64encode(link_url.encode()).decode()
    return Response(content=content, media_type="text/plain",
                    headers={"profile-title": quote(link["label"]), "support-url": "https://t.me/ItzJustEren"})

# ── Subscription Groups ──────────────────────────────────────────────────────
@app.post("/api/subs")
async def create_sub(request: Request, _=Depends(require_auth)):
    body = await request.json()
    name = (body.get("name") or "گروه جدید").strip()[:60]
    desc = (body.get("desc") or "").strip()[:200]
    password = (body.get("password") or "").strip()
    sub_id = generate_uuid()
    uuid_key = secrets.token_urlsafe(16)
    async with SUBS_LOCK:
        SUBS[sub_id] = {
            "name": name,
            "desc": desc,
            "password_hash": hash_password(password) if password else None,
            "uuid_key": uuid_key,
            "created_at": datetime.now().isoformat(),
            "link_ids": [],
        }
    await save_state()
    host = get_host(request)
    return {
        "sub_id": sub_id,
        **SUBS[sub_id],
        "public_url": f"https://{host}/p/{uuid_key}",
        "sub_url": f"https://{host}/sub-group/{uuid_key}",
    }

@app.get("/api/subs")
async def list_subs(request: Request, _=Depends(require_auth)):
    host = get_host(request)
    async with SUBS_LOCK:
        snap_subs = dict(SUBS)
    async with LINKS_LOCK:
        snap_links = dict(LINKS)
    result = []
    for sid, s in snap_subs.items():
        link_ids = s.get("link_ids", [])
        active_count = sum(1 for lid in link_ids if is_link_allowed(snap_links.get(lid)))
        total_used = sum(snap_links[lid].get("used_bytes", 0) for lid in link_ids if lid in snap_links)
        result.append({
            "sub_id": sid,
            **s,
            "password_hash": None,
            "has_password": s.get("password_hash") is not None,
            "links_count": len(link_ids),
            "active_count": active_count,
            "total_used_bytes": total_used,
            "total_used_fmt": fmt_bytes(total_used),
            "public_url": f"https://{host}/p/{s['uuid_key']}",
            "sub_url": f"https://{host}/sub-group/{s['uuid_key']}",
        })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"subs": result}

@app.patch("/api/subs/{sub_id}")
async def update_sub(sub_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        s = SUBS[sub_id]
        if "name" in body:
            s["name"] = str(body["name"])[:60]
        if "desc" in body:
            s["desc"] = str(body["desc"])[:200]
        if "password" in body:
            pw = str(body["password"]).strip()
            s["password_hash"] = hash_password(pw) if pw else None
        if "link_ids" in body:
            s["link_ids"] = list(body["link_ids"])
    await save_state()
    return {"ok": True}

@app.delete("/api/subs/{sub_id}")
async def delete_sub(sub_id: str, _=Depends(require_auth)):
    async with SUBS_LOCK:
        if sub_id not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        name = SUBS[sub_id].get("name", sub_id)
        del SUBS[sub_id]
    async with LINKS_LOCK:
        for link in LINKS.values():
            if link.get("sub_id") == sub_id:
                link["sub_id"] = None
    await save_state()
    return {"ok": True, "deleted": sub_id}

@app.get("/sub-group/{uuid_key}")
async def sub_group_subscription(uuid_key: str, request: Request):
    import base64
    async with SUBS_LOCK:
        sub = next((s for s in SUBS.values() if s.get("uuid_key") == uuid_key), None)
    if not sub:
        raise HTTPException(status_code=404, detail="not found")
    if sub.get("password_hash"):
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            raise HTTPException(status_code=403, detail="wrong password")
    host = get_host(request)
    link_ids = sub.get("link_ids", [])
    async with LINKS_LOCK:
        lines = []
        for lid in link_ids:
            link = LINKS.get(lid)
            if link and is_link_allowed(link):
                lines.append(generate_link_url(lid, link, host))
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain",
                    headers={"profile-title": quote(sub["name"]), "support-url": "https://t.me/ItzJustEren"})

# ── Stats ────────────────────────────────────────────────────────────────────
@app.get("/stats")
async def get_stats(_=Depends(require_auth)):
    async with LINKS_LOCK:
        snap = dict(LINKS)
    return {
        "active_connections": len(connections),
        "total_traffic_mb": round(stats["total_bytes"] / (1024 ** 2), 2),
        "total_requests": stats["total_requests"],
        "total_errors": stats["total_errors"],
        "uptime": uptime(),
        "timestamp": datetime.now().isoformat(),
        "hourly": dict(hourly_traffic),
        "recent_errors": list(error_logs)[-10:],
        "links_count": len(snap),
        "active_links": sum(1 for l in snap.values() if is_link_allowed(l)),
        "expired_links": sum(1 for l in snap.values() if is_link_expired(l)),
        "subs_count": len(SUBS),
        "singbox_status": singbox_status(),
        "wallets_count": len(WALLETS),
        "cards_count": len(USER_CARDS),
    }

def uptime() -> str:
    secs = int(time.time() - stats["start_time"])
    h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

@app.get("/api/connections")
async def get_connections(_=Depends(require_auth)):
    async with LINKS_LOCK:
        snap = dict(LINKS)
    grouped: dict[str, dict] = {}
    for conn_id, c in connections.items():
        ip = c.get("ip", "نامشخص")
        link = snap.get(c.get("uuid"))
        label = link.get("label") if link else "نامشخص"
        g = grouped.get(ip)
        if g is None:
            g = {"ip": ip, "sessions": 0, "bytes": 0, "labels": set(), "transports": set(),
                 "first_connected_at": c.get("connected_at"), "last_connected_at": c.get("connected_at")}
            grouped[ip] = g
        g["sessions"] += 1
        g["bytes"] += c.get("bytes", 0)
        g["labels"].add(label)
        g["transports"].add(c.get("transport", "singbox"))
    result = []
    for ip, g in grouped.items():
        result.append({
            "ip": ip,
            "sessions": g["sessions"],
            "labels": sorted(g["labels"]),
            "label": " · ".join(sorted(g["labels"])) if g["labels"] else "نامشخص",
            "transports": sorted(g["transports"]),
            "bytes": g["bytes"],
            "bytes_fmt": fmt_bytes(g["bytes"]),
            "connected_at": g["first_connected_at"],
            "last_connected_at": g["last_connected_at"],
        })
    result.sort(key=lambda x: x.get("last_connected_at") or "", reverse=True)
    return {"connections": result, "count": len(result), "raw_count": len(connections)}

@app.get("/api/activity")
async def get_activity(_=Depends(require_auth)):
    return {"logs": list(activity_logs)[-150:]}

# ── Wallet API ──────────────────────────────────────────────────────────────
@app.get("/api/wallet/{user_id}")
async def get_wallet(user_id: int, _=Depends(require_auth)):
    return {
        "balance": await get_balance(user_id),
        "transactions": [t for t in TRANSACTIONS if t["user_id"] == user_id][-20:]
    }

@app.post("/api/wallet/add")
async def add_wallet(request: Request, _=Depends(require_auth)):
    body = await request.json()
    user_id = body.get("user_id")
    amount = body.get("amount")
    description = body.get("description", "شارژ کیف پول")
    if not user_id or not amount or amount <= 0:
        raise HTTPException(400, "user_id و amount مثبت الزامی هستند")
    await add_balance(user_id, amount, description, request.state.user_id if hasattr(request.state, 'user_id') else None)
    return {"ok": True}

# ── Card API ─────────────────────────────────────────────────────────────────
@app.get("/api/card/{user_id}")
async def get_card(user_id: int, _=Depends(require_auth)):
    return await get_card_status(user_id)

@app.post("/api/card/approve/{user_id}")
async def approve_card(user_id: int, _=Depends(require_auth)):
    async with CARDS_LOCK:
        if user_id not in USER_CARDS:
            raise HTTPException(404, "کارت یافت نشد")
        USER_CARDS[user_id]["status"] = "approved"
        USER_CARDS[user_id]["approved_at"] = datetime.now().isoformat()
    await save_state()
    return {"ok": True}

@app.post("/api/card/reject/{user_id}")
async def reject_card(user_id: int, _=Depends(require_auth)):
    async with CARDS_LOCK:
        if user_id not in USER_CARDS:
            raise HTTPException(404, "کارت یافت نشد")
        USER_CARDS[user_id]["status"] = "rejected"
    await save_state()
    return {"ok": True}

# ── Referral API ─────────────────────────────────────────────────────────────
@app.get("/api/referral/{user_id}")
async def get_referral(user_id: int, _=Depends(require_auth)):
    info = await get_referral_info(user_id)
    if not info:
        info = {"code": await generate_referral_code(user_id), "earnings": 0, "referred_users": []}
    return info

# ── Discount API ─────────────────────────────────────────────────────────────
@app.post("/api/discount/create")
async def create_discount(request: Request, _=Depends(require_auth)):
    body = await request.json()
    code = body.get("code", "").strip().upper()
    percent = body.get("percent")
    max_uses = body.get("max_uses", 1)
    expires_days = body.get("expires_days", 30)
    if not code or not percent:
        raise HTTPException(400, "کد و درصد الزامی هستند")
    expires_at = (datetime.now() + timedelta(days=expires_days)).isoformat()
    result = await create_discount_code(code, percent, max_uses, expires_at, request.state.user_id)
    if not result:
        raise HTTPException(400, "کد تکراری است")
    return {"ok": True}

@app.get("/api/discount/list")
async def list_discounts(_=Depends(require_auth)):
    return {"discounts": DISCOUNT_CODES}

# ── Product Management ──────────────────────────────────────────────────────
@app.post("/api/products")
async def create_product(request: Request, _=Depends(require_auth)):
    body = await request.json()
    name = body.get("name", "").strip()
    if not name:
        raise HTTPException(400, "نام محصول الزامی است")
    try:
        volume_gb = float(body.get("volume_gb", 0))
        duration_days = int(body.get("duration_days", 0))
        speed_mbps = float(body.get("speed_mbps", 0))
        price = float(body.get("price", 0))
    except (TypeError, ValueError):
        raise HTTPException(400, "مقادیر عددی نامعتبر")
    if volume_gb <= 0 or duration_days <= 0 or price <= 0:
        raise HTTPException(400, "حجم، مدت و قیمت باید مثبت باشند")
    product_id = secrets.token_hex(8)
    async with PRODUCTS_LOCK:
        PRODUCTS[product_id] = {
            "product_id": product_id,
            "name": name,
            "volume_gb": volume_gb,
            "duration_days": duration_days,
            "speed_mbps": speed_mbps,
            "price": price,
            "created_at": datetime.now().isoformat(),
        }
    await save_state()
    return {"ok": True, "product_id": product_id}

@app.get("/api/products")
async def list_products(_=Depends(require_auth)):
    async with PRODUCTS_LOCK:
        return {"products": list(PRODUCTS.values())}

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: str, _=Depends(require_auth)):
    async with PRODUCTS_LOCK:
        if product_id not in PRODUCTS:
            raise HTTPException(404, "محصول یافت نشد")
        del PRODUCTS[product_id]
    await save_state()
    return {"ok": True}

# ── Orders ──────────────────────────────────────────────────────────────────
@app.get("/api/orders")
async def list_orders(_=Depends(require_auth)):
    async with ORDERS_LOCK:
        return {"orders": list(ORDERS.values())}

@app.patch("/api/orders/{order_id}")
async def update_order(order_id: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    status = body.get("status")
    async with ORDERS_LOCK:
        if order_id not in ORDERS:
            raise HTTPException(404, "سفارش یافت نشد")
        if status:
            ORDERS[order_id]["status"] = status
    await save_state()
    return {"ok": True}

# ── Admin Management ────────────────────────────────────────────────────────
@app.get("/api/admins")
async def list_admins(_=Depends(require_auth)):
    return {"admins": list(ADMIN_IDS), "owner_id": OWNER_ID}

@app.post("/api/admins")
async def add_admin(request: Request, _=Depends(require_auth)):
    body = await request.json()
    user_id = body.get("user_id")
    if not user_id:
        raise HTTPException(400, "user_id الزامی است")
    user_id = int(user_id)
    global ADMIN_IDS
    ADMIN_IDS.add(user_id)
    await save_state()
    return {"ok": True}

@app.delete("/api/admins/{user_id}")
async def remove_admin(user_id: int, _=Depends(require_auth)):
    if user_id == OWNER_ID:
        raise HTTPException(400, "نمی‌توان اونر را حذف کرد")
    global ADMIN_IDS
    if user_id not in ADMIN_IDS:
        raise HTTPException(404, "ادمین یافت نشد")
    ADMIN_IDS.remove(user_id)
    await save_state()
    return {"ok": True}

# ── Settings ────────────────────────────────────────────────────────────────
@app.get("/api/settings/card")
async def get_card_settings(_=Depends(require_auth)):
    return {"card_number": CARD_NUMBER, "card_owner_name": CARD_OWNER_NAME}

@app.post("/api/settings/card")
async def set_card_settings(request: Request, _=Depends(require_auth)):
    body = await request.json()
    new_card = body.get("card_number", "").strip()
    new_owner = body.get("card_owner_name", "").strip()
    if not new_card:
        raise HTTPException(400, "شماره کارت نمی‌تواند خالی باشد")
    global CARD_NUMBER, CARD_OWNER_NAME
    CARD_NUMBER = new_card
    CARD_OWNER_NAME = new_owner if new_owner else CARD_OWNER_NAME
    await save_state()
    return {"ok": True}

@app.get("/api/settings/price")
async def get_price_per_gb(_=Depends(require_auth)):
    return {"price_per_gb": PRICE_PER_GB}

@app.post("/api/settings/price")
async def set_price_per_gb(request: Request, _=Depends(require_auth)):
    body = await request.json()
    price = float(body.get("price_per_gb", 0))
    if price <= 0:
        raise HTTPException(400, "قیمت باید مثبت باشد")
    global PRICE_PER_GB
    PRICE_PER_GB = price
    await save_state()
    return {"ok": True}

@app.get("/api/settings/reymit")
async def get_reymit_links(_=Depends(require_auth)):
    return {"links": REYMIT_LINKS}

@app.post("/api/settings/reymit")
async def set_reymit_links(request: Request, _=Depends(require_auth)):
    body = await request.json()
    links = body.get("links", [])
    if not links or not isinstance(links, list):
        raise HTTPException(400, "لینک‌ها باید به‌صورت لیست باشند")
    global REYMIT_LINKS
    REYMIT_LINKS = [l.strip() for l in links if l.strip()]
    await save_state()
    return {"ok": True}

@app.get("/api/settings/stars_rate")
async def get_stars_rate(_=Depends(require_auth)):
    return {"stars_rate": CONFIG["stars_rate"]}

@app.post("/api/settings/stars_rate")
async def set_stars_rate(request: Request, _=Depends(require_auth)):
    body = await request.json()
    rate = int(body.get("stars_rate", 1000))
    if rate <= 0:
        raise HTTPException(400, "نرخ باید مثبت باشد")
    CONFIG["stars_rate"] = rate
    await save_state()
    return {"ok": True}

@app.get("/api/feedbacks")
async def get_feedbacks(_=Depends(require_auth)):
    return {"feedbacks": FEEDBACKS}

@app.post("/api/feedbacks")
async def add_feedback(request: Request, _=Depends(require_auth)):
    body = await request.json()
    text = body.get("text", "").strip()
    if not text:
        raise HTTPException(400, "متن بازخورد نمی‌تواند خالی باشد")
    feedback = {"id": secrets.token_hex(8), "user_id": body.get("user_id"), "username": body.get("username", "کاربر"),
                "text": text, "created_at": datetime.now().isoformat(), "approved": body.get("approved", False)}
    FEEDBACKS.append(feedback)
    await save_state()
    return {"ok": True}

# ── WebSocket ──────────────────────────────────────────────────────────────
@app.websocket("/ws/{uuid}")
async def websocket_tunnel(ws: WebSocket, uuid: str):
    from relay import handle_websocket
    await handle_websocket(ws, uuid, connections, LINKS, LINKS_LOCK, stats, error_logs, hourly_traffic, logger)

# ── XHTTP ──────────────────────────────────────────────────────────────────
from xhttp import router as xhttp_router
app.include_router(xhttp_router)

# ── HTML Pages (پنل اصلی + مینی‌اپ) ─────────────────────────────────────────
from pages import LOGIN_HTML, DASHBOARD_HTML, CYRUS_MINIAPP_HTML, get_public_page_html

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(url="/dashboard")
    return HTMLResponse(content=LOGIN_HTML)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(url="/login")
    return HTMLResponse(content=DASHBOARD_HTML)

@app.get("/p/{uuid_key}", response_class=HTMLResponse)
async def public_sub_page(uuid_key: str, request: Request):
    async with SUBS_LOCK:
        sub = next(({"sub_id": sid, **s} for sid, s in SUBS.items() if s.get("uuid_key") == uuid_key), None)
    if not sub:
        return HTMLResponse("<h2 style='font-family:sans-serif;padding:40px'>گروه پیدا نشد</h2>", status_code=404)
    return HTMLResponse(content=get_public_page_html(uuid_key))

@app.get("/api/public/sub/{uuid_key}")
async def public_sub_data(uuid_key: str, request: Request):
    async with SUBS_LOCK:
        sub_entry = next(((sid, s) for sid, s in SUBS.items() if s.get("uuid_key") == uuid_key), None)
    if not sub_entry:
        raise HTTPException(status_code=404, detail="not found")
    sub_id, sub = sub_entry
    has_pw = sub.get("password_hash") is not None
    if has_pw:
        pw = request.query_params.get("pw", "")
        if hash_password(pw) != sub["password_hash"]:
            return JSONResponse({"locked": True, "name": sub["name"]})
    host = get_host(request)
    link_ids = sub.get("link_ids", [])
    async with LINKS_LOCK:
        snap = dict(LINKS)
    links_out = []
    active_conns = 0
    for lid in link_ids:
        link = snap.get(lid)
        if not link:
            continue
        allowed = is_link_allowed(link)
        conn_count = sum(1 for c in connections.values() if c.get("uuid") == lid)
        active_conns += conn_count
        links_out.append({
            "uuid": lid,
            "label": link["label"],
            "active": allowed,
            "protocol": link.get("protocol", "vless"),
            "used_bytes": link.get("used_bytes", 0),
            "used_fmt": fmt_bytes(link.get("used_bytes", 0)),
            "limit_bytes": link.get("limit_bytes", 0),
            "limit_fmt": "∞" if link.get("limit_bytes", 0) == 0 else fmt_bytes(link["limit_bytes"]),
            "expires_at": link.get("expires_at"),
            "link_url": generate_link_url(lid, link, host),
            "sub_url": f"https://{host}/sub/{lid}",
            "connections": conn_count,
            "ip_limit": link.get("ip_limit", 0),
            "speed_limit_bytes": link.get("speed_limit_bytes", 0),
        })
    total_used = sum(l["used_bytes"] for l in links_out)
    return {
        "locked": False,
        "name": sub["name"],
        "desc": sub.get("desc", ""),
        "sub_url": f"https://{host}/sub-group/{uuid_key}",
        "active_connections": active_conns,
        "total_used_fmt": fmt_bytes(total_used),
        "links": links_out,
    }

# ── مینی‌اپ Cyrus Bot ──────────────────────────────────────────────────────
@app.get("/cyrus", response_class=HTMLResponse)
async def cyrus_mini_app(request: Request):
    """صفحه ورود مینی‌اپ Cyrus Bot (تم آبی-یخی-مشکی)"""
    return HTMLResponse(content=CYRUS_MINIAPP_HTML)

@app.post("/api/miniapp/login")
async def miniapp_login(request: Request):
    """ورود از طریق مینی‌اپ"""
    body = await request.json()
    password = body.get("password")
    if hash_password(str(password)) != AUTH["password_hash"]:
        raise HTTPException(status_code=401, detail="رمز عبور اشتباه است")
    token = await create_session()
    return {"ok": True, "token": token}

@app.get("/api/miniapp/stats")
async def miniapp_stats(request: Request, token: str = None):
    """دریافت آمار برای مینی‌اپ"""
    if not token or not await is_valid_session(token):
        raise HTTPException(status_code=401, detail="unauthorized")
    async with LINKS_LOCK:
        snap = dict(LINKS)
    return {
        "active_connections": len(connections),
        "total_traffic_mb": round(stats["total_bytes"] / (1024 ** 2), 2),
        "links_count": len(snap),
        "active_links": sum(1 for l in snap.values() if is_link_allowed(l)),
        "subs_count": len(SUBS),
        "products_count": len(PRODUCTS),
        "orders_pending": len([o for o in ORDERS.values() if o.get("status") == "pending"]),
        "wallets_count": len(WALLETS),
        "cards_pending": len([c for c in USER_CARDS.values() if c.get("status") == "pending"]),
        "singbox_status": singbox_status(),
        "uptime": uptime(),
    }

# ── Proxy ────────────────────────────────────────────────────────────────────
_HOP = {"connection","keep-alive","proxy-authenticate","proxy-authorization",
        "te","trailers","transfer-encoding","upgrade","content-encoding","content-length"}

@app.api_route("/proxy/{target_url:path}", methods=["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS"])
async def http_proxy(target_url: str, request: Request):
    if not target_url.startswith("http"):
        target_url = "https://" + target_url
    try:
        body = await request.body()
        headers = {k: v for k, v in request.headers.items() if k.lower() not in _HOP and k.lower() != "host"}
        resp = await http_client.request(method=request.method, url=target_url, headers=headers, content=body)
        stats["total_bytes"] += len(resp.content)
        stats["total_requests"] += 1
        hourly_traffic[now_ir().strftime("%H:00")] += len(resp.content)
        return Response(content=resp.content, status_code=resp.status_code,
                        headers={k: v for k, v in resp.headers.items() if k.lower() not in _HOP})
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "url": target_url, "time": datetime.now().isoformat()})
        raise HTTPException(status_code=502, detail=f"Proxy error: {exc}")

# ── Telegram bot ─────────────────────────────────────────────────────────────
from telegram_bot import start_bot as _tg_start_bot, stop_bot as _tg_stop_bot

# ── Helpers ──────────────────────────────────────────────────────────────────
def parse_size_to_bytes(value: float, unit: str) -> int:
    unit = unit.upper()
    if unit == "GB": return int(value * 1024 ** 3)
    if unit == "MB": return int(value * 1024 ** 2)
    if unit == "KB": return int(value * 1024)
    return int(value)

def parse_speed_to_bytes(value: float, unit: str) -> int:
    if value <= 0:
        return 0
    unit = (unit or "MBIT").upper()
    if unit == "MBIT":
        return int(value * 1024 * 1024 / 8)
    if unit == "KB":
        return int(value * 1024)
    if unit == "MB":
        return int(value * 1024 * 1024)
    return int(value)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=CONFIG["port"], log_level="info", workers=1)
