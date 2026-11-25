#!/usr/bin/env python3
"""enx: hand the scorer exactly one line, nothing else."""

import json
import os
import pathlib

TOP = 200
NAME = "entry.txt"


def normalize(blob):
    return next((ln.rstrip() for ln in blob.replace("\r\n", "\n").split("\n")
                 if ln.strip()), "")


def ship():
    neighborhood = pathlib.Path(__file__).resolve().parent
    origin = neighborhood / NAME
    try:
        blob = origin.read_text(encoding="utf-8")
    except OSError:
        print(json.dumps({"done": False, "note": "origin file missing"}))
        return 2
    line = normalize(blob)
    gauge = len(line)
    verdict = bool(line.strip()) and gauge <= TOP
    if not verdict:
        print(json.dumps({"done": False, "gauge": gauge, "top": TOP}))
        return 1
    yard = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    os.makedirs(yard, exist_ok=True)
    pathlib.Path(yard, NAME).write_text(line, encoding="utf-8", newline="\n")
    print(json.dumps({"done": True, "gauge": gauge, "top": TOP}))
    return 0


if __name__ == "__main__":
    raise SystemExit(ship())
