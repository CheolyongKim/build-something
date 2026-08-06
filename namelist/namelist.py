#!/usr/bin/env python3
"""Chain build (mode B): namegen -> jsonfmt -> json2csv -> csv2md.

INPUT : namegen/  a batch of fantasy names
PROCESS: wrap as JSON, jsonfmt/ validates+pretty, json2csv/ -> CSV
OUTPUT: csv2md/  renders the name roster table

Reuses namegen, jsonfmt, json2csv, csv2md as subprocesses (no reimplementation).
Usage: namelist.py [count]   (default 8)
  namelist.py --demo   run once, assert the table has a name column
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def report(n):
    names = run([sys.executable, "namegen/namegen.py", str(n)]).splitlines()
    rows = [{"idx": i + 1, "name": w} for i, w in enumerate(names)]
    js = run(["node", "jsonfmt/jsonfmt.js"], input_text=json.dumps(rows))
    csv = run(["node", "json2csv/json2csv.js"], input_text=js)
    return run([sys.executable, "csv2md/csv2md.py"], input_text=csv)

def main():
    if "--demo" in sys.argv:
        md = report(8)
        assert "name" in md and "idx" in md, "FAIL: missing columns"
        assert md.strip().count("\n") >= 8, "FAIL: thin table"
        print("namelist_ok: namegen->jsonfmt->json2csv->csv2md table", file=sys.stderr)
        sys.exit(0)
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8
    print(report(n), end="")

if __name__ == "__main__":
    main()
