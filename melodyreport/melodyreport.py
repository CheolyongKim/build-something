#!/usr/bin/env python3
"""Chain build (mode B): go-tone -> freq -> csv2md.

INPUT : go-tone/  procedural melody, printed as a scale-index sequence (--notes)
PROCESS: freq/freq.py counts how often each scale degree appears
OUTPUT: csv2md/csv2md.py renders a "melody profile" table

Reuses go-tone, freq, csv2md as subprocesses (no reimplementation).
Usage: melodyreport.py [seed]   (default 7)
  melodyreport.py --demo   run once, assert the table shows degree counts
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def report(seed):
    # go-tone is a compiled exe; call it directly via the built binary
    notes = run([os.path.join(ROOT, "go-tone", "go-tone.exe"), str(seed), "--notes"]).strip()
    counts = run([sys.executable, "freq/freq.py", "8"], input_text=notes)
    rows = ["degree,count"]
    for line in counts.splitlines():
        m = re.match(r"\s*(\d+)\s+(\w+)", line)
        if m:
            rows.append(f"{m.group(2)},{m.group(1)}")
    csv = "\n".join(rows)
    return run([sys.executable, "csv2md/csv2md.py"], input_text=csv)

def main():
    if "--demo" in sys.argv:
        md = report(7)
        assert "degree" in md, "FAIL: missing header"
        assert md.strip().count("\n") >= 4, "FAIL: thin table"
        print("melodyreport_ok: scale-degree frequency table rendered", file=sys.stderr)
        sys.exit(0)
    seed = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 7
    print(report(seed), end="")

if __name__ == "__main__":
    main()
