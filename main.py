#!/usr/bin/env python3
"""Ship the ai-excited-01 entry picture to the harness output folder.

The picture in this repository is a phoenix in watercolor and ink
that flies straight at the viewer out of a large gilt-framed painting
of a sky. Gold, orange and red washes with dark ink lines and paint
drips make the bird; its wings are spread so wide they have smashed
through the frame's left and right sides, so those two sides are
broken open with splinters and torn canvas bursting out from them,
while the top and bottom rails of the frame are still whole. The
bird's tail hangs back inside the painting. Two small students cower
below with their hands on their heads, the wall behind is plain and
dark, and the picture holds no writing anywhere.

This script first makes sure the file beside it is byte for byte the
picture the entry was built from — it measures the length, looks at
the opening bytes, and takes the SHA-256 — and only then copies it to
the output folder. Anything different stops it before it writes.
"""

import hashlib
import os
import sys
from pathlib import Path

FILENAME = "entry.png"
WANT_BYTES = 204691
WANT_SHA = "54f15b35923e7593d3e4671fd784c2ad15c67cd0606a6a063b0b1426cd263678"
JPEG_MAGIC = b"\xff\xd8\xff"
DEFAULT_OUTPUT = "/output"


def die(what):
    """Report a bad picture and quit without writing anything."""
    print(f"entry picture is wrong: {what}", file=sys.stderr)
    sys.exit(1)


def check_image():
    """Load entry.png from this script's folder and prove it matches."""
    here = Path(__file__).resolve().parent
    blob = (here / FILENAME).read_bytes()

    if len(blob) != WANT_BYTES:
        die(f"entry.png is {len(blob)} bytes, expected {WANT_BYTES}")
    if blob[:3] != JPEG_MAGIC:
        die("entry.png does not start with the JPEG marker")
    digest = hashlib.sha256(blob).hexdigest()
    if digest != WANT_SHA:
        die(f"entry.png hashes to {digest}, expected {WANT_SHA}")
    return blob, digest


def run():
    picture, digest = check_image()
    outdir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT))
    outdir.mkdir(parents=True, exist_ok=True)
    target = outdir / FILENAME
    target.write_bytes(picture)
    print(f"copied {target} ({len(picture)} bytes, sha256 {digest})")


if __name__ == "__main__":
    run()
