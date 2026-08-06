#!/usr/bin/env python3
"""Chain: markov -> rps --auto -> go-ascii --text
1. markov learns an RPS match log and spits a "bot persona" line (flavor)
2. rps --auto N plays bot-vs-bot, emits a W/L/T result sequence
3. we turn the sequence into a win-rate bar grid and render it via go-ascii --text
Reuses markov.py, rps.py, go-ascii (Go) as subprocesses. No reimplementation.

Usage: rpsmarkov.py [rounds]   rpsmarkov.py --demo
"""
import os, re, subprocess, sys, random

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GO = os.path.join(REPO, "go-ascii", "go-ascii.exe")

def run(cmd, inp=None, cwd=REPO):
    return subprocess.run(cmd, input=inp, cwd=cwd, capture_output=True, text=True, timeout=120)

def persona():
    # feed markov a fake RPS commentary corpus; it returns a generated line
    corpus = ("rock beats scissors paper beats rock scissors beats paper "
              "the bot counters your habit the adaptive bot never rests "
              "victory favors the patient hand fortune spins the wheel")
    out = run([sys.executable, os.path.join(REPO, "markov", "markov.py"), "1", "2"], inp=corpus)
    line = out.stdout.strip().split("\n")[0]
    return line or "the adaptive bot never rests"

def match(rounds):
    out = run([sys.executable, os.path.join(REPO, "rps", "rps.py"), "--auto", str(rounds)])
    seq = re.sub(r"[^WLT]", "", out.stdout)
    return seq

def grid(seq, cols=50):
    # group into cols buckets, show win-rate as a bar of '#'
    w = seq.count("W"); l = seq.count("L"); t = seq.count("T")
    total = max(1, len(seq))
    winrate = w / total
    bar = "#" * int(winrate * cols)
    lines = [
        f"W {w}  L {l}  T {t}   winrate {winrate:.0%}",
        f"[{bar}{' '*(cols-len(bar))}]",
        "",
        "last 50 results:",
        " ".join(seq[-50:]),
    ]
    return "\n".join(lines)

def main():
    if "--demo" in sys.argv:
        p = persona()
        seq = match(120)
        assert set(seq) <= set("WLT") and len(seq) == 120, "bad sequence"
        g = grid(seq)
        assert "winrate" in g and "%" in g, "grid malformed"
        # end-to-end through go-ascii --text
        rendered = run([GO, "--text"], inp=g).stdout
        assert "winrate" in rendered, "go-ascii --text dropped content"
        print("rpsmarkov_ok: persona + 120-round auto match + grid + go-ascii render", file=sys.stderr)
        return
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 200
    print("BOT PERSONA:", persona())
    print()
    seq = match(rounds)
    g = grid(seq)
    # render the grid through go-ascii --text (passthrough ASCII renderer)
    print(run([GO, "--text"], inp=g).stdout, end="")

if __name__ == "__main__":
    main()
