#!/usr/bin/env python3
"""Roast the Smart Fridge — one-line entry.

Reads entry.txt (the single roast line, kept next to this file),
checks it against the competition gate, writes it to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt) and prints
exactly those bytes to stdout. Standard library only, deterministic:
every run produces the same bytes. `python3 main.py --check` validates
the line against the gate without writing or printing it.
"""

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY_PATH = os.path.join(HERE, "entry.txt")
MIN_CHARS = 1
MAX_CHARS = 160


def check_gate(text):
    """Return the list of gate violations for a candidate line.

    The gate (from competition.yaml): entry.txt must be UTF-8 text of
    1 to 160 characters, not only white space, on a single line.
    An empty list means the line passes.
    """
    problems = []
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        problems.append(
            "line is %d chars, gate is %d-%d" % (len(text), MIN_CHARS, MAX_CHARS)
        )
    if text != text.strip() or "\n" in text or "\r" in text:
        problems.append("entry must be one line with no edge whitespace")
    if not text.strip():
        problems.append("entry must not be only whitespace")
    return problems


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    check_only = "--check" in argv
    with open(ENTRY_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    problems = check_gate(text)
    if problems:
        for problem in problems:
            print("gate FAIL: %s" % problem, file=sys.stderr)
        raise SystemExit(1)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if check_only:
        print("gate OK: %d chars, sha256 %s" % (len(text), digest))
        return
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8", newline="") as f:
        f.write(text)
    sys.stdout.write(text)
    print("gate OK: %d chars, sha256 %s" % (len(text), digest), file=sys.stderr)


if __name__ == "__main__":
    main()
