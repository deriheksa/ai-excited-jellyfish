#!/usr/bin/env python3
"""Deliver the ai-excited-01 picture to the harness output folder.

The picture shipped with this entry is entry.png. The extension is a
hangover from the harness convention — the bytes are a JPEG. It shows a
giant phoenix of living flame bursting out of a gilt-framed sunrise
painting on a classroom wall: the frame is smashed, splinters, embers
and burning feathers are flying everywhere, and four small students
below duck under their desks with their hands on their heads.

This program has a single, strict chore. It loads the bundled picture,
checks that it is bit-for-bit the picture this entry was built from —
correct JPEG opening marker, correct byte count, correct SHA-256 —
and only then copies it to the harness output directory, still named
entry.png. Anything that fails a check stops the run with an error and
no output file is written.
"""

import hashlib
import os
import sys
from pathlib import Path

PICTURE = "entry.png"
EXPECTED_SIZE = 225418
EXPECTED_DIGEST = "300702fb686884e3846a19dcbc75276c065c6a46800fcd840ee6a210a8ca4bed"
JPEG_PREFIX = b"\xff\xd8\xff"
FALLBACK_OUT = "/output"


def die(reason):
    print(f"picture check failed: {reason}", file=sys.stderr)
    sys.exit(1)


def main():
    folder = Path(__file__).resolve().parent
    data = (folder / PICTURE).read_bytes()

    if data[:3] != JPEG_PREFIX:
        die("the bundled file is not a JPEG (bad opening bytes)")
    if len(data) != EXPECTED_SIZE:
        die(f"the bundled file is {len(data)} bytes, not {EXPECTED_SIZE}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_DIGEST:
        die(f"the bundled file hashes to {digest}, not {EXPECTED_DIGEST}")

    destination = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", FALLBACK_OUT))
    destination.mkdir(parents=True, exist_ok=True)
    written = destination / PICTURE
    written.write_bytes(data)
    print(f"wrote {written} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
