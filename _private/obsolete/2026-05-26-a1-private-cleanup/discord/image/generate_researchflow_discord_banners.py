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


def canvas(c1: tuple[int, int, int], c2: tuple[int, int, int], c3: tuple[int, int, int] | None = None) -> Image.Image:
    img = Image.new("RGBA", (W * SCALE, H * SCALE), (0, 0, 0, 255))
    px = img.load()
    for y in range(H * SCALE):
        yy = y / (H * SCALE - 1)
        for x in range(W * SCALE):
            xx = x / (W * SCALE - 1)
            t = (xx * 0.72 + yy * 0.28)
            if c3:
                if t < 0.55:
                    u = t / 0.55
                    a, b = c1, c2
                else:
                    u = (t - 0.55) / 0.45
                    a, b = c2, c3
            else:
                u = t
                a, b = c1, c2
            px[x, y] = tuple(int(a[i] * (1 - u) + b[i] * u) for i in range(3)) + (255,)
    return img


def add_noise(img: Image.Image, opacity: int = 18, seed: int = 0) -> None:
    rng = random.Random(seed)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    pix = overlay.load()
    for y in range(0, img.size[1], 2):
        for x in range(0, img.size[0], 2):
            v = rng.randint(0, opacity)
            pix[x, y] = (255, 255, 255, v)
    img.alpha_composite(overlay)


def rect(draw: ImageDraw.ImageDraw, xy, fill, outline=None, width=1, radius=12):
    xy = tuple(int(v * SCALE) for v in xy)
    draw.rounded_rectangle(xy, radius=radius * SCALE, fill=fill, outline=outline, width=width * SCALE)


def line(draw: ImageDraw.ImageDraw, pts, fill, width=2):
    draw.line([(int(x * SCALE), int(y * SCALE)) for x, y in pts], fill=fill, width=width * SCALE)


def text(draw: ImageDraw.ImageDraw, xy, s: str, size: int, fill, bold=False, anchor=None):
    draw.text((xy[0] * SCALE, xy[1] * SCALE), s, font=font(size, bold), fill=fill, anchor=anchor)


def circle(draw: ImageDraw.ImageDraw, xy, r, fill, outline=None, width=1):
    x, y = xy
    box = [(x - r) * SCALE, (y - r) * SCALE, (x + r) * SCALE, (y + r) * SCALE]
    draw.ellipse(box, fill=fill, outline=outline, width=width * SCALE)


def glow(img: Image.Image, xy, r, color, strength=120):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = xy
    d.ellipse([(x - r) * SCALE, (y - r) * SCALE, (x + r) * SCALE, (y + r) * SCALE], fill=color[:3] + (strength,))
    layer = layer.filter(ImageFilter.GaussianBlur(r * SCALE * 0.55))
    img.alpha_composite(layer)


def load_logo(max_w: int, max_h: int) -> Image.Image:
    path = ROOT / "assets" / "researchflow-logo-transparent.png"
    if not path.exists():
        path = ROOT / "assets" / "LOGO.png"
    logo = Image.open(path).convert("RGBA")
    logo.thumbnail((max_w * SCALE, max_h * SCALE), Image.Resampling.LANCZOS)
    return logo


def paste_logo(img: Image.Image, xy, max_w=92, max_h=80, opacity=255):
    logo = load_logo(max_w, max_h)
    if opacity < 255:
        alpha = logo.getchannel("A").point(lambda p: int(p * opacity / 255))
        logo.putalpha(alpha)
    img.alpha_composite(logo, (int(xy[0] * SCALE), int(xy[1] * SCALE)))


def paper_stack(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0):
    w, h = 88 * scale, 112 * scale
    for i, off in enumerate([0, 12, 24]):
        fill = [(245, 249, 255, 218), (226, 237, 255, 232), (255, 255, 255, 246)][i]
        rect(draw, (x + off, y + off * 0.35, x + off + w, y + off * 0.35 + h), fill, radius=9)
    for k, ww in enumerate([60, 48, 56, 38]):
        rect(draw, (x + 46, y + 38 + k * 17, x + 46 + ww, y + 45 + k * 17), (23, 35, 55, 150), radius=4)


def graph(draw: ImageDraw.ImageDraw, nodes, color=(125, 211, 252, 230), accent=(52, 211, 153, 230)):
    for a, b in [(0, 1), (1, 2), (1, 3), (3, 4), (2, 5), (4, 6), (5, 6)]:
        if a >= len(nodes) or b >= len(nodes):
            continue
        line(draw, [nodes[a], nodes[b]], color[:3] + (92,), width=2)
    for i, p in enumerate(nodes):
        c = accent if i in {1, 4, 6} else color
        circle(draw, p, 8 if i != 1 else 12, (8, 16, 30, 230), outline=c, width=2)


