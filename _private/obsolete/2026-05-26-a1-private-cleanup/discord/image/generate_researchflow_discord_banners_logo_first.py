from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
W, H = 680, 240
SCALE = 3


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size * SCALE)
    return ImageFont.load_default()


def bg(c1: tuple[int, int, int], c2: tuple[int, int, int], c3: tuple[int, int, int] | None = None) -> Image.Image:
    img = Image.new("RGBA", (W * SCALE, H * SCALE), (0, 0, 0, 255))
    px = img.load()
    for y in range(img.size[1]):
        yy = y / (img.size[1] - 1)
        for x in range(img.size[0]):
            xx = x / (img.size[0] - 1)
            t = min(1, max(0, xx * 0.78 + yy * 0.22))
            if c3 and t > 0.54:
                u = (t - 0.54) / 0.46
                a, b = c2, c3
            else:
                u = t / 0.54 if c3 else t
                a, b = c1, c2
            px[x, y] = tuple(int(a[i] * (1 - u) + b[i] * u) for i in range(3)) + (255,)
    return img


def add_noise(img: Image.Image, seed: int, amount: int = 12) -> None:
    rng = random.Random(seed)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    pix = layer.load()
    for y in range(0, img.size[1], 2):
        for x in range(0, img.size[0], 2):
            pix[x, y] = (255, 255, 255, rng.randint(0, amount))
    img.alpha_composite(layer)


def draw_text(d: ImageDraw.ImageDraw, xy, value: str, size: int, fill, bold=False, anchor=None):
    d.text((xy[0] * SCALE, xy[1] * SCALE), value, font=font(size, bold), fill=fill, anchor=anchor)


def rounded(d: ImageDraw.ImageDraw, xy, fill, outline=None, width=1, radius=14):
    d.rounded_rectangle(tuple(int(v * SCALE) for v in xy), radius=radius * SCALE, fill=fill, outline=outline, width=width * SCALE)


def line(d: ImageDraw.ImageDraw, pts, fill, width=2):
    d.line([(int(x * SCALE), int(y * SCALE)) for x, y in pts], fill=fill, width=width * SCALE)


def circle(d: ImageDraw.ImageDraw, xy, r, fill, outline=None, width=1):
    x, y = xy
    d.ellipse([(x - r) * SCALE, (y - r) * SCALE, (x + r) * SCALE, (y + r) * SCALE], fill=fill, outline=outline, width=width * SCALE)


def glow(img: Image.Image, xy, r, color, alpha=95):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = xy
    d.ellipse([(x - r) * SCALE, (y - r) * SCALE, (x + r) * SCALE, (y + r) * SCALE], fill=color[:3] + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(r * SCALE * 0.48))
    img.alpha_composite(layer)


def logo(max_w: int, max_h: int, opacity: int = 255) -> Image.Image:
    im = Image.open(ROOT / "assets" / "LOGO.png").convert("RGBA")
    im.thumbnail((max_w * SCALE, max_h * SCALE), Image.Resampling.LANCZOS)
    if opacity < 255:
        a = im.getchannel("A").point(lambda p: int(p * opacity / 255))
        im.putalpha(a)
    return im


def paste_logo(img: Image.Image, xy, max_w: int, max_h: int, opacity=255, shadow=True):
    im = logo(max_w, max_h, opacity)
    x, y = int(xy[0] * SCALE), int(xy[1] * SCALE)
    if shadow:
        shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        s = Image.new("RGBA", im.size, (0, 0, 0, 0))
        s.putalpha(im.getchannel("A").point(lambda p: int(p * 0.34)))
        shadow_layer.alpha_composite(s, (x + 9 * SCALE, y + 12 * SCALE))
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(10 * SCALE))
        img.alpha_composite(shadow_layer)
    img.alpha_composite(im, (x, y))


def graph(d: ImageDraw.ImageDraw, nodes, color=(125, 211, 252, 185), accent=(52, 211, 153, 230)):
    edges = [(0, 1), (1, 2), (1, 3), (3, 4), (2, 5), (4, 6), (5, 6)]
    for a, b in edges:
        if a < len(nodes) and b < len(nodes):
            line(d, [nodes[a], nodes[b]], color[:3] + (82,), width=2)
    for i, pt in enumerate(nodes):
        c = accent if i in {1, 4, 6} else color
        circle(d, pt, 8 if i != 1 else 12, (7, 12, 24, 225), outline=c, width=2)


