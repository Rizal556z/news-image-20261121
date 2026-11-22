#!/usr/bin/env python3
"""Ship the Saturday 21 November 2026 news poster.

The poster itself lives in this folder as entry.png (drawn by
draw_poster.py). This entrypoint checks that the file is a real
1024x1024 JPEG, then places an exact copy at
$MAKEFUN_OUTPUT_DIR/entry.png (default: ./out/entry.png).

Pure standard library, no network, no randomness: the same input
always produces the same output bytes.
"""
import hashlib
import os
import struct
import sys

POSTER_NAME = "entry.png"
WANT_WIDTH = 1024
WANT_HEIGHT = 1024


def poster_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, POSTER_NAME)


def output_dir():
    for flag in sys.argv[1:]:
        if flag.startswith("--out="):
            return flag[len("--out="):]
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "out")


def read_jpeg_size(blob):
    """Return (width, height) by walking the JPEG marker segments."""
    if blob[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG: missing SOI marker")
    if blob[-2:] != b"\xff\xd9":
        raise ValueError("not a JPEG: missing EOI marker")
    pos = 2
    while pos + 4 <= len(blob):
        if blob[pos] != 0xFF:
            raise ValueError("corrupt JPEG marker at offset %d" % pos)
        marker = blob[pos + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        size = struct.unpack(">H", blob[pos + 2:pos + 4])[0]
        if size < 2 or pos + 2 + size > len(blob):
            raise ValueError("corrupt JPEG segment at offset %d" % pos)
        if marker == 0xC0:
            height, width = struct.unpack(">HH", blob[pos + 5:pos + 9])
            return width, height
        pos += 2 + size
    raise ValueError("no SOF0 segment found in JPEG")


def check_poster(blob):
    width, height = read_jpeg_size(blob)
    if (width, height) != (WANT_WIDTH, WANT_HEIGHT):
        raise ValueError(
            "poster is %dx%d, expected %dx%d"
            % (width, height, WANT_WIDTH, WANT_HEIGHT)
        )
    if len(blob) < 50000:
        raise ValueError("poster suspiciously small: %d bytes" % len(blob))


def place_copy(blob, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, POSTER_NAME)
    with open(dest, "wb") as fh:
        fh.write(blob)
    os.chmod(dest, 0o644)
    return dest


def run():
    with open(poster_path(), "rb") as fh:
        blob = fh.read()
    check_poster(blob)
    digest = hashlib.sha256(blob).hexdigest()
    dest = place_copy(blob, output_dir())
    with open(dest, "rb") as fh:
        again = fh.read()
    if hashlib.sha256(again).hexdigest() != digest:
        raise ValueError("copy mismatch: digest changed after write")
    print("entry.png: sha256 %s (%d bytes) -> %s" % (digest, len(blob), dest))
    return 0


def main():
    try:
        return run()
    except (OSError, ValueError) as err:
        print("main.py: %s" % err, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
