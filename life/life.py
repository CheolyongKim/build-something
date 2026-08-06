#!/usr/bin/env python3
"""Conway's Game of Life in the terminal. Seeded, deterministic, self-checking."""
import sys, random

W, H, GEN = 40, 18, 12

def step(g):
    n = [[0]*W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            c = sum(g[(y+dy)%H][(x+dx)%W] for dy in (-1,0,1) for dx in (-1,0,1) if (dx,dy)!=(0,0))
            n[y][x] = 1 if g[y][x] and c in (2,3) or (not g[y][x] and c==3) else 0
    return n

def show(g):
    return "\n".join("".join("#" if c else " " for c in row) for row in g)

seed = int(sys.argv[1]) if len(sys.argv)>1 and sys.argv[1].isdigit() else 7
rnd = random.Random(seed)
g = [[1 if rnd.random()<0.3 else 0 for _ in range(W)] for _ in range(H)]

if "--demo" in sys.argv:
    a = g
    for _ in range(GEN): a = step(a)
    b = g
    for _ in range(GEN): b = step(b)
    assert a == b, "FAIL: non-deterministic"
    alive = sum(sum(r) for r in a)
    print(f"gens={GEN} alive_after={alive} deterministic=ok", file=sys.stderr)
    sys.exit(0)

for i in range(GEN):
    print(f"\x1b[H\x1b[2Jgen {i}\n" + show(g))
    g = step(g)
