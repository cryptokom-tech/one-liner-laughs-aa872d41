#!/usr/bin/env python3
"""Entry for make.fun bounty 'One-Liner Laughs'.

Writes a single joke line to /output/entry.txt.
Uses only the Python standard library and is deterministic:
every run produces byte-identical output.
"""

import os

ENTRY_TEXT = "I joined a book club to meet people; we never meet, which is exactly how I like people."
OUTPUT_PATH = "/output/entry.txt"


def check_entry(text):
    """Guard the bounty gate: 1-200 UTF-8 chars, one line, not blank."""
    if not isinstance(text, str):
        raise TypeError(f"entry must be str, got {type(text).__name__}")
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1-200 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    # Fail here, before any file is touched, if the text cannot be
    # represented as UTF-8 (e.g. lone surrogates from a bad edit).
    try:
        text.encode("utf-8", errors="strict")
    except UnicodeEncodeError as exc:
        raise ValueError("entry must be encodable as UTF-8") from exc


def write_entry():
    check_entry(ENTRY_TEXT)
    directory = os.path.dirname(OUTPUT_PATH)
    os.makedirs(directory, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY_TEXT)
    # Read back as raw bytes so a truncated or corrupted write, or a
    # stray trailing newline, fails loudly here rather than silently
    # producing an invalid entry for the judge.
    with open(OUTPUT_PATH, "rb") as handle:
        written_bytes = handle.read()
    if written_bytes != ENTRY_TEXT.encode("utf-8"):
        raise ValueError("written entry does not match ENTRY_TEXT bytes")
    check_entry(written_bytes.decode("utf-8"))


if __name__ == "__main__":
    write_entry()
