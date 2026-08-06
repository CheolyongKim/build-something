#!/usr/bin/env python3
"""Chain build (mode B): rps -> freq -> csv2md.

INPUT : rps/rps.py --auto N       self-play bot battle -> W/L/T sequence
PROCESS: freq/freq.py             count the outcome letters
OUTPUT: csv2md/csv2md.py          render the tally as a markdown table

Reuses the tools as subprocesses (no reimplementation).
Usage: botbattle.py [rounds]   (default 300)
  botbattle.py --demo   run once, assert the table has W/L/T rows
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def battle(rounds):
    seq = run([sys.executable, "rps/rps.py", "--auto", str(rounds)]).strip()
    # rps emits one char per round (W/L/T); space them so freq counts each
    spaced = " ".join(seq)
    counts = run([sys.executable, "freq/freq.py", "3"], input_text=spaced)
    # freq gives "  N letter"; turn into CSV
    rows = ["outcome,count"]
    for line in counts.splitlines():
        m = re.match(r"\s*(\d+)\s+(\w)", line)
        if m:
            rows.append(f"{m.group(2).upper()},{m.group(1)}")
    csv = "\n".join(rows)
    return run([sys.executable, "csv2md/csv2md.py"], input_text=csv)

def main():
    if "--demo" in sys.argv:
        md = battle(300)
        assert all(k in md for k in ("W", "L", "T")), "FAIL: missing outcomes"
        assert md.strip().count("\n") >= 3, "FAIL: thin table"
        print("botbattle_ok: W/L/T table rendered", file=sys.stderr)
        sys.exit(0)
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 300
    print(battle(rounds), end="")

if __name__ == "__main__":
    main()
