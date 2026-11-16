#!/usr/bin/env python3
"""Deliver the ai-excited-01 entry image to the harness output directory.

The image this repository ships is a watercolor and ink phoenix: gold,
orange and red washes with dark ink outlines, bursting head-on out of
a large gilt-framed watercolor painting straight at the viewer. The
frame is genuinely broken — its bottom rail is missing across the
middle, with jagged ends, and the phoenix's tail comes through that
open gap while the other three sides stay whole. Two tiny students
duck below with their hands over their heads, the wall behind is plain
and dark, and there is no writing of any kind in the picture.

Before it writes anything, this script proves the file on disk is
exactly the image the entry was made from: it checks the JPEG opening
bytes, the byte count, and the SHA-256 digest, and refuses to continue
if any of them differs.
"""

import hashlib
import os
import sys
from pathlib import Path

PICTURE = "entry.png"
EXPECTED_LENGTH = 201965
EXPECTED_DIGEST = "b1819d1a5509c0d2136b47898e9800d519de071963c0142fa81d364e42258ab7"
JPEG_HEAD = b"\xff\xd8\xff"
FALLBACK_OUT = "/output"


def fail(reason):
    """Print why the picture is wrong and stop without writing output."""
    print(f"bad entry picture: {reason}", file=sys.stderr)
    sys.exit(1)


def load_picture():
    """Read entry.png next to this script and check it three ways."""
    folder = Path(__file__).resolve().parent
    data = (folder / PICTURE).read_bytes()

    if data[:3] != JPEG_HEAD:
        fail("entry.png does not open with the JPEG marker")
    if len(data) != EXPECTED_LENGTH:
        fail(f"entry.png is {len(data)} bytes, not {EXPECTED_LENGTH}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_DIGEST:
        fail(f"entry.png digests to {digest}, not {EXPECTED_DIGEST}")
    return data, digest


def main():
    data, digest = load_picture()
    destination = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", FALLBACK_OUT))
    destination.mkdir(parents=True, exist_ok=True)
    written = destination / PICTURE
    written.write_bytes(data)
    print(f"wrote {written} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