def save(img: Image.Image, name: str):
    img = img.resize((W, H), Image.Resampling.LANCZOS).convert("RGB")
    out = OUT / name
    img.save(out, "PNG", optimize=True)
    return out


def banner_dark_lab():
    img = canvas((8, 13, 28), (16, 44, 66), (10, 80, 75))
    add_noise(img, 12, 1)
    d = ImageDraw.Draw(img)
    glow(img, (535, 55), 105, (88, 101, 242), 105)
    glow(img, (625, 220), 125, (52, 211, 153), 80)
    for y in range(34, 230, 34):
        line(d, [(0, y), (680, y + 18)], (255, 255, 255, 13), 1)
    paste_logo(img, (38, 39), 112, 88)
    text(d, (162, 88), "ResearchFlow", 36, (248, 250, 252, 255), True)
    text(d, (165, 124), "Evidence-grounded research memory", 17, (203, 213, 225, 235), False)
    rect(d, (166, 154, 398, 182), (15, 23, 42, 136), outline=(96, 165, 250, 90), radius=14)
    text(d, (182, 161), "collect -> analyze -> assist", 14, (147, 197, 253, 245))
    graph(d, [(500, 70), (552, 92), (604, 54), (520, 145), (580, 160), (638, 120), (622, 195)])
    return save(img, "researchflow_discord_banner_01_dark_lab.png")


def banner_blurple_community():
    img = canvas((23, 29, 61), (88, 101, 242), (20, 184, 166))
    add_noise(img, 10, 2)
    d = ImageDraw.Draw(img)
    glow(img, (100, 225), 120, (255, 255, 255), 42)
    for i in range(8):
        circle(d, (475 + i * 30, 44 + (i % 3) * 35), 3, (255, 255, 255, 95))
    rect(d, (34, 36, 200, 204), (255, 255, 255, 34), outline=(255, 255, 255, 64), radius=20)
    paste_logo(img, (67, 55), 112, 92, opacity=246)
    text(d, (236, 80), "ResearchFlow", 35, (255, 255, 255, 255), True)
    text(d, (238, 117), "Build the literature layer before experiments", 16, (232, 240, 255, 240))
    for i, label in enumerate(["Papers", "Evidence", "Ideas"]):
        x = 238 + i * 104
        rect(d, (x, 152, x + 86, 184), (255, 255, 255, 38), outline=(255, 255, 255, 70), radius=16)
        text(d, (x + 43, 160), label, 12, (30, 41, 59, 245), True, anchor="ma")
    return save(img, "researchflow_discord_banner_02_blurple_community.png")


def banner_obsidian_graph():
    img = canvas((11, 18, 32), (31, 41, 55), (88, 28, 135))
    add_noise(img, 16, 3)
    d = ImageDraw.Draw(img)
    glow(img, (600, 42), 135, (168, 85, 247), 90)
    glow(img, (80, 208), 100, (14, 165, 233), 65)
    paper_stack(d, 48, 58, 0.86)
    for i in range(5):
        x = 300 + i * 46
        rect(d, (x, 42 + (i % 2) * 16, x + 62, 98 + (i % 2) * 16), (15, 23, 42, 170), outline=(148, 163, 184, 55), radius=9)
        rect(d, (x + 10, 58 + (i % 2) * 16, x + 48, 63 + (i % 2) * 16), (226, 232, 240, 105), radius=3)
        rect(d, (x + 10, 72 + (i % 2) * 16, x + 36, 77 + (i % 2) * 16), (148, 163, 184, 80), radius=3)
    graph(d, [(350, 157), (408, 133), (470, 166), (530, 132), (596, 160), (625, 95), (585, 205)], color=(196, 181, 253, 230), accent=(56, 189, 248, 235))
    text(d, (170, 96), "ResearchFlow", 34, (248, 250, 252, 255), True)
    text(d, (173, 132), "Paper analysis -> Obsidian-ready memory", 15, (216, 180, 254, 236))
    text(d, (173, 160), "agent-readable  |  local-first  |  source-grounded", 12, (203, 213, 225, 220))
    return save(img, "researchflow_discord_banner_03_obsidian_graph.png")


