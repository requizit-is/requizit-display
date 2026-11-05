"""Build ReQuizit Display from the REQUIZIT 2025 edition of Bebas Neue Bold."""

from pathlib import Path

from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).parent
SOURCE = ROOT / "sources" / "BebasNeue_Bold_REQUIZIT_2025.otf"
OUT = ROOT / "fonts"

FAMILY = "ReQuizit Display"
STYLE = "Bold"
PS_NAME = "ReQuizitDisplay-Bold"
VERSION = "1.001"
VENDOR = "REQZ"
OFL_URL = "https://openfontlicense.org"
NUMERO = "uni2116"
# How far the raised o of № moves into the right side bearing of the N.
NUMERO_TUCK = 20

COPYRIGHT = (
    "Copyright (c) 2010 by Ryoichi Tsunekawa. All rights reserved. "
    "Modifications copyright 2025 Igor Churmeev (ReQuizit)."
)
TRADEMARK = "Bebas Neue is a trademark of Dharma Type."

NAMES = {
    0: COPYRIGHT,
    1: FAMILY,
    2: STYLE,
    3: f"{VERSION};{VENDOR};{PS_NAME}",
    4: f"{FAMILY} {STYLE}",
    5: f"Version {VERSION}",
    6: PS_NAME,
    7: TRADEMARK,
    8: "ReQuizit",
    9: "Ryoichi Tsunekawa; Igor Churmeev",
    10: (
        "Based on Bebas Neue Bold by Ryoichi Tsunekawa (Dharma Type), 2014 edition, "
        "with ReQuizit icons and the numero sign added and Cyrillic U redrawn."
    ),
    11: "https://github.com/requizit-is/requizit-display",
    12: "http://dharmatype.com",
    13: (
        "This Font Software is licensed under the SIL Open Font License, Version 1.1. "
        f"This license is available with a FAQ at: {OFL_URL}"
    ),
    14: OFL_URL,
}


def rename(font: TTFont) -> None:
    name = font["name"]
    name.names = []
    for name_id, text in NAMES.items():
        name.setName(text, name_id, 3, 1, 0x409)

    cff = font["CFF "].cff
    cff.fontNames = [PS_NAME]
    top = cff.topDictIndex[0]
    top.FamilyName = FAMILY
    top.FullName = f"{FAMILY} {STYLE}"
    top.version = VERSION
    top.Copyright = COPYRIGHT
    top.Notice = TRADEMARK

    font["OS/2"].achVendID = VENDOR
    font["OS/2"].fsType = 0
    font["head"].fontRevision = float(VERSION)
    if "DSIG" in font:
        del font["DSIG"]


def add_numero(font: TTFont) -> None:
    """Draws № from N and the raised o with its bar (º)."""
    glyphs = font.getGlyphSet()
    hmtx = font["hmtx"]
    shift = hmtx["N"][0] - NUMERO_TUCK
    width = shift + hmtx["ordmasculine"][0]
    pen = T2CharStringPen(width, glyphs)
    glyphs["N"].draw(pen)
    glyphs["ordmasculine"].draw(TransformPen(pen, (1, 0, 0, 1, shift, 0)))

    top = font["CFF "].cff.topDictIndex[0]
    strings = top.CharStrings
    strings.charStringsIndex.append(pen.getCharString(private=top.Private, globalSubrs=top.GlobalSubrs))
    strings.charStrings[NUMERO] = len(strings.charStringsIndex) - 1
    order = [*font.getGlyphOrder(), NUMERO]
    top.charset = order
    font.setGlyphOrder(order)
    font["maxp"].numGlyphs += 1
    hmtx[NUMERO] = (width, hmtx["N"][1])
    for table in font["cmap"].tables:
        if table.isUnicode():
            table.cmap[0x2116] = NUMERO


def build(source: Path = SOURCE, out: Path = OUT) -> dict[str, Path]:
    font = TTFont(source)
    rename(font)
    add_numero(font)
    paths = {
        "otf": out / "otf" / f"{PS_NAME}.otf",
        "woff2": out / "webfonts" / f"{PS_NAME}.woff2",
    }
    for flavor, path in paths.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        font.flavor = "woff2" if flavor == "woff2" else None
        font.save(path)
    return paths


if __name__ == "__main__":
    for path in build().values():
        print(path.relative_to(ROOT))
