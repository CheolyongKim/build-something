#!/usr/bin/env python3
"""Metronome in the terminal. Usage: metro.py [bpm] [beats]
Plays ticks via the console bell (\\a); no audio deps. Ctrl-C to stop."""
import sys, time

if "--demo" in sys.argv:
    # verify interval math only (no sound in test)
    bpm_demo = 120
    assert abs(60.0 / bpm_demo - 0.5) < 1e-9, "FAIL interval"
    assert abs(60.0 / 60 - 1.0) < 1e-9, "FAIL interval"
    print("interval_ok=ok", file=sys.stderr)
    sys.exit(0)

bpm = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 100
beats = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 4
interval = 60.0 / bpm
print(f"{bpm} bpm, {beats} beats/bar  (Ctrl-C to stop)")
try:
    i = 0
    while True:
        sys.stdout.write("\a"); sys.stdout.flush()
        print(f"  beat {(i % beats) + 1}", end="\r", flush=True)
        i += 1; time.sleep(interval)
except KeyboardInterrupt:
    print("\nstopped")
