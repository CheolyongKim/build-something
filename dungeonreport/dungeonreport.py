#!/usr/bin/env python3
"""Chain build (mode B): dungeon -> freq -> csv2md.

INPUT : dungeon/        seeded ASCII dungeon (C#, '#'=wall '.',floor)
PROCESS: this script   translates tiles to words, freq counts them
OUTPUT: csv2md/         renders a dungeon-composition table

Reuses dungeon + csv2md as subprocesses; the tile->word map is the only glue.
Usage: dungeonreport.py [rooms?]   (rooms arg ignored, kept for parity)
  dungeonreport.py --demo   run once, assert the table shows wall/floor counts
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def report():
    maze = run(["dotnet", "run", "--project", "dungeon"])
    # translate each non-space tile to a word so freq can count it
    words = " ".join("wall" if ch == "#" else "floor" if ch == "." else "void"
                     for line in maze.splitlines() for ch in line)
    counts = run([sys.executable, "freq/freq.py", "3"], input_text=words)
    rows = ["tile,count"]
    for line in counts.splitlines():
        m = re.match(r"\s*(\d+)\s+(\w+)", line)
        if m:
            rows.append(f"{m.group(2)},{m.group(1)}")
    csv = "\n".join(rows)
    return run([sys.executable, "csv2md/csv2md.py"], input_text=csv)

def main():
    if "--demo" in sys.argv:
        md = report()
        assert "wall" in md and "floor" in md, "FAIL: missing tiles"
        assert md.strip().count("\n") >= 2, "FAIL: thin table"
        print("dungeonreport_ok: wall/floor table rendered", file=sys.stderr)
        sys.exit(0)
    print(report(), end="")

if __name__ == "__main__":
    main()
