#!/usr/bin/env python3
"""ai-excited-01 entry: deliver the jellyfish image to /output/entry.png.

The picture is baked into this repo as entry.png. It is a JPEG by its
first bytes (the name stays entry.png, per the rules): a giant glowing
glass jellyfish floating low over terraced rice fields at dusk, tiny
farmers looking up from below.

This program does one job and nothing else. It reads entry.png, proves
it is exactly the file we built — right magic bytes, right byte count,
right SHA-256 — and then copies it, untouched, to the output directory
the harness reads. If any of those checks fails it stops loudly instead
of writing a wrong file.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

EXPECTED_BYTES = 231036
EXPECTED_SHA256 = "90d935bb259f8fd8157971cdb6e816b25d0beac29d2039598bed9402abc2e019"
JPEG_SOI = b"\xff\xd8\xff"


def fail(message):
    print(f"entry check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    source = os.path.join(HERE, "entry.png")
    with open(source, "rb") as handle:
        blob = handle.read()
    if blob[:3] != JPEG_SOI:
        fail("entry.png does not start with the JPEG magic bytes")
    if len(blob) != EXPECTED_BYTES:
        fail(f"entry.png is {len(blob)} bytes, expected {EXPECTED_BYTES}")
    digest = hashlib.sha256(blob).hexdigest()
    if digest != EXPECTED_SHA256:
        fail(f"entry.png sha256 {digest} does not match {EXPECTED_SHA256}")
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(source, target)
    print(f"wrote {target} ({len(blob)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
