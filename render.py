#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news poster used as entry.png.

Everything on the page is drawn with Pillow primitives: the icons, the map,
the type and the rules. No downloaded pictures, no network, no copied layout.
The story list below is the researched news index; sources are named beside
the lead items and in the footer legend.
"""

from __future__ import annotations

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = "#F6F2E8"
INK = "#152238"
RED = "#C5332B"
NAVY = "#132943"
GREEN = "#2C7A5B"
GOLD = "#D9A12B"
MUTED = "#6A7382"
LINE = "#C9C6BA"
PALE = "#E8E3D5"
WHITE = "#FFFFFF"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")

_cache: dict[tuple[int, bool, bool], ImageFont.FreeTypeFont] = {}


def f(size: int, bold: bool = False, serif: bool = False) -> ImageFont.FreeTypeFont:
    key = (size, bold, serif)
    if key not in _cache:
        path = SERIF if serif else (BOLD if bold else REG)
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def tw(d: ImageDraw.ImageDraw, s: str, font: ImageFont.FreeTypeFont) -> int:
    box = d.textbbox((0, 0), s, font=font)
    return box[2] - box[0]


def wrap(d: ImageDraw.ImageDraw, s: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    for para in s.split("\n"):
        current = ""
        for word in para.split():
            trial = (current + " " + word).strip()
            if current and tw(d, trial, font) > width:
                lines.append(current)
                current = word
            else:
                current = trial
        if current:
            lines.append(current)
    return lines


def para(
    d: ImageDraw.ImageDraw,
    x: int,
    y: int,
    s: str,
    font: ImageFont.FreeTypeFont,
    fill: str,
    width: int,
    gap: int = 3,
    max_lines: int | None = None,
) -> int:
    lines = wrap(d, s, font, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    yy = y
    for line in lines:
        d.text((x, yy), line, font=font, fill=fill)
        yy += font.size + gap
    return yy


def stars(d: ImageDraw.ImageDraw, cx: int, cy: int, r: int, n: int, fill: str) -> None:
    import math

    pts = []
    for i in range(n * 2):
        a = -math.pi / 2 + i * math.pi / n
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=fill)


def balloon(d: ImageDraw.ImageDraw, x: int, y: int, accent: str = GOLD) -> None:
    d.ellipse((x, y, x + 62, y + 46), fill=accent, outline=INK, width=2)
    d.polygon([(x + 31, y + 46), (x + 25, y + 52), (x + 37, y + 52)], fill=accent)
    d.line((x + 31, y + 52, x + 29, y + 74), fill=INK, width=2)
    d.text((x + 7, y + 10), "100", font=f(20, True, True), fill=WHITE)
    for dx in (8, 26, 44):
        d.line((x + dx, y - 12, x + dx - 4, y - 2), fill=MUTED, width=2)
    d.arc((x + 2, y - 18, x + 56, y + 4), 190, 350, fill=MUTED, width=3)


def candle(d: ImageDraw.ImageDraw, x: int, y: int) -> None:
    d.rectangle((x + 18, y + 32, x + 46, y + 74), fill=WHITE, outline=INK, width=2)
    d.line((x + 32, y + 22, x + 32, y + 32), fill=INK, width=2)
    d.polygon([(x + 32, y + 2), (x + 42, y + 24), (x + 32, y + 30), (x + 22, y + 24)], fill=GOLD)
    d.line((x + 8, y + 76, x + 56, y + 76), fill=INK, width=2)


def chessboard(d: ImageDraw.ImageDraw, x: int, y: int) -> None:
    s = 11
    for r in range(6):
        for c in range(6):
            if (r + c) % 2 == 0:
                d.rectangle((x + c * s, y + r * s, x + (c + 1) * s, y + (r + 1) * s), fill=INK)
    d.rectangle((x, y, x + 66, y + 66), outline=INK, width=2)
    for px, col in ((x + 20, WHITE), (x + 46, INK)):
        d.ellipse((px - 8, y + 26, px + 8, y + 42), fill=col, outline=INK, width=1)
        d.rectangle((px - 5, y + 42, px + 5, y + 54), fill=col, outline=INK, width=1)
        d.polygon([(px - 9, y + 28), (px, y + 12), (px + 9, y + 28)], fill=col, outline=INK)


def tariff(d: ImageDraw.ImageDraw, x: int, y: int) -> None:
    d.line((x + 4, y + 70, x + 74, y + 70), fill=INK, width=2)
    for i, h in enumerate((22, 38, 54, 66)):
        d.rectangle((x + 8 + i * 16, y + 70 - h, x + 20 + i * 16, y + 70), fill=RED if i > 1 else MUTED)
    d.line((x + 6, y + 12, x + 72, y + 52), fill=NAVY, width=3)
    d.polygon([(x + 72, y + 52), (x + 60, y + 49), (x + 68, y + 40)], fill=NAVY)
    d.text((x + 4, y - 4), "14", font=f(17, True), fill=RED)


def flame(d: ImageDraw.ImageDraw, x: int, y: int, color: str = RED) -> None:
    d.polygon([(x + 28, y), (x + 46, y + 30), (x + 38, y + 48), (x + 52, y + 42),
               (x + 44, y + 72), (x + 10, y + 72), (x + 6, y + 40)], fill=color, outline=INK)
    d.polygon([(x + 28, y + 34), (x + 38, y + 56), (x + 18, y + 56)], fill=GOLD)


def tanker(d: ImageDraw.ImageDraw, x: int, y: int) -> None:
    flame(d, x + 36, y - 4)
    d.rounded_rectangle((x + 2, y + 40, x + 68, y + 64), radius=5, fill=MUTED, outline=INK, width=2)
    d.rectangle((x + 46, y + 30, x + 62, y + 42), fill=NAVY)
    for dx in (16, 34, 52):
        d.ellipse((x + dx - 5, y + 60, x + dx + 5, y + 70), fill=INK)


def refinery(d: ImageDraw.ImageDraw, x: int, y: int) -> None:
    for dx, h in ((6, 40), (26, 58), (48, 46)):
        d.rectangle((x + dx, y + 72 - h, x + dx + 14, y + 72), fill=MUTED, outline=INK, width=1)
        d.line((x + dx + 3, y + 74 - h, x + dx + 11, y + 74 - h), fill=INK, width=2)
    flame(d, x + 24, y - 10)
    d.line((x + 2, y + 74, x + 68, y + 74), fill=INK, width=2)
    d.ellipse((x + 56, y - 6, x + 68, y + 6), fill=NAVY)
    d.line((x + 44, y + 2, x + 56, y), fill=NAVY, width=2)


def eu_icon(d: ImageDraw.ImageDraw, x: int, y: int) -> None:
    d.ellipse((x + 4, y + 8, x + 72, y + 76), fill=NAVY)
    for i in range(12):
        a = i * 3.14159 / 6
        stars(d, int(x + 38 + 22 * __import__("math").cos(a)),
              int(y + 42 + 22 * __import__("math").sin(a)), 4, 5, GOLD)


def factory(d: ImageDraw.ImageDraw, x: int, y: int) -> None:
    d.polygon([(x + 4, y + 72), (x + 4, y + 38), (x + 24, y + 52),
               (x + 24, y + 38), (x + 44, y + 52), (x + 44, y + 32),
               (x + 68, y + 46), (x + 68, y + 72)], fill=MUTED, outline=INK)
    d.line((x + 8, y + 22, x + 56, y + 22), fill=GREEN, width=4)
    d.polygon([(x + 56, y + 14), (x + 70, y + 22), (x + 56, y + 30)], fill=GREEN)
    d.text((x + 8, y + 54), "+36%", font=f(11, True), fill=WHITE)


def station(d: ImageDraw.ImageDraw, x: int, y: int) -> None:
    d.rectangle((x + 26, y + 26, x + 50, y + 50), fill=NAVY, outline=INK, width=2)
    d.rectangle((x + 4, y + 32, x + 26, y + 44), fill=GOLD, outline=INK, width=1)
    d.rectangle((x + 50, y + 32, x + 72, y + 44), fill=GOLD, outline=INK, width=1)
    for dx in (10, 16, 54, 60):
        d.line((x + dx, y + 34, x + dx, y + 42), fill=INK, width=1)
    d.line((x + 38, y + 26, x + 38, y + 10), fill=INK, width=2)
    d.ellipse((x + 34, y + 4, x + 42, y + 12), fill=RED)


def map_shape(d: ImageDraw.ImageDraw, bx: int, by: int, bw: int, bh: int) -> None:
    continents = [
        [(0.03, 0.14), (0.10, 0.07), (0.21, 0.08), (0.28, 0.14), (0.25, 0.27),
         (0.18, 0.32), (0.16, 0.45), (0.09, 0.35), (0.05, 0.26)],
        [(0.21, 0.48), (0.30, 0.46), (0.32, 0.60), (0.26, 0.88), (0.20, 0.75), (0.18, 0.58)],
        [(0.44, 0.18), (0.53, 0.13), (0.57, 0.20), (0.52, 0.30), (0.44, 0.28)],
        [(0.45, 0.34), (0.56, 0.32), (0.60, 0.48), (0.54, 0.68), (0.48, 0.60), (0.43, 0.44)],
        [(0.58, 0.12), (0.85, 0.09), (0.94, 0.24), (0.84, 0.37), (0.70, 0.43), (0.60, 0.32)],
        [(0.81, 0.63), (0.91, 0.60), (0.94, 0.72), (0.84, 0.76)],
    ]
    for poly in continents:
        pts = [(bx + int(px * bw), by + int(py * bh)) for px, py in poly]
        d.polygon(pts, fill="#D8D2C0", outline=MUTED)
    pins = [
        (0.16, 0.25, "1"), (0.52, 0.40, "2"), (0.70, 0.22, "3"),
        (0.50, 0.23, "4"), (0.69, 0.44, "5"), (0.86, 0.28, "6"),
        (0.54, 0.39, "7"), (0.59, 0.43, "8"), (0.88, 0.69, "9"),
    ]
    for px, py, num in pins:
        cx, cy = bx + int(px * bw), by + int(py * bh)
        d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=RED, outline=WHITE, width=2)
        d.text((cx, cy), num, font=f(10, True), fill=WHITE, anchor="mm")


LEADS = [
    {
        "n": "1", "region": "USA · NEW YORK", "tag": "CONFIRMED",
        "title": "Macy's 100th parade\nmoved to Saturday",
        "sub": "Gusts up to 60 mph and storm warnings force the first weather delay in a century.",
        "source": "AP · AL JAZEERA · FRANCE 24", "icon": balloon, "bg": "#F0E6D2",
    },
    {
        "n": "2", "region": "INDIA · MUMBAI", "tag": "ANNIVERSARY",
        "title": "18 years since the\n26/11 Mumbai attacks",
        "sub": "Candles and a pledge ceremony at the Gateway of India; 166 killed in 2008.",
        "source": "PIB · PTI · DD NEWS", "icon": candle, "bg": "#E9DCD5",
    },
    {
        "n": "3", "region": "WORLD · CHESS", "tag": "LIVE TODAY",
        "title": "Gukesh–Sindarov\nGame 3 in Geneva",
        "sub": "World Championship match stays finely balanced after two drawn openers.",
        "source": "FIDE · WORLD CHESS", "icon": chessboard, "bg": "#DFE6E8",
    },
]

SECONDARY = [
    ("WORLD TRADE", "Trump tariffs target 14 partners", tariff, "#EAD8D2"),
    ("EGYPT", "31 dead in Cairo tanker fire", tanker, "#F0DED4"),
    ("UKRAINE · RUSSIA", "Two Samara refineries ablaze", refinery, "#E5DED6"),
    ("EUROPE · BRUSSELS", "EU leaders open budget, Ukraine talks", eu_icon, "#DFE3E8"),
    ("BANGLADESH", "Garment wages rise 36%", factory, "#E5E9D8"),
    ("CHINA · SPACE", "First foreigner aboard Tiangong", station, "#DAE2E9"),
]

NUMBERS = [
    ("100", "years of Macy's parade"),
    ("31", "killed near Cairo"),
    ("36%", "Bangladesh wage rise"),
    ("14", "economies face new tariffs"),
    ("18", "years since 26/11"),
]

UTC = [
    "00:30  Cairo tanker fire reported",
    "05:00  India remembers 26/11",
    "09:00  EU summit opens, Brussels",
    "13:00  Students march in Paris",
    "13:30  Parade moved in New York",
    "14:00  Chess Game 3, Geneva",
    "20:00  US tariff plan detailed",
]

DATE_CHECK = [
    "25 Nov — first Cairo reports; toll rose today",
    "25 Nov — Bangladesh protests; raise announced today",
    "25 Nov — Shenzhou-24 launch; docking reported today",
    "24 Nov — chess Game 2 draw; Game 3 is today",
    "2008 — Mumbai attacks; today is the memorial",
]

BRIEFS = [
    "10  Court blocks Trump birthright curbs",
    "11  Fed sees prices, wages rising",
    "12  King tides bring flood warnings",
    "13  EU budget, Ukraine aid talks open",
    "14  Paris students march on campus budget",
    "15  US clears F-16 gear for Kyiv",
    "16  Gaza aid guards accused of live fire",
    "17  Houthis close in on Aden",
    "18  Belgium split over Iran hack claim",
    "19  Bangladesh sets Tk 17,000 wage floor",
    "20  India urges human control of arms",
    "21  First Pakistani astronaut on Tiangong",
    "22  Australia inflation hits 4.9%",
    "23  Virgin staff strike at 4 airports",
    "24  Kospi leads Asian share rebound",
    "25  China rejects overcapacity claim",
    "26  Tokyo chips shift after China rule",
    "27  Brazil tightens household debt rules",
    "28  76 hostages freed in Bogota siege",
    "29  Zambia bars term-limit protests",
    "30  Belgrade detains media owner",
    "31  US tech stocks slip on AI fears",
    "32  Nigeria clears 62 Ebola contacts",
    "33  10 dead in Guinea mining clashes",
    "34  Search for six after US plane crash",
    "35  Iowa bomb-chemicals blast hailed",
    "36  Chile telescope to hunt Earth-like worlds",
]


def lead_card(im: Image.Image, d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, item: dict) -> None:
    d.rounded_rectangle((x, y, x + w, y + h), radius=9, fill=WHITE, outline=LINE, width=2)
    d.rounded_rectangle((x + 6, y + 6, x + w - 6, y + 106), radius=6, fill=item["bg"])
    tile = Image.new("RGBA", (80, 80), (0, 0, 0, 0))
    item["icon"](ImageDraw.Draw(tile), 0, 0)
    im.paste(tile, (x + 22, y + 12), tile)
    d.ellipse((x + w - 46, y + 12, x + w - 12, y + 46), fill=RED)
    d.text((x + w - 29, y + 29), item["n"], font=f(18, True), fill=WHITE, anchor="mm")
    d.rectangle((x + w - 150, y + 66, x + w - 16, y + 92), fill=NAVY)
    d.text((x + w - 83, y + 79), item["tag"], font=f(10, True), fill=WHITE, anchor="mm")
    d.text((x + 14, y + 116), item["region"], font=f(11, True), fill=RED)
    yy = para(d, x + 14, y + 135, item["title"], f(21, True, True), INK, w - 28, 2, 2)
    yy = para(d, x + 14, yy + 3, item["sub"], f(12), MUTED, w - 28, 2, 2)
    d.text((x + 14, y + h - 20), item["source"], font=f(9, True), fill=GREEN)


def small_card(d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int,
               region: str, title: str, icon, bg: str, num: int) -> None:
    d.rounded_rectangle((x, y, x + w, y + h), radius=7, fill=WHITE, outline=LINE, width=2)
    d.rounded_rectangle((x + 5, y + 5, x + 82, y + h - 5), radius=5, fill=bg)
    icon(d, x + 8, y + 15)
    d.text((x + 92, y + 10), region, font=f(9, True), fill=RED)
    para(d, x + 92, y + 28, title, f(15, True), INK, w - 104, 1, 2)
    d.text((x + 92, y + h - 20), "%02d" % num, font=f(10, True), fill=MUTED)


def section_head(d: ImageDraw.ImageDraw, x: int, y: int, text: str, color: str = NAVY) -> None:
    d.rectangle((x, y + 2, x + 4, y + 17), fill=RED)
    d.text((x + 10, y), text, font=f(12, True), fill=color)


def build() -> None:
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)

    d.rectangle((0, 0, W, 32), fill=NAVY)
    d.text((22, 9), "MAKE.FUN  ·  A DAY IN WORLD NEWS", font=f(12, True), fill=WHITE)
    d.text((W - 22, 9), "20 STORIES  ·  9 REGIONS  ·  26 NOV 2026", font=f(12, True),
           fill=GOLD, anchor="ra")

    d.text((22, 42), "THURSDAY", font=f(18, True), fill=RED)
    d.text((18, 62), "26 NOVEMBER 2026", font=f(52, True, True), fill=INK)
    d.rounded_rectangle((W - 244, 46, W - 22, 110), radius=8, fill=NAVY)
    d.text((W - 133, 62), "ONE DAY", font=f(18, True), fill=WHITE, anchor="mm")
    d.text((W - 133, 88), "ONE IMAGE", font=f(18, True), fill=GOLD, anchor="mm")
    d.text((22, 126), "Every item happened or was first reported on 26 November 2026 (UTC)."
           " Original drawings; sources named.", font=f(13), fill=MUTED)
    d.line((22, 152, W - 22, 152), fill=INK, width=2)

    cw, gap = 320, 12
    for i, item in enumerate(LEADS):
        lead_card(im, d, 22 + i * (cw + gap), 164, cw, 232, item)

    section_head(d, 22, 406, "THE DAY'S OTHER BIG STORIES · 4-9")
    for i, (region, title, icon, bg) in enumerate(SECONDARY):
        col, row = i % 3, i // 3
        small_card(d, 22 + col * (cw + gap), 428 + row * 112, cw, 104,
                   region, title, icon, bg, i + 4)

    d.rectangle((22, 660, W - 22, 710), fill=NAVY)
    for i, (big, label) in enumerate(NUMBERS):
        cx = 22 + int((W - 44) * (i + 0.5) / 5)
        d.text((cx, 668), big, font=f(27, True), fill=GOLD, anchor="mt")
        d.text((cx, 698), label, font=f(10), fill=WHITE, anchor="mt")
        if i:
            d.line((cx - 92, 670, cx - 92, 700), fill="#4E647B", width=1)

    section_head(d, 22, 722, "WHERE IT HAPPENED · PINS 1-9")
    d.rounded_rectangle((22, 744, 350, 872), radius=6, fill=PALE, outline=LINE)
    map_shape(d, 34, 754, 304, 108)

    section_head(d, 362, 722, "THE DAY IN UTC")
    for i, line in enumerate(UTC):
        d.text((372, 750 + i * 17), line, font=f(11, bold=(i % 2 == 0)), fill=INK)

    section_head(d, 700, 722, "DATE CHECK · NOT 26 NOV")
    for i, line in enumerate(DATE_CHECK):
        d.text((710, 750 + i * 17), "· " + line, font=f(10), fill=MUTED)

    d.line((22, 882, W - 22, 882), fill=INK, width=2)
    section_head(d, 22, 890, "ALSO ON THURSDAY · STORIES 10-20")
    for i, line in enumerate(BRIEFS[:11]):
        col, row = divmod(i, 6)
        d.text((22 + col * 490, 910 + row * 17), line, font=f(13), fill=INK)

    im.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes", im.size)


if __name__ == "__main__":
    build()
