#!/usr/bin/env python3
"""Chain build (mode B): rps --auto -> jsonfmt -> json2csv -> csv2md.

INPUT : rps/rps.py --auto N     self-play bot battle -> W/L/T sequence
PROCESS: jsonfmt/ + json2csv/    wrap the sequence as JSON, validate, -> CSV
OUTPUT: csv2md/                  renders a per-round outcome table

Reuses rps, jsonfmt, json2csv, csv2md as subprocesses (no reimplementation).
Usage: battlelog.py [rounds]   (default 200)
  battlelog.py --demo   run once, assert the table has a round column
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def report(n):
    seq = run([sys.executable, "rps/rps.py", "--auto", str(n)]).strip()
    rows = [{"round": i + 1, "outcome": ch} for i, ch in enumerate(seq)]
    js = json.dumps(rows)
    js = run(["node", "jsonfmt/jsonfmt.js"], input_text=js)
    csv = run(["node", "json2csv/json2csv.js"], input_text=js)
    return run([sys.executable, "csv2md/csv2md.py"], input_text=csv)

def main():
    if "--demo" in sys.argv:
        md = report(200)
        assert "round" in md and "outcome" in md, "FAIL: missing columns"
        assert md.strip().count("\n") >= 10, "FAIL: thin table"
        print("battlelog_ok: rps->jsonfmt->json2csv->csv2md table", file=sys.stderr)
        sys.exit(0)
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 200
    print(report(n), end="")

if __name__ == "__main__":
    main()
