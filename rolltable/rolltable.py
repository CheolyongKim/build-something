#!/usr/bin/env python3
"""Chain build (mode B): dice -> freq -> csv2md.

INPUT : dice/   many 3d6 stat rolls (values 3..18)
PROCESS: freq/freq.py counts how often each total came up
OUTPUT: csv2md/csv2md.py renders the roll-distribution table

Reuses dice, freq, csv2md as subprocesses (no reimplementation).
Usage: rolltable.py [rolls]   (default 600)
  rolltable.py --demo   run once, assert the table shows a 3..18 spread
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def table(rolls):
    # one dotnet call yields `rolls` stat totals (dice supports `stat count N`)
    out = run(["dotnet", "run", "--project", "dice", "--", "stat", "count", str(rolls)]).splitlines()
    vals = [int(l.split()[0]) for l in out if l.strip()]
    spaced = " ".join(str(v) for v in vals[:rolls])
    counts = run([sys.executable, "freq/freq.py", "18"], input_text=spaced)
    rows = ["roll,count"]
    for line in counts.splitlines():
        m = re.match(r"\s*(\d+)\s+(\d+)", line)
        if m:
            rows.append(f"{m.group(2)},{m.group(1)}")
    csv = "\n".join(rows)
    return run([sys.executable, "csv2md/csv2md.py"], input_text=csv)

def main():
    if "--demo" in sys.argv:
        md = table(600)
        assert "roll" in md, "FAIL: missing header"
        assert md.strip().count("\n") >= 10, "FAIL: too few rows (expected 3..18 spread)"
        print("rolltable_ok: 3d6 distribution table rendered", file=sys.stderr)
        sys.exit(0)
    rolls = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 600
    print(table(rolls), end="")

if __name__ == "__main__":
    main()
