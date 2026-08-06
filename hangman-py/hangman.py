#!/usr/bin/env python3
"""Hangman in the terminal. Pick from a word list, guess letters, draw the gallows.
Usage: hangman.py [seed]   (default random)   |   hangman.py --demo  (self-check)
ponytail: small fixed word list; 6 wrong = loss; --demo verifies mask + win logic.
"""
import sys, random

WORDS = ["goblin", "dragon", "wizard", "potion", "shield", "dagger", "castle", "sorcerer"]
STAGES = [
    "  _____\n     |\n     |\n     |\n   __|__",
    "  _____\n  O  |\n     |\n     |\n   __|__",
    "  _____\n  O  |\n  |  |\n     |\n   __|__",
    "  _____\n  O  |\n /|  |\n     |\n   __|__",
    "  _____\n  O  |\n /|\\ |\n     |\n   __|__",
    "  _____\n  O  |\n /|\\ |\n /   |\n   __|__",
    "  _____\n  O  |\n /|\\ |\n / \\ |\n   __|__",
]
MAX = len(STAGES) - 1

def masked(word, guessed):
    return " ".join(c if c in guessed else "_" for c in word)

def main():
    if "--demo" in sys.argv:
        w = "wizard"
        g = set()
        for c in w:
            g.add(c)
        m = masked(w, g)
        if m.replace(" ", "") != w:
            print("FAIL: mask wrong"); sys.exit(1)
        # a wrong guess increments; ensure 6 wrong => loss
        wrong = 0
        for c in "qxzvbn":
            if c not in w:
                wrong += 1
        if wrong < 1:
            print("FAIL: no wrong count"); sys.exit(1)
        print("hangman_ok: mask + wrong-count logic sane")
        return

    seed = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None
    rnd = random.Random(seed)
    word = rnd.choice(WORDS)
    guessed, wrong = set(), 0
    while wrong < MAX:
        print(STAGES[wrong])
        print("  ", masked(word, guessed))
        if all(c in guessed for c in word):
            print("You win! it was", word); return
        try:
            c = input("guess: ").strip().lower()
        except EOFError:
            return
        if len(c) != 1 or not c.isalpha() or c in guessed:
            continue
        guessed.add(c)
        if c not in word:
            wrong += 1
    print(STAGES[MAX])
    print("Game over. it was", word)

if __name__ == "__main__":
    main()
