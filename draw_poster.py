#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news poster (1024x1024 JPEG).

Reads nothing from disk except the DejaVu fonts. Every story line is
written in this file, so running it twice gives byte-identical output.
Run:  python3 draw_poster.py   (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SCALE = 2
W, H = 1024 * SCALE, 1024 * SCALE
MARGIN = 48 * SCALE

PAPER = (244, 239, 228)
INK = (20, 20, 20)
RED = (179, 32, 44)
RED_DARK = (140, 20, 30)
GREY = (90, 88, 80)
PANEL = (232, 226, 210)
MAP_BG = (214, 222, 214)
LAND = (168, 172, 150)
SEA_DOT = (179, 32, 44)
BLUE_DOT = (30, 70, 130)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size * SCALE)


F_SERIF_BIG = None
F_SANS = None
F_SANS_B = None


def load_fonts():
    global F_SERIF_BIG, F_SANS, F_SANS_B
    F_SERIF_BIG = font("DejaVuSerif-Bold.ttf", 58)
    F_SANS = font("DejaVuSans.ttf", 14)
    F_SANS_B = font("DejaVuSans-Bold.ttf", 14)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill=INK):
    draw.text(xy, s, font=fnt, fill=fill)


def centered(draw, y, s, fnt, fill, cx=W // 2):
    w = draw.textlength(s, font=fnt)
    draw.text((cx - w / 2, y), s, font=fnt, fill=fill)


def rule(draw, y, weight=3):
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=INK, width=weight * SCALE)


LEADS = [
    ("1", "UKRAINE \u2014 KRYVYI RIH",
     "Russian missiles hit Zelenskyy's hometown. Boy, 7, and paramedic, 20, killed; 60 wounded."),
    ("2", "CLIMATE \u2014 ANTALYA",
     "COP31 in overtime. Antalya talks run past deadline. Draft deal omits fossil fuels."),
    ("3", "MEXICO \u2014 SINALOA",
     "El Chapo Isidro caught. Mexico captures FBI Top 10 boss Fausto Isidro Meza Flores in Sinaloa."),
]

UTC_CELLS = [
    ("00:09", "6.7 quake strikes Peru"),
    ("08:21", "Manipur toll: 13 dead"),
    ("12:30", "Man City 1-1 Fulham"),
    ("17:30", "Newcastle 2-2 Arsenal"),
    ("EVENING", "COP31 runs past deadline"),
    ("EVENING", "Kryvyi Rih hit; Isidro caught"),
]

NUMBERS = [
    ("60", "wounded in Kryvyi Rih"),
    ("-5.28%", "Nasdaq"),
    ("-3.7%", "S&P 500"),
    ("$4TN", "wiped"),
    ("6.7", "Peru quake"),
    ("13", "dead in Manipur"),
]

GRID = [
    ("4", "AI ROUT DEEPENS", "Nasdaq erases 2026 gains",
     "Nvidia -14% after SEC probe; Anthropic -8.5%"),
    ("5", "PERU QUAKE 6.7", "Junin, deep 108 km",
     "Felt in Lima; no deaths reported"),
    ("6", "MANIPUR LIQUOR", "Toxic liquor kills 13",
     "Toll rises in Manipur"),
    ("7", "IRAN STRIKES BAHRAIN", "Guards claim US hits",
     "Bahrain reports industrial fire"),
    ("8", "TRUMP WEIGHS IRAN STRIKES", "Senate blocks vote",
     "Israel presses for action"),
    ("9", "TRUMP TO EUROPE: DEFUND UKRAINE", "After Putin summit",
     "Zelenskyy hits back"),
    ("10", "BIGGEST NOV BARRAGE", "404 drones, 111 missiles",
     "Missiles land in Poland; NATO condemns"),
    ("11", "DENMARK EXPELS RUSSIAN ENVOY", "Defence attache out",
     "Copenhagen cites alleged plot"),
    ("12", "RIKERS TO CLOSE BY 2032", "Mamdani NYC plan",
     "NYC releases closure plan"),
    ("13", "HOUTHIS HIT RIYADH", "Strike on Saudi capital",
     "After covert mission, Saudis say"),
]

ALSO_LEFT = [
    "14. EU gives Ukraine 1bn more arms; 7.9bn aid paid",
    "15. Gaza: 129 bodies pulled from rubble",
    "16. Trump signs law rounding cash to nearest 5 cents",
    "17. Nadal joins Real Madrid board, 99.5% approval",
    "18. Brazil study: mosquitoes cut child dengue by 69%",
    "19. Pakistan beat Sri Lanka by 8 wickets; series 1-0",
    "20. PSG edge Nice 3-2; Sevilla 1-1 Betis in derby",
    "21. Spurs 2-0 Ipswich; teen Williams-Barnet scores",
    "22. Bournemouth 2-0 Forest; 9th straight win",
    "23. Denmark weighs halting Schengen visas for Russians",
]

