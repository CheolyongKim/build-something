#!/usr/bin/env python3
"""Chain build (mode B): namegen -> freq -> csv2md.

INPUT : namegen/  a batch of fantasy names
PROCESS: freq/freq.py counts letters used across all names
OUTPUT: csv2md/csv2md.py renders a name-letter frequency table

Reuses namegen, freq, csv2md as subprocesses (no reimplementation).
Usage: namefreq.py [count]   (default 200)
  namefreq.py --demo   run once, assert the table shows letter rows
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def report(n):
    names = run([sys.executable, "namegen/namegen.py", str(n)]).lower()
    letters = " ".join(names.replace("\n", ""))  # one char per token
    counts = run([sys.executable, "freq/freq.py", "26"], input_text=letters)
    rows = ["letter,count"]
    for line in counts.splitlines():
        m = re.match(r"\s*(\d+)\s+(\w)", line)
        if m:
            rows.append(f"{m.group(2)},{m.group(1)}")
    csv = "\n".join(rows)
    return run([sys.executable, "csv2md/csv2md.py"], input_text=csv)

def main():
    if "--demo" in sys.argv:
        md = report(200)
        assert "letter" in md, "FAIL: missing header"
        assert md.strip().count("\n") >= 5, "FAIL: thin table"
        print("namefreq_ok: name-letter frequency table rendered", file=sys.stderr)
        sys.exit(0)
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 200
    print(report(n), end="")

if __name__ == "__main__":
    main()
