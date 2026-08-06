#!/usr/bin/env python3
"""Chain build (mode B): serve -> freq -> csv2md.

INPUT : serve/server.js       serves a text corpus over HTTP
PROCESS: freq/freq.py          counts word frequencies from the corpus
OUTPUT: csv2md/csv2md.py       renders top words as a markdown table
This script boots serve on a port, fetches the corpus, ranks words, renders them.
Usage: wordrank.py [top]  (default 10)"""
import os, sys, subprocess, time, urllib.request, tempfile, csv, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = 8137

def main():
    top = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 10
    # a corpus file to serve
    corpus = os.path.join(ROOT, "wordrank", "corpus.txt")
    os.makedirs(os.path.dirname(corpus), exist_ok=True)
    open(corpus, "w").write(
        "the hero fought the goblin the wizard cast a spell the hero fell the goblin fled "
        * 3 + " a dragon woke and the hero rose to fight the dragon the wizard helped the hero")
    # boot serve as a child process
    srv = subprocess.Popen(["node", "serve/server.js", str(PORT), os.path.dirname(corpus)],
                           cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.0)
        text = urllib.request.urlopen(f"http://localhost:{PORT}/corpus.txt", timeout=5).read().decode()
        freq = subprocess.run(["python", "freq/freq.py", str(top)], input=text,
                              cwd=ROOT, capture_output=True, text=True, check=True).stdout
        # freq prints "count word" lines; turn into csv then markdown
        rows = [r.split(None, 1) for r in freq.splitlines() if r.strip()]
        out_csv = "word,count\n" + "\n".join(f"{w},{c}" for c, w in rows)
        md = subprocess.run(["python", "csv2md/csv2md.py"], input=out_csv,
                            cwd=ROOT, capture_output=True, text=True, check=True).stdout
        print(md, end="")
    finally:
        srv.terminate()

if "--demo" in sys.argv:
    corpus = os.path.join(ROOT, "wordrank", "corpus.txt")
    os.makedirs(os.path.dirname(corpus), exist_ok=True)
    open(corpus, "w").write("the hero fought the goblin the hero the hero")
    srv = subprocess.Popen(["node", "serve/server.js", str(PORT), os.path.dirname(corpus)], cwd=ROOT,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.0)
        text = urllib.request.urlopen(f"http://localhost:{PORT}/corpus.txt", timeout=5).read().decode()
        assert "hero" in text and "goblin" in text, "FAIL: corpus not served"
        freq = subprocess.run(["python", "freq/freq.py", "3"], input=text, cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout
        rows = [r.split(None, 1) for r in freq.splitlines() if r.strip()]
        assert rows[0][1] == "the" or rows[0][1] == "hero", "FAIL: top word wrong"
        out_csv = "word,count\n" + "\n".join(f"{w},{c}" for c, w in rows)
        md = subprocess.run(["python", "csv2md/csv2md.py"], input=out_csv, cwd=ROOT,
                           capture_output=True, text=True, check=True).stdout
        assert "word" in md and "count" in md, "FAIL: md header"
        print("chain_ok=ok top={}".format(rows[0][1]), file=sys.stderr)
    finally:
        srv.terminate()
    sys.exit(0)

if __name__ == "__main__":
    main()
