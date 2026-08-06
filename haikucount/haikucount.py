#!/usr/bin/env python3
"""Chain build (mode B): haiku -> freq -> csv2md.

INPUT : haiku/  generated 5-7-5 haiku lines (syllable-tagged)
PROCESS: freq/freq.py counts words used across the haiku batch
OUTPUT: csv2md/csv2md.py renders a haiku-word frequency table

Reuses haiku, freq, csv2md as subprocesses (no reimplementation).
Usage: haikucount.py [haiku]   (default 10)
  haikucount.py --demo   run once, assert the table shows word rows
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def report(n):
    # haiku prints 3 lines per poem separated by blank lines; collect words
    out = run([sys.executable, "haiku/haiku.py", str(n)])
    words = " ".join(out.lower().split())
    counts = run([sys.executable, "freq/freq.py", "15"], input_text=words)
    rows = ["word,count"]
    for line in counts.splitlines():
        m = re.match(r"\s*(\d+)\s+(\w+)", line)
        if m:
            rows.append(f"{m.group(2)},{m.group(1)}")
    csv = "\n".join(rows)
    return run([sys.executable, "csv2md/csv2md.py"], input_text=csv)

def main():
    if "--demo" in sys.argv:
        md = report(10)
        assert "word" in md, "FAIL: missing header"
        assert md.strip().count("\n") >= 3, "FAIL: thin table"
        print("haikucount_ok: haiku-word frequency table rendered", file=sys.stderr)
        sys.exit(0)
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 10
    print(report(n), end="")

if __name__ == "__main__":
    main()
