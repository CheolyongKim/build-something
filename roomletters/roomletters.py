#!/usr/bin/env python3
"""Chain build (mode B): dungeonmap -> freq -> csv2md.

INPUT : dungeonmap/  room manifest (maze -> names) as a markdown table
PROCESS: parse room names from the table, freq counts their letters
OUTPUT: csv2md/      renders a room-name letter-frequency table

Reuses dungeonmap, freq, csv2md as subprocesses (no reimplementation).
Usage: roomletters.py [rooms]   (default 8)
  roomletters.py --demo   run once, assert the table shows letter rows
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def report(rooms):
    md = run([sys.executable, "dungeonmap/dungeonmap.py", str(rooms)])
    names = []
    for line in md.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0].isdigit():  # room_id, x, y, name
            names.append(cells[3])
    letters = " ".join("".join(names).lower())
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
        md = report(8)
        assert "letter" in md, "FAIL: missing header"
        assert md.strip().count("\n") >= 4, "FAIL: thin table"
        print("roomletters_ok: room-name letter table rendered", file=sys.stderr)
        sys.exit(0)
    rooms = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8
    print(report(rooms), end="")

if __name__ == "__main__":
    main()
