import pytest
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

from build import SOURCE, build

# Name IDs allowed to mention the original: trademark notice and description (credit).
CREDIT_IDS = {7, 10}


@pytest.fixture(scope="module")
def paths(tmp_path_factory):
    return build(out=tmp_path_factory.mktemp("fonts"))


@pytest.fixture(scope="module", params=["otf", "woff2"])
def font(request, paths):
    return TTFont(paths[request.param])


def names(font):
    return {r.nameID: str(r) for r in font["name"].names}


def outlines(font):
    glyphs = font.getGlyphSet()
    result = {}
    for name in font.getGlyphOrder():
        pen = RecordingPen()
        glyphs[name].draw(pen)
        result[name] = pen.value
    return result


def test_writes_otf_and_woff2(paths):
    assert paths["otf"].name == "ReQuizitDisplay-Bold.otf"
    assert paths["woff2"].name == "ReQuizitDisplay-Bold.woff2"
    assert TTFont(paths["otf"]).flavor is None
    assert TTFont(paths["woff2"]).flavor == "woff2"


def test_family_and_style_names(font):
    n = names(font)
    assert n[1] == "ReQuizit Display"
    assert n[2] == "Bold"
    assert n[3] == "1.001;REQZ;ReQuizitDisplay-Bold"
    assert n[4] == "ReQuizit Display Bold"
    assert n[5] == "Version 1.001"
    assert n[6] == "ReQuizitDisplay-Bold"


def test_names_drop_the_original_family_name(font):
    for r in font["name"].names:
        if r.nameID not in CREDIT_IDS:
            assert "Bebas" not in str(r), r.nameID
            assert "REQUIZIT 2025" not in str(r), r.nameID


def test_cff_names_match_the_name_table(font):
    cff = font["CFF "].cff
    top = cff.topDictIndex[0]
    assert cff.fontNames == ["ReQuizitDisplay-Bold"]
    assert top.FamilyName == "ReQuizit Display"
    assert top.FullName == "ReQuizit Display Bold"
    assert top.version == "1.001"
    assert top.Copyright == names(font)[0]
    assert top.Notice == names(font)[7]


def test_copyright_keeps_the_original_notice_and_adds_the_changes(font):
    assert names(font)[0] == (
        "Copyright (c) 2010 by Ryoichi Tsunekawa. All rights reserved. "
        "Modifications copyright 2025 Igor Churmeev (ReQuizit)."
    )


def test_credits_the_original_design(font):
    n = names(font)
    assert n[7] == "Bebas Neue is a trademark of Dharma Type."
    assert n[8] == "ReQuizit"
    assert n[9] == "Ryoichi Tsunekawa; Igor Churmeev"
    assert "Bebas Neue Bold by Ryoichi Tsunekawa (Dharma Type)" in n[10]
    assert n[11] == "https://github.com/requizit-is/requizit-display"
    assert n[12] == "http://dharmatype.com"


def test_license_fields_point_to_the_ofl(font):
    n = names(font)
    assert n[13] == (
        "This Font Software is licensed under the SIL Open Font License, Version 1.1. "
        "This license is available with a FAQ at: https://openfontlicense.org"
    )
    assert n[14] == "https://openfontlicense.org"


def test_metadata_no_longer_claims_the_original_vendor(font):
    assert font["OS/2"].achVendID == "REQZ"
    assert font["head"].fontRevision == pytest.approx(1.001, abs=1 / 65536)  # 16.16 fixed point
    assert "DSIG" not in font


def test_allows_installable_embedding(font):
    assert font["OS/2"].fsType == 0


def test_keeps_bold_style_bits(font):
    assert font["OS/2"].usWeightClass == 700
    assert font["head"].macStyle & 1


def test_keeps_every_glyph_of_the_source(font):
    source = TTFont(SOURCE)
    assert font.getBestCmap() == {**source.getBestCmap(), 0x2116: "uni2116"}
    built = outlines(font)
    assert {name: built[name] for name in source.getGlyphOrder()} == outlines(source)


def test_draws_numero_from_n_and_the_raised_o(font):
    glyphs = font.getGlyphSet()
    hmtx = font["hmtx"]
    width, lsb = hmtx["uni2116"]
    shift = width - hmtx["ordmasculine"][0]
    assert hmtx["N"][0] - 40 <= shift <= hmtx["N"][0]
    assert lsb == hmtx["N"][1]
    expected = RecordingPen()
    glyphs["N"].draw(expected)
    glyphs["ordmasculine"].draw(TransformPen(expected, (1, 0, 0, 1, shift, 0)))
    actual = RecordingPen()
    glyphs["uni2116"].draw(actual)
    assert actual.value == expected.value
