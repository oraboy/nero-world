#!/usr/bin/env python3
"""
Write a name -> URL mapping for the reference images using GitHub raw URLs.
Midjourney accepts raw.githubusercontent.com; these are durable and account-owned.

Usage: python3 scripts/make_url_map.py
"""
import os
import glob

ASSETS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
MAP = os.path.join(ASSETS, "ref_urls.md")
BASE = "https://raw.githubusercontent.com/oraboy/nero-world/main/assets"


def rows(paths):
    out = []
    for p in sorted(paths):
        name = os.path.basename(p)
        out.append(f"| {name} | {BASE}/{name} |\n")
    return out


def main():
    pairs = [p for p in glob.glob(os.path.join(ASSETS, "*.png"))
             if "-" in os.path.basename(p) and not os.path.basename(p).startswith("profile_")]
    profiles = glob.glob(os.path.join(ASSETS, "profile_*.png"))

    with open(MAP, "w") as f:
        f.write("# Reference image URLs (GitHub raw, public)\n\n")
        f.write("Repo: https://github.com/oraboy/nero-world\n\n")
        f.write("## Pairs (two-character side-by-side)\n\n")
        f.write("| file | url |\n|---|---|\n")
        f.writelines(rows(pairs))
        f.write("\n## Profiles (single character)\n\n")
        f.write("| file | url |\n|---|---|\n")
        f.writelines(rows(profiles))
    print("wrote", MAP)


if __name__ == "__main__":
    main()