def save(img: Image.Image, name: str) -> Path:
    out = OUT / name
    img.resize((W, H), Image.Resampling.LANCZOS).convert("RGB").save(out, "PNG", optimize=True)
    return out


def banner_01_logo_orbit():
    img = bg((6, 12, 28), (14, 47, 73), (8, 93, 88))
    add_noise(img, 11)
    d = ImageDraw.Draw(img)
    glow(img, (150, 120), 132, (56, 189, 248), 85)
    glow(img, (450, 42), 118, (52, 211, 153), 54)
    for y in range(18, 230, 28):
        line(d, [(0, y), (680, y + 10)], (255, 255, 255, 12), 1)
    paste_logo(img, (24, 22), 226, 188)
    draw_text(d, (286, 82), "ResearchFlow", 39, (248, 250, 252, 255), True)
    draw_text(d, (289, 121), "Evidence-grounded research memory", 16, (203, 213, 225, 238))
    rounded(d, (290, 151, 530, 181), (15, 23, 42, 150), outline=(125, 211, 252, 90), radius=15)
    draw_text(d, (306, 158), "papers -> evidence -> ideas", 13, (147, 197, 253, 245), True)
    graph(d, [(584, 66), (622, 82), (652, 58), (598, 128), (635, 146), (662, 110), (656, 188)])
    return save(img, "researchflow_discord_banner_logo_01_orbit.png")


def banner_02_community_launch():
    img = bg((30, 35, 82), (88, 101, 242), (22, 163, 184))
    add_noise(img, 12, 10)
    d = ImageDraw.Draw(img)
    glow(img, (560, 190), 130, (34, 211, 238), 70)
    rounded(d, (34, 30, 246, 210), (255, 255, 255, 42), outline=(255, 255, 255, 72), radius=22)
    paste_logo(img, (44, 47), 184, 150)
    draw_text(d, (284, 78), "ResearchFlow", 38, (255, 255, 255, 255), True)
    draw_text(d, (286, 116), "Community for knowledge-grounded research", 15, (236, 244, 255, 238))
    for i, label in enumerate(["Papers", "Agents", "Obsidian"]):
        x = 286 + i * 104
        rounded(d, (x, 151, x + 90, 183), (255, 255, 255, 48), outline=(255, 255, 255, 74), radius=16)
        draw_text(d, (x + 45, 159), label, 11, (22, 31, 59, 245), True, anchor="ma")
    return save(img, "researchflow_discord_banner_logo_02_community.png")


def banner_03_graph_memory():
    img = bg((8, 13, 25), (23, 37, 84), (76, 29, 149))
    add_noise(img, 13, 15)
    d = ImageDraw.Draw(img)
    glow(img, (490, 86), 140, (168, 85, 247), 74)
    paste_logo(img, (474, 34), 184, 152, opacity=236)
    for i in range(6):
        x = 52 + i * 42
        y = 40 + int(math.sin(i) * 12)
        rounded(d, (x, y, x + 56, y + 52), (15, 23, 42, 178), outline=(148, 163, 184, 58), radius=9)
        rounded(d, (x + 10, y + 14, x + 42, y + 19), (226, 232, 240, 105), radius=3)
        rounded(d, (x + 10, y + 29, x + 34, y + 34), (148, 163, 184, 88), radius=3)
    graph(d, [(76, 211), (132, 196), (196, 215), (256, 198), (316, 217), (378, 199), (430, 224)], color=(196, 181, 253, 135), accent=(56, 189, 248, 190))
    draw_text(d, (52, 112), "ResearchFlow", 37, (248, 250, 252, 255), True)
    draw_text(d, (55, 149), "Paper analysis -> agent-readable memory", 15, (226, 232, 240, 238))
    draw_text(d, (55, 178), "local-first  |  source-grounded  |  reusable", 12, (203, 213, 225, 220))
    return save(img, "researchflow_discord_banner_logo_03_graph_memory.png")


