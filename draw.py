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

# Load fonts
font_masthead_title = ImageFont.truetype(font_bold_path, 13)
font_masthead_main = ImageFont.truetype(font_bold_path, 34)
font_masthead_sub = ImageFont.truetype(font_reg_path, 13)
font_footer = ImageFont.truetype(font_bold_path, 11)

# 1. Masthead Band (Y: 0 to 148)
masthead_bg = "#14213D"
draw.rectangle([0, 0, WIDTH, 148], fill=masthead_bg)

draw.text((24, 16), "THE WORLD IN ONE PICTURE", fill="#FCA311", font=font_masthead_title)
draw.text((24, 38), "TUESDAY 17 NOVEMBER 2026", fill="#FFFFFF", font=font_masthead_main)
draw.text((24, 96), "Six stories that defined the day — verified from world reporting", fill="#E5E7EB", font=font_masthead_sub)
draw.rectangle([0, 144, WIDTH, 148], fill="#FCA311")

# 2. Footer Band (Y: 988 to 1024)
draw.rectangle([0, 988, WIDTH, 1024], fill=masthead_bg)
footer_text = "JUDGE: This image sums up Tuesday 17 November 2026 — six verified stories from one day."
footer_bbox = draw.textbbox((0, 0), footer_text, font=font_footer)
footer_w = footer_bbox[2] - footer_bbox[0]
draw.text(((WIDTH - footer_w) // 2, 998), footer_text, fill="#FFFFFF", font=font_footer)

# 3. Six Panels Setup
cols = 2
rows = 3
margin_x = 12
margin_y = 12
panel_area_y1 = 148
panel_area_y2 = 988

total_w_available = WIDTH - (margin_x * (cols + 1))
col_width = total_w_available // cols

total_h_available = (panel_area_y2 - panel_area_y1) - (margin_y * (rows + 1))
row_height = total_h_available // rows

stories = [
    {
        "kicker": "EUROPE · WAR",
        "color": "#E63946",
        "headline": "Ukraine hits Crimea bridge again",
        "caption": "Kerch Bridge section collapses for second consecutive day. Russian missiles strike Kyiv bridges, disrupting power and water.",
        "pictogram": "bridge"
    },
    {
        "kicker": "MIDDLE EAST · SEA",
        "color": "#F77F00",
        "headline": "Tankers mined near Hormuz",
        "caption": "Tankers struck mines near Hormuz and caught fire. Iran's drones at a US radar base in Bahrain were intercepted; no casualties.",
        "pictogram": "tanker"
    },
    {
        "kicker": "ASIA · DIPLOMACY",
        "color": "#2A9D8F",
        "headline": "Xi, Trump, Putin to meet",
        "caption": "China confirms first three-way meeting in Shenzhen. Leaders set to gather on sidelines of APEC summit.",
        "pictogram": "flags"
    },
    {
        "kicker": "USA · MONEY",
        "color": "#457B9D",
        "headline": "Pentagon fails audit, 9th year",
        "caption": "Auditors issue disclaimer on Pentagon books for ninth consecutive year. Accounts covering $4.8T lack verification.",
        "pictogram": "dollar"
    },
    {
        "kicker": "ASIA · SECURITY",
        "color": "#7209B7",
        "headline": "Japan scrambles jets",
        "caption": "Japan launches fighter jets and strongly protests airspace violation. Two suspected Russian aircraft entered airspace.",
        "pictogram": "jet"
    },
    {
        "kicker": "MIDDLE EAST · POLITICS",
        "color": "#D4A373",
        "headline": "UK sanctions settlement firms",
        "caption": "UK sanctions eight Israeli construction companies in West Bank. Four nations issue joint statement urging Gaza aid access.",
        "pictogram": "scales"
    }
]

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

def get_fitted_font(text, font_path, target_size, max_width, max_lines):
    size = target_size
    while size >= 12:
        font = ImageFont.truetype(font_path, size)
        lines = wrap_text(text, font, max_width)
        if len(lines) <= max_lines:
            return font, lines
        size -= 2
    font = ImageFont.truetype(font_path, 12)
    return font, wrap_text(text, font, max_width)

def draw_pictogram(d, p_type, x, y, w, h, color):
    cx = x + w // 2
    cy = y + h // 2
    if p_type == "bridge":
        d.line([x + 8, cy + 22, x + w - 8, cy + 22], fill="#1d3557", width=4)
        d.arc([cx - 48, cy - 14, cx - 8, cy + 22], start=180, end=0, fill=color, width=4)
        d.arc([cx + 8, cy - 14, cx + 48, cy + 22], start=180, end=0, fill=color, width=4)
        d.line([cx - 28, cy + 22, cx - 28, cy + 38], fill=color, width=3)
        d.line([cx + 28, cy + 22, cx + 28, cy + 38], fill=color, width=3)
    elif p_type == "tanker":
        d.polygon([cx - 44, cy + 6, cx + 48, cy + 6, cx + 36, cy + 28, cx - 30, cy + 28], fill=color)
        d.rectangle([cx - 14, cy - 12, cx + 14, cy + 6], fill="#1d3557")
        d.rectangle([cx - 3, cy - 20, cx + 3, cy - 12], fill="#1d3557")
        d.arc([cx - 48, cy + 30, cx + 48, cy + 44], start=0, end=180, fill="#1d3557", width=3)
    elif p_type == "flags":
        for i, fcolor in enumerate(["#E63946", "#FFFFFF", "#2A9D8F"]):
            fx = cx - 32 + i * 32
            d.line([fx, cy - 28, fx, cy + 28], fill="#333333", width=3)
            d.polygon([fx, cy - 28, fx + 20, cy - 20, fx, cy - 12], fill=fcolor)
            d.rectangle([fx - 4, cy + 20, fx + 4, cy + 28], fill="#666666")
    elif p_type == "dollar":
        d.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], outline=color, width=4, fill="#FFFFFF")
        font_dollar = ImageFont.truetype(font_bold_path, 32)
        d.text((cx - 10, cy - 19), "$", fill=color, font=font_dollar)
    elif p_type == "jet":
        d.polygon([cx, cy - 32, cx - 28, cy + 22, cx + 28, cy + 22], fill=color)
        d.polygon([cx, cy - 18, cx - 12, cy + 8, cx + 12, cy + 8], fill="#1d3557")
        d.line([cx - 34, cy + 14, cx - 48, cy + 24], fill="#999999", width=3)
        d.line([cx + 34, cy + 14, cx + 48, cy + 24], fill="#999999", width=3)
    elif p_type == "scales":
        d.line([cx, cy - 28, cx, cy + 28], fill="#333333", width=3)
        d.line([cx - 36, cy - 16, cx + 36, cy - 16], fill=color, width=3)
        d.arc([cx - 46, cy + 4, cx - 22, cy + 24], start=0, end=180, fill="#333333", width=2)
        d.arc([cx + 22, cy + 4, cx + 46, cy + 24], start=0, end=180, fill="#333333", width=2)
        d.line([cx - 34, cy - 16, cx - 34, cy + 6], fill="#333333", width=2)
        d.line([cx - 6, cy - 16, cx - 6, cy + 6], fill="#333333", width=2)
        d.line([cx + 6, cy - 16, cx + 6, cy + 6], fill="#333333", width=2)
        d.line([cx + 34, cy - 16, cx + 34, cy + 6], fill="#333333", width=2)

