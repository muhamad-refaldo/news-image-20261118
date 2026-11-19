#!/usr/bin/env python3
"""Generate entry.png v2 - 1024x1024 summary of world news, 18 Nov 2026.
Deterministic: no network, no random, no timestamps, fixed fonts and colours.
Run: python3 generate_image.py  -> writes entry.png next to this file.

v2: a lead hero story with a drawn picture, and every story gets its own
drawn pictogram, so a viewer who missed the day can tell what happened
from the pictures as well as the words. Same six stories and same facts
as v1, only the composition and the pictures are new.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 232)
NAVY = (15, 32, 64)
GOLD = (201, 162, 39)
INK = (20, 20, 20)
CARD = (255, 255, 255)
LINE = (220, 214, 200)
WHITE = (255, 255, 255)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def wrap_lines(text, fnt, max_w, max_lines):
    """Word-wrap text to fit max_w pixels, at most max_lines lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
            if len(lines) >= max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons
# Each draws a simple white pictogram centred in (cx, cy) with size s.
# All drawn from primitives: no copied artwork, no photos.

def icon_summit(d, cx, cy, s):
    # Skyline with three towers and a flag on the tallest.
    base = cy + s * 0.42
    towers = [(-0.62, 0.62), (-0.18, 0.90), (0.28, 0.72)]
    for dx, h in towers:
        x0 = cx + dx * s
        x1 = x0 + s * 0.24
        y0 = base - h * s
        d.rectangle([x0, y0, x1, base], fill=WHITE)
        for wy in range(3):
            yy = y0 + 8 + wy * 16
            if yy < base - 6:
                d.rectangle([x0 + 6, yy, x1 - 6, yy + 5], fill=(27, 58, 110))
    # flag pole + flag on the tallest tower
    px = cx + 0.28 * s + s * 0.12
    d.line([px, base - 0.90 * s - 26, px, base - 0.90 * s], fill=WHITE, width=3)
    d.polygon([(px, base - 0.90 * s - 26), (px + 26, base - 0.90 * s - 18),
               (px, base - 0.90 * s - 10)], fill=GOLD)
    d.line([cx - s * 0.75, base, cx + s * 0.75, base], fill=WHITE, width=4)


def icon_flame(d, cx, cy, s):
    # Flame over waves: a strike on the Gulf.
    flame = [(cx, cy - s * 0.55), (cx + s * 0.30, cy - s * 0.10),
             (cx + s * 0.34, cy + s * 0.22), (cx + s * 0.14, cy + s * 0.42),
             (cx - s * 0.14, cy + s * 0.42), (cx - s * 0.34, cy + s * 0.22),
             (cx - s * 0.30, cy - s * 0.10)]
    d.polygon(flame, fill=WHITE)
    inner = [(cx, cy + s * 0.05), (cx + s * 0.14, cy + s * 0.22),
             (cx, cy + s * 0.38), (cx - s * 0.14, cy + s * 0.22)]
    d.polygon(inner, fill=GOLD)
    for yy in (0.52, 0.64):
        y = cy + s * yy
        d.arc([cx - s * 0.55, y - 12, cx - s * 0.05, y + 12], 200, 340,
              fill=WHITE, width=4)
        d.arc([cx + s * 0.05, y - 12, cx + s * 0.55, y + 12], 200, 340,
              fill=WHITE, width=4)


def icon_bridge(d, cx, cy, s):
    # A bridge with its middle span broken and falling.
    deck = cy + s * 0.10
    d.line([cx - s * 0.70, deck, cx - s * 0.14, deck], fill=WHITE, width=5)
    d.line([cx + s * 0.14, deck, cx + s * 0.70, deck], fill=WHITE, width=5)
    for tx in (-0.52, 0.52):
        x = cx + tx * s
        d.line([x, deck - s * 0.42, x, deck], fill=WHITE, width=5)
        d.line([x - 14, deck - s * 0.42, x + 14, deck - s * 0.42],
               fill=WHITE, width=4)
    d.arc([cx - s * 0.55, deck - s * 0.55, cx + s * 0.55, deck + s * 0.35],
          180, 360, fill=WHITE, width=4)
    # falling pieces under the gap
    d.rectangle([cx - 10, deck + 26, cx + 2, deck + 38], fill=GOLD)
    d.rectangle([cx + 12, deck + 44, cx + 22, deck + 54], fill=WHITE)


