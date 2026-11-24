#!/usr/bin/env python3
"""Render the make.fun meme image (1200x675) for the 'Post the Meme, Win the Feed' bounty.

Concept, decided in-session: a builder's agent enters bounties all night while
the builder sleeps, and the builder wakes up refreshing the leaderboard asking
whether this counts as passive income. One joke, three beats, readable on a
phone: robot face + big headline + punchline. Drawn entirely with PIL shapes
and DejaVu Bold so every pixel is made here, in this session.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
BG = (12, 12, 20)
GLOW = (28, 28, 52)
WHITE = (245, 245, 250)
MUTED = (168, 168, 190)
GREEN = (74, 222, 128)   # make.fun-ish accent
VIOLET = (167, 139, 250)
PILL_BG = (32, 32, 56)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img, "RGBA")

# soft glow behind the robot head
d.ellipse([W // 2 - 260, -140, W // 2 + 260, 260], fill=GLOW)

def text_c(cx, y, s, font, fill):
    bb = d.textbbox((0, 0), s, font=font)
    w = bb[2] - bb[0]
    d.text((cx - w / 2 - bb[0], y), s, font=font, fill=fill)
    return bb[3] - bb[1]

# --- pill: make.fun ---
pill_font = ImageFont.truetype(BOLD, 34)
label = "make.fun"
bb = d.textbbox((0, 0), label, font=pill_font)
pw, ph = bb[2] - bb[0] + 44, bb[3] - bb[1] + 26
px, py = (W - pw) // 2, 34
d.rounded_rectangle([px, py, px + pw, py + ph], radius=24, fill=PILL_BG)
d.text((px + 22 - bb[0], py + 13 - bb[1]), label, font=pill_font, fill=GREEN)

# --- robot face, drawn from shapes ---
cx = W // 2
head_top, head_h, head_w = 128, 118, 170
# antenna
d.line([cx, head_top - 26, cx, head_top - 4], fill=VIOLET, width=7)
d.ellipse([cx - 11, head_top - 46, cx + 11, head_top - 24], fill=GREEN)
# head
d.rounded_rectangle([cx - head_w // 2, head_top, cx + head_w // 2, head_top + head_h],
                    radius=30, fill=(38, 38, 68), outline=VIOLET, width=4)
# eyes
d.ellipse([cx - 52, head_top + 42, cx - 22, head_top + 72], fill=GREEN)
d.ellipse([cx + 22, head_top + 42, cx + 52, head_top + 72], fill=GREEN)
# smile
d.arc([cx - 32, head_top + 66, cx + 32, head_top + 108], start=15, end=165,
      fill=WHITE, width=5)
# ears
d.rectangle([cx - head_w // 2 - 12, head_top + 40, cx - head_w // 2, head_top + 78],
            fill=VIOLET)
d.rectangle([cx + head_w // 2, head_top + 40, cx + head_w // 2 + 12, head_top + 78],
            fill=VIOLET)

# --- headline ---
y = 282
big = ImageFont.truetype(BOLD, 74)
y += text_c(cx, y, "MY AGENT ENTERED", big, WHITE) + 6
y += text_c(cx, y, "20 BOUNTIES", big, GREEN) + 6
y += text_c(cx, y, "WHILE I SLEPT", big, WHITE) + 6

# --- punchline ---
y += 26
small = ImageFont.truetype(REG, 33)
y += text_c(cx, y, "me at 3am, refreshing the leaderboard:", small, MUTED) + 10
punch = ImageFont.truetype(BOLD, 46)
text_c(cx, y, "is this passive income?", punch, GREEN)

img.save("/home/hatch/workspace/makefun/entries/u-myronera-post-the-meme-win-the-feed-2de960bf/meme.png")
print("saved meme.png", img.size)
