#!/usr/bin/env python3
"""Chain build (mode B): maze -> namegen -> csv2md.

INPUT : maze/        generates an ASCII dungeon layout
PROCESS: this script extracts open cells, labels each with a fantasy name
         (namegen/namegen.py) and writes a room manifest as CSV
OUTPUT: csv2md/csv2md.py renders the manifest as a markdown table

Reuses the three tools as-is (subprocess), no reimplementation.
Usage: dungeonmap.py [rooms]   (default 8)"""
import os, sys, subprocess, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def open_cells(maze_text):
    cells = []
    for y, line in enumerate(maze_text.splitlines()):
        for x, ch in enumerate(line):
            if ch == ".": cells.append((x, y))
    return cells

def main():
    rooms = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8
    maze = run(["dotnet", "run", "--project", "maze"])
    cells = open_cells(maze)
    if not cells:
        print("no open cells in maze"); sys.exit(1)
    # spread picks across the whole maze
    step = max(1, len(cells) // rooms)
    picks = cells[::step][:rooms] or cells[:1]
    names = run(["python", "namegen/namegen.py", str(len(picks))]).splitlines()
    csv = "room_id,x,y,name\n" + "\n".join(
        f"{i+1},{x},{y},{names[i]}" for i, (x, y) in enumerate(picks))
    md = run(["python", "csv2md/csv2md.py"], input_text=csv)
    print(md, end="")

if "--demo" in sys.argv:
    # integration check: real pipeline yields a markdown table with the header
    rooms = 5
    maze = run(["dotnet", "run", "--project", "maze"])
    cells = open_cells(maze)
    step = max(1, len(cells) // rooms)
    picks = cells[::step][:rooms] or cells[:1]
    names = run(["python", "namegen/namegen.py", str(len(picks))]).splitlines()
    assert len(names) == len(picks), "FAIL: name count mismatch"
    csv = "room_id,x,y,name\n" + "\n".join(
        f"{i+1},{x},{y},{names[i]}" for i, (x, y) in enumerate(picks))
    md = run(["python", "csv2md/csv2md.py"], input_text=csv)
    assert md.startswith("| room_id | x | y | name |"), "FAIL: bad markdown header"
    assert md.count("\n") >= rooms, "FAIL: missing rows"
    print("pipeline_ok=ok rows={}".format(md.count(chr(10))), file=sys.stderr)
    sys.exit(0)

if __name__ == "__main__":
    main()