def icon_dome(d, cx, cy, s):
    # Capitol dome with a check mark: the Senate flips.
    base = cy + s * 0.42
    d.rectangle([cx - s * 0.55, base - 12, cx + s * 0.55, base], fill=WHITE)
    d.rectangle([cx - s * 0.45, base - 34, cx + s * 0.45, base - 12], fill=WHITE)
    for k in range(-1, 2):
        x = cx + k * s * 0.28
        d.line([x, base - 34, x, base - 12], fill=(80, 40, 110), width=3)
    d.pieslice([cx - s * 0.34, base - s * 0.78, cx + s * 0.34, base - 30],
               180, 360, fill=WHITE)
    d.line([cx, base - s * 0.78 - 22, cx, base - s * 0.78], fill=WHITE, width=3)
    d.polygon([(cx, base - s * 0.78 - 22), (cx + 18, base - s * 0.78 - 16),
               (cx, base - s * 0.78 - 10)], fill=GOLD)
    # check mark
    d.line([cx + s * 0.30, base - s * 0.28, cx + s * 0.44, base - s * 0.12],
           fill=GOLD, width=5)
    d.line([cx + s * 0.44, base - s * 0.12, cx + s * 0.62, base - s * 0.48],
           fill=GOLD, width=5)


def icon_cyclone(d, cx, cy, s):
    # Spiral with an eye, rain below.
    for k, r in enumerate((52, 40, 28, 16)):
        a0 = 20 + k * 70
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 250,
              fill=WHITE, width=5)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=GOLD)
    for k, x in enumerate((-0.45, 0.0, 0.45)):
        xx = cx + x * s
        d.line([xx, cy + s * 0.52, xx - 8, cy + s * 0.68], fill=WHITE, width=4)


def icon_cricket(d, cx, cy, s):
    # Cricket stumps and ball.
    for dx in (-0.30, 0.0, 0.30):
        x = cx + dx * s
        d.line([x, cy - s * 0.30, x, cy + s * 0.42], fill=WHITE, width=7)
    d.line([cx - s * 0.30, cy - s * 0.30, cx - s * 0.02, cy - s * 0.30],
           fill=WHITE, width=5)
    d.line([cx + s * 0.02, cy - s * 0.30, cx + s * 0.30, cy - s * 0.30],
           fill=WHITE, width=5)
    d.ellipse([cx + s * 0.28, cy + s * 0.10, cx + s * 0.62, cy + s * 0.44],
              fill=(200, 40, 40))
    d.arc([cx + s * 0.28, cy + s * 0.10, cx + s * 0.62, cy + s * 0.44],
          300, 60, fill=WHITE, width=3)


ICONS = {
    "summit": icon_summit,
    "flame": icon_flame,
    "bridge": icon_bridge,
    "dome": icon_dome,
    "cyclone": icon_cyclone,
    "cricket": icon_cricket,
}

# ---------------------------------------------------------------- image

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Header
d.rectangle([0, 0, W, 148], fill=NAVY)
d.rectangle([0, 148, W, 154], fill=GOLD)
d.text((48, 20), "WORLD NEWS  \u2022  IN ONE IMAGE", font=font(22, True),
       fill=GOLD)
d.text((48, 48), "18 NOVEMBER 2026", font=font(56, True), fill=WHITE)
d.text((48, 112), "Wednesday  \u2022  Six stories that shaped the world that day",
       font=font(21), fill=(200, 210, 230))
d.rounded_rectangle([800, 28, 976, 122], radius=12, outline=GOLD, width=2)
d.text((824, 42), "18 NOV", font=font(30, True), fill=WHITE)
d.text((848, 84), "2026", font=font(24, True), fill=GOLD)

