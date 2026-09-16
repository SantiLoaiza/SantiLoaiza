"""Utilidad minima para leer/recortar PNG sin dependencias (solo para consultar referencias)."""

import struct
import sys
import zlib


def read_png(path):
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    pos, idat, plte, trns, ihdr = 8, [], None, None, None
    while pos < len(data):
        ln = struct.unpack(">I", data[pos:pos + 4])[0]
        tag = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + ln]
        if tag == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", body)
        elif tag == b"IDAT":
            idat.append(body)
        elif tag == b"PLTE":
            plte = body
        elif tag == b"tRNS":
            trns = body
        pos += 12 + ln

    w, h, depth, ctype, _, _, interlace = ihdr
    assert depth == 8 and interlace == 0, f"no soportado: depth={depth} interlace={interlace}"
    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ctype]
    raw = zlib.decompress(b"".join(idat))

    stride = w * channels
    out, prev = [], bytearray(stride)
    p = 0
    for _ in range(h):
        f = raw[p]; p += 1
        line = bytearray(raw[p:p + stride]); p += stride
        for i in range(stride):
            a = line[i - channels] if i >= channels else 0
            b = prev[i]
            c = prev[i - channels] if i >= channels else 0
            if f == 1:
                line[i] = (line[i] + a) & 255
            elif f == 2:
                line[i] = (line[i] + b) & 255
            elif f == 3:
                line[i] = (line[i] + (a + b) // 2) & 255
            elif f == 4:
                pp = a + b - c
                pa, pb, pc = abs(pp - a), abs(pp - b), abs(pp - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        out.append(line)
        prev = line

    px = []
    for line in out:
        row = []
        for x in range(w):
            v = line[x * channels:(x + 1) * channels]
            if ctype == 6:
                row.append(tuple(v))
            elif ctype == 2:
                row.append((v[0], v[1], v[2], 255))
            elif ctype == 3:
                i = v[0]
                a = trns[i] if trns and i < len(trns) else 255
                row.append((plte[i * 3], plte[i * 3 + 1], plte[i * 3 + 2], a))
            elif ctype == 0:
                row.append((v[0], v[0], v[0], 255))
            else:
                row.append((v[0], v[0], v[0], v[1]))
        px.append(row)
    return px, w, h


def write_png(px, path, bg=(25, 25, 40)):
    h, w = len(px), len(px[0])
    raw = bytearray()
    for row in px:
        raw.append(0)
        for r, g, b, a in row:
            if a < 128:
                r, g, b = bg
            raw += bytes((r, g, b, 255))

    def chunk(tag, body):
        c = tag + body
        return struct.pack(">I", len(body)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    open(path, "wb").write(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(raw), 6))
        + chunk(b"IEND", b"")
    )


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    px, w, h = read_png(src)
    print("size", w, h)
    if len(sys.argv) > 3:  # crop x y cw ch [step]
        x, y, cw, ch = map(int, sys.argv[3:7])
        step = int(sys.argv[7]) if len(sys.argv) > 7 else 1
        if step > 0:
            px = [[px[j][i] for i in range(x, min(x + cw, w), step)]
                  for j in range(y, min(y + ch, h), step)]
        else:  # step negativo = ampliar
            z = -step
            crop = [[px[j][i] for i in range(x, min(x + cw, w))]
                    for j in range(y, min(y + ch, h))]
            px = [[row[i // z] for i in range(len(row) * z)] for row in crop for _ in range(z)]
    write_png(px, dst)
    print("out", len(px[0]), len(px))
