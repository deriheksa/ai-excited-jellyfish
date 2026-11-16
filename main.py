#!/usr/bin/env python3
"""Ship the ai-excited-01 picture to the output folder.

The picture is the user's own black hole: a swirling black-hole
vortex has opened in the middle of a bright, sunlit room and is
pulling the furniture into it — a red leather armchair, a lamp,
books, a small wooden table, a blue-and-white vase with red roses,
rose petals flying everywhere. A framed landscape painting hangs
on the wall at the top right and a big arched window lets sunlight
in from the left. One thing dominates the frame: the black hole
itself, a dark circle ringed with gold. Nothing is written anywhere
in the picture, and nothing was added to it — it is the user's
image, only shrunk and re-encoded to fit the bounty limits.

This script makes sure the picture sitting next to it is exactly
the shipped one, by its byte count, its JPEG opening marker, and
its SHA-256. If any of those three is off, it refuses to write
anything and quits with an error.
"""

import hashlib
import os
import sys
from pathlib import Path

FILENAME = "entry.png"
BYTE_COUNT = 268521
DIGEST = "87f5e1bf5bbb3ddabe05b4a3846f188d232344847418afbbfc5fe23ca83867e6"
JPEG_START = b"\xff\xd8\xff"
DEFAULT_OUT = "/output"


def abort(why):
    """Report a mismatch and stop before writing anything."""
    print(f"entry picture mismatch: {why}", file=sys.stderr)
    sys.exit(1)


def checked_bytes():
    """Load entry.png beside this script and confirm it three ways."""
    here = Path(__file__).resolve().parent
    blob = (here / FILENAME).read_bytes()

    if len(blob) != BYTE_COUNT:
        abort(f"entry.png is {len(blob)} bytes, expected {BYTE_COUNT}")
    if blob[:3] != JPEG_START:
        abort("entry.png does not start with the JPEG marker")
    digest = hashlib.sha256(blob).hexdigest()
    if digest != DIGEST:
        abort(f"entry.png sha256 is {digest}, expected {DIGEST}")
    return blob, digest


def main():
    blob, digest = checked_bytes()
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUT))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / FILENAME
    target.write_bytes(blob)
    print(f"copied {target} ({len(blob)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
