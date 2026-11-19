#!/usr/bin/env python3
"""Render entry.png: a 1024x1024 one-image summary of world news, 18 Nov 2026.

The picture is drawn with Pillow from fixed text, fonts and colours only.
There is no network access, no randomness and no timestamp anywhere, so
every run writes exactly the same bytes.

Run: python3 generate_image.py  -> writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap

# --- canvas -----------------------------------------------------------------
WIDTH, HEIGHT = 1024, 1024
PAPER = (247, 243, 232)      # warm off-white background
NAVY = (15, 32, 64)         # header / footer band
NAVY_SOFT = (27, 58, 110)   # first story accent
GOLD = (201, 162, 39)       # rule + date badge
INK = (20, 20, 20)          # headlines
BODY_INK = (50, 50, 50)     # story text
CARD_FILL = (255, 255, 255)
CARD_LINE = (220, 214, 200)
HEADER_SUB = (200, 210, 230)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def make_font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REGULAR, size)


# --- the six stories of the day ---------------------------------------------
# (number, kicker, headline, body, accent colour)
STORIES = [
    ("01", "SHENZHEN SUMMIT", "Xi & Putin meet before Trump",
     "Xi Jinping and Vladimir Putin meet in Shenzhen, one day before their "
     "first-ever trilateral summit with Donald Trump. APEC opens in the same city.",
     NAVY_SOFT),
    ("02", "GULF ESCALATION", "Iran strikes Kuwait & Bahrain",
     "Iran strikes Kuwait and Bahrain after US jets hit a missile site on "
     "Qeshm Island. Gulf shipping and oil routes come under fire.",
     (140, 30, 30)),
    ("03", "KERCH BRIDGE HIT", "Ukraine strikes a second day",
     "Ukraine hits the Kerch Bridge for a second straight day. Part of the "
     "road span collapses, cutting the link to occupied Crimea.",
     (30, 90, 60)),
    ("04", "US SENATE FLIPS", "Democrats take the Senate",
     "Democrat Mary Peltola beats Republican Dan Sullivan in Alaska, giving "
     "Democrats a projected 56\u201344 majority in the incoming Senate.",
     (80, 40, 110)),
    ("05", "CYCLONE AKVAN", "47,000 evacuated in Odisha",
     "Severe Cyclone Akvan bears down on India's east coast. More than 47,000 "
     "people are evacuated in Odisha ahead of landfall on 20 November.",
     (0, 90, 110)),
    ("06", "DHONI RETIRES", "Cricket's Captain Cool bows out",
     "MS Dhoni retires from the IPL, ending one of cricket's great careers. "
     "In the same week, Ebola cases in DR Congo pass 11,000.",
     (120, 70, 20)),
]


def draw_header(d):
    """Navy band with the date, plus the gold rule underneath it."""
    d.rectangle([0, 0, WIDTH, 168], fill=NAVY)
    d.rectangle([0, 168, WIDTH, 176], fill=GOLD)
    d.text((48, 28), "WORLD NEWS  \u2022  IN ONE IMAGE",
           font=make_font(24, True), fill=GOLD)
    d.text((48, 58), "18 NOVEMBER 2026",
           font=make_font(58, True), fill=(255, 255, 255))
    d.text((48, 124), "Wednesday  \u2022  Six stories that shaped the world that day",
           font=make_font(22), fill=HEADER_SUB)
    # Date badge, top right
    d.rounded_rectangle([788, 36, 976, 128], radius=12, outline=GOLD, width=2)
    d.text((812, 52), "18 NOV", font=make_font(30, True), fill=(255, 255, 255))
    d.text((836, 94), "2026", font=make_font(24, True), fill=GOLD)


def draw_card(d, x, y, w, h, number, kicker, headline, body, accent):
    """One story card: coloured top strip, kicker, headline, wrapped body."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=14,
                        fill=CARD_FILL, outline=CARD_LINE, width=2)
    d.rounded_rectangle([x, y, x + w, y + 8], radius=4, fill=accent)
    d.text((x + 20, y + 22), number, font=make_font(22, True), fill=accent)
    d.text((x + 68, y + 24), kicker, font=make_font(19, True), fill=accent)
    d.text((x + 20, y + 56), headline, font=make_font(26, True), fill=INK)
    text_y = y + 96
    for line in textwrap.wrap(body, width=38)[:4]:
        d.text((x + 20, text_y), line, font=make_font(21), fill=BODY_INK)
        text_y += 30


def draw_footer(d):
    d.rectangle([0, 952, WIDTH, 1024], fill=NAVY)
    d.text((48, 972),
           "Summarised from reports published on 18 November 2026  \u2022  "
           "No single story tells the whole day",
           font=make_font(19), fill=HEADER_SUB)


def main():
    canvas = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw_header(draw)
    # Two columns, three rows of cards.
    card_w, card_h, gap = 472, 240, 16
    for index, story in enumerate(STORIES):
        col, row = index % 2, index // 2
        draw_card(draw,
                  32 + col * (card_w + gap),
                  200 + row * (card_h + gap),
                  card_w, card_h, *story)
    draw_footer(draw)
    canvas.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", canvas.size)


if __name__ == "__main__":
    main()
