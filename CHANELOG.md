# Changelog

تمام تغییرات مهم پروژه TK-SX در این فایل ثبت می‌شود.

فرمت بر اساس [Keep a Changelog](https://keepachangelog.com/fa/1.1.0/)
و نسخه‌بندی بر اساس [Semantic Versioning](https://semver.org/).

## [3.0.0] - 2026-09-11

### Added ✨
- پشتیبانی از VLESS + WebSocket + TLS
- پشتیبانی از VMess و Trojan روی WebSocket
- پشتیبانی از Shadowsocks
- **UDP over TCP** برای VLESS, WireGuard و Hysteria2
- XHTTP Ultra با دو حالت packet-up و stream-up
- سیستم کیف پول کامل با تاریخچه تراکنش‌ها
- پرداخت کارت به کارت با تایید رسید
- پرداخت Reymit
- پرداخت Telegram Stars
- پرداخت Gift (ارسال به @ItzJustEren)
- سیستم معرفی (Referral) با ۱۰٪ کمیسیون
- کد تخفیف با محدودیت تعداد و زمان
- قرعه‌کشی با سیستم بلیت
- Rate Limiting با Token Bucket
- محدودیت IP (ip_limit)
- محدودیت سرعت (speed_limit)
- گروه‌های اشتراک (Subscription Groups) با پسورد
- صفحه‌ی عمومی گروه اشتراک
- مینی‌اپ Cyrus با تم آبی-مشکی
- XHTTP Session Reaper برای پاک‌سازی سشن‌های idle
- Activity Log برای رصد عملیات
- داشبورد فارسی/انگلیسی با تم تیره/روشن

### Fixed 🐛
- **CORS Security**: `allow_origins=["*"]` به دامنه‌ی محدود تغییر کرد
- **Sing-box flow**: حذف `xtls-rprx-vision` از VLESS WebSocket (ناسازگار بود)
- **Sing-box users**: تغییر از `uuid` تکی به آرایه‌ی `users`
- **Circular Import**: در `telegram_bot.py` رفع شد
- **پورت هاردکد**: در Dockerfile به `${PORT}` تغییر کرد
- **Session Management**: بهبود TTL و بازیابی
- **XHTTP**: هدر `\x00\x00` در پاسخ VLESS اضافه شد
- **relay.py**: پشتیبانی کامل از UDP (command=2)
- **DNS Sniffing**: با `sniff: True` فعال شد

### Changed 🔄
- بازنویسی کامل `relay.py` با پشتیبانی UDP
- بهبود پارسر VLESS header (`relay_vless.py`)
- بهبود XHTTP با Session Reaper
- Dockerfile CMD با `${PORT}` برای Railway
- ساختار inboundهای Sing-box: یک inbound مشترک برای هر پروتکل

### Removed ❌
- `xtls-rprx-vision` از VLESS WebSocket
- Telegram bot از startup (غیرفعال شد ولی فایلش می‌مونه)
- `Procfile` و `runtime.txt` (چون Dockerfile داریم)

---

## [2.0.0] - 2025-12-15

### Added
- FastAPI backend
- Sing-box integration
- پنل ادمین اولیه
- سیستم لینک پایه
- WebSocket relay اولیه

---

## [1.0.0] - 2025-10-01

### Added
- نسخه‌ی اولیه پروژه
- Sing-box core
- WebSocket relay پایه
- پنل ورود ساده

---

<div align="center">

**ساخته شده با ❤️ برای ایرانیان**

[@ItzJustEren](https://t.me/ItzJustEren) · [@TaaKaaOrg](https://t.me/TaaKaaOrg)

</div>