# speed_limit.py
# Token Bucket rate limiter برای محدودیت سرعت هر کاربر

import asyncio
import time
from typing import Dict

# uuid -> bytes/sec (0 = بدون محدودیت)
_limits: Dict[str, int] = {}

# uuid -> {"tokens": float, "last": float}
_buckets: Dict[str, dict] = {}

# uuid -> asyncio.Lock
_locks: Dict[str, asyncio.Lock] = {}


def set_limit(uuid: str, bytes_per_sec: int):
    """تنظیم محدودیت سرعت برای یه uuid (بایت بر ثانیه)"""
    _limits[uuid] = max(0, int(bytes_per_sec))


def get_limit(uuid: str) -> int:
    return _limits.get(uuid, 0)


def reset_bucket(uuid: str):
    """پاک کردن bucket و lock یک uuid"""
    _buckets.pop(uuid, None)
    _locks.pop(uuid, None)


def clear_all():
    _limits.clear()
    _buckets.clear()
    _locks.clear()


async def throttle(uuid: str, chunk_size: int):
    """
    Token Bucket rate limiter.
    اگه محدودیتی برای uuid نباشه، فوری برمی‌گرده.
    وگرنه، اگه لازم باشه، sleep میکنه تا token کافی داشته باشه.
    """
    limit = _limits.get(uuid, 0)
    if limit <= 0:
        return

    lock = _locks.get(uuid)
    if lock is None:
        lock = asyncio.Lock()
        _locks[uuid] = lock

    async with lock:
        now = time.monotonic()
        bucket = _buckets.get(uuid)

        if bucket is None:
            bucket = {"tokens": float(limit), "last": now}
            _buckets[uuid] = bucket

        # شارژ مجدد tokenها بر اساس زمان گذشته
        elapsed = now - bucket["last"]
        if elapsed > 0:
            bucket["tokens"] = min(float(limit), bucket["tokens"] + elapsed * limit)
            bucket["last"] = now

        # اگه token کافی داریم، فوری مصرف کن
        if bucket["tokens"] >= chunk_size:
            bucket["tokens"] -= chunk_size
            return

        # وگرنه، منتظر بمون
        needed = chunk_size - bucket["tokens"]
        wait_time = needed / limit  # ثانیه
        await asyncio.sleep(wait_time)

        bucket["tokens"] = 0.0
        bucket["last"] = time.monotonic()