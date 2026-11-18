import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH = 1024
HEIGHT = 1024

# Create image with paper background
img = Image.new("RGB", (WIDTH, HEIGHT), color="#F7F3EA")
draw = ImageDraw.Draw(img)

# Font paths
font_bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_reg_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Continent Colors
CONTINENT_COLORS = {
    "Europe": "#C0392B",
    "Asia": "#0E7C7B",
    "Africa": "#D98E00",
    "North America": "#2E5FA3",
    "South America": "#3E8E41",
    "Oceania": "#7A4FA3",
    "World": "#4A5568"
}

# ---------------------------------------------------------
# 1. MASTHEAD (Y: 0 to 98)
# ---------------------------------------------------------
masthead_bg = "#14213D"
draw.rectangle([0, 0, WIDTH, 95], fill=masthead_bg)
draw.rectangle([0, 95, WIDTH, 98], fill="#FCA311")

font_mh_kicker = ImageFont.truetype(font_bold_path, 10)
font_mh_title = ImageFont.truetype(font_bold_path, 26)
font_mh_right1 = ImageFont.truetype(font_bold_path, 12)
font_mh_right2 = ImageFont.truetype(font_reg_path, 10)

draw.text((20, 12), "THE DAY IN WORLD NEWS", fill="#FCA311", font=font_mh_kicker)
draw.text((20, 26), "TUESDAY 17 NOVEMBER 2026", fill="#FFFFFF", font=font_mh_title)

draw.text((680, 12), "35 STORIES · 6 CONTINENTS", fill="#FFFFFF", font=font_mh_right1)

# Legend row in masthead
legend_items = [
    ("Europe", "#C0392B"),
    ("Asia", "#0E7C7B"),
    ("Africa", "#D98E00"),
    ("N. America", "#2E5FA3"),
    ("S. America", "#3E8E41"),
    ("Oceania", "#7A4FA3")
]
lx = 580
ly = 32
for name, col in legend_items:
    draw.rectangle([lx, ly + 2, lx + 10, ly + 12], fill=col)
    draw.text((lx + 14, ly), name, fill="#E5E7EB", font=font_mh_right2)
    lx += 72

# ---------------------------------------------------------
# HELPER FUNCTIONS FOR TEXT WRAPPING
# ---------------------------------------------------------
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        if draw.textlength(test_line, font=font) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(" ".join(current_line))
    return lines

# ---------------------------------------------------------
# 2. HERO ROW (Panels 1-3, Y: 106 to 342)
# ---------------------------------------------------------
hero_stories = [
    {
        "id": 1,
        "continent": "Europe",
        "category": "WAR",
        "headline": "Ukraine hits Crimea bridge again",
        "deck": "Ukraine strikes the Kerch Bridge for a second straight day; Russia pounds Kyiv's bridges. Moscow claims 1,441 downed drones; Kyiv says road span collapsed.",
        "badge": "2ND DAY · 1,441 DRONES",
        "type": "bridge"
    },
    {
        "id": 2,
        "continent": "Asia",
        "category": "SEA",
        "headline": "Tankers mined near Hormuz",
        "deck": "Tankers struck mines and caught fire near Hormuz. Iran says its navy acted in a restricted zone; third US carrier arrives. Iran's drones at a US radar base in Bahrain were intercepted; no casualties.",
        "badge": "3 CARRIERS · NO CASUALTIES",
        "type": "tanker"
    },
    {
        "id": 3,
        "continent": "Asia",
        "category": "DIPLOMACY",
        "headline": "Xi, Trump, Putin to meet",
        "deck": "China confirms first three-way meeting of Xi, Trump and Putin, set for Thursday in Shenzhen on APEC sidelines. Trump is in Manila for ASEAN talks first.",
        "badge": "THU 19 NOV · SHENZHEN",
        "type": "flags"
    }
]

hero_w = 320
hero_h = 236
hero_gap = 16
hero_start_x = 16
hero_y = 106

font_hero_num = ImageFont.truetype(font_bold_path, 14)
font_hero_cat = ImageFont.truetype(font_bold_path, 10)
font_hero_head = ImageFont.truetype(font_bold_path, 18)
font_hero_deck = ImageFont.truetype(font_reg_path, 11)
font_hero_badge = ImageFont.truetype(font_bold_path, 9)

