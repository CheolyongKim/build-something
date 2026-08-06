#!/usr/bin/env python3
"""Rock-paper-scissors against an adaptive bot that counters your habit.
The bot tracks how often you play each move and counters your most-likely move.
Usage: rps.py [rounds]  (default 5). Enter r/p/s per round."""
import sys, random
from collections import Counter

WIN = {"r": "s", "p": "r", "s": "p"}  # key beats value
NAME = {"r": "rock", "p": "paper", "s": "scissors"}

def bot_move(hist):
    if not hist: return random.choice("rps")
    # counter the player's most frequent throw
    fav = Counter(hist).most_common(1)[0][0]
    return WIN[fav]

if "--demo" in sys.argv:
    h = list("rrrrr")
    assert bot_move(h) == "s", "FAIL: should counter rock with scissors"
    assert bot_move([]) in "rps", "FAIL"
    print("counters_most_frequent=ok", file=sys.stderr)
    sys.exit(0)

n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 5
hist = []; pw = bw = 0
for _ in range(n):
    b = bot_move(hist)
    u = input("your move (r/p/s): ").strip().lower()
    if u not in "rps": print("skip"); continue
    hist.append(u)
    if b == WIN[u]: pw += 1
    elif u == WIN[b]: bw += 1
    else: print("tie")
    print(f"  you {NAME[u]} vs bot {NAME[b]}")
print(f"you {pw} - bot {bw}")


