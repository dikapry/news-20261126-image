#!/usr/bin/env python3
"""Draw one 1024x1024 editorial poster for Thursday 26 November 2026.

All artwork is drawn with Pillow primitives from a fixed, verified story list.
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


def wrap(d: ImageDraw.ImageDraw, s: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    out: list[str] = []
    cur = ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if cur and tw(d, trial, font) > width:
            out.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        out.append(cur)
    return out


# ---------------------------------------------------------------- icons ----
# Each icon draws into a fresh transparent 100x100 tile; the caller pastes it.

def icon_tariff(d: ImageDraw.ImageDraw) -> None:
    d.text((6, 2), "14", font=f(24, True), fill=GOLD)
    d.line((8, 88, 92, 88), fill=MUTED, width=3)
    for i, h in enumerate((22, 38, 52, 66)):
        d.rectangle((10 + i * 19, 86 - h, 24 + i * 19, 86), fill=RED if i > 1 else BLUE)
    d.line((10, 40, 88, 70), fill=ORANGE, width=4)
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
    d.text((4, 4), "8", font=f(20, True), fill=WHITE)


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
    d.text((10, 6), "+36%", font=f(23, True), fill=GOLD)
    d.line((12, 34, 84, 34), fill=TEAL, width=4)
    d.polygon([(84, 34), (72, 28), (72, 40)], fill=TEAL)


def icon_space(d: ImageDraw.ImageDraw) -> None:
    d.polygon([(46, 4), (62, 28), (62, 68), (46, 82), (30, 68), (30, 28)], fill=WHITE, outline=BLUE)
    d.ellipse((40, 34, 52, 46), fill=TEAL)
    d.polygon([(30, 68), (46, 88), (62, 68)], fill=RED)
    d.rectangle((6, 40, 30, 56), fill=BLUE, outline=WHITE, width=2)
    d.rectangle((62, 40, 86, 56), fill=BLUE, outline=WHITE, width=2)
    d.text((6, 70), "24", font=f(16, True), fill=GOLD)


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
    d.text((4, 4), "PR", font=f(18, True), fill=TEAL)


CARDS = [
    (1, "US TARIFFS ON 14 PARTNERS", "up to 20% on China", RED, icon_tariff),
    (2, "UKRAINE HITS RUSSIAN AIRBASE", "5 aircraft damaged", BLUE, icon_airbase),
    (3, "INDONESIA MINE FLOOD", "8 dead · 18 trapped", TEAL, icon_flood),
    (4, "CAIRO TANKER FIRE", "at least 30 dead", ORANGE, icon_tanker),
    (5, "BANGLADESH +36% WAGES", "12,500 to 17,000 taka", GOLD, icon_wages),
    (6, "PAKISTAN IN SPACE", "first astronaut on Tiangong", BLUE, icon_space),
    (7, "HORMUZ / RAS TANURA", "2 tankers hit mines", RED, icon_oil),
    (8, "MISS UNIVERSE PR", "Jennifer Barreto wins", GOLD, icon_crown),
]

PINS = [
    (0.16, 0.24, "1"), (0.55, 0.22, "2"), (0.82, 0.64, "3"),
    (0.54, 0.40, "4"), (0.72, 0.47, "5"), (0.86, 0.31, "6"),
    (0.61, 0.43, "7"), (0.25, 0.38, "8"), (0.90, 0.26, "9"),
    (0.28, 0.55, "10"),
]

CONTINENTS = [
    [(0.03, 0.12), (0.10, 0.06), (0.21, 0.08), (0.28, 0.14), (0.25, 0.27),
     (0.18, 0.32), (0.16, 0.45), (0.09, 0.35), (0.05, 0.24)],
    [(0.21, 0.48), (0.30, 0.46), (0.32, 0.60), (0.26, 0.88), (0.20, 0.75), (0.18, 0.58)],
    [(0.44, 0.18), (0.53, 0.13), (0.57, 0.20), (0.52, 0.30), (0.44, 0.28)],
    [(0.45, 0.34), (0.56, 0.32), (0.60, 0.48), (0.54, 0.68), (0.48, 0.60), (0.43, 0.44)],
    [(0.58, 0.12), (0.85, 0.09), (0.94, 0.24), (0.84, 0.37), (0.70, 0.43), (0.60, 0.32)],
    [(0.81, 0.63), (0.91, 0.60), (0.94, 0.72), (0.84, 0.76)],
]


def draw_map(im: Image.Image, d: ImageDraw.ImageDraw) -> None:
    d.rounded_rectangle((22, 176, 1002, 430), radius=10, fill=PANEL, outline=CARD_EDGE, width=2)
    bx, by, bw, bh = 54, 192, 920, 210
    for gx in range(1, 8):
        d.line((bx + gx * bw // 8, by, bx + gx * bw // 8, by + bh), fill="#142C44", width=1)
    for gy in range(1, 4):
        d.line((bx, by + gy * bh // 4, bx + bw, by + gy * bh // 4), fill="#142C44", width=1)
    for poly in CONTINENTS:
        pts = [(bx + int(px * bw), by + int(py * bh)) for px, py in poly]
        d.polygon(pts, fill="#234761", outline="#376582")
    for px, py, num in PINS:
        cx, cy = bx + int(px * bw), by + int(py * bh)
        d.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill="#0B1726", outline=RED, width=3)
        d.text((cx, cy), num, font=f(12, True), fill=WHITE, anchor="mm")
    d.text((34, 404), "9 = NORTH KOREA", font=f(11, True), fill=MUTED)
    d.text((858, 404), "10 = COLOMBIA", font=f(11, True), fill=MUTED)
    d.text((520, 404), "10 STORIES · 10 PINNED LOCATIONS", font=f(11, True), fill=GOLD, anchor="mt")


def draw_card(im: Image.Image, d: ImageDraw.ImageDraw, spec: tuple, x: int, y: int) -> None:
    num, label, detail, color, icon = spec
    d.rounded_rectangle((x, y, x + 240, y + 224), radius=10, fill=CARD, outline=CARD_EDGE, width=2)
    d.rounded_rectangle((x + 2, y + 2, x + 238, y + 108), radius=8, fill="#102139")
    d.rectangle((x + 14, y + 96, x + 226, y + 100), fill=color)
    tile = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    icon(ImageDraw.Draw(tile))
    im.paste(tile, (x + 70, y + 4), tile)
    d.ellipse((x + 196, y + 12, x + 228, y + 44), fill=color)
    d.text((x + 212, y + 28), str(num), font=f(15, True), fill="#0B1726", anchor="mm")
    lines = wrap(d, label, f(17, True), 214)
    for i, line in enumerate(lines[:2]):
        d.text((x + 13, y + 118 + i * 22), line, font=f(17, True), fill=WHITE)
    d.text((x + 13, y + 168), detail, font=f(13), fill=MUTED)
    d.line((x + 13, y + 196, x + 227, y + 196), fill=CARD_EDGE, width=1)
    d.text((x + 13, y + 203), "26 NOV 2026", font=f(10, True), fill=color)


def build() -> None:
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)

    for i, col in enumerate((RED, ORANGE, GOLD, TEAL, BLUE)):
        d.rectangle((i * W // 5, 0, (i + 1) * W // 5 - 1, 7), fill=col)

    d.text((24, 24), "THE WORLD IN ONE DAY", font=f(19, True), fill=MUTED)
    d.text((24, 52), "THURSDAY", font=f(22, True), fill=GOLD)
    d.text((20, 82), "26 NOVEMBER 2026", font=f(62, True), fill=WHITE)
    d.rounded_rectangle((786, 40, 1000, 150), radius=10, fill=PANEL, outline=CARD_EDGE, width=2)
    d.text((893, 62), "ONE DAY", font=f(24, True), fill=WHITE, anchor="mm")
    d.text((893, 98), "ONE IMAGE", font=f(24, True), fill=GOLD, anchor="mm")
    d.line((24, 166, 1000, 166), fill=CARD_EDGE, width=2)

    draw_map(im, d)

    for i, spec in enumerate(CARDS):
        col, row = i % 4, i // 4
        draw_card(im, d, spec, 22 + col * 250, 444 + row * 238)

    d.rounded_rectangle((22, 930, 1002, 1004), radius=8, fill="#132941", outline=CARD_EDGE, width=2)
    d.text((40, 948), "RUSSIA ~500,000 DEAD", font=f(16, True), fill=RED)
    d.text((386, 948), "•", font=f(16, True), fill=MUTED)
    d.text((410, 948), "NK 80–120 WARHEADS", font=f(16, True), fill=GOLD)
    d.text((718, 948), "•", font=f(16, True), fill=MUTED)
    d.text((742, 948), "COLOMBIA HOSTAGES FREED", font=f(15, True), fill=TEAL)
    d.text((40, 978), "ILLUSTRATED WITH CODE · NO PHOTOS · 26 NOV 2026", font=f(11, True), fill=MUTED)

    im.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes", im.size)


if __name__ == "__main__":
    build()
