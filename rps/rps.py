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

if "--auto" in sys.argv:
    # bot vs bot self-play: adaptive counter-bot (B) vs slightly-noisy counter-bot (A)
    n = 200
    for a in sys.argv:
        if a.isdigit(): n = int(a)
    a_hist, b_hist = [], []
    aw = bw = 0
    seq = []
    for _ in range(n):
        b = bot_move(a_hist)                 # B counters A's habit
        # A counters B's habit, but with 20% noise so the loop isn't degenerate
        if b_hist and random.random() < 0.8:
            a = "rps"[( "rps".index(bot_move(b_hist)) + 1) % 3]
        else:
            a = random.choice("rps")
        a_hist.append(a); b_hist.append(b)
        if b == WIN[a]: aw += 1; seq.append("W")
        elif a == WIN[b]: bw += 1; seq.append("L")
        else: seq.append("T")
    print("".join(seq))
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


