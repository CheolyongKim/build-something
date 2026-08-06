#!/usr/bin/env python3
"""CSV -> markdown table. Reads stdin. First line is the header."""
import sys, csv, io

rows = list(csv.reader(io.StringIO(sys.stdin.read())))
if not rows: sys.exit(0)
header, body = rows[0], rows[1:]
print("| " + " | ".join(header) + " |")
print("| " + " | ".join("---" for _ in header) + " |")
for r in body:
    print("| " + " | ".join(r) + " |")

if "--demo" in sys.argv:
    src = "name,hp\nhero,30\ngoblin,8\n"
    import io as _io
    old = sys.stdin; sys.stdin = _io.StringIO(src)
    out = []
    rs = list(csv.reader(_io.StringIO(src)))
    h, b = rs[0], rs[1:]
    out.append("| " + " | ".join(h) + " |")
    out.append("| " + " | ".join("---" for _ in h) + " |")
    for r in b: out.append("| " + " | ".join(r) + " |")
    sys.stdin = old
    assert out[0] == "| name | hp |" and "hero" in out[2], "FAIL"
    print("header_ok=ok", file=sys.stderr)
