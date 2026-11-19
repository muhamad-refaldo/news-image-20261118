#!/usr/bin/env python3
"""Entry point for the make.fun news-image bounty (18 Nov 2026).

The entry is a pre-rendered picture: this program only copies it to the
output folder. Standard library only, no network, no timestamps — the
bytes written are identical on every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def run():
    """Copy entry.png into the output directory as /output/entry.png."""
    destination_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(destination_dir, exist_ok=True)
    destination = os.path.join(destination_dir, "entry.png")
    shutil.copyfile(SOURCE, destination)
    print("wrote", destination)
    return 0


if __name__ == "__main__":
    sys.exit(run())
