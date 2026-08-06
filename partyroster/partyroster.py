#!/usr/bin/env python3
"""Chain build (mode B): namegen + dice -> json2csv -> csv2md.

INPUT : namegen/  fantasy names        dice/ 6 stat rolls per hero
PROCESS: this script assembles a JSON party roster (glue only)
OUTPUT : json2csv/ -> csv2md/  renders the roster as a markdown table

Reuses namegen, dice, json2csv, csv2md as subprocesses (no reimplementation).
Usage: partyroster.py [heroes]   (default 4)
  partyroster.py --demo   run once, assert the table has name + 6 stat columns
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def build(n):
    names = run([sys.executable, "namegen/namegen.py", str(n)]).splitlines()
    roster = []
    for i in range(n):
        # dice: 6 "SUM  (..)" lines; first token is the sum
        sums = [int(l.split()[0]) for l in
                run(["dotnet", "run", "--project", "dice", "--", "stat"]).splitlines() if l.strip()][:6]
        roster.append({"name": names[i], "STR": sums[0], "DEX": sums[1],
                       "CON": sums[2], "INT": sums[3], "WIS": sums[4], "CHA": sums[5]})
    csv = run(["node", "json2csv/json2csv.js"], input_text=json.dumps(roster))
    return run([sys.executable, "csv2md/csv2md.py"], input_text=csv)

def main():
    if "--demo" in sys.argv:
        md = build(3)
        assert "name" in md and "| STR |" in md, "FAIL: missing name/stat cols"
        assert md.strip().count("\n") >= 3, "FAIL: thin table"
        print("partyroster_ok: name + 6 stat columns rendered", file=sys.stderr)
        sys.exit(0)
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 4
    print(build(n), end="")

if __name__ == "__main__":
    main()
