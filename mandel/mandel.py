#!/usr/bin/env python3
"""Mandelbrot rendered as ASCII. Self-check known points: c=0 in set, c=2 escapes fast."""
import sys

W, H = 70, 30
RE_MIN, RE_MAX, IM_MIN, IM_MAX = -2.0, 1.0, -1.2, 1.2
CHARS = " .:-=+*#%@"

def iters(re_, im, max_i=60):
    zr = zi = 0.0
    for i in range(max_i):
        if zr*zr + zi*zi > 4: return i
        zr, zi = zr*zr - zi*zi + re_, 2*zr*zi + im
    return max_i

def render():
    out = []
    for y in range(H):
        im = IM_MAX - (y/(H-1))*(IM_MAX-IM_MIN)
        row = []
        for x in range(W):
            re_ = RE_MIN + (x/(W-1))*(RE_MAX-RE_MIN)
            row.append(CHARS[min(iters(re_, im)*len(CHARS)//61, len(CHARS)-1)])
        out.append("".join(row))
    return "\n".join(out)

if "--demo" in sys.argv:
    assert iters(0.0, 0.0) == 60, "FAIL: origin should be in set"
    assert iters(2.0, 2.0) < 5, "FAIL: (2,2) should escape fast"
    print("origin_in_set=ok escape_ok=ok", file=sys.stderr)
    sys.exit(0)

print(render())
