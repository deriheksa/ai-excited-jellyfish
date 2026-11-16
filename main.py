#!/usr/bin/env python3
"""Hand the ai-excited-01 picture to the harness.

The picture bundled with this entry is entry.png. The name is a
leftover: the bytes inside are a JPEG. It shows a giant grey-brown
elephant smashing out of a huge gilt-framed savanna painting in a dark
museum hall — the frame splintering apart, wood and torn canvas flying
— while four tiny visitors underneath duck and throw their hands up.

The script does one dull job and does it strictly. It reads the
bundled picture, proves it is exactly the file this entry was built
from (right opening bytes, right length, right SHA-256), and only then
copies those bytes to the harness output folder as entry.png. If the
bundled file is anything else — wrong, truncated, swapped — the script
stops with an error and writes nothing.
"""

import hashlib
import os
import sys
from pathlib import Path

FILENAME = "entry.png"
WANTED_BYTES = 170537
WANTED_SHA256 = "bf0c7a0d989e65325762e9b162647dd50f8dc29645fbcc561cb4d7ac8590d960"
JPEG_OPENING = b"\xff\xd8\xff"
DEFAULT_OUT = "/output"


def fail(message):
    print(f"entry.png rejected: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    here = Path(__file__).resolve().parent
    blob = (here / FILENAME).read_bytes()

    if blob[:3] != JPEG_OPENING:
        fail("the file does not start with the JPEG marker")
    if len(blob) != WANTED_BYTES:
        fail(f"the file is {len(blob)} bytes, expected {WANTED_BYTES}")
    digest = hashlib.sha256(blob).hexdigest()
    if digest != WANTED_SHA256:
        fail(f"sha256 {digest} does not match {WANTED_SHA256}")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUT))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / FILENAME
    target.write_bytes(blob)
    print(f"wrote {target} ({len(blob)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
