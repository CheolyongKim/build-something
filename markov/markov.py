#!/usr/bin/env python3
"""Markov-chain text generator. Reads text from stdin, emits N sentences.
Usage: cat corpus.txt | markov.py [sentences] [order]"""
import sys, re, random

def build(text, order=2):
    words = re.findall(r"\S+", text)
    chains = {}
    for i in range(len(words) - order):
        key = tuple(words[i:i+order]); chains.setdefault(key, []).append(words[i+order])
    return words, chains

def gen(words, chains, n=3, order=2):
    out = []
    for _ in range(n):
        key = random.choice(list(chains)) if chains else tuple(words[:order])
        sent = list(key)
        for _ in range(40):
            nxt = chains.get(key)
            if not nxt: break
            w = random.choice(nxt); sent.append(w); key = (*key[1:], w)
            if w.endswith((".", "!", "?")): break
        out.append(" ".join(sent))
    return " ".join(out)

if "--demo" in sys.argv:
    t = "the cat sat on the mat the cat ran the dog sat the dog ran"
    w, c = build(t, 2); random.seed(0)
    assert len(c) > 0
    # determinism: same seed -> same output
    random.seed(1); a = gen(w, c, 2, 2)
    random.seed(1); b = gen(w, c, 2, 2)
    assert a == b, "FAIL: non-deterministic"
    print("chains>0 ok deterministic=ok", file=sys.stderr); sys.exit(0)

args = [a for a in sys.argv[1:] if a != "--demo"]
n = int(args[0]) if len(args) > 0 and args[0].isdigit() else 3
order = int(args[1]) if len(args) > 1 and args[1].isdigit() else 2
text = sys.stdin.read()
w, c = build(text, order)
print(gen(w, c, n, order))
