#!/usr/bin/env python3
"""Copy the ai-excited-01 entry image into the harness output folder.

The repository ships one picture, entry.png. Inside it is a JPEG of a
giant phoenix made of living flame breaking out of a large gilt-framed
painting: the frame is shattered, splinters and torn canvas fly around
the bird, and two small students crouch below with their hands over
their heads. The room is plain and dark, there is no writing anywhere
in the picture, and the phoenix is the single clear shape in it.

Before anything is written, this program proves the bundled picture
is the exact file the entry was built from. It checks the opening
bytes, the byte count, and the SHA-256 digest, in that order. A failed
check stops the program with an error and no output file.
"""

import hashlib
import os
import sys
from pathlib import Path

PICTURE = "entry.png"
EXPECTED_LENGTH = 193281
EXPECTED_DIGEST = "959440b2308282609f92d049943e20711fa5e16d09bc8708c79cb577c3e32d5c"
JPEG_START = b"\xff\xd8\xff"
OUTPUT_DIR = "/output"


def fail(reason):
    """Print why the picture was rejected, then stop with an error."""
    print(f"picture rejected: {reason}", file=sys.stderr)
    sys.exit(1)


def load_picture():
    """Read the bundled picture and check it matches the entry."""
    folder = Path(__file__).resolve().parent
    data = (folder / PICTURE).read_bytes()

    if data[:3] != JPEG_START:
        fail("the bundled picture does not begin with the JPEG marker")
    if len(data) != EXPECTED_LENGTH:
        fail(f"the bundled picture is {len(data)} bytes, not {EXPECTED_LENGTH}")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_DIGEST:
        fail(f"the bundled picture digests to {digest}, not {EXPECTED_DIGEST}")
    return data, digest


def run():
    data, digest = load_picture()
    destination = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", OUTPUT_DIR))
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / PICTURE
    target.write_bytes(data)
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    run()
