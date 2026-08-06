#!/usr/bin/env python3
"""Word frequency counter over stdin. Usage: cat file | freq.py [top N]"""
import sys, re
from collections import Counter

n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 10
text = sys.stdin.read().lower()
words = re.findall(r"[a-z0-9']+", text)
c = Counter(words)
for w, k in c.most_common(n):
    print(f"{k:6} {w}")

if "--demo" in sys.argv:
    import io
    old = sys.stdin; sys.stdin = io.StringIO("a a b b b c")
    c = Counter(re.findall(r"[a-z0-9']+", sys.stdin.read().lower()))
    sys.stdin = old
    assert c["b"] == 3 and c.most_common(1)[0][0] == "b", "FAIL"
    print("count_ok=ok", file=sys.stderr)
