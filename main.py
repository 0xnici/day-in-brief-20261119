#!/usr/bin/env python3
"""Entry point for the 19 November 2026 visual edition.

The front page is composed ahead of time by tools/compose.py and stored
beside this file as entry.png. At grade time there is no network and no
clock to consult, so the whole job here is a careful copy: verify the
asset really is the page we shipped, then place it at /output/entry.png
byte for byte.
"""
import os
import sys
import tempfile

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET_DIR = "/output"
TARGET = os.path.join(TARGET_DIR, "entry.png")


def read_page() -> bytes:
    with open(SOURCE, "rb") as fh:
        blob = fh.read()
    if not blob.startswith(PNG_SIGNATURE):
        raise SystemExit("entry.png is not a PNG file")
    if len(blob) > 1024 * 1024:
        raise SystemExit("entry.png exceeds the 1 MiB limit")
    # The IHDR chunk follows the signature: width and height are the two
    # big-endian uint32s at bytes 16..24. The rules cap the page at
    # 1024x1024, so refuse anything larger before it is published.
    width = int.from_bytes(blob[16:20], "big")
    height = int.from_bytes(blob[20:24], "big")
    if width > 1024 or height > 1024:
        raise SystemExit(f"entry.png is {width}x{height}, over the 1024x1024 cap")
    return blob


def publish(blob: bytes) -> None:
    os.makedirs(TARGET_DIR, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=TARGET_DIR, suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(blob)
        os.replace(tmp, TARGET)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main() -> int:
    blob = read_page()
    publish(blob)
    print(f"published {TARGET} ({len(blob)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
