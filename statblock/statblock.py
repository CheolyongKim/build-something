#!/usr/bin/env python3
"""Chain build (mode B): dice -> json2csv -> csv2md.

INPUT : dice/   N 3d6 stat rolls (dice stat count N)
PROCESS: this script wraps rolls into a JSON array (glue only)
OUTPUT : json2csv/ -> csv2md/  renders a per-roll table

Reuses dice, json2csv, csv2md as subprocesses (no reimplementation).
Usage: statblock.py [rolls]   (default 12)
  statblock.py --demo   run once, assert the table has a roll column
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def block(n):
    out = run(["dotnet", "run", "--project", "dice", "--", "stat", "count", str(n)]).splitlines()
    rolls = []
    for i, l in enumerate(out):
        if not l.strip():
            continue
        # "SUM  (a+b+c drop d)"
        total = int(l.split()[0])
        parts = l[l.find("(")+1:l.find(" drop ")].split("+")
        rolls.append({"#": i + 1, "total": total,
                      "d1": int(parts[0]), "d2": int(parts[1]), "d3": int(parts[2])})
    csv = run(["node", "json2csv/json2csv.js"], input_text=json.dumps(rolls))
    return run([sys.executable, "csv2md/csv2md.py"], input_text=csv)

def main():
    if "--demo" in sys.argv:
        md = block(12)
        assert "#" in md and "total" in md, "FAIL: missing columns"
        assert md.strip().count("\n") >= 12, "FAIL: thin table"
        print("statblock_ok: per-roll stat table rendered", file=sys.stderr)
        sys.exit(0)
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 12
    print(block(n), end="")

if __name__ == "__main__":
    main()