stories = [
    ("01", "SHENZHEN SUMMIT", "Xi & Putin meet before Trump",
     "Xi Jinping and Vladimir Putin meet in Shenzhen, one day before their "
     "first-ever trilateral summit with Donald Trump. APEC opens in the "
     "same city.", (27, 58, 110), "summit"),
    ("02", "GULF ESCALATION", "Iran strikes Kuwait & Bahrain",
     "Iran hits Kuwait and Bahrain after US jets strike a Qeshm Island "
     "site; Gulf shipping is hit.", (140, 30, 30), "flame"),
    ("03", "KERCH BRIDGE HIT", "Ukraine strikes a second day",
     "Ukraine hits the Kerch Bridge again. A road span collapses, "
     "cutting the link to Crimea.", (30, 90, 60),
     "bridge"),
    ("04", "US SENATE FLIPS", "Democrats take the Senate",
     "Mary Peltola beats Dan Sullivan in Alaska, giving Democrats a "
     "projected 56\u201344 Senate majority.", (80, 40, 110),
     "dome"),
    ("05", "CYCLONE AKVAN", "47,000 evacuated in Odisha",
     "Cyclone Akvan bears down on India's east coast. Over 47,000 "
     "evacuated in Odisha.", (0, 90, 110),
     "cyclone"),
    ("06", "DHONI RETIRES", "Captain Cool bows out",
     "MS Dhoni retires from the IPL, ending one of cricket's great "
     "careers. In the same week, Ebola cases in DR Congo pass 11,000.",
     (120, 70, 20), "cricket"),
]


def hero_card(s):
    num, kicker, headline, body, color, icon = s
    x0, y0, x1, y1 = 32, 170, 992, 390
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=CARD, outline=LINE,
                        width=2)
    d.rounded_rectangle([x0, y0, x0 + 320, y1], radius=14, fill=color)
    d.rectangle([x0 + 300, y0, x0 + 320, y1], fill=color)
    ICONS[icon](d, x0 + 160, y0 + 104, 150)
    tx = x0 + 348
    d.text((tx, y0 + 22), "LEAD STORY  \u2022  " + kicker,
           font=font(20, True), fill=color)
    for i, ln in enumerate(wrap_lines(headline, font(34, True), 580, 2)):
        d.text((tx, y0 + 52 + i * 42), ln, font=font(34, True), fill=INK)
    yy = y0 + 136
    for ln in wrap_lines(body, font(21), 580, 3):
        d.text((tx, yy), ln, font=font(21), fill=(50, 50, 50))
        yy += 29


def grid_card(s, x0, y0):
    num, kicker, headline, body, color, icon = s
    x1, y1 = x0 + 472, y0 + 200
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=CARD, outline=LINE,
                        width=2)
    d.rounded_rectangle([x0, y0, x0 + 118, y1], radius=14, fill=color)
    d.rectangle([x0 + 98, y0, x0 + 118, y1], fill=color)
    ICONS[icon](d, x0 + 59, y0 + 100, 84)
    tx = x0 + 136
    d.text((tx, y0 + 16), num + "  " + kicker, font=font(19, True),
           fill=color)
    yy = y0 + 46
    for ln in wrap_lines(headline, font(24, True), 318, 2):
        d.text((tx, yy), ln, font=font(24, True), fill=INK)
        yy += 30
    yy += 6
    for ln in wrap_lines(body, font(19), 318, 3):
        d.text((tx, yy), ln, font=font(19), fill=(50, 50, 50))
        yy += 25


def bottom_card(s):
    num, kicker, headline, body, color, icon = s
    x0, y0, x1, y1 = 32, 838, 992, 968
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=CARD, outline=LINE,
                        width=2)
    d.rounded_rectangle([x0, y0, x0 + 150, y1], radius=14, fill=color)
    d.rectangle([x0 + 130, y0, x0 + 150, y1], fill=color)
    ICONS[icon](d, x0 + 75, y0 + 71, 96)
    tx = x0 + 172
    d.text((tx, y0 + 18), num + "  " + kicker, font=font(19, True),
           fill=color)
    d.text((tx, y0 + 46), headline, font=font(26, True), fill=INK)
    yy = y0 + 86
    for ln in wrap_lines(body, font(20), 780, 2):
        d.text((tx, yy), ln, font=font(20), fill=(50, 50, 50))
        yy += 27


hero_card(stories[0])
grid_card(stories[1], 32, 406)
grid_card(stories[2], 520, 406)
grid_card(stories[3], 32, 622)
grid_card(stories[4], 520, 622)
bottom_card(stories[5])

# Footer
d.rectangle([0, 984, W, 1024], fill=NAVY)
d.text((48, 995), "Summarised from reports published on 18 November 2026  "
       "\u2022  No single story tells the whole day", font=font(19),
       fill=(200, 210, 230))

img.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", img.size)
