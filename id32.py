#!/usr/bin/env python3
import sys, base64, ipaddress, struct

USAGE = """Usage:
  id32.py enc <IPv4:Port>   # 例: id32.py enc 192.168.11.3:3000
  id32.py dec <code>        # 例: id32.py dec f4vh6tqv64
Note: 6 bytes (IPv4 4B + Port 2B) -> Base32(lower, no padding). Typical length = 10 chars.
"""

def _b32_nopad_lower(b: bytes) -> str:
    return base64.b32encode(b).decode("ascii").lower().rstrip("=")

def _b32_decode_nopad(code: str) -> bytes:
    pad_len = (8 - (len(code) % 8)) % 8
    return base64.b32decode(code.upper() + ("=" * pad_len))

def enc(s: str) -> str:
    try:
        ip_str, port_str = s.split(":", 1)
        ip_bytes = ipaddress.IPv4Address(ip_str).packed
        port = int(port_str)
        if not (1 <= port <= 65535):
            raise ValueError("port out of range")
        data = ip_bytes + struct.pack(">H", port)
        return _b32_nopad_lower(data)
    except Exception as e:
        raise ValueError(f"invalid input '{s}': {e}")

def dec(code: str) -> str:
    b = _b32_decode_nopad(code)
    if len(b) != 6:
        raise ValueError(f"decoded length {len(b)} != 6")
    ip_bytes, port_bytes = b[:4], b[4:]
    ip_str = str(ipaddress.IPv4Address(ip_bytes))
    port = struct.unpack(">H", port_bytes)[0]
    if not (1 <= port <= 65535):
        raise ValueError("port out of range after decode")
    return f"{ip_str}:{port}"

def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("enc", "dec"):
        print(USAGE, file=sys.stderr); sys.exit(1)
    op, arg = sys.argv[1], sys.argv[2]
    try:
        if op == "enc":
            print(enc(arg))
        else:
            print(dec(arg))
    except Exception as e:
        print(f"error: {e}", file=sys.stderr); sys.exit(2)

if __name__ == "__main__":
    main()
