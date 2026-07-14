# speed_limit.py - Token Bucket
import asyncio, time
from main import LINKS
_buckets = {}
MIN_RATE = 1024; MIN_BURST = 16*1024
class _Bucket:
    __slots__ = ("rate", "capacity", "tokens", "last")
    def __init__(self, rate): self.rate = max(rate, MIN_RATE); self.capacity = max(self.rate, MIN_BURST); self.tokens = self.capacity; self.last = time.monotonic()
    def _refill(self):
        now = time.monotonic(); elapsed = now - self.last
        if elapsed > 0: self.last = now; self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
    async def consume(self, n):
        while True:
            self._refill()
            if self.tokens >= n: self.tokens -= n; return
            wait = (n - self.tokens) / self.rate
            await asyncio.sleep(min(max(wait, 0.004), 0.5))
def _get_bucket(uuid, rate):
    b = _buckets.get(uuid)
    if b is None or b.rate != max(rate, MIN_RATE): b = _Bucket(rate); _buckets[uuid] = b
    return b
async def throttle(uuid, nbytes):
    if nbytes <= 0: return
    link = LINKS.get(uuid)
    rate = int((link or {}).get("speed_limit_bytes", 0) or 0)
    if rate <= 0: return
    await _get_bucket(uuid, rate).consume(nbytes)
def reset_bucket(uuid): _buckets.pop(uuid, None)
