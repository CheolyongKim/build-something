#!/usr/bin/env python3
"""Chain build (mode B): hangman wordlist -> markov -> freq -> csv2md.

INPUT : inline hangman word list (goblin, dragon, ...) as the markov corpus
PROCESS: markov/markov.py remixes the fantasy words; freq/freq.py counts them
OUTPUT: csv2md/csv2md.py renders a "most-conjured words" table

Reuses markov, freq, csv2md as subprocesses (no reimplementation).
Usage: wordconjure.py [sentences]   (default 20)
  wordconjure.py --demo   run once, assert the table has rows
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ponytail: small fixed corpus pulled from hangman's word list (8 words) -> glue only
CORPUS = "goblin dragon wizard potion shield dagger castle sorcerer " * 6

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def conjure(n):
    remix = run([sys.executable, "markov/markov.py", str(n), "2"], input_text=CORPUS)
    freq = run([sys.executable, "freq/freq.py", "8"], input_text=remix)
    rows = ["word,count"]
    for line in freq.splitlines():
        m = re.match(r"\s*(\d+)\s+(\w+)", line)
        if m:
            rows.append(f"{m.group(2)},{m.group(1)}")
    csv = "\n".join(rows)
    return run([sys.executable, "csv2md/csv2md.py"], input_text=csv)

def main():
    if "--demo" in sys.argv:
        md = conjure(20)
        assert md.strip().count("\n") >= 6, "FAIL: thin table"
        assert "word" in md, "FAIL: missing header"
        print("wordconjure_ok: fantasy-word frequency table rendered", file=sys.stderr)
        sys.exit(0)
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 20
    print(conjure(n), end="")

if __name__ == "__main__":
    main()
