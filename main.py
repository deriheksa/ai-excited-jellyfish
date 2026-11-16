#!/usr/bin/env python3
"""Deliver the ai-excited-01 picture to the harness output directory.

The artwork lives in this repository as entry.png. Although the name
ends in .png, the bytes are a JPEG (see the leading marker below). The
scene: a huge translucent jellyfish smashing up through the surface of
a flooded rice terrace at dusk, spray and droplets flying everywhere,
while five small farmers underneath throw their arms in the air.

This script is deliberately boring. It loads the bundled picture,
checks that it is bit-for-bit the picture we built — correct opening
bytes, correct length, correct SHA-256 fingerprint — and only then
writes those exact bytes out as /output/entry.png. Anything unexpected
about the bundled file makes the script abort with an error instead of
handing the harness a wrong or damaged image.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

# Facts about the picture bundled in this repository.
PICTURE_NAME = "entry.png"
PICTURE_SIZE = 201933
PICTURE_SHA256 = "3867c080df3e8ab741dd92d78d3054617394fa2cc60d1ddb10f335d0e9157941"
JPEG_START = bytes((0xFF, 0xD8, 0xFF))
FALLBACK_OUTPUT_DIR = "/output"


class PictureMismatch(Exception):
    """The bundled picture is not the exact file this entry is built on."""


def load_picture() -> bytes:
    """Read the bundled picture next to this script."""
    picture_path = Path(__file__).resolve().parent / PICTURE_NAME
    try:
        return picture_path.read_bytes()
    except OSError as exc:
        raise PictureMismatch(f"could not read {picture_path}: {exc}") from exc


def check_picture(data: bytes) -> str:
    """Confirm the picture is the exact one we expect; return its hash."""
    if data[:3] != JPEG_START:
        raise PictureMismatch("picture does not begin with the JPEG marker")
    if len(data) != PICTURE_SIZE:
        raise PictureMismatch(
            f"picture is {len(data)} bytes, but {PICTURE_SIZE} were expected"
        )
    fingerprint = hashlib.sha256(data).hexdigest()
    if fingerprint != PICTURE_SHA256:
        raise PictureMismatch(
            f"picture sha256 {fingerprint} does not match {PICTURE_SHA256}"
        )
    return fingerprint


def write_picture(data: bytes) -> Path:
    """Write the checked bytes to the harness output directory."""
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", FALLBACK_OUTPUT_DIR))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / PICTURE_NAME
    out_path.write_bytes(data)
    return out_path


def run() -> int:
    try:
        data = load_picture()
        fingerprint = check_picture(data)
        out_path = write_picture(data)
    except PictureMismatch as exc:
        print(f"entry check failed: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {out_path} ({len(data)} bytes, sha256 {fingerprint})")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
