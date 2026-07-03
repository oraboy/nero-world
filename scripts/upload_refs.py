#!/usr/bin/env python3
"""
Upload reference images to catbox.moe (permanent, public, no account) and write
a name -> URL mapping to assets/ref_urls.md. Safe to re-run: it only uploads
files not already present in the existing mapping.

Usage:
    python3 scripts/upload_refs.py            # uploads pairs + profiles
"""
import os
import glob
import subprocess

ASSETS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
MAP = os.path.join(ASSETS, "ref_urls.md")
API = "https://catbox.moe/user/api.php"


def load_existing():
    urls = {}
    if not os.path.exists(MAP):
        return urls
    for line in open(MAP):
        line = line.strip()
        if line.startswith("|") and "http" in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 2 and cells[1].startswith("http"):
                urls[cells[0]] = cells[1]
    return urls


def upload(path):
    out = subprocess.run(
        ["curl", "-sS", "-F", "reqtype=fileupload",
         "-F", f"fileToUpload=@{path}", API],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    if not out.startswith("http"):
        raise RuntimeError(f"upload failed for {path}: {out}")
    return out


def collect():
    # pairs: any <a>-<b>.png (not profile_*)
    pairs = sorted(
        p for p in glob.glob(os.path.join(ASSETS, "*.png"))
        if "-" in os.path.basename(p) and not os.path.basename(p).startswith("profile_")
    )
    profiles = sorted(glob.glob(os.path.join(ASSETS, "profile_*.png")))
    return pairs, profiles


def main():
    urls = load_existing()
    pairs, profiles = collect()
    for path in pairs + profiles:
        name = os.path.basename(path)
        if name in urls:
            print("skip (have)", name)
            continue
        url = upload(path)
        urls[name] = url
        print("uploaded", name, "->", url)

    with open(MAP, "w") as f:
        f.write("# Reference image URLs (catbox.moe, public)\n\n")
        f.write("## Pairs (two-character side-by-side)\n\n")
        f.write("| file | url |\n|---|---|\n")
        for name in sorted(n for n in urls if not n.startswith("profile_")):
            f.write(f"| {name} | {urls[name]} |\n")
        f.write("\n## Profiles (single character)\n\n")
        f.write("| file | url |\n|---|---|\n")
        for name in sorted(n for n in urls if n.startswith("profile_")):
            f.write(f"| {name} | {urls[name]} |\n")
    print("wrote", MAP)


if __name__ == "__main__":
    main()
