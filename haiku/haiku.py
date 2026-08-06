#!/usr/bin/env python3
"""Haiku generator. Words are syllable-tagged so lines hit 5/7/5 exactly.
Usage: haiku.py [n] (default 1)   |   haiku.py --demo (self-check)
"""
import sys, random

# (word, syllables)
W5 = [("soft",1),("moon",1),("cold",1),("wind",1),("blue",1),("frog",1),
      ("old",1),("pine",1),("still",1),("lake",1),("red",1),("leaf",1),
      ("wild",1),("sea",1),("dim",1),("star",1),("calm",1),("night",1),
      ("deep",1),("snow",1),("green",1),("mist",1),("rain",1),("sun",1)]
W7 = [("whispers",2),("through",1),("the",1),("still",1),("night",1),
      ("falls",1),("softly",2),("on",1),("stone",1),("drifts",1),("above",1),
      ("quiet",2),("hills",1),("breaks",1),("morning",2),("calm",1),("again",2),
      ("calls",1),("lost",1),("ones",1),("away",1),("sings",1),("beneath",1),
      ("pale",1),("moon",1),("runs",1),("toward",1),("open",2),("sea",1),
      ("echoes",2),("empty",2),("hall",1),("sleeps",1),("cold",1),("snow",1)]
# two 5-syllable lines: reuse W5 words; second line can include a few longer ones
W5B = [("dreams",1),("fade",1),("light",1),("grows",1),("time",1),("flows",1),
       ("echo",2),("dies",1),("shadow",2),("moves",1),("clears",1),("wave",1),
       ("rests",1),("fire",1),("ends",1),("heart",1),("stills",1),("wind",1),
       ("sinks",1),("stops",1),("frost",1),("falls",1),("dawn",1),("comes",1)]

TARGET = [5, 7, 5]
BANKS = [W5, W7, W5B]

def build_line(words, target, rnd):
    # greedy: pick words without immediate repeats until target reached
    line = []
    left = target
    prev = None
    guard = 0
    while left > 0 and guard < 50:
        guard += 1
        pick = rnd.choice(words)
        if pick[0] == prev:  # avoid adjacent repeats
            continue
        if pick[1] <= left:
            line.append(pick); left -= pick[1]; prev = pick[0]
    return [w for w, _ in line]

def gen(rnd):
    return [build_line(b, t, rnd) for b, t in zip(BANKS, TARGET)]

def main():
    if "--demo" in sys.argv:
        rnd = random.Random(7)
        for _ in range(20):
            a, b, c = gen(rnd)
            # verify syllable totals via tag
            ta = sum(dict(W5)[w] for w in a)
            tb = sum(dict(W7)[w] for w in b)
            tc = sum(dict(W5B)[w] for w in c)
            assert (ta, tb, tc) == (5, 7, 5), f"FAIL: {ta}{tb}{tc}"
        print("haiku_ok: 20 well-formed 5-7-5 haiku", file=sys.stderr)
        return
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1
    rnd = random.Random()
    for _ in range(n):
        a, b, c = gen(rnd)
        print(" ".join(a)); print(" ".join(b)); print(" ".join(c)); print()

if __name__ == "__main__":
    main()