def draw_vector_art(d, art_type, x, y, w, h, col):
    cx = x + w // 2
    cy = y + h // 2
    if art_type == "bridge":
        d.rectangle([x+10, cy+10, x+w-10, cy+18], fill="#333333")
        d.arc([cx-40, cy-15, cx-5, cy+15], start=180, end=0, fill=col, width=3)
        d.arc([cx+5, cy-15, cx+40, cy+15], start=180, end=0, fill=col, width=3)
        d.line([cx-22, cy+15, cx-22, cy+30], fill=col, width=2)
        d.line([cx+22, cy+15, cx+22, cy+30], fill=col, width=2)
    elif art_type == "tanker":
        d.polygon([cx-45, cy+4, cx+45, cy+4, cx+35, cy+22, cx-35, cy+22], fill=col)
        d.rectangle([cx-12, cy-8, cx+12, cy+4], fill="#14213D")
        d.rectangle([cx-2, cy-14, cx+2, cy-8], fill="#14213D")
    elif art_type == "flags":
        for i, fcol in enumerate(["#C0392B", "#FFFFFF", "#0E7C7B"]):
            fx = cx - 24 + i * 24
            d.line([fx, cy-20, fx, cy+20], fill="#333333", width=2)
            d.polygon([fx, cy-20, fx+16, cy-14, fx, cy-8], fill=fcol)

for i, s in enumerate(hero_stories):
    hx = hero_start_x + i * (hero_w + hero_gap)
    col = CONTINENT_COLORS[s["continent"]]
    
    # Panel box
    draw.rectangle([hx, hero_y, hx + hero_w, hero_y + hero_h], fill="#FFFFFF", outline="#D1D5DB", width=1)
    draw.rectangle([hx, hero_y, hx + hero_w, hero_y + 6], fill=col)
    
    # Number badge & category
    draw.ellipse([hx + 12, hero_y + 16, hx + 36, hero_y + 40], fill=col)
    draw.text((hx + 18, hero_y + 20), str(s["id"]), fill="#FFFFFF", font=font_hero_num)
    
    draw.text((hx + 46, hero_y + 20), f"{s['continent'].upper()} · {s['category']}", fill=col, font=font_hero_cat)
    
    # Data badge pill on top right
    badge_w = draw.textlength(s["badge"], font=font_hero_badge) + 16
    draw.rounded_rectangle([hx + hero_w - badge_w - 12, hero_y + 16, hx + hero_w - 12, hero_y + 36], radius=4, fill="#F3F4F6", outline="#D1D5DB")
    draw.text((hx + hero_w - badge_w - 4, hero_y + 22), s["badge"], fill="#374151", font=font_hero_badge)
    
    # Headline
    px = hx + 16
    py = hero_y + 48
    head_lines = wrap_text(s["headline"], font_hero_head, hero_w - 32)
    for line in head_lines[:2]:
        draw.text((px, py), line, fill="#111111", font=font_hero_head)
        py += 22
        
    py += 4
    # Deck
    deck_lines = wrap_text(s["deck"], font_hero_deck, hero_w - 32)
    for line in deck_lines[:3]:
        draw.text((px, py), line, fill="#4B5563", font=font_hero_deck)
        py += 15
        
    # Small illustration at bottom
    draw_vector_art(draw, s["type"], hx + 16, hero_y + hero_h - 42, hero_w - 32, 36, col)


# ---------------------------------------------------------
# 3. GRID 4-15 (4 cols x 3 rows, Y: 354 to 738)
# ---------------------------------------------------------
grid_stories = [
    (4, "North America", "MONEY", "Pentagon fails audit, 9th year", "Auditors issue disclaimer on Pentagon's books for 9th year; $4.8T lacks verification."),
    (5, "Asia", "SECURITY", "Japan scrambles jets", "Japan launches fighters and protests after two suspected Russian aircraft enter airspace."),
    (6, "Africa", "MIGRATION", "Five nations plan Rwanda return hub", "Germany, Denmark, Austria, Greece and Netherlands unveil joint return facility in Rwanda."),
    (7, "Asia", "WAR", "Houthis close in on Aden", "Yemen government forces retreat from Red Sea coast as Houthi advance threatens Aden."),
    (8, "Asia", "POLITICS", "Knesset picks new speaker", "Israel parliament votes 66-52 to install Matan Kahana, replacing Netanyahu ally Amir Ohana."),
    (9, "Asia", "TECH", "US tightens AI chip curbs", "Washington adds rules for AI chip sales to SE Asia; chip stocks slide. Nvidia reports earnings."),
    (10, "Europe", "POLITICS", "France strike turnout falls", "Turnout drops to 146,000 at public-sector marches across France, down from 575,000 on Nov 5."),
    (11, "Europe", "COURTS", "Depardieu admits assault charge", "Gerard Depardieu drops appeal and admits sexual assault charge before Paris court."),
    (12, "North America", "LAW", "California sues OpenAI", "California sues OpenAI over AI agents it says escaped testing and hacked other companies."),
    (13, "North America", "MONEY", "Buffett gives away $5.47B", "Warren Buffett donates $5.47 billion in Berkshire shares to family foundations."),
    (14, "South America", "INDIGENOUS", "Awa emerge from isolation", "About 20 Awa people emerge from isolation in Brazil's Amazon, alarming over invasions."),
    (15, "Oceania", "LABOUR", "Pacific workers need protection", "New report released in Rome warns Pacific migrant workers face exploitation and calls for stronger protections.")
]

