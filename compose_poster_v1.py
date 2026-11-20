#!/usr/bin/env python3
"""Compose the news-image-20261120 entry poster (1024x1024 PNG).

The hero artwork (hero.png, AI-generated, no text) is cropped into six
story icons plus a world-map banner; every word on the poster is drawn
here with PIL so the text is crisp and legible. Run:
    python3 compose_poster.py   # writes entry.png next to this file
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 243, 227)
NAVY = (20, 38, 77)
NAVY_LIGHT = (31, 58, 110)
RED = (178, 44, 32)
TEAL = (26, 122, 140)
INK = (24, 28, 36)
GREY = (90, 96, 104)
CARD = (255, 255, 255)
LINE = (205, 198, 178)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning lines that fit `width` pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    ("JUSTICE  ·  THE HAGUE",
     "World court: Myanmar committed genocide",
     "The ICJ finds Myanmar responsible for genocide against the Rohingya \u2014 the first such ruling against a state."),
    ("DIPLOMACY  ·  SHENZHEN",
     "Trump, Xi and Putin hold first three-way summit",
     "The three leaders meet in Shenzhen and sign a joint peace declaration, with no breakthrough on Ukraine."),
    ("WAR IN EUROPE  ·  KYIV",
     "Russia strikes Kyiv bridges; Poland reports incursion",
     "Overnight strikes kill eight in Kyiv. Poland says two missiles and a drone crossed its airspace."),
    ("MIDDLE EAST  ·  RIYADH",
     "Houthi missile hits Riyadh\u2019s tallest tower",
     "A missile damages the Saudi sovereign wealth fund tower in the capital\u2019s financial district."),
    ("MARKETS  ·  NEW YORK",
     "Anthropic soars on debut as stocks slide",
     "Shares close 17% above their IPO price. The Nikkei falls 4.8%; the S&P drops a fifth straight day."),
    ("HEALTH  ·  KENYA",
     "Kenya\u2019s Ebola outbreak ends",
     "The last patient is discharged, 37 days after the first case was confirmed."),
]

ALSO = ("ALSO TODAY  \u2014  IMF warns global public debt nears 100% of GDP  \u00b7  "
        "Italy fines Meta \u20ac805m  \u00b7  GTA 6 tops $2.3bn in sales  \u00b7  "
        "Record floods hit Florida")


def main():
    hero = Image.open("hero.png").convert("RGB")
    hw, hh = hero.size

    # --- crop the six icons out of the top vignette strip -----------------
    strip_h = int(hh * 0.40)
    icons = []
    for i in range(6):
        x0 = int(hw * i / 6)
        x1 = int(hw * (i + 1) / 6)
        # each vignette sits roughly centred in its sixth, with a margin
        cx = (x0 + x1) // 2
        side = int(hw / 6 * 0.82)
        box = (cx - side // 2, (strip_h - side) // 2,
               cx + side // 2, (strip_h + side) // 2)
        icons.append(hero.crop(box).resize((96, 96), Image.LANCZOS))

    # --- crop the world-map banner ----------------------------------------
    map_band = hero.crop((0, int(hh * 0.405), hw, hh))
    map_band = map_band.resize((W, 196), Image.LANCZOS)

    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # --- masthead ----------------------------------------------------------
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.rectangle([0, 104, W, 108], fill=RED)
    f_title = font(SERIF_B, 38)
    d.text((28, 18), "THE WORLD IN ONE DAY", font=f_title, fill=CREAM)
    f_date = font(SANS_B, 24)
    date = "FRIDAY, 20 NOVEMBER 2026"
    d.text((W - 28 - d.textlength(date, font=f_date), 26), date,
           font=f_date, fill=(232, 184, 74))
    f_sub = font(SANS, 19)
    d.text((28, 72), "The day\u2019s world news, in one image",
           font=f_sub, fill=(196, 205, 224))

    # --- map banner --------------------------------------------------------
    img.paste(map_band, (0, 108))
    d.rectangle([0, 300, W, 304], fill=NAVY)

    # --- story grid: 2 columns x 3 rows -----------------------------------
    gx, gy = 20, 316
    cw, ch, gap = 482, 188, 16
    f_kick = font(SANS_B, 15)
    f_head = font(SERIF_B, 22)
    f_body = font(SANS, 16)
    for i, (kicker, head, body) in enumerate(STORIES):
        x = gx + (i % 2) * (cw + gap)
        y = gy + (i // 2) * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=10,
                            fill=CARD, outline=LINE, width=1)
        img.paste(icons[i], (x + 14, y + 12))
        tx = x + 118
        tw = cw - 118 - 16
        d.text((tx, y + 16), kicker, font=f_kick, fill=RED)
        lines = wrap(d, head, f_head, tw)[:2]
        ly = y + 40
        for ln in lines:
            d.text((tx, ly), ln, font=f_head, fill=INK)
            ly += 28
        blines = wrap(d, body, f_body, tw)[:3]
        for ln in blines:
            d.text((tx, ly), ln, font=f_body, fill=(52, 58, 68))
            ly += 21

    # --- also-today strip + footer -----------------------------------------
    d.rectangle([0, 928, W, H], fill=NAVY)
    f_also = font(SANS_B, 17)
    also_lines = wrap(d, ALSO, f_also, W - 56)
    ay = 940
    for ln in also_lines:
        d.text((28, ay), ln, font=f_also, fill=CREAM)
        ay += 22

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
