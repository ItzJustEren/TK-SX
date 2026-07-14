[English](/README.md) | [فارسی](/fa.readme.md) | [العربية](/README.ar_EG.md) | [中文](/README.zh_CN.md) | [Español](/README.es_ES.md) | [Русский](/README.ru_RU.md) | [Türkçe](/README.tr_TR.md)

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ItzJustEren/TK-SX/main/media/tk-sx-dark.png">
    <img alt="TK-SX" src="https://raw.githubusercontent.com/ItzJustEren/TK-SX/main/media/tk-sx-light.png">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/ItzJustEren/TK-SX/releases"><img src="https://img.shields.io/github/v/release/ItzJustEren/TK-SX" alt="Release"></a>
  <a href="https://github.com/ItzJustEren/TK-SX/actions"><img src="https://img.shields.io/github/actions/workflow/status/ItzJustEren/TK-SX/release.yml" alt="Build"></a>
  <a href="#"><img src="https://img.shields.io/github/go-mod/go-version/ItzJustEren/TK-SX" alt="Python Version"></a>
  <a href="https://github.com/ItzJustEren/TK-SX/releases/latest"><img src="https://img.shields.io/github/downloads/ItzJustEren/TK-SX/total" alt="Downloads"></a>
  <a href="https://www.gnu.org/licenses/gpl-3.0.en.html"><img src="https://img.shields.io/badge/license-GPL%20V3-blue.svg?longCache=true" alt="License"></a>
  <a href="https://pkg.go.dev/github.com/ItzJustEren/TK-SX"><img src="https://pkg.go.dev/badge/github.com/ItzJustEren/TK-SX" alt="Python Reference"></a>
</p>

**TK-SX** is an advanced, open-source web control panel for managing [Sing-box](https://github.com/SagerNet/sing-box) servers. It provides a clean, multi-language interface for deploying, configuring, and monitoring a wide range of proxy and VPN protocols — from a single VPS to multi‑node deployments.

Built on top of a powerful Python/FastAPI stack, TK-SX brings together **the best of X-UI and Mirza Bot**, combining a full-featured admin panel with an integrated Telegram store bot in one seamless package.

> [!IMPORTANT]
> This project is intended for personal use only. Please do not use it for illegal purposes or in a production environment.

## Features

- **Multi‑protocol inbounds** — VLESS, VMess, Trojan, Shadowsocks, WireGuard, Hysteria2, HTTP, SOCKS5, TUN, Dokodemo‑door, and Snell.
- **Modern transports & security** — WebSocket, gRPC, HTTPUpgrade, XHTTP, plus TLS, XTLS, REALITY, and full UDP over TCP support.
- **Per‑client management** — traffic quotas, expiry dates, IP limits, live online status, one‑click share links, QR codes, and subscriptions.
- **Integrated Telegram store bot (Cyrus Bot)** — automated product purchasing, free trials, renewals, referrals, discount codes, lottery, and full admin controls directly inside Telegram.
- **Built‑in wallet system** — users can top up and pay from balance; admins can charge users directly.
- **Affiliate / referral system** — 10% commission on referred purchases.
- **Discount codes & gift codes** — flexible promo system with usage limits.
- **Lottery system** — tickets earned per purchase.
- **XHTTP Ultra transport** — packet‑up and stream‑up modes with adaptive flow control.
- **Traffic statistics** — per inbound, per client, with hourly charts and live monitoring.
- **Multi‑node support** — manage and scale across multiple servers from a single panel.
- **RESTful API** — fully documented, accessible via Swagger.
- **Flexible storage** — JSON‑based persistence (lightweight, no database required) with optional migration to SQLite/PostgreSQL.
- **14 UI languages** with dark and light themes (RTL and LTR).
- **Mini App** — mobile‑friendly admin dashboard with eagle‑themed design, accessible directly from Telegram.

## Screenshots

<details>
<summary>Click to expand</summary>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./media/01-overview-dark.png">
  <img alt="Overview" src="./media/01-overview-light.png">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./media/02-add-inbound-dark.png">
  <img alt="Inbounds" src="./media/02-add-inbound-light.png">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./media/03-add-client-dark.png">
  <img alt="Add client" src="./media/03-add-client-light.png">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./media/04-bot-panel-dark.png">
  <img alt="Bot panel" src="./media/04-bot-panel-light.png">
</picture>

</details>

## Supported Platforms

**Operating systems:** Ubuntu, Debian, Fedora, CentOS, RHEL, AlmaLinux, Rocky Linux, Arch, openSUSE, Alpine, and Windows (via Docker).

**Architectures:** `amd64` · `arm64` · `armv7`.

## Database Options

TK-SX uses a simple JSON file (`/data/tksx_state.json`) by default — zero configuration, perfect for small to medium deployments. For high‑client or multi‑node setups, you can switch to SQLite or PostgreSQL.

## Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| `PORT` | Web server port | `8000` |
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | — |
| `ADMIN_PASSWORD` | Admin panel password | `taakaa` |
| `CARD_NUMBER` | Default card number shown to users | `6037-9910-1234-5678` |
| `CARD_OWNER_NAME` | Card owner name | `نام صاحب کارت` |
| `PRICE_PER_GB` | Price per GB (in thousand tomans) | `6` |
| `REQUIRED_CHANNEL` | Telegram channel users must join | `@TaaKaaOrg` |
| `ADMIN_GROUP_ID` | Group ID for card submissions | — |
| `STARS_RATE` | Telegram Stars exchange rate (toman per star) | `1000` |
| `BOT_USERNAME` | Bot username for referral links | `CyrusBot` |
| `DATA_DIR` | Directory for state file | `/data` |

## Supported Languages

The panel UI is available in 14 languages:

English · فارسی · العربية · 中文（简体） · 中文（繁體） · Español · Русский · Українська · Türkçe · Tiếng Việt · 日本語 · Bahasa Indonesia · Português (Brasil) · Deutsch

## Contributing

Contributions are welcome. Please read the [Contributing Guide](/CONTRIBUTING.md) before opening an issue or pull request.

## A Special Thanks to

- [alireza0](https://github.com/alireza0/) for the original S-UI design.
- [MHSanaei](https://github.com/MHSanaei/) for the 3x-ui panel inspiration.
- [SagerNet](https://github.com/SagerNet/) for the Sing‑box core.

## Acknowledgment

- [Iran v2ray rules](https://github.com/chocolate4u/Iran-v2ray-rules) (License: **GPL-3.0**): _Enhanced v2ray/xray routing rules with built‑in Iranian domains and a focus on security and adblocking._
- [Russia v2ray rules](https://github.com/runetfreedom/russia-v2ray-rules-dat) (License: **GPL-3.0**): _Automatically updated V2Ray routing rules based on data on blocked domains and addresses in Russia._

## Community Tools

Tools and integrations built by the community around TK‑SX.

- [terraform-provider-tksx](https://github.com/example/terraform-provider-tksx) (License: **MIT**): _Manage inbounds, clients, and panel settings as code with Terraform._

## Support the project

**If this project is helpful to you, you may wish to give it a**:star2:

<a href="https://www.buymeacoffee.com/ItzJustEren" target="_blank">
<img src="./media/default-yellow.png" alt="Buy Me A Coffee" style="height: 70px !important;width: 277px !important;" >
</a>

## Stargazers over Time

[![Stargazers over time](https://starchart.cc/ItzJustEren/TK-SX.svg?variant=adaptive)](https://starchart.cc/ItzJustEren/TK-SX)
