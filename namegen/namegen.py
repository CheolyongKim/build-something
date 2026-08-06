#!/usr/bin/env python3
"""Fantasy name generator (syllable concat), seeded. Usage: namegen.py [n] [seed]"""
import sys, random

ONSET = ["br", "cr", "dr", "th", "st", "gl", "sh", "v", "z", "m", "kr", "sn", "tr", "f", "l", "w"]
NUC = ["a", "o", "i", "e", "u", "ae", "y", "ei", "ou"]
CODA = ["n", "r", "th", "k", "l", "x", "d", "s", "m", "z", ""]

def name(rnd):
    syl = rnd.randint(2, 3)
    s = "".join(rnd.choice(ONSET) + rnd.choice(NUC) + rnd.choice(CODA) for _ in range(syl))
    return s.capitalize()

n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8
seed = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 7
rnd = random.Random(seed)
for _ in range(n): print(name(rnd))

if "--demo" in sys.argv:
    a = [name(random.Random(3)) for _ in range(5)]
    b = [name(random.Random(3)) for _ in range(5)]
    assert a == b, "FAIL: non-deterministic"
    assert all(s[0].isupper() for s in a), "FAIL: not capitalized"
    print("deterministic=ok capitalized=ok", file=sys.stderr)