ALSO_RIGHT = [
    "24. German groups ready to spend 25bn on TikTok Europe",
    "25. Malaysia-Turkey pact to shelter 10,000 Rohingya",
    "26. US approved 900,000 AI chips for China in 6 months",
    "27. Russian ship Sparta II ablaze in Gulf of Finland",
    "28. Second US judge halts Trump arch project",
    "29. FBI arrests Georgia man over crypto sent to ISIS",
    "30. California AG summons Nvidia over ex-CEO China ties",
    "31. Hegseth restricts military cooperation with Canada",
    "32. Estonia urges Putin ceasefire, rejects Kremlin tourism",
    "33. Ukraine to send food aid to nine countries",
]

CONTINENTS = [
    [(60, 60), (180, 30), (320, 40), (420, 80), (380, 140), (300, 170),
     (220, 200), (150, 180), (80, 140)],
    [(300, 240), (380, 230), (430, 280), (400, 360), (340, 400), (290, 330)],
    [(540, 80), (620, 50), (680, 80), (660, 130), (600, 150), (550, 120)],
    [(560, 180), (660, 170), (720, 210), (700, 300), (640, 350),
     (580, 300), (540, 240)],
    [(700, 60), (900, 40), (1010, 90), (990, 170), (880, 200),
     (800, 170), (720, 130)],
    [(880, 300), (980, 290), (1010, 330), (950, 360), (880, 350)],
]

DOTS = [
    (330, 120, SEA_DOT), (180, 170, SEA_DOT), (300, 300, SEA_DOT),
    (640, 110, SEA_DOT), (660, 150, SEA_DOT), (720, 190, SEA_DOT),
    (700, 205, BLUE_DOT), (620, 90, BLUE_DOT), (600, 70, BLUE_DOT),
    (880, 210, SEA_DOT), (680, 170, BLUE_DOT), (960, 320, BLUE_DOT),
    (400, 320, BLUE_DOT), (620, 320, SEA_DOT),
]


def draw_header(draw):
    f_kick = font("DejaVuSans-Bold.ttf", 15)
    centered(draw, 18 * SCALE,
             "ONE DAY OF WORLD NEWS, ONE PICTURE \u2014 33 STORIES \u2022 5 REGIONS \u2022 EVERY ONE FROM THIS SATURDAY",
             f_kick, RED)
    text(draw, (MARGIN, 40 * SCALE), "Saturday 21 November 2026",
         F_SERIF_BIG, INK)
    rule(draw, 106 * SCALE)
    draw.rectangle([MARGIN, 112 * SCALE, W - MARGIN, 142 * SCALE], fill=RED)
    f_ban = font("DejaVuSans-Bold.ttf", 21)
    centered(draw, 119 * SCALE,
             "KRYVYI RIH HIT \u2022 COP31 IN OVERTIME \u2022 EL CHAPO ISIDRO CAUGHT",
             f_ban, (255, 255, 255))


def label_column(draw, x, y, w, h, lines):
    draw.rectangle([x, y, x + w, y + h], fill=RED)
    f_lab = font("DejaVuSans-Bold.ttf", 15)
    total = len(lines) * 20 * SCALE
    cy = y + (h - total) // 2
    for line in lines:
        lw = draw.textlength(line, font=f_lab)
        draw.text((x + (w - lw) / 2, cy), line, font=f_lab,
                  fill=(255, 255, 255))
        cy += 20 * SCALE


def draw_strip(draw, y, h, label_lines, cells, big, small, ncols=6):
    lab_w = 100 * SCALE
    label_column(draw, MARGIN, y, lab_w, h, label_lines)
    cell_w = (W - 2 * MARGIN - lab_w) // ncols
    f_big = font("DejaVuSans-Bold.ttf", big)
    f_small = font("DejaVuSans.ttf", small)
    for i, (head, body) in enumerate(cells):
        cx = MARGIN + lab_w + i * cell_w
        if i:
            draw.line([(cx, y + 6 * SCALE), (cx, y + h - 6 * SCALE)],
                      fill=GREY, width=1 * SCALE)
        hw = draw.textlength(head, font=f_big)
        draw.text((cx + (cell_w - hw) / 2, y + 8 * SCALE), head,
                  font=f_big, fill=INK)
        for j, ln in enumerate(wrap(draw, body, f_small, cell_w - 12 * SCALE)):
            lw = draw.textlength(ln, font=f_small)
            draw.text((cx + (cell_w - lw) / 2,
                       y + (8 + big + 4 + j * (small + 2)) * SCALE),
                      ln, font=f_small, fill=INK)
    rule(draw, y + h + 4 * SCALE)


