#!/usr/bin/env python3
"""Compose the news-image-20261120 entry poster, v2 (1024x1024 PNG).

Dense broadsheet: masthead + top story (ICJ genocide ruling) + four
illustrated leads + world map + 31 one-line stories in 7 region groups
(36 stories total) + by-the-numbers strip + date check. Every word is
drawn here with PIL so the text is crisp; the icons are cropped from the
text-free AI illustrations hero.png / hero2.png. Run:
    python3 compose_poster.py   # writes entry.png next to this file
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 243, 227)
NAVY = (20, 38, 77)
RED = (178, 44, 32)
GOLD = (232, 184, 74)
INK = (24, 28, 36)
GREY = (82, 88, 98)
CARD = (255, 255, 255)
LINE = (205, 198, 178)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
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


def icons_from(hero, n=6, strip_top=0.0, strip_bottom=0.40, size=96):
    """Crop n evenly spaced vignettes out of a hero strip."""
    hw, hh = hero.size
    y0, y1 = int(hh * strip_top), int(hh * strip_bottom)
    out = []
    for i in range(n):
        cx = int(hw * (i + 0.5) / n)
        cy = (y0 + y1) // 2
        side = int(hw / n * 0.80)
        box = (cx - side // 2, cy - side // 2,
               cx + side // 2, cy + side // 2)
        out.append(hero.crop(box).resize((size, size), Image.LANCZOS))
    return out


LEADS = [
    ("CYCLONE  ·  INDIA",
     "Akvan slams India's east coast",
     "Landfall near Gopalpur; 300,000 evacuated."),
    ("SUMMIT  ·  SHENZHEN",
     "Trump, Xi, Putin hold first summit",
     "Peace declaration signed; no breakthrough on Ukraine."),
    ("WAR  ·  KYIV",
     "Russia strikes Kyiv bridges; 8 killed",
     "Overnight barrage; Poland reports airspace incursion."),
    ("CLIMATE  ·  ANTALYA",
     "COP31 draft drops fossil fuels",
     "Final-day deal strips phase-out; $120bn target cut."),
]

# (region, [(place, headline), ...]) — 31 one-line stories
GROUPS = [
    ("EUROPE", [
        ("BERLIN", "Ukraine allies meet; Europe ready to talk to Russia."),
        ("KERCH", "Third Ukrainian strike hits Crimea Bridge; Putin vows response."),
        ("BRUSSELS", "UK and EU set to agree youth mobility scheme."),
        ("TALLINN", "Estonia to shut its Russia border for at least six months."),
        ("COPENHAGEN", "Denmark ratifies Greenland security deal."),
    ]),
    ("MIDDLE EAST", [
        ("RIYADH", "Houthi missile damages Saudi wealth fund tower."),
        ("HORMUZ", "Iran war: tanker attacks intensify; US cost put at $48.3bn."),
        ("BAGHDAD", "Iraq orders Iran-backed militia out of Jurf al-Nasr."),
        ("GAZA", "Israeli troops cross Yellow Line in central Gaza."),
        ("MOGADISHU", "Somalia expels UAE ambassador over sovereignty."),
    ]),
    ("ASIA & PACIFIC", [
        ("YONGBYON", "IAEA: North Korea expanding uranium enrichment."),
        ("TOKYO", "Japan inflation at year's high; rate hike on track."),
        ("DHAKA", "Violence in Bangladesh ahead of Hasina's planned return."),
        ("PESHAWAR", "Pakistan says it killed 22 militants in northwest raids."),
        ("ULAANBAATAR", "Mongolian president resigns; election within four months."),
        ("SEOUL", "Court orders retrial of ex-PM Han in martial law case."),
    ]),
    ("AFRICA", [
        ("SUDAN", "Drone strike kills 10 at gold mine in South Kordofan."),
        ("BADME", "Strikes reported on Ethiopia-Eritrea border."),
        ("NAIROBI", "Kenya's Ebola outbreak ends; last patient discharged."),
        ("DAKAR", "Migrant boat capsizes off Senegal; dozens missing."),
    ]),
    ("AMERICAS", [
        ("WASHINGTON", "Senate passes energy permitting bill, 62–33."),
        ("CALIFORNIA", "State opens probe into Nvidia after Huang resigns."),
        ("WASHINGTON", "White House fires cyber director after tech outages."),
        ("NEW YORK", "Race for UN chief stalls after eight votes."),
        ("CARACAS", "US and Venezuela sign military cooperation deal."),
    ]),
    ("MARKETS & TECH", [
        ("NEW YORK", "Anthropic closes 17% above IPO price in Nasdaq debut."),
        ("NEW YORK", "S&P falls fifth straight day; Nikkei drops 4.8%."),
        ("NEW YORK", "Gold falls 4.2% as dollar and yields stay high."),
        ("WASHINGTON", "IMF warns global debt will near 100% of GDP."),
    ]),
    ("CULTURE & SCIENCE", [
        ("WORLD", "GTA 6 launch tops $2.3 billion in sales."),
        ("SPACE", "Voyager 1 reaches one light-day from Earth."),
    ]),
]

NUMBERS = ("BY THE NUMBERS  —  300,000 evacuated  ·  9–6 ICJ vote  ·  "
           "$81.3bn IPO  ·  Nikkei −4.8%  ·  Brent $90.05  ·  Voyager 1: 1 light-day")

FOOTER = ("DATE CHECK — Every story from Friday 20 November 2026  ·  "
          "Sources: BBC · Reuters · AP · The Guardian · Al Jazeera")


def main():
    hero = Image.open("hero.png").convert("RGB")
    hero2 = Image.open("hero2.png").convert("RGB")
    h1 = icons_from(hero, 6, 0.0, 0.40, 96)      # scales, summit, skyline, ...
    h2 = icons_from(hero2, 6, 0.12, 0.90, 96)    # cyclone, leaf, tanker, ...

    map_band = hero.crop((0, int(hero.size[1] * 0.405), hero.size[0],
                          hero.size[1])).resize((W, 92), Image.LANCZOS)

    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # --- masthead ----------------------------------------------------------
    d.rectangle([0, 0, W, 88], fill=NAVY)
    d.rectangle([0, 88, W, 92], fill=RED)
    d.text((24, 12), "THE WORLD IN ONE DAY", font=font(SERIF_B, 34),
           fill=CREAM)
    f_date = font(SANS_B, 21)
    date = "FRIDAY, 20 NOVEMBER 2026"
    d.text((W - 24 - d.textlength(date, font=f_date), 18), date,
           font=f_date, fill=GOLD)
    d.text((24, 56), "36 stories  ·  7 regions  ·  Every figure sourced",
           font=font(SANS, 16), fill=(196, 205, 224))

    # --- top story ---------------------------------------------------------
    ty = 92
    d.rectangle([0, ty, W, ty + 58], fill=(255, 250, 230))
    d.rectangle([0, ty, 8, ty + 58], fill=RED)
    img.paste(h1[0].resize((46, 46), Image.LANCZOS), (20, ty + 6))
    d.text((78, ty + 7), "TOP STORY — WORLD COURT: MYANMAR COMMITTED GENOCIDE",
           font=font(SANS_B, 19), fill=RED)
    d.text((78, ty + 31),
           "First ruling against a state  ·  9–6  ·  The Hague — 1.3 million Rohingya still displaced",
           font=font(SANS, 15), fill=INK)

    # --- four lead cards ----------------------------------------------------
    ly, lh = 158, 178
    cw = 242
    gap = (W - 2 * 20 - 4 * cw) // 3
    lead_icons = [h2[0], h1[1], h1[2], h2[1]]
    for i, (kicker, head, body) in enumerate(LEADS):
        x = 20 + i * (cw + gap)
        d.rounded_rectangle([x, ly, x + cw, ly + lh], radius=8,
                            fill=CARD, outline=LINE, width=1)
        img.paste(lead_icons[i].resize((58, 58), Image.LANCZOS),
                  (x + 12, ly + 12))
        tx = x + 80
        tw = cw - 80 - 12
        d.text((tx, ly + 12), kicker, font=font(SANS_B, 12), fill=RED)
        hl = wrap(d, head, font(SERIF_B, 17), tw)[:3]
        yy = ly + 32
        for ln in hl:
            d.text((tx, yy), ln, font=font(SERIF_B, 17), fill=INK)
            yy += 21
        bl = wrap(d, body, font(SANS, 13), cw - 24)[:2]
        yy = ly + 108
        for ln in bl:
            d.text((x + 12, yy), ln, font=font(SANS, 13), fill=GREY)
            yy += 17

    # --- map banner with lead dots ------------------------------------------
    my = 344
    img.paste(map_band, (0, my))
    d.rectangle([0, my + 88, W, my + 92], fill=NAVY)
    # dots: (x fraction of width, y fraction of banner) — no labels; the
    # leads above already name the places, and labels collide at this size.
    dots = [(0.485, 0.16), (0.556, 0.20), (0.556, 0.32),
            (0.708, 0.44), (0.789, 0.40)]
    for fx, fy in dots:
        px, py = int(W * fx), my + int(92 * fy)
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                  outline=(255, 255, 255), width=2)

    # --- region lists, 3 columns --------------------------------------------
    cols = [[GROUPS[0], GROUPS[1]], [GROUPS[2], GROUPS[3]],
            [GROUPS[4], GROUPS[5], GROUPS[6]]]
    col_w = 318
    col_x = [20, 353, 686]
    gy = 448
    f_head = font(SANS_B, 14)
    f_item = font(SANS, 14)
    f_item_b = font(SANS_B, 14)
    for ci, groups in enumerate(cols):
        x = col_x[ci]
        y = gy
        for region, items in groups:
            d.text((x, y), region, font=f_head, fill=RED)
            d.line([x, y + 20, x + col_w, y + 20], fill=RED, width=2)
            y += 26
            for place, head in items:
                prefix = f"{place} — "
                pre_w = d.textlength(prefix, font=f_item_b)
                lines = wrap(d, head, f_item, col_w - pre_w)
                d.text((x, y), prefix, font=f_item_b, fill=INK)
                yy = y
                for j, ln in enumerate(lines):
                    d.text((x + (pre_w if j == 0 else 0), yy), ln,
                           font=f_item, fill=INK)
                    yy += 17
                y = yy + 2
            y += 6

    # --- numbers strip + footer ----------------------------------------------
    d.rectangle([0, 936, W, 978], fill=NAVY)
    f_num = font(SANS_B, 14)
    while d.textlength(NUMBERS, font=f_num) > W - 48 and f_num.size > 10:
        f_num = font(SANS_B, f_num.size - 1)
    d.text((24, 948), NUMBERS, font=f_num, fill=CREAM)
    d.rectangle([0, 978, W, H], fill=(12, 22, 48))
    d.text((24, 991), FOOTER, font=font(SANS, 13), fill=(196, 205, 224))

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
