#!/usr/bin/env python3
"""Chain: namegen + dice + lorem -> a markdown RPG character sheet.
Reuses existing tools as subprocesses (no reimplementation).

Usage:
  charactersheet.py [n]            generate n sheets (default 1)
  charactersheet.py --demo         run pipeline once, assert the sheet is well-formed
"""
import os, re, subprocess, sys, random

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICE = os.path.join(REPO, "dice", "dice.csproj")

RACES = ["Human", "Elf", "Dwarf", "Orc", "Halfling", "Tiefling"]
CLASSES = ["Rogue", "Wizard", "Warrior", "Cleric", "Ranger", "Bard"]

def run(cmd, cwd=REPO):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120)

def gen_name(seed):
    out = run([sys.executable, os.path.join(REPO, "namegen", "namegen.py"), "1", str(seed)])
    return out.stdout.strip().splitlines()[0]

def gen_stats():
    # dice stat -> 6 lines "SUM  (a+b+c drop d)"; first token is the sum
    out = run(["dotnet", "run", "--project", "dice", "--", "stat"])
    sums = [int(l.split()[0]) for l in out.stdout.splitlines() if l.strip()]
    return sums[:6]

def gen_backstory(seed, words=35):
    out = run([sys.executable, os.path.join(REPO, "lorem", "lorem.py"), "1", str(words)])
    return out.stdout.strip().splitlines()[0]

def sheet(name, stats, race, cls, backstory):
    abil = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    rows = "\n".join(f"| {abil[i]} | {stats[i]} |" for i in range(6))
    return f"""# {name}
**{race} {cls}**

| Ability | Score |
|---|---|
{rows}

> {backstory}
"""

def main():
    if "--demo" in sys.argv:
        rnd = random.Random(42)
        s = sheet(gen_name(1), gen_stats(), "Elf", "Wizard", gen_backstory(1))
        assert re.search(r"^# \w+", s), "missing name"
        assert len(re.findall(r"\|\s*(STR|DEX|CON|INT|WIS|CHA)\s*\|\s*\d+\s*\|", s)) == 6, "missing 6 stats"
        assert "> " in s, "missing backstory"
        print("charactersheet_ok: name + 6 stats + backstory composed", file=sys.stderr)
        return
    n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 1
    rnd = random.Random()
    for i in range(n):
        name = gen_name(rnd.randint(0, 9999))
        stats = gen_stats()
        race = rnd.choice(RACES); cls = rnd.choice(CLASSES)
        back = gen_backstory(rnd.randint(0, 9999))
        print(sheet(name, stats, race, cls, back))
        print()

if __name__ == "__main__":
    main()
