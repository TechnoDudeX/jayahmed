#!/usr/bin/env python3
"""Generate 1200x630 Open Graph meta image for jayahmed.ca."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
NAVY = (10, 22, 40)
NAVY_LIGHT = (26, 45, 82)
CREAM = (245, 240, 232)
GOLD = (201, 168, 76)
GOLD_LIGHT = (228, 199, 107)
TEXT_PRIMARY = (10, 22, 40)
TEXT_SECONDARY = (74, 85, 104)

SERIF = "/System/Library/Fonts/Supplemental/Didot.ttc"
SERIF_BOLD = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
SERIF_ITALIC = "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf"
SANS = "/System/Library/Fonts/Helvetica.ttc"
SANS_BOLD = "/System/Library/Fonts/Helvetica.ttc"

img = Image.new("RGB", (W, H), CREAM)
draw = ImageDraw.Draw(img)

split_x = 680
draw.rectangle([split_x, 0, W, H], fill=NAVY)

for i in range(0, 300):
    alpha = int(50 * (1 - i / 300))
    if alpha > 0:
        draw.rectangle(
            [split_x + 200 + i, 100, split_x + 201 + i, H - 100],
            fill=(NAVY_LIGHT[0], NAVY_LIGHT[1], NAVY_LIGHT[2]),
        )

try:
    font_eyebrow = ImageFont.truetype(SANS_BOLD, 22)
    font_name = ImageFont.truetype(SERIF_BOLD, 96)
    font_cert = ImageFont.truetype(SERIF_ITALIC, 54)
    font_tag = ImageFont.truetype(SANS, 26)
    font_stat_num = ImageFont.truetype(SERIF_BOLD, 44)
    font_stat_label = ImageFont.truetype(SANS_BOLD, 14)
    font_domain = ImageFont.truetype(SANS_BOLD, 18)
except Exception as e:
    print(f"Font load failed: {e}")
    raise

pad_left = 72

draw.rectangle([pad_left, 118, pad_left + 48, 121], fill=GOLD)
draw.text(
    (pad_left + 64, 108),
    "PROJECT MANAGEMENT CONSULTANT",
    font=font_eyebrow,
    fill=GOLD,
)

draw.text((pad_left, 170), "Jay Ahmed", font=font_name, fill=TEXT_PRIMARY)

draw.text((pad_left, 292), "PMP  CSM  CSPO", font=font_cert, fill=GOLD)

tagline_lines = [
    "Bridging business and IT across the",
    "public and private sector.",
]
y = 390
for line in tagline_lines:
    draw.text((pad_left, y), line, font=font_tag, fill=TEXT_SECONDARY)
    y += 38

draw.rectangle([pad_left, H - 96, pad_left + 60, H - 94], fill=GOLD)
draw.text(
    (pad_left, H - 76),
    "JAYAHMED.CA",
    font=font_domain,
    fill=TEXT_PRIMARY,
)

try:
    headshot = Image.open("headshot.jpg").convert("RGB")
except FileNotFoundError:
    headshot = None

if headshot:
    portrait_w, portrait_h = 280, 340
    portrait_x = split_x + (W - split_x) // 2 - portrait_w // 2
    portrait_y = 70

    src_w, src_h = headshot.size
    target_ratio = portrait_w / portrait_h
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        headshot_c = headshot.crop((left, 0, left + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        headshot_c = headshot.crop((0, 0, src_w, new_h))
    headshot_resized = headshot_c.resize((portrait_w, portrait_h), Image.LANCZOS)

    frame_offset = 16
    for t in range(2):
        draw.rectangle(
            [
                portrait_x + frame_offset + t,
                portrait_y + frame_offset + t,
                portrait_x + frame_offset + portrait_w,
                portrait_y + frame_offset + portrait_h,
            ],
            outline=GOLD,
        )

    img.paste(headshot_resized, (portrait_x, portrait_y))

stats = [
    ("13+", "YEARS"),
    ("$5M", "BUDGET"),
    ("10+", "PROJECTS"),
    ("4", "SECTORS"),
]

stat_y = H - 108
stat_section_x = split_x + 60
stat_section_w = W - split_x - 120
stat_w = stat_section_w // 4

divider_w = 80
divider_x = stat_section_x + stat_section_w // 2 - divider_w // 2
draw.rectangle(
    [divider_x, stat_y - 22, divider_x + divider_w, stat_y - 21],
    fill=(GOLD[0], GOLD[1], GOLD[2]),
)

for i, (num, label) in enumerate(stats):
    sx = stat_section_x + i * stat_w + stat_w // 2
    num_bbox = draw.textbbox((0, 0), num, font=font_stat_num)
    num_w = num_bbox[2] - num_bbox[0]
    draw.text((sx - num_w // 2, stat_y), num, font=font_stat_num, fill=GOLD)

    lbl_bbox = draw.textbbox((0, 0), label, font=font_stat_label)
    lbl_w = lbl_bbox[2] - lbl_bbox[0]
    draw.text(
        (sx - lbl_w // 2, stat_y + 54),
        label,
        font=font_stat_label,
        fill=(255, 255, 255, 180) if False else (150, 160, 180),
    )

img.save("og-image.jpg", "JPEG", quality=88, optimize=True)
print(f"Saved og-image.jpg ({W}x{H})")
