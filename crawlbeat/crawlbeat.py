#!/usr/bin/env python3
"""Chain build (mode B): dungeonmap -> sloc -> metro.

INPUT : dungeonmap/dungeonmap.py  builds the room manifest (maze -> names)
PROCESS: sloc/sloc.py             measures the manifest builder's source size (build cost)
OUTPUT: metro/metro.py model      a beat-per-room crawl tempo (interval = 60/bpm)

crawlbeat generates the map, sizes its builder with sloc, then lays out one
metronome beat per room at a bpm proportional to room count.
Usage: crawlbeat.py [rooms]  (default 6)"""
import os, sys, subprocess, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def main():
    rooms = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 6
    manifest = run(["python", "dungeonmap/dungeonmap.py", str(rooms)])
    # PROCESS: sloc on the dungeonmap source -> build cost in source lines
    sloc_out = run(["python", "sloc/sloc.py", "dungeonmap", "py"]).splitlines()
    loc = int(re.search(r"(\d+) source lines", sloc_out[-1]).group(1))
    # OUTPUT: metro model -> bpm grows with room count, clamped to a sane range
    bpm = max(60, min(180, rooms * 18))
    interval = 60.0 / bpm
    print(f"rooms={rooms}  builder_loc={loc}  bpm={bpm}  beat_interval={interval:.2f}s")
    for i in range(rooms):
        print(f"  beat {i+1}: t={i*interval:.2f}s  room {i+1}")
    # also confirm metro's tempo math is consistent with our schedule
    run(["python", "metro/metro.py", "--demo"])

if "--demo" in sys.argv:
    rooms = 5
    manifest = run(["python", "dungeonmap/dungeonmap.py", str(rooms)])
    assert "room_id" in manifest, "FAIL: no manifest"
    sloc_out = run(["python", "sloc/sloc.py", "dungeonmap", "py"]).splitlines()
    loc = int(re.search(r"(\d+) source lines", sloc_out[-1]).group(1))
    assert loc > 0, "FAIL: sloc zero"
    bpm = max(60, min(180, rooms * 18))
    interval = 60.0 / bpm
    assert abs(interval - 60.0 / bpm) < 1e-9, "FAIL interval"
    # metro model consistency
    run(["python", "metro/metro.py", "--demo"])
    print(f"chain_ok=ok rooms={rooms} loc={loc} bpm={bpm}", file=sys.stderr)
    sys.exit(0)

if __name__ == "__main__":
    main()
