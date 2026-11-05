"""Build ReQuizit Display from the REQUIZIT 2025 edition of Bebas Neue Bold."""

from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).parent
SOURCE = ROOT / "sources" / "BebasNeue_Bold_REQUIZIT_2025.otf"
OUT = ROOT / "fonts"

FAMILY = "ReQuizit Display"
STYLE = "Bold"
PS_NAME = "ReQuizitDisplay-Bold"
VERSION = "1.000"
VENDOR = "REQZ"
OFL_URL = "https://openfontlicense.org"

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
        "with ReQuizit icons added and Cyrillic U redrawn."
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


def build(source: Path = SOURCE, out: Path = OUT) -> dict[str, Path]:
    font = TTFont(source)
    rename(font)
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
