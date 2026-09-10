# relay_vless.py
# پارسر هدر VLESS — استخراج command, address, port, payload از اولین بایت‌های کلاینت

import asyncio
import ipaddress
import socket
from typing import Tuple

async def parse_vless_header(data: bytes) -> Tuple[str, str, int, bytes]:
    """
    پارس هدر VLESS.
    ساختار:
      [1 byte version]
      [16 bytes UUID]
      [1 byte addon_length]
      [addon_length bytes addon]
      [1 byte command]  (1=TCP, 2=UDP, 3=Mux)
      [2 bytes port (big-endian)]
      [1 byte address_type]  (1=IPv4, 2=Domain, 3=IPv6)
      [address]
      [payload...]
    """
    if len(data) < 18:
        raise ValueError("Header too short")

    version = data[0]
    if version != 0:
        raise ValueError(f"Unsupported VLESS version: {version}")

    # UUID = bytes 1..17 (16 bytes) — ما از قبل UUID رو از path داریم، پس skip
    pos = 17

    # addon_length
    addon_length = data[pos]
    pos += 1
    if addon_length > 0:
        pos += addon_length

    if len(data) < pos + 1:
        raise ValueError("Header incomplete (command)")

    # command
    command = data[pos]
    pos += 1

    # port (2 bytes, big-endian)
    if len(data) < pos + 2:
        raise ValueError("Header incomplete (port)")
    port = int.from_bytes(data[pos:pos + 2], "big")
    pos += 2

    # address type
    if len(data) < pos + 1:
        raise ValueError("Header incomplete (addr_type)")
    addr_type = data[pos]
    pos += 1

    # address
    if addr_type == 1:  # IPv4
        if len(data) < pos + 4:
            raise ValueError("Header incomplete (IPv4)")
        address = socket.inet_ntoa(data[pos:pos + 4])
        pos += 4
    elif addr_type == 2:  # Domain
        if len(data) < pos + 1:
            raise ValueError("Header incomplete (domain length)")
        domain_len = data[pos]
        pos += 1
        if len(data) < pos + domain_len:
            raise ValueError("Header incomplete (domain)")
        address = data[pos:pos + domain_len].decode("idna", errors="ignore")
        pos += domain_len
    elif addr_type == 3:  # IPv6
        if len(data) < pos + 16:
            raise ValueError("Header incomplete (IPv6)")
        address = str(ipaddress.IPv6Address(data[pos:pos + 16]))
        pos += 16
    else:
        raise ValueError(f"Unsupported address type: {addr_type}")

    # payload (بخش باقی‌مانده)
    payload = data[pos:] if pos < len(data) else b""

    return command, address, port, payload