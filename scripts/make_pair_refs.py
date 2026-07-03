#!/usr/bin/env python3
"""
Build side-by-side two-character reference sheets for Midjourney multi-char refs.

Takes the single-character portraits in assets/profile_<name>.png and combines
every pair into a side-by-side panel image named <name>-<name>.png in the same
folder. Each source is center-cropped to a square "cover" panel so faces stay
centered and both panels are equal width, then joined with a thin divider.

Usage:
    python3 scripts/make_pair_refs.py                # all pairs, all profiles
    python3 scripts/make_pair_refs.py nero loren     # only pairs among these
    python3 scripts/make_pair_refs.py --pair nero loren   # just this one pair

Naming: files are <a>-<b>.png with names sorted alphabetically for stability
(so nero+loren -> loren-nero.png). Existing outputs are overwritten.
"""
import sys
import glob
import os
from itertools import combinations
from PIL import Image

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")
ASSETS = os.path.abspath(ASSETS)
PANEL = 1024          # each panel is PANEL x PANEL
DIVIDER = 6           # px width of divider between panels
DIVIDER_COLOR = (10, 10, 12)


def cover_square(img, size):
    """Center-crop to square, then resize to size x size."""
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    return img.resize((size, size), Image.LANCZOS)


def panels_from(name):
    path = os.path.join(ASSETS, f"profile_{name}.png")
    return cover_square(Image.open(path).convert("RGB"), PANEL)


def make_pair(a, b):
    left = panels_from(a)
    right = panels_from(b)
    canvas = Image.new("RGB", (PANEL * 2 + DIVIDER, PANEL), DIVIDER_COLOR)
    canvas.paste(left, (0, 0))
    canvas.paste(right, (PANEL + DIVIDER, 0))
    lo, hi = sorted([a, b])
    out = os.path.join(ASSETS, f"{lo}-{hi}.png")
    canvas.save(out)
    return out


def all_names():
    names = []
    for p in sorted(glob.glob(os.path.join(ASSETS, "profile_*.png"))):
        names.append(os.path.basename(p)[len("profile_"):-len(".png")])
    return names


def main(argv):
    if argv and argv[0] == "--pair" and len(argv) == 3:
        print("wrote", make_pair(argv[1], argv[2]))
        return
    names = argv if argv else all_names()
    for a, b in combinations(sorted(names), 2):
        print("wrote", make_pair(a, b))


if __name__ == "__main__":
    main(sys.argv[1:])
