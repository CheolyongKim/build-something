#!/usr/bin/env python3
"""Chain build (mode B): lorem -> markov -> freq.

INPUT : lorem/lorem.py       fake lorem prose (corpus)
PROCESS: markov/markov.py    remixes the prose via word-markov chains
OUTPUT: freq/freq.py         word-frequency analysis of the remix

Reuses the three tools as subprocesses (no reimplementation).
Usage: loreforge.py [paragraphs] [words_per_para] [freq_top]
  loreforge.py --demo   run pipeline once, assert a non-trivial remix + freq table
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd, input_text=None):
    return subprocess.run(cmd, cwd=ROOT, input=input_text, capture_output=True,
                          text=True, check=True).stdout

def forge(p, wp, top):
    corpus = run([sys.executable, "lorem/lorem.py", str(p), str(wp)])
    remix = run([sys.executable, "markov/markov.py", "3", "2"], input_text=corpus)
    freq = run([sys.executable, "freq/freq.py", str(top)], input_text=remix)
    return corpus, remix, freq

def main():
    if "--demo" in sys.argv:
        _, remix, freq = forge(2, 40, 5)
        words = re.findall(r"[a-z0-9']+", remix.lower())
        assert len(words) > 20, "FAIL: remix too short"
        assert "ipsum" in remix.lower(), "FAIL: remix lost corpus words"
        assert freq.strip().count("\n") >= 4, "FAIL: freq table thin"
        print("loreforge_ok: remix={}w freq_rows={}".format(
            len(words), freq.strip().count(chr(10))), file=sys.stderr)
        sys.exit(0)
    argv = [a for a in sys.argv[1:] if a != "--demo"]
    p = int(argv[0]) if len(argv) > 0 and argv[0].isdigit() else 2
    wp = int(argv[1]) if len(argv) > 1 and argv[1].isdigit() else 40
    top = int(argv[2]) if len(argv) > 2 and argv[2].isdigit() else 10
    _, remix, freq = forge(p, wp, top)
    print("# LOREFORGE remix")
    print(remix)
    print("\n# Top words")
    print(freq, end="")

if __name__ == "__main__":
    main()
