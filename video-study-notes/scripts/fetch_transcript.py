#!/usr/bin/env python3
"""Download one YouTube transcript per URL with uvx yt-dlp, then clean it.

Usage:
  fetch_transcript.py URL [URL ...] --out DIR
  fetch_transcript.py --from-file notes.md --out DIR [--limit N]

Each URL is a separate yt-dlp run. The cleaned transcript and chunk files
land in DIR/<video-id>/. Raw WebVTT is kept next to them. Prefers a
language's *-orig caption, then that language, then the first caption found.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

URL_RE = re.compile(r"https?://[^\s<>)]+")
ID_RE = re.compile(r"(?:v=|youtu\.be/|shorts/)([A-Za-z0-9_-]{6,})")
CLEAN = Path(__file__).with_name("clean_vtt.py")


def urls_from(text: str) -> list[str]:
    found: list[str] = []
    for match in URL_RE.findall(text):
        if "youtu" not in match and "youtube" not in match:
            continue
        url = match.rstrip(".,")
        if url not in found:
            found.append(url)
    return found


def video_id(url: str) -> str:
    match = ID_RE.search(url)
    return match.group(1) if match else "video"


def pick_vtt(paths: list[Path], lang: str) -> Path | None:
    order = [f".{lang}-orig.vtt", f".{lang}.vtt"]

    def rank(path: Path) -> tuple[int, str]:
        name = path.name
        for index, suffix in enumerate(order):
            if name.endswith(suffix):
                return (index, name)
        return (len(order), name)

    candidates = [path for path in paths if path.suffix == ".vtt" and path.stat().st_size > 0]
    if not candidates:
        return None
    return sorted(candidates, key=rank)[0]


def download_one(url: str, out_dir: Path, lang: str) -> None:
    target = out_dir / video_id(url)
    target.mkdir(parents=True, exist_ok=True)
    template = str(target / "%(id)s.%(ext)s")
    command = [
        "uvx",
        "yt-dlp",
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs",
        f"{lang}.*,en.*",
        "--convert-subs",
        "vtt",
        "-o",
        template,
        url,
    ]
    print(" ".join(command), flush=True)
    completed = subprocess.run(command, check=False)
    chosen = pick_vtt(list(target.glob("*.vtt")), lang)
    if chosen is None:
        raise SystemExit(f"no subtitles for {url} (yt-dlp exit {completed.returncode})")
    transcript = target / "transcript.txt"
    chunk_dir = target / "chunks"
    subprocess.run(
        [
            sys.executable,
            str(CLEAN),
            str(chosen),
            str(transcript),
            "--chunk-dir",
            str(chunk_dir),
        ],
        check=True,
    )
    print(f"source {chosen}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="*")
    parser.add_argument("--from-file")
    parser.add_argument("--out", default="/tmp/video-study-notes")
    parser.add_argument("--lang", default="pl")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    urls = list(args.urls)
    if args.from_file:
        urls.extend(urls_from(Path(args.from_file).read_text(encoding="utf-8")))
    seen: list[str] = []
    for url in urls:
        if url not in seen:
            seen.append(url)
    if args.limit:
        seen = seen[: args.limit]
    if not seen:
        raise SystemExit("no URLs")
    if args.list:
        print("\n".join(seen))
        return
    out = Path(args.out)
    for url in seen:
        download_one(url, out, args.lang)


if __name__ == "__main__":
    main()
