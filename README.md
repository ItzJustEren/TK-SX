<div align="center">
  <br>
  <img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&weight=900&size=60&duration=3000&pause=500&color=F97316&center=true&vCenter=true&width=600&height=80&lines=TK-SX" alt="TK-SX">
  <br>
  <h3 style="color:#F97316; font-size:24px; font-weight:300; letter-spacing:4px;">
    ⚡ THE ULTIMATE VPN MANAGEMENT PANEL ⚡
  </h3>
  <br>
  <p style="color:#B0B0B0; font-size:14px;">
    <a href="#english" style="color:#F97316; font-weight:700;">English</a> &nbsp;·&nbsp;
    <a href="#persian" style="color:#B0B0B0;">فارسی</a>
  </p>
  <br>
  <img src="https://img.shields.io/github/v/release/ItzJustEren/TK-SX?style=for-the-badge&color=F97316&label=Release" alt="Release">
  <img src="https://img.shields.io/github/license/ItzJustEren/TK-SX?style=for-the-badge&color=F97316" alt="License">
  <img src="https://img.shields.io/badge/Python-3.12-F97316?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.104-F97316?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Railway-Ready-F97316?style=for-the-badge&logo=railway&logoColor=white" alt="Railway">
  <br><br>
</div>

---

## 🚀 What is TK-SX?

**TK-SX** is a **next-generation VPN management panel** built on the powerful **Sing-box** core. It combines a professional web dashboard, a **complete Telegram store bot (Cyrus Bot)** with all Mirza Bot features, and a beautiful **Mini App** for mobile management — all in one seamless package.

Designed for **Railway** and capable of handling **15+ concurrent users** with minimal resource usage, TK-SX is the ultimate solution for VPN providers, resellers, and individual users who want a **fully automated** system.

---

## ✨ Features

### 🔥 Core Panel
- **11 VPN Protocols** — VLESS, VMess, Trojan, Shadowsocks, SOCKS5, HTTP, WireGuard, Hysteria2, TUN, Dokodemo-door, Snell
- **UDP over TCP** for WireGuard & Hysteria2 (bypasses Railway UDP limitations)
- **XHTTP Ultra** with packet-up & stream-up modes (adaptive flow control)
- **Real-time connection monitoring** with IP tracking
- **Subscription groups** with public pages and password protection
- **Traffic charts** — hourly, daily, peak usage
- **Full Persian/English UI** with dark/light themes

### 💰 Wallet & Payments
- **Built-in wallet system** with transaction history
- **Card-to-card payments** with receipt verification
- **Reymit payment gateway** integration
- **Telegram Stars** support (configurable rate)
- **Gift payments** (send to @ItzJustEren with clear instructions)

### 🔗 Referral & Marketing
- **Affiliate system** — 10% commission on referrals
- **Unique referral codes** for each user
- **Discount codes** (admin-created, with usage limits)
- **Lottery system** with tickets per purchase

### 🤖 Cyrus Bot (Telegram Store)
- **Automated product purchasing**
- **Free trial** (50MB, once a week)
- **Subscription renewal** with one click
- **User leveling** (Level 10 = 5GB free bonus)
- **Order approval/rejection** with reasons (fake receipt, late submission)
- **User feedback system** with admin approval
- **Full admin panel** inside Telegram

### 🖥️ Mini App (Mobile Dashboard)
- **Login page** with welcome message
- **Real-time stats** — connections, links, products, orders
- **Quick access** to main panel and Telegram bot
- **Ice-blue & black theme** with eagle logo
- **Fully responsive** for mobile

---

## 📦 Supported Protocols