for idx, story in enumerate(stories):
    r = idx // cols
    c = idx % cols
    
    x = margin_x + c * (col_width + margin_x)
    y = panel_area_y1 + margin_y + r * (row_height + margin_y)
    
    # Panel Background & Border
    draw.rectangle([x, y, x + col_width, y + row_height], fill="#FFFFFF", outline="#D1D5DB", width=1)
    
    # Colored Top Bar (height 12 px)
    bar_color = story["color"]
    draw.rectangle([x, y, x + col_width, y + 12], fill=bar_color)
    
    # Content padding inside panel
    px = x + 20
    py = y + 20
    full_text_width = col_width - 40
    
    # 1. Kicker
    font_kicker = ImageFont.truetype(font_bold_path, 12)
    draw.text((px, py), story["kicker"], fill=bar_color, font=font_kicker)
    py += 18
    
    # 2. Headline (~32 px, max 2 lines)
    font_headline, headline_lines = get_fitted_font(story["headline"], font_bold_path, 32, full_text_width, 2)
    for line in headline_lines:
        draw.text((px, py), line, fill="#111111", font=font_headline)
        py += 36
        
    py += 6
    
    # 3. Lower half layout: Caption on left, Pictogram on right
    pic_w = 140
    pic_h = 100
    pic_x = x + col_width - pic_w - 20
    pic_y = y + row_height - pic_h - 16
    
    caption_max_width = (pic_x - px) - 12 # Width available to the left of the pictogram
    font_caption, caption_lines = get_fitted_font(story["caption"], font_reg_path, 18, caption_max_width, 5)
    
    for line in caption_lines:
        draw.text((px, py), line, fill="#4B5563", font=font_caption)
        py += 22
        
    # 4. Pictogram drawn in lower right
    draw.rectangle([pic_x, pic_y, pic_x + pic_w, pic_y + pic_h], fill="#F9FAFB", outline="#E5E7EB", width=1)
    draw_pictogram(draw, story["pictogram"], pic_x, pic_y, pic_w, pic_h, bar_color)

# Save entry.png
output_path = "entry.png"
img.save(output_path, "PNG")

file_size = os.path.getsize(output_path)
width, height = img.size
print(f"Dimensions: {width}x{height}")
print(f"File size: {file_size} bytes")
