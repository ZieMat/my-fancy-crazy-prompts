#!/usr/bin/env python3
"""Turn a WebVTT caption file into plain transcript text.

Usage:
  clean_vtt.py INPUT.vtt OUTPUT.txt [--chunk-words N] [--chunk-dir DIR]

Drops cue timings, alignment settings, and word-level tags. YouTube
auto-captions repeat themselves; the short "settled" cues are kept and
consecutive duplicates are removed. When those cues are absent, overlapping
lines are merged instead.

Writes OUTPUT.txt with a [HH:MM:SS] marker every five minutes. With
--chunk-dir, also writes numbered chunk files of about --chunk-words words.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

CUE_TIME = re.compile(
    r"(?:(\d+):)?(\d{2}):(\d{2})\.(\d{3})\s+-->\s+"
    r"(?:(\d+):)?(\d{2}):(\d{2})\.(\d{3})"
)
TAG = re.compile(r"<[^>]+>")
INLINE_TIME = re.compile(r"\d{2}:\d{2}:\d{2}\.\d{3}|\d{2}:\d{2}\.\d{3}")


def seconds(hours: str | None, minutes: str, secs: str, millis: str) -> float:
    return int(hours or 0) * 3600 + int(minutes) * 60 + int(secs) + int(millis) / 1000


def stamp(total: float) -> str:
    whole = int(total)
    return f"{whole // 3600:02d}:{(whole % 3600) // 60:02d}:{whole % 60:02d}"


def parse_cues(text: str) -> list[tuple[float, float, str]]:
    cues: list[tuple[float, float, str]] = []
    for block in re.split(r"\n\n+", text.replace("\r\n", "\n")):
        match = CUE_TIME.search(block)
        if not match:
            continue
        start = seconds(*match.group(1, 2, 3, 4))
        end = seconds(*match.group(5, 6, 7, 8))
        body = "\n".join(
            line.strip() for line in block.splitlines()[1:] if line.strip()
        )
        if body:
            cues.append((start, end, body))
    return cues


def visible(line: str) -> str:
    cleaned = TAG.sub("", line)
    cleaned = INLINE_TIME.sub("", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip(" -")


def settled_phrases(cues: list[tuple[float, float, str]]) -> list[tuple[float, str]]:
    short = [
        (start, visible(body))
        for start, end, body in cues
        if end - start <= 0.05 and visible(body)
    ]
    if len(short) >= max(3, len(cues) // 5):
        phrases = short
    else:
        phrases = []
        for start, _end, body in cues:
            lines = [visible(line) for line in body.splitlines()]
            lines = [line for line in lines if line]
            if not lines:
                continue
            plain = [line for line in lines if "<" not in line]
            phrases.append((start, plain[-1] if plain else lines[-1]))
    deduped: list[tuple[float, str]] = []
    for start, phrase in phrases:
        if deduped and deduped[-1][1] == phrase:
            continue
        if deduped:
            phrase = new_tail(deduped[-1][1], phrase)
            if not phrase:
                continue
        deduped.append((start, phrase))
    return deduped


def new_tail(previous: str, current: str) -> str:
    if current == previous or current in previous:
        return ""
    if current.startswith(previous):
        return current[len(previous) :].strip()
    max_check = min(len(previous), len(current), 400)
    for size in range(max_check, 8, -1):
        if previous[-size:] == current[:size]:
            return current[size:].strip()
    return current


def render(phrases: list[tuple[float, str]], every: int = 300) -> str:
    parts: list[str] = []
    next_mark = 0
    bucket: list[str] = []

    def flush() -> None:
        if bucket:
            parts.append(" ".join(bucket).strip())
            bucket.clear()

    for start, phrase in phrases:
        while start >= next_mark:
            flush()
            parts.append(f"[{stamp(next_mark)}]")
            next_mark += every
        bucket.append(phrase)
    flush()
    return "\n\n".join(part for part in parts if part) + "\n"


def write_chunks(text: str, directory: Path, words_per_chunk: int) -> list[Path]:
    directory.mkdir(parents=True, exist_ok=True)
    chunks: list[list[str]] = []
    current: list[str] = []
    count = 0
    for block in text.split("\n\n"):
        block_words = len(block.split())
        if current and count >= words_per_chunk and block.startswith("["):
            chunks.append(current)
            current = []
            count = 0
        current.append(block)
        count += block_words
    if current:
        chunks.append(current)
    paths: list[Path] = []
    for index, blocks in enumerate(chunks, start=1):
        path = directory / f"{index:03d}.txt"
        path.write_text("\n\n".join(blocks).strip() + "\n", encoding="utf-8")
        paths.append(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vtt")
    parser.add_argument("output")
    parser.add_argument("--chunk-words", type=int, default=2500)
    parser.add_argument("--chunk-dir")
    args = parser.parse_args()
    cues = parse_cues(Path(args.vtt).read_text(encoding="utf-8", errors="replace"))
    if not cues:
        raise SystemExit(f"no cues in {args.vtt}")
    text = render(settled_phrases(cues))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(f"wrote {output} ({len(text.split())} words)")
    if args.chunk_dir:
        paths = write_chunks(text, Path(args.chunk_dir), args.chunk_words)
        print(f"chunks {len(paths)} in {args.chunk_dir}")


if __name__ == "__main__":
    main()
