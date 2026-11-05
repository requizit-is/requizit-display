# ReQuizit Display

The headline typeface of ReQuizit. One weight, Bold. Latin, Icelandic and Russian Cyrillic.

ReQuizit Display is a modified version of [Bebas Neue](https://github.com/dharmatype/Bebas-Neue) by Ryoichi Tsunekawa (Dharma Type), licensed under the SIL Open Font License 1.1.

## Files

| File | Use |
| --- | --- |
| `fonts/otf/ReQuizitDisplay-Bold.otf` | Desktop apps, print |
| `fonts/webfonts/ReQuizitDisplay-Bold.woff2` | Websites |

## Use on a website

```css
@font-face {
  font-family: "ReQuizit Display";
  src: url("ReQuizitDisplay-Bold.woff2") format("woff2");
  font-weight: 700;
  font-display: swap;
}
```

## Icons

The font draws ReQuizit icons on the code points of fractions and Roman numerals. Text that contains these characters shows the icons.

| Icon | Filled | Outlined |
| --- | --- | --- |
| Blank shield | U+2150 ⅐ | U+2167 Ⅷ |
| Shield 1 | U+2160 Ⅰ | U+2170 ⅰ |
| Shield 5 | U+2161 Ⅱ | U+2171 ⅱ |
| Shield 7 | U+2162 Ⅲ | U+2172 ⅲ |
| Shield 13 | U+2164 Ⅴ | U+2173 ⅳ |
| Shield 42 | U+2165 Ⅵ | U+2174 ⅴ |
| Shield 80 | U+2166 Ⅶ | U+2175 ⅵ |
| Shield 99 | U+2176 ⅶ | U+2180 ↀ |
| Shield 100 | U+2177 ⅷ | U+2181 ↁ |
| Shield 146 | U+2178 ⅸ | U+2182 ↂ |
| Shield 160 | U+2179 ⅹ | U+2183 Ↄ |
| Brain apple | U+2159 ⅙ | |

## Build

Requires [uv](https://docs.astral.sh/uv/).

```sh
uv run python build.py   # writes fonts/
uv run pytest            # checks the names, license fields and glyphs
```

The build takes `sources/BebasNeue_Bold_REQUIZIT_2025.otf`, gives it the ReQuizit Display names, adds the numero sign № (drawn from N and º) and writes the files in `fonts/`. It does not change the glyphs of the source. To change a glyph, edit the source file in a font editor, then rebuild and record the change in `FONTLOG.txt`.

## Credits and license

- Bebas Neue: Ryoichi Tsunekawa, [Dharma Type](http://dharmatype.com). The 2014 edition this font starts from was published with [Fontfabric](https://www.fontfabric.com).
- Changes for ReQuizit: Igor Churmeev.

Licensed under the SIL Open Font License 1.1, see [OFL.txt](OFL.txt). The change history is in [FONTLOG.txt](FONTLOG.txt).

Bebas Neue is a trademark of Dharma Type. ReQuizit Display is not affiliated with or endorsed by Dharma Type.
