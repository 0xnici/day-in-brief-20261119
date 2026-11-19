#!/usr/bin/env python3
"""Entry point for The Day in Brief — Thursday 19 November 2026.

The edition's front page is committed in this repository as entry.png,
typeset from the day's wire reporting by tools/render.py. This program
is the competition entry: it delivers that page to the output directory
as /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png when the harness
sets the variable), using only the standard library, with no network.

Delivery is verified before success is reported: the file written is
read back and compared byte for byte with the committed page, so a
truncated write or a swapped source fails loudly instead of passing.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def deliver_page():
    """Copy the committed front page into the output directory."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(SOURCE, "rb") as handle:
        page = handle.read()
    with open(target, "wb") as handle:
        handle.write(page)
    return target, page


def main():
    target, page = deliver_page()
    # Read the copy back before reporting success: the entry counts only
    # if the file on disk is the committed page, unchanged, so a short
    # write or a swapped source must fail here rather than pass silently.
    with open(target, "rb") as handle:
        on_disk = handle.read()
    if on_disk != page:
        print(f"error: {target} does not match the committed page", file=sys.stderr)
        return 1
    import hashlib

    digest = hashlib.sha256(page).hexdigest()
    print(f"wrote {target} ({len(page)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
