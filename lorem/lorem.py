#!/usr/bin/env python3
"""Lorem ipsum generator. Usage: lorem.py [paragraphs] [words_per_para]"""
import sys, random

WORDS = ("lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod "
         "tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam "
         "quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo").split()

def para(n):
    w = [random.choice(WORDS) for _ in range(n)]
    w[0] = w[0].capitalize()
    return " ".join(w) + "."

n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 3
wp = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 40
random.seed(1)
for _ in range(n): print(para(wp))

if "--demo" in sys.argv:
    random.seed(1); a = para(5); b = para(5)
    random.seed(1); c = para(5)
    assert a == c and a.endswith(".") and a[0].isupper(), "FAIL"
    print("deterministic=ok capitalized=ok", file=sys.stderr)
