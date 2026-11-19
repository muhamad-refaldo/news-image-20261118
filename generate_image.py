#!/usr/bin/env python3
"""Generate entry.png - 1024x1024 summary of world news, 18 Nov 2026.
Deterministic: no network, no random, no timestamps, fixed fonts and colours.
Run: python3 generate_image.py  -> writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap

W, H = 1024, 1024
BG = (247, 243, 232)
NAVY = (15, 32, 64)
GOLD = (201, 162, 39)
INK = (20, 20, 20)
CARD = (255, 255, 255)
LINE = (220, 214, 200)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Header
d.rectangle([0, 0, W, 168], fill=NAVY)
d.rectangle([0, 168, W, 176], fill=GOLD)
d.text((48, 28), "WORLD NEWS  \u2022  IN ONE IMAGE", font=font(24, True), fill=(201, 162, 39))
d.text((48, 58), "18 NOVEMBER 2026", font=font(58, True), fill=(255, 255, 255))
d.text((48, 124), "Wednesday  \u2022  Six stories that shaped the world that day", font=font(22), fill=(200, 210, 230))
# Date badge on right
d.rounded_rectangle([788, 36, 976, 128], radius=12, outline=(201, 162, 39), width=2)
d.text((812, 52), "18 NOV", font=font(30, True), fill=(255, 255, 255))
d.text((836, 94), "2026", font=font(24, True), fill=(201, 162, 39))

stories = [
    ("01", "SHENZHEN SUMMIT", "Xi & Putin meet before Trump",
     "Xi Jinping and Vladimir Putin meet in Shenzhen, one day before their first-ever trilateral summit with Donald Trump. APEC opens in the same city.", (27, 58, 110)),
    ("02", "GULF ESCALATION", "Iran strikes Kuwait & Bahrain",
     "Iran strikes Kuwait and Bahrain after US jets hit a missile site on Qeshm Island. Gulf shipping and oil routes come under fire.", (140, 30, 30)),
    ("03", "KERCH BRIDGE HIT", "Ukraine strikes a second day",
     "Ukraine hits the Kerch Bridge for a second straight day. Part of the road span collapses, cutting the link to occupied Crimea.", (30, 90, 60)),
    ("04", "US SENATE FLIPS", "Democrats take the Senate",
     "Democrat Mary Peltola beats Republican Dan Sullivan in Alaska, giving Democrats a projected 56\u201344 majority in the incoming Senate.", (80, 40, 110)),
    ("05", "CYCLONE AKVAN", "47,000 evacuated in Odisha",
     "Severe Cyclone Akvan bears down on India's east coast. More than 47,000 people are evacuated in Odisha ahead of landfall on 20 November.", (0, 90, 110)),
    ("06", "DHONI RETIRES", "Cricket's Captain Cool bows out",
     "MS Dhoni retires from the IPL, ending one of cricket's great careers. In the same week, Ebola cases in DR Congo pass 11,000.", (120, 70, 20)),
]

# 2 columns x 3 rows
x0, y0 = 32, 200
cw, ch, gap = 472, 240, 16
for i, (num, kicker, headline, body, color) in enumerate(stories):
    col = i % 2
    row = i // 2
    x = x0 + col * (cw + gap)
    y = y0 + row * (ch + gap)
    # card
    d.rounded_rectangle([x, y, x + cw, y + ch], radius=14, fill=CARD, outline=LINE, width=2)
    d.rounded_rectangle([x, y, x + cw, y + 8], radius=4, fill=color)
    d.text((x + 20, y + 22), num, font=font(22, True), fill=color)
    d.text((x + 68, y + 24), kicker, font=font(19, True), fill=color)
    d.text((x + 20, y + 56), headline, font=font(26, True), fill=INK)
    # wrap body to ~38 chars
    lines = textwrap.wrap(body, width=38)
    yy = y + 96
    for line in lines[:4]:
        d.text((x + 20, yy), line, font=font(21), fill=(50, 50, 50))
        yy += 30

# Footer
d.rectangle([0, 952, W, 1024], fill=NAVY)
d.text((48, 972), "Summarised from reports published on 18 November 2026  \u2022  No single story tells the whole day", font=font(19), fill=(200, 210, 230))

img.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", img.size)
