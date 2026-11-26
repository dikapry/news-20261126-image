#!/usr/bin/env python3
"""One 1024x1024 poster for 26 November 2026: 8 large stories, no fine print.

Every mark is drawn with Pillow primitives from a fixed, verified story list.
No network, no photographs, no third-party logos.
"""

from __future__ import annotations

import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

BG = "#0B1726"
PANEL = "#0F2238"
CARD = "#162B43"
CARD_EDGE = "#2D4A66"
WHITE = "#F5F2E9"
MUTED = "#9BB0C6"
RED = "#EA4B3C"
ORANGE = "#F08A3C"
GOLD = "#F5C445"
TEAL = "#35C2B0"
BLUE = "#56A0E6"

FONTS = "/usr/share/fonts/truetype/dejavu"
REG = os.path.join(FONTS, "DejaVuSans.ttf")
BOLD = os.path.join(FONTS, "DejaVuSans-Bold.ttf")
_cache: dict[tuple[int, bool], ImageFont.FreeTypeFont] = {}


def f(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    key = (size, bold)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(BOLD if bold else REG, size)
    return _cache[key]


def tw(d: ImageDraw.ImageDraw, s: str, font: ImageFont.FreeTypeFont) -> int:
    b = d.textbbox((0, 0), s, font=font)
    return b[2] - b[0]


# ---------------------------------------------------------------- icons ----
# Icons draw into a transparent 100x100 tile; the caller pastes it onto the poster.

def icon_tariff(d: ImageDraw.ImageDraw) -> None:
    d.text((4, 0), "14", font=f(26, True), fill=GOLD)
    d.line((8, 90, 92, 90), fill=MUTED, width=3)
    for i, h in enumerate((24, 40, 56, 72)):
        d.rectangle((10 + i * 19, 88 - h, 24 + i * 19, 88), fill=RED if i > 1 else BLUE)
    d.line((10, 38, 88, 70), fill=ORANGE, width=4)
    d.polygon([(88, 70), (76, 68), (84, 59)], fill=ORANGE)


def icon_airbase(d: ImageDraw.ImageDraw) -> None:
    d.line((4, 84, 96, 84), fill=MUTED, width=3)
    for dx, dy in ((16, 24), (46, 14), (72, 30)):
        d.polygon([(dx + 12, dy + 6), (dx, dy + 12), (dx + 4, dy + 16),
                   (dx + 12, dy + 13), (dx + 12, dy + 20), (dx + 16, dy + 20),
                   (dx + 16, dy + 12), (dx + 26, dy + 14)], fill=BLUE)
    for a in range(0, 360, 45):
        r = math.radians(a)
        d.line((78 + 10 * math.cos(r), 72 + 10 * math.sin(r),
                78 + 18 * math.cos(r), 72 + 18 * math.sin(r)), fill=ORANGE, width=3)
    d.ellipse((70, 64, 86, 80), fill=RED)


def icon_flood(d: ImageDraw.ImageDraw) -> None:
    d.rounded_rectangle((14, 30, 86, 78), radius=10, fill="#223C52", outline=GOLD, width=3)
    d.ellipse((38, 46, 62, 78), fill="#0B1726")
    d.ellipse((30, 16, 70, 46), fill=ORANGE)
    d.rectangle((43, 8, 57, 22), fill=GOLD)
    for y in (64, 76, 88):
        pts = [(x, y + (5 if x % 20 < 10 else -5)) for x in range(2, 100, 4)]
        d.line(pts, fill=TEAL, width=4)
    d.text((2, 2), "8", font=f(20, True), fill=WHITE)


def icon_tanker(d: ImageDraw.ImageDraw) -> None:
    d.polygon([(40, 6), (58, 34), (51, 52), (64, 46), (56, 74), (24, 74),
               (20, 42)], fill=ORANGE, outline=RED)
    d.polygon([(40, 34), (52, 58), (34, 58)], fill=GOLD)
    d.rounded_rectangle((8, 56, 92, 78), radius=5, fill=MUTED, outline=WHITE, width=2)
    d.rectangle((66, 46, 84, 58), fill=BLUE)
    for x in (26, 48, 72):
        d.ellipse((x - 6, 74, x + 6, 86), fill="#0B1726", outline=WHITE, width=2)


def icon_wages(d: ImageDraw.ImageDraw) -> None:
    d.polygon([(6, 84), (6, 48), (28, 62), (28, 48), (50, 62), (50, 38),
               (86, 54), (86, 84)], fill="#254861", outline=WHITE, width=2)
    d.text((6, 4), "+36%", font=f(22, True), fill=GOLD)
    d.line((12, 34, 84, 34), fill=TEAL, width=4)
    d.polygon([(84, 34), (72, 28), (72, 40)], fill=TEAL)


def icon_space(d: ImageDraw.ImageDraw) -> None:
    d.polygon([(46, 4), (62, 28), (62, 68), (46, 82), (30, 68), (30, 28)], fill=WHITE, outline=BLUE)
    d.ellipse((40, 34, 52, 46), fill=TEAL)
    d.polygon([(30, 68), (46, 88), (62, 68)], fill=RED)
    d.rectangle((6, 40, 30, 56), fill=BLUE, outline=WHITE, width=2)
    d.rectangle((62, 40, 86, 56), fill=BLUE, outline=WHITE, width=2)
    d.text((4, 70), "24", font=f(16, True), fill=GOLD)


def icon_oil(d: ImageDraw.ImageDraw) -> None:
    d.line((26, 86, 50, 12, 74, 86), fill=GOLD, width=4)
    for y in (30, 50, 70):
        d.line((28 + (y - 10) // 8, y, 72 - (y - 10) // 8, y), fill=GOLD, width=3)
    d.ellipse((4, 62, 22, 80), outline=RED, width=4)
    for a in range(0, 360, 45):
        r = math.radians(a)
        d.line((13 + 9 * math.cos(r), 71 + 9 * math.sin(r),
                13 + 14 * math.cos(r), 71 + 14 * math.sin(r)), fill=RED, width=3)
    d.line((74, 48, 96, 48), fill=TEAL, width=3)


def icon_crown(d: ImageDraw.ImageDraw) -> None:
    d.polygon([(12, 74), (20, 30), (38, 52), (50, 22), (62, 52),
               (80, 30), (88, 74)], fill=GOLD, outline=WHITE, width=2)
    d.rectangle((12, 76, 88, 86), fill=GOLD, outline=WHITE, width=2)
    d.ellipse((44, 60, 56, 72), fill=RED)
    d.text((2, 2), "PR", font=f(18, True), fill=TEAL)


# number badge, two title lines, detail line, accent, icon
STORIES = [
    ("1", "TRUMP TARIFFS", "14 PARTNERS", "China up to 20%", RED, icon_tariff),
    ("2", "UKRAINE", "HITS AIRBASE", "5 planes damaged", BLUE, icon_airbase),
    ("3", "INDONESIA", "MINE FLOOD", "8 dead · 18 trapped", TEAL, icon_flood),
    ("4", "EGYPT", "TANKER FIRE", "30+ dead near Cairo", ORANGE, icon_tanker),
    ("5", "BANGLADESH", "+36% WAGES", "12,500 to 17,000 taka", GOLD, icon_wages),
    ("6", "PAKISTAN", "IN SPACE", "first on Tiangong", BLUE, icon_space),
]

WIDE = [
    ("7", "MIDDLE EAST", "RAS TANURA + HORMUZ", "2 tankers hit mines", RED, icon_oil),
    ("8", "MISS UNIVERSE", "JENNIFER BARRETO", "San Juan, Puerto Rico", GOLD, icon_crown),
]

STATS = [
    ("14", "PARTNERS"), ("5", "PLANES"), ("8", "DEAD"),
    ("+36%", "WAGES"), ("1ST", "ASTRONAUT"),
]


def paste_icon(im: Image.Image, icon, x: int, y: int) -> None:
    tile = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    icon(ImageDraw.Draw(tile))
    im.paste(tile, (x, y), tile)


def card(im: Image.Image, d: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int,
         spec: tuple, big: bool = False) -> None:
    num, line1, line2, detail, color, icon = spec
    d.rounded_rectangle((x, y, x + w, y + h), radius=10, fill=CARD, outline=CARD_EDGE, width=2)
    d.rectangle((x + 2, y + 2, x + w - 2, y + 8), fill=color)
    paste_icon(im, icon, x + 14, y + 18)
    badge_y = y + 18 if big else y + 118
    d.ellipse((x + w - 52, badge_y, x + w - 18, badge_y + 34), fill=color)
    d.text((x + w - 35, badge_y + 17), num, font=f(17, True), fill="#0B1726", anchor="mm")
    tx = x + 124
    title_size = 21 if big else 19
    d.text((tx, y + 22), line1, font=f(title_size, True), fill=WHITE)
    d.text((tx, y + 50), line2, font=f(title_size, True), fill=color)
    d.text((tx, y + 88), detail, font=f(14), fill=MUTED)
    d.line((x + 14, y + h - 34, x + w - 14, y + h - 34), fill=CARD_EDGE, width=1)
    d.text((x + 14, y + h - 27), "26 NOV 2026", font=f(11, True), fill=MUTED)


def build() -> None:
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)

    for i, col in enumerate((RED, ORANGE, GOLD, TEAL, BLUE)):
        d.rectangle((i * W // 5, 0, (i + 1) * W // 5 - 1, 7), fill=col)

    d.text((24, 22), "THURSDAY", font=f(21, True), fill=GOLD)
    d.text((24, 50), "THE WORLD IN ONE DAY", font=f(18, True), fill=MUTED)
    d.text((20, 76), "26 NOVEMBER 2026", font=f(64, True), fill=WHITE)
    d.text((24, 150), "Events reported 26 Nov 2026 UTC", font=f(12), fill=MUTED)
    d.rounded_rectangle((800, 32, 1000, 132), radius=10, fill=PANEL, outline=CARD_EDGE, width=2)
    d.text((900, 58), "8 STORIES", font=f(20, True), fill=WHITE, anchor="mm")
    d.text((900, 94), "ONE DAY", font=f(20, True), fill=GOLD, anchor="mm")
    d.line((22, 172, 1002, 172), fill=CARD_EDGE, width=2)

    for i, spec in enumerate(STORIES):
        col, row = i % 3, i // 3
        card(im, d, 22 + col * 326, 184 + row * 220, 314, 208, spec)

    for i, spec in enumerate(WIDE):
        card(im, d, 22 + i * 496, 624, 484, 134, spec, big=True)

    d.rounded_rectangle((22, 774, 1002, 848), radius=10, fill=PANEL, outline=CARD_EDGE, width=2)
    for i, (big, label) in enumerate(STATS):
        cx = 22 + int(980 * (i + 0.5) / 5)
        d.text((cx, 788), big, font=f(32, True), fill=GOLD if i % 2 == 0 else TEAL, anchor="mt")
        d.text((cx, 828), label, font=f(13, True), fill=WHITE, anchor="mt")
        if i:
            d.line((cx - 92, 792, cx - 92, 836), fill=CARD_EDGE, width=1)

    d.rounded_rectangle((22, 864, 1002, 1006), radius=10, fill="#132941", outline=CARD_EDGE, width=2)
    d.text((40, 880), "RUSSIA ~500,000 DEAD", font=f(17, True), fill=RED)
    d.text((392, 880), "•", font=f(17, True), fill=MUTED)
    d.text((418, 880), "NK 80–120 WARHEADS", font=f(17, True), fill=GOLD)
    d.text((730, 880), "•", font=f(17, True), fill=MUTED)
    d.text((756, 880), "COLOMBIA 76 FREED", font=f(16, True), fill=TEAL)
    d.text((40, 968), "REPORTED 26 NOV 2026 · ILLUSTRATED WITH CODE · NO PHOTOS",
           font=f(12, True), fill=MUTED)

    im.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes", im.size)


if __name__ == "__main__":
    build()
