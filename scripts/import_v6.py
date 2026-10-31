#!/usr/bin/env python3
"""Overlay the approved Stopododo V6 ZIP onto the integration branch.

Usage (from the repository root in Codespaces):
    python3 scripts/import_v6.py Stopododo_Site_V6_SEO_10_Langues.zip --push
The script never touches main, never deletes existing files, and preserves legal pages.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path, PurePosixPath
import subprocess
import sys
import zipfile

LANGS = ("fr", "en", "es", "it", "de", "nl", "pt", "ar", "ja", "ko")
LEGAL = {"confidentialite.html", "conditions.html", "accessibilite.html", "contact.html"}
EXPECTED = {
    "index.html", "sitemap.xml", "video-sitemap.xml", "robots.txt",
    "styles-v3.css", "seo-v6.css", "site-v3.js",
    "fr/assombrir-ecran-android.html", "fr/minuteur-sommeil-android.html",
    "fr/arreter-video-automatiquement.html",
}
for lang in LANGS:
    EXPECTED |= {
        f"{lang}/index.html", f"{lang}/video-stopododo.html",
        f"assets/videos/{lang}.mp4", f"assets/img/video-posters/{lang}.webp",
    }

def git(*args: str, capture: bool = True) -> str:
    result = subprocess.run(["git", *args], capture_output=capture,
                            text=True, check=True)
    return result.stdout.strip() if capture else ""

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="Approved V6 ZIP archive")
    parser.add_argument("--push", action="store_true",
                        help="Commit and push onto integration-v6-seo, not main")
    args = parser.parse_args()

    root = Path(git("rev-parse", "--show-toplevel")).resolve()
    current = git("branch", "--show-current")
    if current != "integration-v6-seo":
        sys.exit(f"Refusing to modify branch {current!r}: checkout integration-v6-seo first.")

    archive = args.archive.resolve()
    if not archive.is_file():
        sys.exit(f"Archive not found: {archive}")

    previous_legal = {
        str(p.relative_to(root)): sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*.html") if p.name in LEGAL and ".git" not in p.parts
    }
    if len(previous_legal) < 40:
        sys.exit("Expected legal pages from the previous multilingual site were not found.")

    worktree = git("status", "--porcelain", "--untracked-files=all")
    others = []
    for line in worktree.splitlines():
        path = line[3:]
        if path not in {archive.name, ".gitignore"}:
            others.append(line)
    if others:
        sys.exit("Working tree contains unrelated changes. Commit/stash them first:\n" +
                 "\n".join(others[:15]))

    with zipfile.ZipFile(archive) as z:
        infos = [x for x in z.infolist() if not x.is_dir()]
        names = {x.filename for x in infos}
        missing = EXPECTED - names
        if missing:
            sys.exit("Missing expected V6 assets:\n" + "\n".join(sorted(missing)))
        if sum(i.file_size for i in infos) > 35_000_000:
            sys.exit("ZIP unexpectedly large; aborting.")
        for info in infos:
            posix = PurePosixPath(info.filename)
            if (posix.is_absolute() or ".." in posix.parts or
                "\\" in info.filename or not posix.parts or
                posix.parts[0] in {".git", ".github"} or
                posix.name in LEGAL or info.file_size > 4_000_000):
                sys.exit(f"Unsafe or disallowed ZIP entry: {info.filename}")
        print(f"Importing {len(infos)} approved V6 files on {current}.")
        updated_paths = []
        for info in infos:
            path = root.joinpath(*PurePosixPath(info.filename).parts)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(z.read(info))
            updated_paths.append(info.filename)

    for rel, checksum in previous_legal.items():
        path = root / rel
        if not path.is_file() or sha256(path.read_bytes()).hexdigest() != checksum:
            sys.exit(f"Legal page was modified: {rel}")

    for lang in LANGS:
        source = root / "assets" / "videos" / (lang + ".mp4")
        if source.read_bytes()[:8][4:] != b"ftyp":
            sys.exit(f"Invalid MP4: {source}")
    print("Legal documents retained. 10 MP4 files and expected pages present.")
    print("Review in local preview before publishing.")
    if args.push:
        git("add", "--", *updated_paths, capture=False)
        subprocess.run(["git", "diff", "--cached", "--check"], check=True)
        if git("diff", "--cached", "--name-only"):
            git("commit", "-m", "Integrate approved Stopododo V6 SEO site (no main deployment)",
                capture=False)
            git("push", "origin", "HEAD:refs/heads/integration-v6-seo", capture=False)
        print("V6 pushed to integration-v6-seo only. Main remains unchanged.")
    else:
        print("Files copied locally only. Re-run with --push to commit and push.")

if __name__ == "__main__":
    main()
