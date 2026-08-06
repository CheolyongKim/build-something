#!/usr/bin/env python3
"""Chain build (mode B): passgen -> dungeonmap -> csv2md.

INPUT : passgen/passgen.js        a unique lock code per room
PROCESS: dungeonmap/dungeonmap.py builds the room manifest (maze -> names)
OUTPUT: csv2md/csv2md.py          renders the final crawl sheet
This script merges lock codes into the manifest and re-renders with csv2md.
Usage: party.py [rooms]  (default 6)"""
import os, sys, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def md_rows(md):
    """Parse a markdown table into a list of cell-lists (header + data rows)."""
    out = []
    for line in md.splitlines():
        if not line.strip().startswith("|"): continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if set(cells) <= {"", "---"}: continue  # separator row
        out.append(cells)
    return out

def build(rooms):
    manifest = run(["python", "dungeonmap/dungeonmap.py", str(rooms)])
    data = md_rows(manifest)
    codes = run(["node", "passgen/passgen.js", "words", str(rooms)]).splitlines()[0].split("-")
    data[0].append("lock_code")
    for i in range(1, len(data)):
        data[i].append(codes[i - 1] if i - 1 < len(codes) else "?")
    return data

def main():
    rooms = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 6
    data = build(rooms)
    out_csv = "\n".join(",".join(r) for r in data)
    print(run(["python", "csv2md/csv2md.py"], input_text=out_csv), end="")

if "--demo" in sys.argv:
    rooms = 4
    data = build(rooms)
    out_csv = "\n".join(",".join(r) for r in data)
    md = run(["python", "csv2md/csv2md.py"], input_text=out_csv)
    assert "lock_code" in md, "FAIL: lock_code column missing"
    assert md.count("\n") >= rooms, "FAIL: row count"
    assert len(data[0]) == 5, f"FAIL: expected 5 cols, got {len(data[0])}"
    print("chain_ok=ok rooms={} cols={}".format(rooms, len(data[0])), file=sys.stderr)
    sys.exit(0)

if __name__ == "__main__":
    main()
