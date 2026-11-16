#!/usr/bin/env python3
"""Ship the ai-excited-01 entry picture to the harness output folder.

The picture in this repository is a watercolor and ink phoenix: the
bird is painted in gold, orange and red washes with dark ink outlines,
bursting straight out of a large gilt-framed watercolor painting toward
the viewer, head-on. The frame is shattered, ink and paint splash
around it, and two tiny students crouch below with their hands over
their heads. The wall behind is plain and dark, and the picture holds
no writing of any kind.

This program first makes sure the picture on disk is exactly the file
the entry was built from, then copies it to the output folder. It
checks the byte count, the SHA-256 digest, and the JPEG opening bytes;
if any of them is wrong it stops with an error and writes nothing.
"""

import hashlib
import os
import sys
from pathlib import Path

IMAGE_NAME = "entry.png"
IMAGE_BYTES = 229818
IMAGE_SHA256 = "f2299540776ebc9e7d531c0724f628201016d4ddff5edb7c43c475d53f2d4a35"
JPEG_MAGIC = b"\xff\xd8\xff"
DEFAULT_OUT = "/output"


def abort(message):
    """Report a bad picture and stop without writing output."""
    print(f"entry rejected: {message}", file=sys.stderr)
    sys.exit(1)


def checked_picture():
    """Load entry.png and prove it is the exact entry picture."""
    here = Path(__file__).resolve().parent
    blob = (here / IMAGE_NAME).read_bytes()

    if len(blob) != IMAGE_BYTES:
        abort(f"entry.png is {len(blob)} bytes, expected {IMAGE_BYTES}")
    digest = hashlib.sha256(blob).hexdigest()
    if digest != IMAGE_SHA256:
        abort(f"entry.png hashes to {digest}, expected {IMAGE_SHA256}")
    if blob[:3] != JPEG_MAGIC:
        abort("entry.png does not start with the JPEG marker")
    return blob, digest


def main():
    blob, digest = checked_picture()
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUT))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / IMAGE_NAME
    target.write_bytes(blob)
    print(f"copied {target} ({len(blob)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
