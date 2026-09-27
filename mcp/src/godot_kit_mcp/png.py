"""Minimal RGBA PNG encoder/decoder (stdlib only). Enough for greybox art."""

import struct
import zlib

SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _chunk(tag: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


def encode_png(width: int, height: int, rgba: bytes | bytearray) -> bytes:
    if len(rgba) != width * height * 4:
        raise ValueError(f"expected {width * height * 4} bytes of RGBA, got {len(rgba)}")
    stride = width * 4
    raw = b"".join(b"\x00" + bytes(rgba[y * stride:(y + 1) * stride]) for y in range(height))
    header = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return SIGNATURE + _chunk(b"IHDR", header) + _chunk(b"IDAT", zlib.compress(raw, 9)) + _chunk(b"IEND", b"")


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def _unfilter(raw: bytes, height: int, stride: int, bpp: int) -> bytearray:
    out = bytearray(height * stride)
    prev = bytes(stride)
    pos = 0
    for y in range(height):
        filt = raw[pos]
        pos += 1
        line = bytearray(raw[pos:pos + stride])
        pos += stride
        for i in range(len(line)):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if filt == 1:
                line[i] = (line[i] + a) & 0xFF
            elif filt == 2:
                line[i] = (line[i] + b) & 0xFF
            elif filt == 3:
                line[i] = (line[i] + (a + b) // 2) & 0xFF
            elif filt == 4:
                line[i] = (line[i] + _paeth(a, b, c)) & 0xFF
            elif filt not in (0,):
                raise ValueError(f"unsupported PNG filter type {filt}")
        out[y * stride:(y + 1) * stride] = line
        prev = line
    return out


def decode_png(data: bytes) -> tuple[int, int, bytes]:
    if not data.startswith(SIGNATURE):
        raise ValueError("not a PNG")
    pos, width, height, idat, color_type = len(SIGNATURE), 0, 0, b"", 6
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        tag, body = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + length]
        if tag == b"IHDR":
            width, height = struct.unpack(">II", body[:8])
            color_type = body[9]
        elif tag == b"IDAT":
            idat += body
        pos += 12 + length
    channels = {2: 3, 6: 4}.get(color_type)
    if channels is None:
        raise ValueError(f"unsupported PNG color type {color_type}")
    stride = width * channels
    raw = _unfilter(zlib.decompress(idat), height, stride, channels)
    if channels == 4:
        return width, height, bytes(raw)
    out = bytearray(width * height * 4)
    for i in range(width * height):
        out[i * 4:i * 4 + 3] = raw[i * 3:i * 3 + 3]
        out[i * 4 + 3] = 255
    return width, height, bytes(out)