| Protocol | V2RayNG | Sing-box Client | UDP over TCP |
|----------|---------|-----------------|--------------|
| **VLESS** | ✅ | ✅ | ❌ |
| **VMess** | ✅ | ✅ | ❌ |
| **Trojan** | ✅ | ✅ | ❌ |
| **Shadowsocks** | ✅ | ✅ | ❌ |
| **SOCKS5** | ✅ | ✅ | ❌ |
| **HTTP** | ✅ | ✅ | ❌ |
| **WireGuard** | ❌ | ✅ | ✅ |
| **Hysteria2** | ❌ | ✅ | ✅ |
| **TUN** | ❌ | ✅ | ❌ |
| **Dokodemo-door** | ❌ | ✅ | ❌ |
| **Snell** | ❌ | ✅ | ❌ |

---

## 📁 Project Structure
TK-SX/
├── main.py # FastAPI core with all APIs
├── telegram_bot.py # Cyrus Bot (full Mirza features)
├── singbox_manager.py # Sing-box management + UDP over TCP
├── relay.py # WebSocket handler
├── xhttp.py # XHTTP Ultra transport
├── speed_limit.py # Token Bucket rate limiter
├── pages.py # All HTML pages (panel + mini-app)
├── requirements.txt # Python dependencies
├── Dockerfile # For Railway deployment
├── railway.json # Railway build config
├── README.md # This file
└── fa.readme.md # Persian version

---

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Web server port | `8000` |
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | — |
| `ADMIN_PASSWORD` | Admin panel password | `taakaa` |
| `CARD_NUMBER` | Default card number | `6037-9910-1234-5678` |
| `CARD_OWNER_NAME` | Card owner name | `نام صاحب کارت` |
| `PRICE_PER_GB` | Price per GB (thousand tomans) | `6` |
| `REQUIRED_CHANNEL` | Required channel for bot | `@TaaKaaOrg` |
| `ADMIN_GROUP_ID` | Group ID for card submissions | — |
| `STARS_RATE` | Telegram Stars rate (toman/star) | `1000` |
| `BOT_USERNAME` | Bot username for referral links | `CyrusBot` |

---

## 📱 Client Apps

| App | Protocols | Platform |
|-----|-----------|----------|
| **V2RayNG** | VLESS, VMess, Trojan, Shadowsocks, SOCKS5, HTTP | Android |
| **Nekobox** | VLESS, VMess, Trojan, Shadowsocks, SOCKS5, HTTP | Android |
| **Hiddify** | All protocols (Sing-box core) | Android, iOS |
| **Sing-box** | All protocols | All platforms |
| **Streisand** | All protocols | iOS |
| **Quantumult X** | VLESS, VMess, Trojan | iOS |

---

## 🛠️ Built With

- **[FastAPI](https://fastapi.tiangolo.com/)** — Web framework
- **[Sing-box](https://github.com/SagerNet/sing-box)** — Core proxy engine
- **[Aiogram](https://docs.aiogram.dev/)** — Telegram bot framework
- **[Tabler Icons](https://tabler.io/icons)** — UI icons
- **[Chart.js](https://www.chart.js/)** — Traffic charts
- **[Docker](https://www.docker.com/)** — Containerization

---

## 📞 Support & Community

- **Telegram Support**: [@ItzJustEren](https://t.me/ItzJustEren)
- **Telegram Channel**: [@TaaKaaOrg](https://t.me/TaaKaaOrg)
- **GitHub Issues**: [Report a bug](https://github.com/ItzJustEren/TK-SX/issues)

---

## 🌟 Support the Project

**If you like this project, please give it a star!** ⭐

<a href="https://www.buymeacoffee.com/ItzJustEren" target="_blank">
  <img src="https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg" alt="Buy Me A Coffee" height="40">
</a>

---

<div align="center">
  <br>
  <p style="color:#6B6B6B; font-size:12px;">
    Made with ❤️ by <a href="https://github.com/ItzJustEren" style="color:#F97316;">ItzJustEren</a> &amp; <a href="https://t.me/TaaKaaOrg" style="color:#F97316;">TaaKaa Team</a>
  </p>
  <br>
</div>


