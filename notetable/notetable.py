#!/usr/bin/env python3
"""Chain build (mode B): go-tone -> json2csv -> csv2md.

INPUT : go-tone/  procedural melody as a scale-index sequence (--notes)
PROCESS: this script wraps the notes into a JSON array (glue only)
OUTPUT: json2csv/ -> csv2md/  renders a per-beat note table

Reuses go-tone, json2csv, csv2md as subprocesses (no reimplementation).
Usage: notetable.py [seed]   (default 7)
  notetable.py --demo   run once, assert the table has beat + note columns
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOTONE_EXE = os.path.join(ROOT, "go-tone", "go-tone.exe")

def ensure_gotone():
    if not os.path.exists(GOTONE_EXE):
        subprocess.run(["go", "build", "-o", GOTONE_EXE, "."],
                       cwd=os.path.join(ROOT, "go-tone"), check=True)

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def table(seed):
    notes = run([GOTONE_EXE, str(seed), "--notes"]).split()
    rows = [{"beat": i + 1, "degree": int(n)} for i, n in enumerate(notes)]
    csv = run(["node", "json2csv/json2csv.js"], input_text=json.dumps(rows))
    return run([sys.executable, "csv2md/csv2md.py"], input_text=csv)

def main():
    ensure_gotone()
    if "--demo" in sys.argv:
        md = table(7)
        assert "beat" in md and "degree" in md, "FAIL: missing columns"
        assert md.strip().count("\n") >= 10, "FAIL: thin table"
        print("notetable_ok: per-beat note table rendered", file=sys.stderr)
        sys.exit(0)
    seed = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 7
    print(table(seed), end="")

if __name__ == "__main__":
    main()
