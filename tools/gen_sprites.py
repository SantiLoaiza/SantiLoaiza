"""Genera los sprites 8-bit del README como PNG (sin dependencias externas)."""

import os
import struct
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "sprites")
SCALE = 10  # nearest-neighbour: mantiene el borde duro del pixel art

PALETTE = {
    ".": None,
    "K": (0, 0, 0), "W": (255, 255, 255),
    # Mario
    "R": (229, 37, 33), "S": (252, 188, 137), "H": (108, 60, 18),
    "O": (32, 56, 236), "Y": (255, 215, 0),
    # Sonic
    "B": (28, 111, 214), "P": (246, 192, 142),
    # Hercules (colores tomados del sprite del juego de Eurocom)
    "A": (190, 92, 42),    # pelo castano rojizo
    "t": (228, 156, 102),  # piel bronceada
    "u": (94, 47, 27),     # cuero de la coraza y la falda
    "j": (42, 74, 122),    # capa azul
    "G": (212, 160, 23), "N": (74, 42, 24), "L": (198, 204, 214),
    # Enderman / invaders
    "E": (17, 17, 17), "M": (224, 60, 255), "V": (0, 228, 54), "C": (41, 173, 255),
    # Computadores
    "D": (92, 100, 112), "X": (20, 22, 30), "Q": (0, 228, 54),
    "Z": (255, 236, 39), "F": (255, 0, 77),
    # Logos de lenguajes
    "1": (55, 118, 171), "2": (255, 212, 59),   # Python azul / amarillo
    "3": (247, 223, 30), "4": (49, 120, 198),   # JavaScript / TypeScript
    "5": (227, 79, 38), "6": (239, 101, 42),    # HTML5
}

SPRITES = {}

# ------------------------------------------------------------------ personajes
SPRITES["mario"] = """
.....RRRRR......
...RRRRRRRRRRR..
...HHHSSSKS.....
..HSHSSSSKSSS...
..HSHHSSSSKSSS..
..HHSSSSSSHHH...
....SSSSSSSS....
...RRROORRR.....
..RRRRROORRRRR..
.RRRRRROORRRRRR.
.SSRRROOOORRRSS.
.SSSROYOOYORSSS.
.SSSOOOOOOOOSSS.
...OOOO..OOOO...
..HHHH....HHHH..
.HHHHH....HHHHH.
"""

SPRITES["sonic"] = """
.....BB..BBB....
....BBBB.BBBB...
...BBBBBBBBBB...
..BBBWWWWWWBB...
..BBBWKWWKWBB...
..BBBWKWWKWBB...
...BBPPPKPPPB...
....PPPPPPPP....
......BBBB......
..WWBBPPPPBBWW..
..WWBBPPPPBBWW..
.....BBPPBB.....
......BBBB......
.....PP..PP.....
..RRRRR..RRRRR..
..WWWWW..WWWWW..
"""

SPRITES["hercules"] = """
......AAAA........
.....AAAAAA.......
.....AttttA...L...
.....tKttKt...L...
.....tttttt...L...
......tttt....L...
...jjtttttjj..L...
..jjttuuuuttj.L...
..jttuuuuuutt.L...
...ttuuuuuutt.L...
...ttGGGGGGttGGG..
....uuuuuuuu..N...
....uuu..uuu......
.....tt..tt.......
.....tt..tt.......
....NNN..NNN......
"""

SPRITES["enderman"] = """
....EEEEEE....
....EEEEEE....
...EMMEEMME...
....EEEEEE....
...EEEEEEEE...
..EEEEEEEEEE..
..E.EEEEEE.E..
..E.EEEEEE.E..
..E.EEEEEE.E..
..E.EEEEEE.E..
..E..EEEE..E..
.....EEEE.....
.....E..E.....
.....E..E.....
.....E..E.....
....EE..EE....
"""

# ------------------------------------------------------------------- invaders
SPRITES["invader1"] = """
..V.....V..
...V...V...
..VVVVVVV..
.VV.VVV.VV.
VVVVVVVVVVV
V.VVVVVVV.V
V.V.....V.V
...VV.VV...
"""

SPRITES["invader2"] = """
...CC...
..CCCC..
.CCCCCC.
CC.CC.CC
CCCCCCCC
..C..C..
.C.CC.C.
C.C..C.C
"""

# --------------------------------------------------------------- computadores
SPRITES["pc1"] = """
.DDDDDDDDDDDD...
.DXXXXXXXXXXD...
.DXQQQQQQQQXD...
.DXQXXXXXXQXD...
.DXQXQQQQXQXD...
.DXQXXXXXXQXD...
.DXQQQQQQQQXD...
.DXXXXXXXXXXD...
.DDDDDDDDDDDD...
....DDDDDD......
...DDDDDDDD.....
................
.DDDDDDDDDDDDDD.
.DXXXXXXXXXXXXD.
.DDDDDDDDDDDDDD.
................
"""