def banner_minimal_pro():
    img = canvas((242, 246, 251), (226, 232, 240), (209, 250, 229))
    d = ImageDraw.Draw(img)
    for r, c in [(122, (88, 101, 242, 50)), (92, (20, 184, 166, 60)), (62, (14, 165, 233, 60))]:
        glow(img, (570, 126), r, c, c[3])
    rect(d, (32, 32, 648, 208), (255, 255, 255, 158), outline=(15, 23, 42, 28), radius=20)
    paste_logo(img, (55, 58), 100, 84, opacity=245)
    text(d, (175, 94), "ResearchFlow", 37, (15, 23, 42, 255), True)
    text(d, (178, 132), "Structured paper evidence for research agents", 16, (51, 65, 85, 230))
    rect(d, (178, 158, 344, 185), (15, 23, 42, 230), radius=13)
    text(d, (194, 164), "local knowledge base", 12, (248, 250, 252, 245), True)
    graph(d, [(520, 68), (562, 58), (615, 78), (552, 112), (614, 126), (646, 96)], color=(15, 23, 42, 150), accent=(20, 184, 166, 215))
    return save(img, "researchflow_discord_banner_04_minimal_pro.png")


def banner_open_source_pipeline():
    img = canvas((3, 7, 18), (12, 74, 110), (5, 150, 105))
    add_noise(img, 14, 4)
    d = ImageDraw.Draw(img)
    glow(img, (118, 70), 92, (34, 211, 238), 72)
    glow(img, (560, 190), 112, (34, 197, 94), 80)
    text(d, (46, 72), "ResearchFlow", 35, (240, 253, 250, 255), True)
    text(d, (48, 109), "Open research memory, built from papers", 16, (204, 251, 241, 230))
    steps = [("collect", 64), ("download", 172), ("analyze", 296), ("index", 414), ("assist", 524)]
    for i, (label, x) in enumerate(steps):
        rect(d, (x, 155, x + 84, 188), (15, 23, 42, 185), outline=(94, 234, 212, 86), radius=12)
        text(d, (x + 42, 163), label, 12, (236, 253, 245, 245), True, anchor="ma")
        if i < len(steps) - 1:
            line(d, [(x + 88, 171), (steps[i + 1][1] - 8, 171)], (125, 211, 252, 140), 2)
            line(d, [(steps[i + 1][1] - 16, 164), (steps[i + 1][1] - 8, 171), (steps[i + 1][1] - 16, 178)], (125, 211, 252, 140), 2)
    paper_stack(d, 500, 34, 0.55)
    return save(img, "researchflow_discord_banner_05_open_source_pipeline.png")


def banner_warm_study():
    img = canvas((255, 251, 235), (224, 242, 254), (204, 251, 241))
    d = ImageDraw.Draw(img)
    glow(img, (75, 70), 112, (251, 191, 36), 68)
    glow(img, (592, 130), 130, (45, 212, 191), 88)
    for i in range(12):
        x = 438 + i * 18
        y = 42 + int(math.sin(i * 0.9) * 20)
        circle(d, (x, y), 4, (15, 118, 110, 70))
    rect(d, (34, 40, 646, 200), (255, 255, 255, 168), outline=(15, 23, 42, 24), radius=22)
    paste_logo(img, (50, 57), 104, 86, opacity=245)
    text(d, (178, 88), "ResearchFlow", 35, (17, 24, 39, 255), True)
    text(d, (181, 125), "A calm community for evidence-grounded research", 15, (71, 85, 105, 230))
    rect(d, (181, 154, 278, 181), (20, 184, 166, 220), radius=13)
    text(d, (197, 160), "join the lab", 12, (255, 255, 255, 250), True)
    graph(d, [(502, 63), (542, 46), (590, 63), (548, 96), (602, 102), (636, 76)], color=(15, 118, 110, 160), accent=(14, 165, 233, 215))
    return save(img, "researchflow_discord_banner_06_warm_study.png")


def contact_sheet(paths: list[Path]):
    sheet = Image.new("RGB", (W * 2, H * 3), (15, 23, 42))
    for idx, path in enumerate(paths):
        im = Image.open(path).convert("RGB")
        x = (idx % 2) * W
        y = (idx // 2) * H
        sheet.paste(im, (x, y))
    out = OUT / "researchflow_discord_banner_contact_sheet.png"
    sheet.save(out, "PNG", optimize=True)
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    paths = [
        banner_dark_lab(),
        banner_blurple_community(),
        banner_obsidian_graph(),
        banner_minimal_pro(),
        banner_open_source_pipeline(),
        banner_warm_study(),
    ]
    paths.append(contact_sheet(paths))
    for p in paths:
        print(p)


if __name__ == "__main__":
    main()
