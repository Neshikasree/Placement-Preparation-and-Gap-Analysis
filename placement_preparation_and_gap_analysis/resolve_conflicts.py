"""Resolve git merge-conflict markers in every file, keeping ONE side.

Usage (run from your project folder):
    python resolve_conflicts.py head       # keep the TOP part  (<<<<<<< HEAD ... =======)
    python resolve_conflicts.py incoming   # keep the BOTTOM part (======= ... >>>>>>>)
"""
import os, sys

side = sys.argv[1] if len(sys.argv) > 1 else ""
if side not in ("head", "incoming"):
    sys.exit("Usage: python resolve_conflicts.py head|incoming")

SKIP = {".git", "venv", ".venv", "__pycache__", "node_modules"}
fixed = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for name in files:
        if name.endswith((".db", ".png", ".jpg", ".pyc", ".pptx", ".zip")) or name == "resolve_conflicts.py":
            continue
        path = os.path.join(root, name)
        try:
            text = open(path, encoding="utf-8", newline="").read()
        except Exception:
            continue
        if not any(l.startswith(("<<<<<<<", "=======", ">>>>>>>")) for l in text.splitlines()):
            continue
        lines = text.splitlines(keepends=True)
        first = next((l for l in lines if l.startswith(("<<<<<<<", "=======", ">>>>>>>"))), "")
        # The "<<<<<<< HEAD" line may have been deleted by hand: then the file starts in the top part
        out, state = [], ("head" if first.startswith("=======") else "normal")
        for line in lines:
            if state == "normal" and line.startswith("<<<<<<<"):
                state = "head"; continue
            if state == "head" and line.startswith("======="):
                state = "incoming"; continue
            if state == "incoming" and line.startswith(">>>>>>>"):
                state = "normal"; continue
            if state == "normal" or state == side:
                out.append(line)
        open(path, "w", encoding="utf-8", newline="").write("".join(out))
        fixed.append(path)

print("Fixed {} file(s):".format(len(fixed)))
for f in fixed:
    print("  ", f)