SPRITES["pc2"] = """
...DDDDDDDDDDDD.
...DXXXXXXXXXXD.
...DXZZZZZZZZXD.
...DXZXXXXXXZXD.
...DXZXFFFFXZXD.
...DXZXXXXXXZXD.
...DXZZZZZZZZXD.
...DXXXXXXXXXXD.
...DDDDDDDDDDDD.
......DDDDDD....
.....DDDDDDDD...
................
.DDDDDDDDDDDDDD.
.DXXXXXXXXXXXXD.
.DDDDDDDDDDDDDD.
................
"""

# ------------------------------------------------------------------- lenguajes
SPRITES["python"] = """
......1111111.......
.....111111111......
....11111111111.....
....11W11111111.....
....11111111111.....
....11111111111.....
....11111111111.....
..111111111111222...
..1111111..2222222..
..1111111..2222222..
..1111111..2222222..
..1111111..2222222..
...11.222222222222..
.....22222222222....
.....22222222222....
.....22222222222....
.....22222222W22....
.....22222222222....
......222222222.....
.......2222222......
"""

SPRITES["js"] = """
33333333333333333333
33333333333333333333
33333333333333333333
33333333333333333333
33333333333333333333
33333333333333333333
33333333333333333333
33333333333333333333
33333333333333333333
33333333333333333333
333333KKK333KKKK3333
33333333K33K33333333
33333333K33K33333333
33333333K333KKK33333
3333K333K333333K3333
3333K333K333333K3333
33333KKK333KKKK33333
33333333333333333333
33333333333333333333
33333333333333333333
"""

SPRITES["ts"] = """
44444444444444444444
44444444444444444444
44444444444444444444
44444444444444444444
44444444444444444444
44444444444444444444
44444444444444444444
44444444444444444444
44444444444444444444
44444444444444444444
4444WWWWW444WWWW4444
444444W4444W44444444
444444W4444W44444444
444444W44444WWW44444
444444W4444444W44444
444444W4444444W44444
444444W4444WWWW44444
44444444444444444444
44444444444444444444
44444444444444444444
"""

SPRITES["html"] = """
55555555555555555555
56666666666666666665
56666666666666666665
56666666666666666665
566666WWWWWWWW666665
566666WW666666666665
566666WW666666666665
566666WWWWWWW6666665
566666666666WW666665
566666666666WW666665
566666W66666WW666665
566666WWWWWWW6666665
56666666666666666665
56666666666666666665
.566666666666666665.
..5666666666666665..
...56666666666665...
....566666666665....
......56666665......
........5555........
"""


def png_bytes(rows_px, w, h):
    raw = b"".join(b"\x00" + b"".join(rows_px[y][x] for x in range(w)) for y in range(h))

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def grid(art):
    rows = [r.rstrip() for r in art.strip("\n").split("\n")]
    width = max(len(r) for r in rows)
    return [r.ljust(width, ".") for r in rows], width, len(rows)


TRANSPARENT = bytes((0, 0, 0, 0))


def build(name, art):
    rows, gw, gh = grid(art)
    w, h = gw * SCALE, gh * SCALE
    out = []
    for y in range(h):
        src = rows[y // SCALE]
        out.append([
            TRANSPARENT if PALETTE[src[x // SCALE]] is None else bytes(PALETTE[src[x // SCALE]] + (255,))
            for x in range(w)
        ])
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name + ".png"), "wb") as f:
        f.write(png_bytes(out, w, h))
    return gw, gh


def preview(names, path, cols=5, cell=20, scale=6):
    """Hoja de contacto para revisar los sprites de un vistazo."""
    rowsn = (len(names) + cols - 1) // cols
    w, h = cols * cell * scale, rowsn * cell * scale
    bg = bytes((29, 43, 83, 255))
    canvas = [[bg for _ in range(w)] for _ in range(h)]
    for i, name in enumerate(names):
        g, gw, gh = grid(SPRITES[name])
        ox = (i % cols) * cell * scale + ((cell - gw) // 2) * scale
        oy = (i // cols) * cell * scale + ((cell - gh) // 2) * scale
        for y in range(gh * scale):
            for x in range(gw * scale):
                color = PALETTE[g[y // scale][x // scale]]
                if color is not None:
                    canvas[oy + y][ox + x] = bytes(color + (255,))
    with open(path, "wb") as f:
        f.write(png_bytes(canvas, w, h))


if __name__ == "__main__":
    for name, art in SPRITES.items():
        gw, gh = build(name, art)
        print(f"{name:10s} {gw:2d}x{gh:2d}")
    preview(list(SPRITES), os.path.join(ROOT, "tools", "_preview.png"))
    preview(["mario", "hercules", "python", "js", "ts", "html"],
            os.path.join(ROOT, "tools", "_preview_big.png"), cols=3, cell=22, scale=12)
    print("preview -> tools/_preview.png")