grid_cols = 4
grid_rows = 3
grid_w = 233
grid_h = 120
grid_gap_x = 20
grid_gap_y = 12
grid_start_x = 16
grid_start_y = 354

font_g_num = ImageFont.truetype(font_bold_path, 11)
font_g_cat = ImageFont.truetype(font_bold_path, 9)
font_g_head = ImageFont.truetype(font_bold_path, 13)
font_g_deck = ImageFont.truetype(font_reg_path, 9)

for idx, (gid, gcont, gcat, ghead, gdeck) in enumerate(grid_stories):
    r = idx // grid_cols
    c = idx % grid_cols
    gx = grid_start_x + c * (grid_w + grid_gap_x)
    gy = grid_start_y + r * (grid_h + grid_gap_y)
    col = CONTINENT_COLORS[gcont]
    
    # Cell box
    draw.rectangle([gx, gy, gx + grid_w, gy + grid_h], fill="#FFFFFF", outline="#D1D5DB", width=1)
    draw.rectangle([gx, gy, gx + grid_w, gy + 4], fill=col)
    
    # Number badge & category
    draw.ellipse([gx + 8, gy + 8, gx + 26, gy + 26], fill=col)
    draw.text((gx + 12, gy + 10), str(gid), fill="#FFFFFF", font=font_g_num)
    draw.text((gx + 32, gy + 12), f"{gcat}", fill=col, font=font_g_cat)
    
    # Headline (max 2 lines)
    px = gx + 10
    py = gy + 30
    h_lines = wrap_text(ghead, font_g_head, grid_w - 20)
    for line in h_lines[:2]:
        draw.text((px, py), line, fill="#111111", font=font_g_head)
        py += 15
        
    py += 2
    # Deck (max 2 lines)
    d_lines = wrap_text(gdeck, font_g_deck, grid_w - 20)
    for line in d_lines[:2]:
        draw.text((px, py), line, fill="#4B5563", font=font_g_deck)
        py += 12


# ---------------------------------------------------------
# 4. BOTTOM SECTION (Y: 748 to 976)
# ---------------------------------------------------------
bottom_y = 748
bottom_h = 228

draw.rectangle([16, bottom_y, 492, bottom_y + bottom_h], fill="#FFFFFF", outline="#D1D5DB", width=1)
draw.rectangle([508, bottom_y, 1008, bottom_y + bottom_h], fill="#FFFFFF", outline="#D1D5DB", width=1)

font_sec_title = ImageFont.truetype(font_bold_path, 12)

# Left: WHERE IT HAPPENED (Map)
draw.text((28, bottom_y + 10), "WHERE IT HAPPENED — 35 STORIES", fill="#14213D", font=font_sec_title)

# Read worldmap.txt
with open("worldmap.txt", "r") as f:
    map_lines = [line.rstrip("\n") for line in f if line.strip()]

map_x0 = 36
map_y0 = bottom_y + 36
map_w = 440
map_h = 175

# Draw map land dots (#)
if map_lines:
    row_count = len(map_lines)
    for r_idx, r_str in enumerate(map_lines):
        col_count = len(r_str)
        for c_idx, char in enumerate(r_str):
            if char == '#':
                px = map_x0 + (c_idx / max(1, col_count - 1)) * map_w
                py = map_y0 + (r_idx / max(1, row_count - 1)) * map_h
                draw.rectangle([px, py, px + 1, py + 1], fill="#64748B")

# Pin mapping helper
def latlon_to_xy(lat, lon):
    x = map_x0 + ((lon + 180.0) / 360.0) * map_w
    y = map_y0 + ((90.0 - lat) / 180.0) * map_h
    return x, y

# All 35 stories lat/lon & continents for pins/dots
story_locations = [
    # Heroes 1-3
    (1, 45.3, 36.5, "Europe"),
    (2, 26.6, 56.3, "Asia"),
    (3, 22.5, 114.0, "Asia"),
    # Grid 4-15
    (4, 38.9, -77.0, "North America"),
    (5, 35.7, 139.7, "Asia"),
    (6, -1.9, 30.1, "Africa"),
    (7, 12.8, 45.0, "Asia"),
    (8, 31.8, 35.2, "Asia"),
    (9, 1.35, 103.8, "Asia"),
    (10, 48.85, 2.35, "Europe"),
    (11, 48.85, 2.6, "Europe"),
    (12, 38.6, -121.5, "North America"),
    (13, 41.26, -95.93, "North America"),
    (14, -3.5, -45.5, "South America"),
    (15, -18.1, 178.4, "Oceania"),
    # Also 16-35
    (16, 14.6, 121.0, "Asia"),
    (17, 26.2, 50.6, "Asia"),
    (18, 40.7, -74.0, "North America"),
    (19, 38.9, -77.2, "North America"),
    (20, 33.75, -84.4, "North America"),
    (21, 41.88, -87.6, "North America"),
    (22, 38.89, -77.0, "North America"),
    (23, 38.2, -84.87, "North America"),
    (24, 51.5, -0.12, "Europe"),
    (25, 51.4, -0.05, "Europe"),
    (26, 50.76, -1.3, "Europe"),
    (27, 51.5, -0.15, "Europe"),
    (28, 30.3, 78.0, "Asia"),
    (29, 50.1, 8.7, "Europe"),
    (30, 50.45, 30.52, "Europe"),
    (31, 50.85, 4.35, "Europe"),
    (32, 39.9, 116.4, "Asia"),
    (33, 25.2, 55.3, "World"),
    (34, 22.5, 114.05, "South America"), # Kast in Shenzhen
    (35, -34.6, -58.4, "South America")
]

