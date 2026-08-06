#!/usr/bin/env python3
"""Chain build (mode B): dice -> jsonfmt -> json2csv -> csv2md.

INPUT : dice/          N 3d6 stat rolls (dice stat count N)
PROCESS: jsonfmt/      validate + pretty-print the JSON roster (new node in the pile)
         json2csv/     JSON array -> CSV
OUTPUT: csv2md/        renders a per-roll table

Reuses dice, jsonfmt, json2csv, csv2md as subprocesses (no reimplementation).
Usage: jsonreport.py [rolls]   (default 10)
  jsonreport.py --demo   run once, assert the table has a total column
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def report(n):
    out = run(["dotnet", "run", "--project", "dice", "--", "stat", "count", str(n)]).splitlines()
    rolls = []
    for i, l in enumerate(out):
        if not l.strip():
            continue
        total = int(l.split()[0])
        parts = l[l.find("(")+1:l.find(" drop ")].split("+")
        rolls.append({"#": i + 1, "total": total,
                      "d1": int(parts[0]), "d2": int(parts[1]), "d3": int(parts[2])})
    js = json.dumps(rolls)
    js = run(["node", "jsonfmt/jsonfmt.js"], input_text=js)   # pretty/validate
    csv = run(["node", "json2csv/json2csv.js"], input_text=js)
    return run([sys.executable, "csv2md/csv2md.py"], input_text=csv)

def main():
    if "--demo" in sys.argv:
        md = report(10)
        assert "total" in md and "#" in md, "FAIL: missing columns"
        assert md.strip().count("\n") >= 10, "FAIL: thin table"
        print("jsonreport_ok: dice->jsonfmt->json2csv->csv2md table", file=sys.stderr)
        sys.exit(0)
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 10
    print(report(n), end="")

if __name__ == "__main__":
    main()
