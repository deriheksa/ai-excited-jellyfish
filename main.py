#!/usr/bin/env python3
"""Deliver the ai-excited-01 picture to the output directory.

The picture is a watercolor-and-ink phoenix that bursts straight
toward the viewer out of a gilt-framed painting of a sky. Its wings
are spread so wide they have torn clean through the frame's left and
right sides: those two rails are gone entirely, so behind the wings
there is only the dark wall, with broken stubs and splinters at the
corners where the rails used to be. The top and bottom rails are
still whole, and the bird's tail stays inside the painting. Two
small students crouch below with their hands over their heads, the
wall is plain and dark, and there is no writing anywhere in it.

Before it writes anything, this script proves the picture next to
it is exactly the one the entry was made from, by its length, its
JPEG opening bytes, and its SHA-256. If any of those disagree, it
stops and writes nothing.
"""

import hashlib
import os
import sys
from pathlib import Path

PICTURE = "entry.png"
EXPECTED_LENGTH = 214819
EXPECTED_HASH = "ea0add6982293c05dfea397b590d09a975a5c7c62777887b9c9ee7b05cc0c335"
JPEG_HEAD = b"\xff\xd8\xff"
FALLBACK_DIR = "/output"


def fail(reason):
    """Complain about a picture that does not match, then quit."""
    print(f"picture does not match: {reason}", file=sys.stderr)
    sys.exit(1)


def load_picture():
    """Read entry.png beside this file and check it three ways."""
    folder = Path(__file__).resolve().parent
    data = (folder / PICTURE).read_bytes()

    if data[:3] != JPEG_HEAD:
        fail("entry.png does not open with the JPEG marker")
    if len(data) != EXPECTED_LENGTH:
        fail(f"entry.png is {len(data)} bytes, not {EXPECTED_LENGTH}")
    hashed = hashlib.sha256(data).hexdigest()
    if hashed != EXPECTED_HASH:
        fail(f"entry.png hashes to {hashed}, not {EXPECTED_HASH}")
    return data, hashed


def main():
    picture, hashed = load_picture()
    where = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", FALLBACK_DIR))
    where.mkdir(parents=True, exist_ok=True)
    done = where / PICTURE
    done.write_bytes(picture)
    print(f"wrote {done} ({len(picture)} bytes, sha256 {hashed})")


if __name__ == "__main__":
    main()
