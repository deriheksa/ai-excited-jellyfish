#!/usr/bin/env python3
"""Ship the ai-excited-01 entry picture to the harness output directory.

The bundled picture is entry.png. The name follows the harness
convention; the bytes inside are a JPEG. It shows a phoenix made of
living flame tearing out of a gilt-framed sunrise painting on a
classroom wall. The frame is smashed, splinters and burning feathers
fly in every direction, and four small students below duck under their
desks with their hands over their heads. A chalkboard reads
"Pop Quiz: Myths POSTPONED!".

This script does one guarded job: it reads the bundled picture,
proves it is exactly the picture this entry was built from, and only
then places a copy in the harness output directory under the same
name. The checks are the JPEG opening marker, the exact byte length,
and the exact SHA-256 digest. If any check fails, the script prints
what went wrong, exits with a failure status, and writes nothing.
"""

import hashlib
import os
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
WANT_BYTES = 225418
WANT_SHA256 = "300702fb686884e3846a19dcbc75276c065c6a46800fcd840ee6a210a8ca4bed"
JPEG_MAGIC = b"\xff\xd8\xff"
DEFAULT_OUTPUT = "/output"


def abort(problem):
    """Report a failed check and stop without writing anything."""
    print(f"entry check failed: {problem}", file=sys.stderr)
    raise SystemExit(1)


def checked_picture():
    """Load the bundled picture and prove it is the expected one."""
    here = Path(__file__).resolve().parent
    blob = (here / SOURCE_NAME).read_bytes()

    if len(blob) != WANT_BYTES:
        abort(f"bundled picture is {len(blob)} bytes, expected {WANT_BYTES}")
    if blob[: len(JPEG_MAGIC)] != JPEG_MAGIC:
        abort("bundled picture does not start with the JPEG marker")
    digest = hashlib.sha256(blob).hexdigest()
    if digest != WANT_SHA256:
        abort(f"bundled picture hashes to {digest}, expected {WANT_SHA256}")
    return blob, digest


def main():
    blob, digest = checked_picture()
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / SOURCE_NAME
    target.write_bytes(blob)
    print(f"wrote {target} ({len(blob)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
