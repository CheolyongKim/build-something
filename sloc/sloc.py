#!/usr/bin/env python3
"""Count source lines (non-blank, non-comment) in a directory tree.
Usage: sloc.py [path] [ext...]
  defaults: . over cwd, exts = cs py js ts go rs"""
import sys, os, re

root = sys.argv[1] if len(sys.argv) > 1 else "."
exts = sys.argv[2:] or ["cs", "py", "js", "ts", "go", "rs"]
comment = {".py": re.compile(r"^\s*#"), ".cs": re.compile(r"^\s*//"),
           ".js": re.compile(r"^\s*//"), ".ts": re.compile(r"^\s*//"),
           ".go": re.compile(r"^\s*//"), ".rs": re.compile(r"^\s*//")}

tot = 0; files = 0
for dp, _, fs in os.walk(root):
    for f in fs:
        ext = os.path.splitext(f)[1]
        if ext[1:] not in exts: continue
        files += 1; cm = comment.get(ext)
        with open(os.path.join(dp, f), encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                s = line.strip()
                if s and not (cm and cm.match(s)): tot += 1
print(f"{files} files, {tot} source lines")

if "--demo" in sys.argv:
    import tempfile, os as _os
    d = tempfile.mkdtemp()
    p = _os.path.join(d, "x.py")
    open(p, "w").write("# c\n\nprint(1)\n  # n\nx=2\n")
    c = 0
    for line in open(p):
        s = line.strip()
        if s and not re.match(r"^\s*#", s): c += 1
    assert c == 2, f"FAIL: got {c}"
    print("count_ok=ok", file=sys.stderr)
