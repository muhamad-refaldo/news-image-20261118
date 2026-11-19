#!/usr/bin/env python3
"""Entry point for the make.fun news-image bounty (18 Nov 2026).

Copies the pre-rendered entry.png to /output/entry.png.
Deterministic: stdlib only, no network, no timestamps, same bytes every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("wrote", dst)
    return 0

if __name__ == "__main__":
    sys.exit(main())