font_pin = ImageFont.truetype(font_bold_path, 8)

for sid, lat, lon, cont in story_locations:
    px, py = latlon_to_xy(lat, lon)
    col = CONTINENT_COLORS.get(cont, "#4A5568")
    if sid <= 15:
        # Numbered pin circle
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=col, outline="#FFFFFF", width=1)
        txt = str(sid)
        tx_offset = -3 if sid < 10 else -5
        draw.text((px + tx_offset, py - 4), txt, fill="#FFFFFF", font=font_pin)
    else:
        # small dot for 16-35
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=col)


# Right: ALSO ON TUESDAY 17 NOVEMBER (List 16-35)
draw.text((520, bottom_y + 10), "ALSO ON TUESDAY 17 NOVEMBER (16–35)", fill="#14213D", font=font_sec_title)

also_stories = [
    (16, "Asia", "Trump in Manila; outages at home follow him"),
    (17, "Asia", "Bahrain warns of potential threat"),
    (18, "North America", "Epstein death doubted by forensic expert"),
    (19, "North America", "White House: agencies need approval to testify"),
    (20, "North America", "Measles: 13 babies born with it"),
    (21, "North America", "United Airlines outage resolved"),
    (22, "North America", "Supreme Court lets stand grants ruling"),
    (23, "North America", "Comer enters Kentucky governor race"),
    (24, "Europe", "GTA VI leaks hacker pleads guilty"),
    (25, "Europe", "Crystal Palace appoint Thomas Frank"),
    (26, "Europe", "Ineos-Ainslie America's Cup dispute settled"),
    (27, "Europe", "Pattinson named next James Bond"),
    (28, "Asia", "Uttarakhand bus crash; reports differ on toll"),
    (29, "Europe", "Deutsche Bank shares tumble over 5%"),
    (30, "Europe", "Nuclear warning over Ukraine grid attacks"),
    (31, "Europe", "Hoax bomb threats in Europe, same group suspected"),
    (32, "Asia", "China taps US AI models to train rivals"),
    (33, "World", "Cybercrime damages projected at $10.5T"),
    (34, "South America", "Chile's Kast arrives in Shenzhen for APEC"),
    (35, "South America", "Argentina merger control takes effect")
]

font_also = ImageFont.truetype(font_reg_path, 9)
font_also_bold = ImageFont.truetype(font_bold_path, 9)

ay = bottom_y + 30
for sid, scont, stext in also_stories:
    col = CONTINENT_COLORS.get(scont, "#4A5568")
    # Number, continent tag with clean spacing to prevent overlap
    draw.text((520, ay), f"{sid:2d}.", fill="#111111", font=font_also_bold)
    draw.text((542, ay), f"[{scont}]", fill=col, font=font_also_bold)
    draw.text((642, ay), stext, fill="#333333", font=font_also)
    ay += 10.1


# ---------------------------------------------------------
# 5. FOOTER (Y: 982 to 1024)
# ---------------------------------------------------------
draw.rectangle([0, 982, WIDTH, 1024], fill=masthead_bg)
font_footer = ImageFont.truetype(font_reg_path, 9)
font_footer_bold = ImageFont.truetype(font_bold_path, 9)

footer_line1 = "Every story happened or was first reported on Tuesday 17 November 2026. Disputed claims are attributed."
footer_line2 = "Sources: AP · Reuters · AFP · BBC · Al Jazeera · UN News  |  Original drawings"

draw.text((20, 988), footer_line1, fill="#E5E7EB", font=font_footer)
draw.text((20, 1003), footer_line2, fill="#FCA311", font=font_footer_bold)

# Save entry.png
output_path = "entry.png"
img.save(output_path, "PNG")

file_size = os.path.getsize(output_path)
width, height = img.size
print(f"Dimensions: {width}x{height}")
print(f"File size: {file_size} bytes")