def banner_04_clean_white():
    img = bg((246, 250, 255), (232, 244, 250), (210, 250, 235))
    d = ImageDraw.Draw(img)
    glow(img, (545, 125), 142, (14, 165, 233), 48)
    glow(img, (132, 66), 96, (251, 191, 36), 52)
    rounded(d, (30, 31, 650, 209), (255, 255, 255, 166), outline=(15, 23, 42, 27), radius=22)
    paste_logo(img, (438, 34), 188, 156)
    graph(d, [(319, 84), (358, 72), (404, 96), (348, 124), (397, 143), (431, 111)], color=(15, 23, 42, 88), accent=(20, 184, 166, 155))
    draw_text(d, (64, 89), "ResearchFlow", 40, (15, 23, 42, 255), True)
    draw_text(d, (67, 128), "Structured paper evidence for research agents", 15, (51, 65, 85, 235))
    rounded(d, (68, 156, 245, 185), (15, 23, 42, 236), radius=14)
    draw_text(d, (84, 163), "local knowledge base", 12, (248, 250, 252, 248), True)
    return save(img, "researchflow_discord_banner_logo_04_clean.png")


def banner_05_pipeline():
    img = bg((3, 7, 18), (12, 74, 110), (5, 150, 105))
    add_noise(img, 14, 13)
    d = ImageDraw.Draw(img)
    glow(img, (552, 92), 142, (34, 211, 238), 72)
    paste_logo(img, (464, 20), 190, 158)
    draw_text(d, (46, 70), "ResearchFlow", 36, (240, 253, 250, 255), True)
    draw_text(d, (49, 108), "Open research memory, built from papers", 16, (204, 251, 241, 232))
    steps = [("collect", 52), ("analyze", 164), ("index", 276), ("assist", 388)]
    for i, (label, x) in enumerate(steps):
        rounded(d, (x, 155, x + 86, 188), (15, 23, 42, 188), outline=(94, 234, 212, 88), radius=12)
        draw_text(d, (x + 43, 163), label, 12, (236, 253, 245, 245), True, anchor="ma")
        if i < len(steps) - 1:
            line(d, [(x + 91, 171), (steps[i + 1][1] - 9, 171)], (125, 211, 252, 150), 2)
            line(d, [(steps[i + 1][1] - 17, 164), (steps[i + 1][1] - 9, 171), (steps[i + 1][1] - 17, 178)], (125, 211, 252, 150), 2)
    return save(img, "researchflow_discord_banner_logo_05_pipeline.png")


def banner_06_warm_lab():
    img = bg((255, 251, 235), (224, 242, 254), (204, 251, 241))
    d = ImageDraw.Draw(img)
    glow(img, (110, 70), 128, (251, 191, 36), 62)
    glow(img, (585, 132), 140, (45, 212, 191), 82)
    rounded(d, (34, 39, 646, 201), (255, 255, 255, 172), outline=(15, 23, 42, 24), radius=22)
    paste_logo(img, (58, 47), 164, 136)
    draw_text(d, (258, 89), "ResearchFlow", 38, (17, 24, 39, 255), True)
    draw_text(d, (261, 127), "A calm lab for evidence-grounded research", 15, (71, 85, 105, 233))
    rounded(d, (262, 155, 367, 183), (20, 184, 166, 222), radius=14)
    draw_text(d, (278, 162), "join the lab", 12, (255, 255, 255, 250), True)
    graph(d, [(497, 62), (538, 47), (584, 64), (544, 97), (598, 105), (632, 78)], color=(15, 118, 110, 158), accent=(14, 165, 233, 215))
    return save(img, "researchflow_discord_banner_logo_06_warm_lab.png")


def contact(paths: list[Path]) -> Path:
    sheet = Image.new("RGB", (W * 2, H * 3), (15, 23, 42))
    for i, p in enumerate(paths):
        sheet.paste(Image.open(p).convert("RGB"), ((i % 2) * W, (i // 2) * H))
    out = OUT / "researchflow_discord_banner_logo_contact_sheet.png"
    sheet.save(out, "PNG", optimize=True)
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        banner_01_logo_orbit(),
        banner_02_community_launch(),
        banner_03_graph_memory(),
        banner_04_clean_white(),
        banner_05_pipeline(),
        banner_06_warm_lab(),
    ]
    paths.append(contact(paths))
    for p in paths:
        print(p)


if __name__ == "__main__":
    main()