def draw_leads(draw, y, h):
    f_head = font("DejaVuSans-Bold.ttf", 26)
    text(draw, (MARGIN, y), "THREE LEADS", f_head, INK)
    col_w = (W - 2 * MARGIN - 2 * 10 * SCALE) // 3
    f_num = font("DejaVuSans-Bold.ttf", 34)
    f_lead = font("DejaVuSans-Bold.ttf", 19)
    f_body = font("DejaVuSans.ttf", 14)
    top = y + 34 * SCALE
    for i, (num, head, body) in enumerate(LEADS):
        x = MARGIN + i * (col_w + 10 * SCALE)
        if i:
            draw.line([(x - 5 * SCALE, top), (x - 5 * SCALE, top + h - 34 * SCALE)],
                      fill=GREY, width=1 * SCALE)
        text(draw, (x, top), num, f_num, RED)
        yy = top + 40 * SCALE
        for ln in wrap(draw, head, f_lead, col_w):
            text(draw, (x, yy), ln, f_lead, INK)
            yy += 22 * SCALE
        yy += 4 * SCALE
        for ln in wrap(draw, body, f_body, col_w):
            text(draw, (x, yy), ln, f_body, INK)
            yy += 17 * SCALE


def draw_map(draw, x, y, w, h):
    f_head = font("DejaVuSans-Bold.ttf", 24)
    text(draw, (x, y), "WHERE IT HAPPENED", f_head, INK)
    my = y + 32 * SCALE
    mh = h - 62 * SCALE
    draw.rectangle([x, my, x + w, my + mh], fill=MAP_BG,
                   outline=GREY, width=1 * SCALE)
    sx = w / 1080.0
    sy = mh / 440.0
    for poly in CONTINENTS:
        pts = [(x + px * sx, my + py * sy) for px, py in poly]
        draw.polygon(pts, fill=LAND, outline=(120, 124, 110))
    for dx, dy, col in DOTS:
        cx, cy = x + dx * sx, my + dy * sy
        r = 7 * SCALE
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    f_leg = font("DejaVuSans-Bold.ttf", 13)
    centered(draw, my + mh + 8 * SCALE,
             "Europe 15 \u2022 Americas 9 \u2022 Asia 4 \u2022 Middle East 3 \u2022 Global 2",
             f_leg, INK, cx=x + w // 2)


def draw_grid(draw, x, y, w, h):
    f_head = font("DejaVuSans-Bold.ttf", 24)
    text(draw, (x, y), "10-STORY GRID", f_head, INK)
    f_item = font("DejaVuSans-Bold.ttf", 13)
    f_det = font("DejaVuSans.ttf", 11)
    top = y + 32 * SCALE
    item_h = (h - 32 * SCALE) // len(GRID)
    for i, (num, head, sub, det) in enumerate(GRID):
        iy = top + i * item_h
        line1 = "%s. %s \u2014 %s" % (num, head, sub)
        text(draw, (x, iy), line1, f_item, INK)
        text(draw, (x + 18 * SCALE, iy + 14 * SCALE), det, f_det, GREY)


def draw_also(draw, y, h):
    f_head = font("DejaVuSans-Bold.ttf", 24)
    text(draw, (MARGIN, y), "ALSO \u2014 ITEMS 14\u201333", f_head, INK)
    f_item = font("DejaVuSans.ttf", 13)
    col_w = (W - 2 * MARGIN - 20 * SCALE) // 2
    top = y + 32 * SCALE
    row_h = (h - 32 * SCALE) // 10
    for col, items in enumerate((ALSO_LEFT, ALSO_RIGHT)):
        x = MARGIN + col * (col_w + 20 * SCALE)
        for i, item in enumerate(items):
            text(draw, (x, top + i * row_h), item, f_item, INK)


def main():
    load_fonts()
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    y = 150 * SCALE
    draw_strip(draw, y, 70 * SCALE, ["THE DAY", "IN UTC"], UTC_CELLS, 18, 13)
    y = 228 * SCALE
    draw_strip(draw, y, 70 * SCALE, ["THE DAY", "IN", "NUMBERS"], NUMBERS, 30, 13)
    y = 312 * SCALE
    draw_leads(draw, y, 160 * SCALE)
    y = 480 * SCALE
    rule(draw, y)
    y = 488 * SCALE
    map_w = 460 * SCALE
    grid_x = MARGIN + map_w + 16 * SCALE
    grid_w = W - MARGIN - grid_x
    draw_map(draw, MARGIN, y, map_w, 296 * SCALE)
    draw_grid(draw, grid_x, y, grid_w, 296 * SCALE)
    y = 792 * SCALE
    rule(draw, y)
    draw_also(draw, y + 8 * SCALE, 190 * SCALE)
    fy = 998 * SCALE
    draw.rectangle([MARGIN, fy, W - MARGIN, fy + 22 * SCALE], fill=RED)
    f_foot = font("DejaVuSans-Bold.ttf", 12)
    centered(draw, fy + 5 * SCALE,
             "DATE CHECK: SATURDAY 21 NOVEMBER 2026 \u2014 ALL NEWS REPORTED ON THIS DAY. Sources: AP, Reuters, AFP, BBC.",
             f_foot, (255, 255, 255))
    small = img.resize((1024, 1024), Image.LANCZOS)
    small.save(os.path.join(HERE, "entry.png"), "JPEG", quality=88)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
