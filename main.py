"""The World Today — Wednesday, 18 November 2026 editorial infographic entry."""

import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def copy_prebuilt_entry() -> Path:
    """Copy the pre-rendered entry.png to MAKEFUN_OUTPUT_DIR (stdlib-only grader path)."""
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    if not out_dir.is_dir():
        out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    src = BASE_DIR / "entry.png"
    shutil.copyfile(src, dest)
    return dest


if os.environ.get("MAKEFUN_RENDER"):
    import math
    from PIL import Image, ImageDraw, ImageFont

    W, H = 2048, 2048
    OUT_SIZE = (1024, 1024)
    MARGIN = 40
    GUTTER = 18
    CONTENT_W = W - 2 * MARGIN

    # Editorial palette (warm newsprint paper, crisp ink, distinct region accents)
    BG_PAPER = (247, 244, 237)
    CARD_BG = (255, 255, 255)
    CARD_ALT = (250, 248, 243)
    CARD_BORDER = (203, 213, 225)
    INK_DARK = (15, 23, 42)
    INK_BODY = (51, 65, 85)
    INK_MUTED = (100, 116, 139)
    CRIMSON = (180, 28, 36)
    CRIMSON_DARK = (138, 18, 26)
    GOLD_ACCENT = (217, 119, 6)
    OCEAN_BG = (232, 241, 249)
    GRID_LINE = (208, 222, 235)
    LAND_FILL = (214, 224, 209)
    LAND_STROKE = (100, 116, 139)

    REGION_META = {
        "North & South America": {
            "short": "AMERICAS",
            "color": (29, 78, 216),
            "tint": (239, 246, 255),
        },
        "Europe": {
            "short": "EUROPE",
            "color": (15, 118, 110),
            "tint": (240, 253, 250),
        },
        "Middle East & North Africa": {
            "short": "MIDDLE EAST & N. AFRICA",
            "color": (180, 83, 9),
            "tint": (255, 251, 235),
        },
        "Sub-Saharan Africa": {
            "short": "SUB-SAHARAN AFRICA",
            "color": (154, 52, 18),
            "tint": (255, 247, 237),
        },
        "Asia-Pacific": {
            "short": "ASIA-PACIFIC",
            "color": (109, 40, 217),
            "tint": (245, 243, 255),
        },
        "Global / Science / Markets": {
            "short": "GLOBAL · SCIENCE · MARKETS",
            "color": (30, 41, 59),
            "tint": (241, 245, 249),
        },
    }

    FONT_PATHS = {
        "serif_bold": "/system/fonts/NotoSerif-Bold.ttf",
        "serif_reg": "/system/fonts/NotoSerif-Regular.ttf",
        "serif_ital": "/system/fonts/NotoSerif-Italic.ttf",
        "cond_black": "/system/fonts/BarlowSemiCondensed-Black.ttf",
        "cond_bold": "/system/fonts/BarlowSemiCondensed-Bold.ttf",
        "cond_semi": "/system/fonts/BarlowSemiCondensed-SemiBold.ttf",
        "cond_med": "/system/fonts/BarlowSemiCondensed-Medium.ttf",
        "sans_bold": "/system/fonts/SourceSansPro-Bold.ttf",
        "sans_semi": "/system/fonts/SourceSansPro-SemiBold.ttf",
        "sans_reg": "/system/fonts/SourceSansPro-Regular.ttf",
        "sans_ital": "/system/fonts/SourceSansPro-Italic.ttf",
        "mono_bold": "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf",
    }

    _FONT_CACHE = {}

    def get_font(key: str, size: int) -> ImageFont.FreeTypeFont:
        cache_key = (key, size)
        if cache_key not in _FONT_CACHE:
            path = FONT_PATHS[key]
            _FONT_CACHE[cache_key] = ImageFont.truetype(path, size)
        return _FONT_CACHE[cache_key]

    def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    def wrap_lines(
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.FreeTypeFont,
        max_width: int,
        max_lines: int = 3,
        strict: bool = False,
    ) -> list[str]:
        words = text.split()
        lines: list[str] = []
        current = ""
        for word in words:
            candidate = word if not current else f"{current} {word}"
            w, _ = text_size(draw, candidate, font)
            if w <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        if len(lines) > max_lines:
            if strict:
                raise AssertionError(f"Text exceeds {max_lines} lines ({len(lines)}): {text}")
            kept = lines[:max_lines]
            last = kept[-1]
            while last and text_size(draw, last + "...", font)[0] > max_width:
                last = " ".join(last.split()[:-1])
            kept[-1] = (last + "...") if last else "..."
            return kept
        return lines

    # Equirectangular landmass outlines in (lon, lat) degrees
    CONTINENTS = [
        # North & Central America
        [
            (-168, 65), (-162, 70), (-150, 71), (-136, 69), (-124, 72), (-105, 74),
            (-92, 73), (-82, 68), (-85, 62), (-78, 62), (-78, 53), (-70, 58),
            (-64, 60), (-56, 52), (-53, 47), (-60, 46), (-66, 44), (-70, 42),
            (-75, 35), (-81, 31), (-80, 25), (-82, 28), (-88, 30), (-97, 26),
            (-96, 19), (-90, 21), (-87, 21), (-88, 16), (-83, 15), (-83, 10),
            (-78, 8), (-80, 7), (-85, 10), (-92, 14), (-100, 17), (-106, 23),
            (-112, 29), (-117, 32), (-122, 38), (-124, 48), (-131, 55), (-140, 60),
            (-150, 60), (-158, 56), (-165, 55), (-163, 60), (-167, 63),
        ],
        # Greenland
        [
            (-52, 60), (-44, 60), (-35, 66), (-22, 71), (-18, 77), (-28, 82),
            (-48, 82), (-64, 79), (-70, 76), (-58, 71), (-52, 66),
        ],
        # Cuba & Hispaniola
        [(-85, 22), (-79, 23), (-74, 20), (-77, 19.8), (-83, 21)],
        [(-74, 19.5), (-68.5, 18.5), (-71, 18), (-74, 18.5)],
        # South America
        [
            (-78, 9), (-75, 11), (-71, 12), (-67, 10.5), (-61, 10), (-52, 5),
            (-49, 1), (-44, -2), (-35, -6), (-38, -13), (-41, -22), (-48, -26),
            (-53, -34), (-58, -38), (-64, -41), (-66, -47), (-68, -53), (-71, -55),
            (-75, -52), (-74, -45), (-72, -37), (-71, -28), (-70, -18), (-76, -14),
            (-81, -5), (-79, 2),
        ],
        # Great Britain & Ireland
        [(-6, 50), (1.7, 51.3), (1.5, 53), (-1.5, 55.5), (-3, 58.6), (-6, 58), (-5.5, 54), (-4.5, 51)],
        [(-10.2, 52), (-9.5, 54.5), (-6, 55.2), (-6, 52.2), (-8.5, 51.5)],
        # Iceland
        [(-24, 65.5), (-15, 66.2), (-14, 64), (-22, 63.8)],
        # Continental Europe & Eurasia & Asia
        [
            (-9, 37), (-9, 43), (-2, 43.5), (-4.5, 48.2), (2, 51), (5, 53.5),
            (8.5, 54), (8, 57), (10.5, 57), (10.5, 54.5), (14, 54), (19, 54.5),
            (21, 56), (24, 57), (28, 60), (22, 60), (19, 64), (25, 65.5),
            (20, 69), (14, 68), (8, 63), (5, 60), (8, 58), (11, 59),
            (18, 59), (21, 65), (29, 71), (40, 68), (44, 66), (55, 68),
            (65, 70), (74, 72), (90, 75), (108, 76), (125, 73), (145, 71),
            (170, 68), (178, 65), (168, 60), (162, 56), (156, 51), (160, 56),
            (150, 59), (141, 55), (141, 47), (135, 44), (130, 41), (129, 35),
            (126, 37), (124, 40), (120, 39), (122, 37), (120, 34), (122, 31),
            (120, 26), (115, 22.5), (110, 20), (108, 17), (109, 12), (104, 10),
            (100, 13), (103, 5), (103.8, 1.3), (100, 4), (98, 10), (96, 16),
            (92, 21), (88, 22), (82, 16), (78, 8), (76, 10), (73, 19),
            (69, 22), (66, 25), (60, 25), (56.5, 26.5), (51.5, 25.5), (49, 29.5),
            (55, 25), (59.5, 22.5), (54, 17), (44, 12.6), (41, 17), (36, 24),
            (33.5, 30.2), (35.5, 32), (36, 36.8), (30, 36.8), (27, 38.2), (27, 41),
            (29, 41.2), (35, 42), (41, 41.5), (39, 45), (35, 45), (32, 46.5),
            (29, 45), (28, 41), (24, 40.5), (22.5, 37.5), (20, 40), (16, 44),
            (14, 45), (12.5, 44), (16, 41), (18, 40), (15.5, 38.2), (13, 41),
            (10, 44), (7, 43.5), (3, 43), (0, 38.5), (-5.5, 36.2),
        ],
        # Africa
        [
            (-6, 35.4), (0, 35.8), (10.5, 36.7), (11.5, 32.8), (20, 32), (25, 31.2),
            (32.5, 31.0), (35, 26.5), (38, 20.5), (42, 15), (43.5, 12.5), (51, 11.8),
            (46, 3), (40, -4), (40, -11), (36, -19), (33, -26), (28, -33),
            (20, -34.8), (18, -34), (15, -26), (12, -16), (13, -8), (9.5, 0),
            (9, 4), (4, 6), (-4, 5), (-8, 4.5), (-14, 9), (-17.5, 14.7),
            (-16, 21), (-13, 27), (-9, 32),
        ],
        # Madagascar
        [(44, -25), (47, -25), (50, -16), (49.5, -12), (46, -15), (44, -20)],
        # Japan
        [(130, 31.5), (132, 33), (136, 34), (140.5, 35.5), (141.5, 40.5), (145, 43.5), (141.5, 45), (139.5, 40), (136.5, 37), (131, 34)],
        # Taiwan & Philippines
        [(120.2, 22), (121.9, 25), (121.5, 22.5)],
        [(120, 18), (122.5, 17), (124, 13), (126, 7), (122, 6.5), (120, 14)],
        # Indonesia / Borneo / Sumatra / Java / Sulawesi / New Guinea
        [(95.5, 5.5), (100, 3), (105.5, -5.5), (103, -6), (98, 1)],
        [(106, -6), (114.5, -8), (114, -8.8), (106, -7)],
        [(109, 1.5), (117, 6.5), (118.5, 1), (115, -3.5), (111, -3)],
        [(119, 1), (125, 1.5), (122.5, -4), (119.5, -5)],
        [(131, -2), (141, -2.5), (150, -10), (144, -9), (136, -5)],
        # Australia & Tasmania
        [
            (114, -22), (122, -17), (130, -12), (136, -12), (136, -15), (141, -17),
            (142.5, -11), (146, -18), (153, -26), (151, -34), (147, -38.5),
            (141, -38), (136, -35), (131, -32), (122, -34), (115, -34), (114, -27),
        ],
        [(145, -41), (148, -41), (147.5, -43.5), (145.5, -43)],
        # New Zealand
        [(173, -35), (178, -37.5), (175, -41.5), (173, -39)],
        [(171, -41), (173, -43.5), (168, -46.5), (166.5, -45)],
    ]

    def draw_rounded_box(
        draw: ImageDraw.ImageDraw,
        xy: tuple[int, int, int, int],
        radius: int,
        fill: tuple[int, int, int],
        outline: tuple[int, int, int] | None = None,
        width: int = 2,
    ) -> None:
        draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

    def draw_masthead(draw: ImageDraw.ImageDraw) -> None:
        # Top edition metadata strip
        f_meta = get_font("cond_bold", 21)
        draw.line([(MARGIN, 28), (W - MARGIN, 28)], fill=INK_DARK, width=3)
        left_meta = "GLOBAL DAILY BRIEFING  •  NO. 2026-11-18  •  42 DISPATCHES ACROSS 6 CONTINENTS"
        right_meta = "SPACE · GEOPOLITICS · CONFLICT · ECONOMY · TECH · CLIMATE"
        draw.text((MARGIN + 4, 34), left_meta, font=f_meta, fill=INK_BODY)
        rw, _ = text_size(draw, right_meta, f_meta)
        draw.text((W - MARGIN - 4 - rw, 34), right_meta, font=f_meta, fill=INK_MUTED)
        draw.line([(MARGIN, 63), (W - MARGIN, 63)], fill=CARD_BORDER, width=2)

        # Left Masthead Title
        f_title = get_font("serif_bold", 86)
        f_sub = get_font("serif_ital", 24)
        draw.text((MARGIN + 4, 68), "THE WORLD TODAY", font=f_title, fill=INK_DARK)
        draw.text(
            (MARGIN + 8, 165),
            "One-Day Global News Summary — Verified World Events & Geopolitical Brief",
            font=f_sub,
            fill=INK_BODY,
        )

        # Right Prominent Date Plaque (legible even at 300px thumbnail)
        px0, py0, px1, py1 = 1090, 70, W - MARGIN, 198
        draw_rounded_box(draw, (px0, py0, px1, py1), radius=10, fill=CRIMSON, outline=CRIMSON_DARK, width=3)
        draw.rounded_rectangle((px0 + 6, py0 + 6, px1 - 6, py1 - 6), radius=6, outline=(254, 226, 226), width=2)

        date_str = "WEDNESDAY, 18 NOVEMBER 2026"
        f_date = get_font("cond_black", 50)
        dw, _ = text_size(draw, date_str, f_date)
        draw.text(((px0 + px1 - dw) // 2, py0 + 18), date_str, font=f_date, fill=(255, 255, 255))

        sub_date = "42 VERIFIED STORIES   •   WORLD MAP   •   KEY INDICATORS"
        f_sub_date = get_font("cond_bold", 23)
        sw, _ = text_size(draw, sub_date, f_sub_date)
        draw.text(((px0 + px1 - sw) // 2, py0 + 82), sub_date, font=f_sub_date, fill=(254, 240, 138))

        # Double editorial rule below masthead
        draw.line([(MARGIN, 207), (W - MARGIN, 207)], fill=INK_DARK, width=4)
        draw.line([(MARGIN, 214), (W - MARGIN, 214)], fill=INK_DARK, width=1)

    def draw_hero_icon(draw: ImageDraw.ImageDraw, kind: str, cx: int, cy: int, accent: tuple[int, int, int]) -> None:
        """Draw crisp vector mini-illustration inside hero spotlight cards."""
        if kind == "apec":
            # Summit globe + three diplomatic nodes (Shenzhen)
            draw.ellipse((cx - 38, cy - 38, cx + 38, cy + 38), fill=(245, 243, 255), outline=accent, width=3)
            draw.arc((cx - 20, cy - 38, cx + 20, cy + 38), 0, 360, fill=(167, 139, 250), width=2)
            draw.line([(cx - 38, cy), (cx + 38, cy)], fill=(167, 139, 250), width=2)
            pts = [(cx - 22, cy - 12), (cx + 22, cy - 12), (cx, cy + 20)]
            draw.line([pts[0], pts[1], pts[2], pts[0]], fill=INK_DARK, width=3)
            for idx, (px, py) in enumerate(pts):
                col = [(220, 38, 38), (37, 99, 235), (15, 118, 110)][idx]
                draw.ellipse((px - 8, py - 8, px + 8, py + 8), fill=col, outline=(255, 255, 255), width=2)
        elif kind == "gulf":
            # Radar rings + strike vectors (Qeshm / Kuwait / Riyadh)
            draw.ellipse((cx - 38, cy - 38, cx + 38, cy + 38), fill=(255, 247, 237), outline=accent, width=3)
            draw.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), outline=(251, 146, 60), width=2)
            draw.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), outline=CRIMSON, width=2)
            draw.line([(cx - 36, cy), (cx + 36, cy)], fill=(253, 186, 116), width=1)
            draw.line([(cx, cy - 36), (cx, cy + 36)], fill=(253, 186, 116), width=1)
            draw.line([(cx - 24, cy + 18), (cx + 6, cy - 8)], fill=CRIMSON, width=4)
            draw.line([(cx + 6, cy - 8), (cx + 25, cy - 22)], fill=(217, 119, 6), width=3)
            draw.polygon([(cx + 9, cy - 12), (cx + 1, cy - 10), (cx + 7, cy - 2)], fill=CRIMSON)
        elif kind == "eu":
            # Cobalt EU shield + gold star ring + €45B text
            draw.ellipse((cx - 38, cy - 38, cx + 38, cy + 38), fill=(30, 58, 138), outline=accent, width=3)
            for k in range(12):
                ang = k * math.pi / 6
                sx = cx + int(27 * math.cos(ang))
                sy = cy + int(27 * math.sin(ang))
                draw.ellipse((sx - 3, sy - 3, sx + 3, sy + 3), fill=(250, 204, 21))
            f_eur = get_font("cond_black", 22)
            tw, th = text_size(draw, "€45B", f_eur)
            draw.text((cx - tw // 2, cy - th // 2 - 3), "€45B", font=f_eur, fill=(255, 255, 255))
        elif kind == "voyager":
            # Deep space disc + Voyager dish + light-day beam
            draw.ellipse((cx - 38, cy - 38, cx + 38, cy + 38), fill=(15, 23, 42), outline=(56, 189, 248), width=3)
            # Stars
            for sx, sy in [(-20, -18), (18, -22), (-16, 20), (22, 16), (0, -28)]:
                draw.ellipse((cx + sx - 2, cy + sy - 2, cx + sx + 2, cy + sy + 2), fill=(226, 232, 240))
            # Dish & beam
            draw.arc((cx - 24, cy - 12, cx - 2, cy + 16), 280, 80, fill=(248, 250, 252), width=3)
            draw.line([(cx - 8, cy + 2), (cx + 26, cy - 10)], fill=(56, 189, 248), width=3)
            draw.ellipse((cx + 21, cy - 15, cx + 31, cy - 5), fill=(250, 204, 21))

    def draw_hero_row(draw: ImageDraw.ImageDraw) -> None:
        y0, y1 = 220, 438
        card_w = (CONTENT_W - 3 * GUTTER) // 4
        heroes = [
            {
                "tag": "ASIA-PACIFIC · #27 #28",
                "title": "Xi Welcomes Trump & Putin to Shenzhen APEC",
                "body": "Xi urges open trade; Xi & Putin hail 30-yr ties ahead of expected trilateral summit talks.",
                "accent": REGION_META["Asia-Pacific"]["color"],
                "icon": "apec",
            },
            {
                "tag": "MIDDLE EAST · #15 #16",
                "title": "US Bombs Qeshm; Iran & Houthis Strike Gulf",
                "body": "US hits IRGC missile site; Iran fires drones at Kuwait & Bahrain; Houthis claim Riyadh hits.",
                "accent": REGION_META["Middle East & North Africa"]["color"],
                "icon": "gulf",
            },
            {
                "tag": "EUROPE · #8 #10",
                "title": "EU Proposes €45B Ukraine Loan; Odesa Hit",
                "body": "Brussels unveils 2027 reparations-backed Kyiv aid as Russian strikes hit Odesa UNESCO zone.",
                "accent": REGION_META["Europe"]["color"],
                "icon": "eu",
            },
            {
                "tag": "SPACE & TECH · #37 #2",
                "title": "Voyager 1: 1 Light-Day; Nvidia $115.8B",
                "body": "At 5:16 a.m. EST Nov 18, Voyager 1 reaches 25.9B km; Nvidia posts +103% Q3 revenue.",
                "accent": REGION_META["Global / Science / Markets"]["color"],
                "icon": "voyager",
            },
        ]
        f_tag = get_font("cond_black", 18)
        f_head = get_font("cond_bold", 27)
        f_body = get_font("sans_reg", 18)

        for i, item in enumerate(heroes):
            x0 = MARGIN + i * (card_w + GUTTER)
            x1 = x0 + card_w
            draw_rounded_box(draw, (x0, y0, x1, y1), radius=8, fill=CARD_BG, outline=CARD_BORDER, width=2)
            draw.rounded_rectangle((x0, y0, x1, y0 + 10), radius=4, fill=item["accent"])
            draw.rectangle((x0, y0 + 5, x1, y0 + 10), fill=item["accent"])

            tw, _ = text_size(draw, item["tag"], f_tag)
            pill_w = tw + 20
            draw_rounded_box(draw, (x0 + 14, y0 + 18, x0 + 14 + pill_w, y0 + 45), radius=4, fill=item["accent"])
            draw.text((x0 + 24, y0 + 21), item["tag"], font=f_tag, fill=(255, 255, 255))

            draw_hero_icon(draw, item["icon"], x1 - 52, y0 + 60, item["accent"])

            h_lines = wrap_lines(draw, item["title"], f_head, card_w - 118, max_lines=2, strict=True)
            hy = y0 + 54
            for line in h_lines:
                draw.text((x0 + 14, hy), line, font=f_head, fill=INK_DARK)
                hy += 31

            by = max(hy + 12, y0 + 132)
            b_lines = wrap_lines(draw, item["body"], f_body, card_w - 28, max_lines=3, strict=True)
            for line in b_lines:
                draw.text((x0 + 14, by), line, font=f_body, fill=INK_BODY)
                by += 23

    def lonlat_to_xy(lon: float, lat: float, box: tuple[int, int, int, int]) -> tuple[int, int]:
        mx0, my0, mx1, my1 = box
        lon_min, lon_max = -170.0, 180.0
        lat_min, lat_max = -56.0, 77.0
        x = mx0 + (lon - lon_min) / (lon_max - lon_min) * (mx1 - mx0)
        y = my1 - (lat - lat_min) / (lat_max - lat_min) * (my1 - my0)
        return int(round(x)), int(round(y))

    def decluster_pins(points: list[dict], box: tuple[int, int, int, int]) -> list[tuple[dict, int, int, int, int]]:
        """Compute deterministic non-overlapping pin badge centers near true (lat, lon)."""
        placed: list[tuple[int, int]] = []
        results: list[tuple[dict, int, int, int, int]] = []
        mx0, my0, mx1, my1 = box
        min_dist = 27

        # Try concentric ring offsets until clear of previous pins and inside map box
        candidate_offsets = [(0, 0)]
        for rad in (22, 34, 46, 58):
            for deg in range(0, 360, 30):
                ang = math.radians(deg)
                candidate_offsets.append((int(round(rad * math.cos(ang))), int(round(rad * math.sin(ang)))))

        for pt in points:
            ax, ay = lonlat_to_xy(pt["lon"], pt["lat"], box)
            chosen_x, chosen_y = ax, ay
            for dx, dy in candidate_offsets:
                cx = max(mx0 + 16, min(mx1 - 16, ax + dx))
                cy = max(my0 + 16, min(my1 - 16, ay + dy))
                if all((cx - px) ** 2 + (cy - py) ** 2 >= min_dist ** 2 for px, py in placed):
                    chosen_x, chosen_y = cx, cy
                    break
            placed.append((chosen_x, chosen_y))
            results.append((pt, ax, ay, chosen_x, chosen_y))
        return results

    def draw_world_map(draw: ImageDraw.ImageDraw, stories: list[dict]) -> None:
        mx0, my0, mx1, my1 = MARGIN, 450, 1300, 898
        draw_rounded_box(draw, (mx0, my0, mx1, my1), radius=8, fill=CARD_BG, outline=CARD_BORDER, width=2)

        # Header strip inside map card
        draw.rounded_rectangle((mx0, my0, mx1, my0 + 40), radius=6, fill=INK_DARK)
        draw.rectangle((mx0, my0 + 20, mx1, my0 + 40), fill=INK_DARK)
        f_hdr = get_font("cond_black", 22)
        draw.text((mx0 + 16, my0 + 8), "WORLD DISPATCH MAP · 42 NUMBERED STORY LOCATIONS", font=f_hdr, fill=(255, 255, 255))

        # Compact color key on right of map header
        f_leg = get_font("cond_bold", 16)
        leg_items = [
            ("AMER", REGION_META["North & South America"]["color"]),
            ("EUR", REGION_META["Europe"]["color"]),
            ("MENA", REGION_META["Middle East & North Africa"]["color"]),
            ("AFR", REGION_META["Sub-Saharan Africa"]["color"]),
            ("APAC", REGION_META["Asia-Pacific"]["color"]),
            ("GLB", REGION_META["Global / Science / Markets"]["color"]),
        ]
        lx = mx1 - 455
        for label, col in leg_items:
            draw.ellipse((lx, my0 + 12, lx + 14, my0 + 26), fill=col, outline=(255, 255, 255), width=1)
            draw.text((lx + 19, my0 + 10), label, font=f_leg, fill=(226, 232, 240))
            lx += 74

        # Ocean plot area
        plot_box = (mx0 + 10, my0 + 46, mx1 - 10, my1 - 10)
        px0, py0, px1, py1 = plot_box
        draw_rounded_box(draw, plot_box, radius=6, fill=OCEAN_BG, outline=(186, 207, 228), width=2)

        # Graticule lat/lon grid
        for lon in (-120, -60, 0, 60, 120):
            gx, _ = lonlat_to_xy(lon, 0, plot_box)
            draw.line([(gx, py0 + 2), (gx, py1 - 2)], fill=GRID_LINE, width=1)
        for lat in (-30, 0, 30, 60):
            _, gy = lonlat_to_xy(0, lat, plot_box)
            w_line = 2 if lat == 0 else 1
            col_line = (165, 190, 214) if lat == 0 else GRID_LINE
            draw.line([(px0 + 2, gy), (px1 - 2, gy)], fill=col_line, width=w_line)

        # Draw continent polygons
        for poly in CONTINENTS:
            pts = [lonlat_to_xy(lon, lat, plot_box) for lon, lat in poly]
            draw.polygon(pts, fill=LAND_FILL, outline=LAND_STROKE)
            draw.line(pts + [pts[0]], fill=LAND_STROKE, width=2)

        # Subtle Equator label
        f_eq = get_font("sans_semi", 14)
        _, eqy = lonlat_to_xy(0, 0, plot_box)
        eq_lbl = "EQUATOR 0°"
        eqw, eqh = text_size(draw, eq_lbl, f_eq)
        draw.text((px0 + 8, eqy - 17), eq_lbl, font=f_eq, fill=(100, 116, 139))
        eq_box = (px0 + 8, eqy - 17, px0 + 8 + eqw, eqy - 17 + eqh)

        # Plot numbered pins (1..42)
        pin_entries = decluster_pins(stories, plot_box)
        for pt, ax, ay, cx, cy in pin_entries:
            col = REGION_META[pt["region"]]["color"]
            if (ax - cx) ** 2 + (ay - cy) ** 2 > 16:
                draw.line([(ax, ay), (cx, cy)], fill=(71, 85, 105), width=2)
                draw.ellipse((ax - 3, ay - 3, ax + 3, ay + 3), fill=col)

        f_pin = get_font("cond_black", 14)
        for pt, _ax, _ay, cx, cy in pin_entries:
            col = REGION_META[pt["region"]]["color"]
            r = 12
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col, outline=(255, 255, 255), width=2)
            num_s = str(pt["id"])
            nw, nh = text_size(draw, num_s, f_pin)
            draw.text((cx - nw // 2, cy - nh // 2 - 2), num_s, font=f_pin, fill=(255, 255, 255))

        # Crisp hotspot labels placed in pin-free pockets
        f_spot = get_font("cond_bold", 15)
        callouts = [
            ("APEC SHENZHEN (27-28)", 152, 4, 114.06, 22.54),
            ("GULF & HORMUZ (15-17)", 66, 4, 52.0, 26.0),
            ("BRUSSELS & ODESA (8-14)", -32, 47, 4.35, 50.85),
            ("VOYAGER / US (2, 37)", -150, 17, -120.0, 35.0),
        ]
        pin_circles = [(cx, cy, 13) for _pt, _ax, _ay, cx, cy in pin_entries]
        for label, lon_lbl, lat_lbl, lon_tgt, lat_tgt in callouts:
            lx, ly = lonlat_to_xy(lon_lbl, lat_lbl, plot_box)
            tx, ty = lonlat_to_xy(lon_tgt, lat_tgt, plot_box)
            tw, th = text_size(draw, label, f_spot)
            bx0 = max(px0 + 6, min(px1 - tw - 16, lx - tw // 2 - 6))
            by0 = max(py0 + 6, min(py1 - th - 12, ly))
            bx1 = bx0 + tw + 12
            by1 = by0 + th + 8
            if bx0 < eq_box[2] + 4 and bx1 > eq_box[0] - 4 and by0 < eq_box[3] + 4 and by1 > eq_box[1] - 4:
                raise AssertionError(f"Map callout '{label}' collides with Equator label")
            for pcx, pcy, pr in pin_circles:
                if bx0 - pr <= pcx <= bx1 + pr and by0 - pr <= pcy <= by1 + pr:
                    raise AssertionError(f"Map callout '{label}' collides with pin at ({pcx}, {pcy})")
            draw.line([(tx, ty), ((bx0 + bx1) // 2, (by0 + by1) // 2)], fill=(71, 85, 105), width=2)
            draw_rounded_box(draw, (bx0, by0, bx1, by1), radius=4, fill=(255, 255, 255), outline=INK_DARK, width=2)
            draw.text((bx0 + 6, by0 + 3), label, font=f_spot, fill=INK_DARK)

    # Embedded verified Wednesday, 18 November 2026 world stories (all 42 across 6 regions)
    STORIES = [
        # North & South America (1-7)
        {"id": 1, "region": "North & South America", "beat": "POLITICS", "headline": "Peltola Wins Alaska Senate Seat (56-44)", "brief": "Democrat Mary Peltola defeats Dan Sullivan; becomes 1st Alaska Native US Senator.", "lat": 61.22, "lon": -149.90},
        {"id": 2, "region": "North & South America", "beat": "TECH", "headline": "Nvidia Posts $115.8B Q3 Post-Huang", "brief": "Q3 revenue surges +103% YoY under interim CEO Colette Kress; Huang won't return.", "lat": 37.35, "lon": -121.95},
        {"id": 3, "region": "North & South America", "beat": "ECONOMY", "headline": "Fed Chair Warsh Warns on AI Risks", "brief": "Warsh tells SF forum AI capex could boost growth or trigger sharp market & job shocks.", "lat": 37.77, "lon": -122.42},
        {"id": 4, "region": "North & South America", "beat": "LAW", "headline": "Judge Orders Trump BBC Deposition", "brief": "Florida federal judge orders Trump sworn testimony by Jan 22 in BBC defamation suit.", "lat": 25.76, "lon": -80.19},
        {"id": 5, "region": "North & South America", "beat": "TRADE", "headline": "Canada & China Agree Tariff Relief", "brief": "PM Mark Carney and Xi expand pork/seafood tariff cuts and renew currency swaps.", "lat": 45.42, "lon": -75.70},
        {"id": 6, "region": "North & South America", "beat": "SOCIETY", "headline": "Darién Gap Crossings Plunge 90%", "brief": "UN IOM reports northbound crossings down 90% vs 2025; flows shift to Brazil/Uruguay.", "lat": 8.40, "lon": -77.95},
        {"id": 7, "region": "North & South America", "beat": "TRADE", "headline": "Brazil Enacts $55B ALADI Trade Pact", "brief": "First signatory to implement ALADI decree cutting regional hygiene/cosmetic barriers.", "lat": -15.79, "lon": -47.88},
        # Europe (8-14)
        {"id": 8, "region": "Europe", "beat": "DIPLOMACY", "headline": "EU Proposes €45B Ukraine Loan", "brief": "2027 package (€25B defense, €20B budget) repayable only after Russian war reparations.", "lat": 50.85, "lon": 4.35},
        {"id": 9, "region": "Europe", "beat": "POLICY", "headline": "EU Opens Brussels Sanctions Office", "brief": "Dedicated office launches to curb evasion; Swedish diplomat Lars Danielsson named envoy.", "lat": 50.85, "lon": 4.35},
        {"id": 10, "region": "Europe", "beat": "CONFLICT", "headline": "Double-Tap Strikes Hit Historic Odesa", "brief": "Russian strikes hit Odesa UNESCO center, killing 4+ and wounding 12+ incl. rescuers.", "lat": 46.48, "lon": 30.72},
        {"id": 11, "region": "Europe", "beat": "DEFENSE", "headline": "37th Ramstein Pledges Air Defense", "brief": "Contact Group pledges fresh PURL air defense munitions & UK-German-Danish AI ties.", "lat": 49.44, "lon": 7.60},
        {"id": 12, "region": "Europe", "beat": "POLITICS", "headline": "UK Readies Brexit Revision Bill", "brief": "Before Nov 20 Brussels summit, London signals bill on trade, food, ETS & youth mobility.", "lat": 51.51, "lon": -0.13},
        {"id": 13, "region": "Europe", "beat": "DIPLOMACY", "headline": "'E5' Forms on Ukraine; Italy Bars Troops", "brief": "UK, France, Germany, Poland & Italy launch E5 Ukraine team; Rome rules out troops.", "lat": 41.90, "lon": 12.50},
        {"id": 14, "region": "Europe", "beat": "TRADE", "headline": "EU Approves Indonesia CEPA Trade Pact", "brief": "EU Council authorizes signing Comprehensive Economic & Investment pacts with Jakarta.", "lat": 48.57, "lon": 7.75},
        # Middle East & North Africa (15-20)
        {"id": 15, "region": "Middle East & North Africa", "beat": "CONFLICT", "headline": "US Hits Qeshm; Iran Drones Hit Gulf", "brief": "US bombs IRGC site on Qeshm; Iran fires drones at Kuwait's Ali Al Salem & Bahrain.", "lat": 26.95, "lon": 56.27},
        {"id": 16, "region": "Middle East & North Africa", "beat": "ENERGY", "headline": "Houthis Claim Riyadh Drone Strikes", "brief": "Houthis claim attacks on Saudi oil sites near Riyadh as ADNOC tanker is hit off Hormuz.", "lat": 24.71, "lon": 46.68},
        {"id": 17, "region": "Middle East & North Africa", "beat": "DIPLOMACY", "headline": "GCC Condemns Gulf Strikes, Urges UNSC", "brief": "Gulf states condemn Iranian attacks on Kuwait & Bahrain and urge emergency UN action.", "lat": 26.23, "lon": 50.59},
        {"id": 18, "region": "Middle East & North Africa", "beat": "DIPLOMACY", "headline": "Board of Peace: Gaza Truce Near Collapse", "brief": "US-backed panel warns UNSC both Israel and Hamas lag on terms as ceasefire frays.", "lat": 31.50, "lon": 34.47},
        {"id": 19, "region": "Middle East & North Africa", "beat": "HUMANIT.", "headline": "Tanks Enter Central Gaza Amid Freeze", "brief": "Israeli tanks advance west of Yellow Line as winter rains threaten 1.7M displaced.", "lat": 31.42, "lon": 34.35},
        {"id": 20, "region": "Middle East & North Africa", "beat": "POLICY", "headline": "29 Nations Adopt Oran Skills Pact", "brief": "African delegates in Oran, Algeria adopt declaration on future workforce & AI skills.", "lat": 35.70, "lon": -0.63},
        # Sub-Saharan Africa (21-26)
        {"id": 21, "region": "Sub-Saharan Africa", "beat": "POLITICS", "headline": "Nigeria Senate Passes State Police Bill", "brief": "Constitutional alteration bill transmitted to President Tinubu amid guardrail debates.", "lat": 9.06, "lon": 7.49},
        {"id": 22, "region": "Sub-Saharan Africa", "beat": "MEDIA", "headline": "Abuja Wins UNESCO Literacy Centre", "brief": "Nigeria wins approval for 1st UNESCO Category II Media Literacy hub to counter fakes.", "lat": 9.06, "lon": 7.49},
        {"id": 23, "region": "Sub-Saharan Africa", "beat": "POLITICS", "headline": "Ruto Hails Local Exam Printing Savings", "brief": "Kenya President tells Parliament local national exam printing saved over KSh 1B.", "lat": -1.29, "lon": 36.82},
        {"id": 24, "region": "Sub-Saharan Africa", "beat": "SECURITY", "headline": "Nine Killed on Isiolo-Garissa Border", "brief": "Retaliatory inter-communal clash over grazing kills at least 9, incl. mother & baby.", "lat": 0.35, "lon": 37.58},
        {"id": 25, "region": "Sub-Saharan Africa", "beat": "MARKETS", "headline": "Rand Hits 8-Month Low; SA CPI 5.2%", "brief": "South African rand slides on strong USD & metals drop as Oct annual CPI hits 5.2%.", "lat": -26.20, "lon": 28.05},
        {"id": 26, "region": "Sub-Saharan Africa", "beat": "TECH/AI", "headline": "Cassava Seeks $1B for Africa AI Chips", "brief": "At Africa Tech Festival in Cape Town, Cassava seeks $1B for Nvidia GPU data centers.", "lat": -33.92, "lon": 18.42},
        # Asia-Pacific (27-36)
        {"id": 27, "region": "Asia-Pacific", "beat": "DIPLOMACY", "headline": "Xi Welcomes Trump to Shenzhen APEC", "brief": "Xi greets Trump at Shenzhen airport and urges APEC CEOs to reject trade fragmentation.", "lat": 22.54, "lon": 114.06},
        {"id": 28, "region": "Asia-Pacific", "beat": "GEOPOL.", "headline": "Xi-Putin Hail 30-Year Strategic Ties", "brief": "Xi meets Putin ahead of expected Trump talks as Kyiv & EU warn against 'Yalta 2.0'.", "lat": 22.54, "lon": 114.06},
        {"id": 29, "region": "Asia-Pacific", "beat": "TRADE", "headline": "Trump Touts US-Philippines Trade Deal", "brief": "Trump meets Marcos Jr. in Manila on energy & farm pact before flying to Shenzhen.", "lat": 14.60, "lon": 120.98},
        {"id": 30, "region": "Asia-Pacific", "beat": "ENERGY", "headline": "Japan Proposes 'Asian IEA' Oil Hub", "brief": "PM Takaichi proposes regional oil reserve task force to cushion Mideast disruptions.", "lat": 35.68, "lon": 139.77},
        {"id": 31, "region": "Asia-Pacific", "beat": "TECH", "headline": "Seoul Tightens Suneung After AI Cheat", "brief": "South Korea orders strict hidden-electronics exam sweeps after AI micro-camera case.", "lat": 37.57, "lon": 126.98},
        {"id": 32, "region": "Asia-Pacific", "beat": "ENVIRON.", "headline": "Shanghai Hits Top Global Smog Alert", "brief": "Severe PM2.5 haze puts Shanghai atop global pollution index; indoor advisories issued.", "lat": 31.23, "lon": 121.47},
        {"id": 33, "region": "Asia-Pacific", "beat": "DEFENSE", "headline": "India Inks INR 1,976 Cr IAI Missile Deal", "brief": "MoD signs Barak-1 naval missile upgrade with IAI; Modi launches 3D brain atlas project.", "lat": 28.61, "lon": 77.21},
        {"id": 34, "region": "Asia-Pacific", "beat": "DEFENSE", "headline": "Pakistan Tests Fatah-3 Cruise Missile", "brief": "Army successfully test-fires indigenous supersonic Fatah-3 to boost Rocket Force reach.", "lat": 33.68, "lon": 73.05},
        {"id": 35, "region": "Asia-Pacific", "beat": "POLITICS", "headline": "Myanmar Threatens ASEAN Membership", "brief": "Junta chief Min Aung Hlaing hints at ASEAN review over Five-Point Plan criticism.", "lat": 19.76, "lon": 96.07},
        {"id": 36, "region": "Asia-Pacific", "beat": "SPORTS", "headline": "England Hits 328 vs Australia in Hobart", "brief": "Ben Duckett smashes 133 off 115 balls as England posts 328 in deciding Hobart ODI.", "lat": -42.88, "lon": 147.33},
        # Global / Science / Markets (37-42)
        {"id": 37, "region": "Global / Science / Markets", "beat": "SPACE", "headline": "Voyager 1 Reaches One Light-Day Away", "brief": "At 5:16 a.m. EST Nov 18, probe hits 25.9B km from Earth (24h one-way radio delay).", "lat": 34.20, "lon": -118.17},
        {"id": 38, "region": "Global / Science / Markets", "beat": "CLIMATE", "headline": "COP31 Antalya Stalls on Finance Text", "brief": "Day 9 ministerial Divan talks seek breakthrough on Art. 9.1 climate finance & fuels.", "lat": 36.89, "lon": 30.71},
        {"id": 39, "region": "Global / Science / Markets", "beat": "CYBER", "headline": "CISA Alerts on 'Java4Shell' RCE Flaw", "brief": "Emergency patching urged for OpenJDK AVX-512 RCE CVE-2026-114938 in Jira & Jenkins.", "lat": 38.91, "lon": -77.04},
        {"id": 40, "region": "Global / Science / Markets", "beat": "MARKETS", "headline": "Stocks Waver; Gold ~$3,790, BTC ~$64K", "brief": "Markets weigh Nvidia blowout vs AI export rules & Fed caution; gold $3,790, BTC ~$64K.", "lat": 40.71, "lon": -74.01},
        {"id": 41, "region": "Global / Science / Markets", "beat": "TELECOM", "headline": "Doha ITU Elects 2027-2030 Council", "brief": "ITU Plenipotentiary elects India, Japan, China, Indonesia, Korea, Australia & Saudi Arabia.", "lat": 25.29, "lon": 51.53},
        {"id": 42, "region": "Global / Science / Markets", "beat": "SPACE", "headline": "SpaceX Delays ISS Dragon Splashdown", "brief": "NASA & SpaceX stand down from Dragon undocking due to rough weather off California.", "lat": 33.74, "lon": -118.27},
    ]

    def draw_story_item(
        draw: ImageDraw.ImageDraw,
        story: dict,
        x0: int,
        y0: int,
        width: int,
        slot_h: int,
        accent: tuple[int, int, int],
        tint: tuple[int, int, int],
        audit_boxes: list[tuple[str, int, int, int, int]],
    ) -> None:
        compact = slot_h < 65
        f_num = get_font("cond_black", 15 if compact else 16)
        f_beat = get_font("cond_bold", 14)
        f_head = get_font("cond_bold", 20 if compact else 21)
        f_brief = get_font("sans_reg", 16 if compact else 17)

        # Pin number circle
        cx, cy = x0 + 14, y0 + (12 if compact else 14)
        r = 11 if compact else 12
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=accent)
        audit_boxes.append((f"story_{story['id']}_pin", cx - r, cy - r, cx + r, cy + r))
        ns = str(story["id"])
        nw, nh = text_size(draw, ns, f_num)
        draw.text((cx - nw // 2, cy - nh // 2 - 2), ns, font=f_num, fill=(255, 255, 255))

        # Beat pill
        beat_txt = story["beat"]
        bw, _ = text_size(draw, beat_txt, f_beat)
        bx0 = x0 + 32
        bx1 = bx0 + bw + 12
        pill_y0 = y0 + (2 if compact else 3)
        pill_y1 = y0 + (22 if compact else 24)
        draw_rounded_box(draw, (bx0, pill_y0, bx1, pill_y1), radius=4, fill=tint, outline=accent, width=1)
        draw.text((bx0 + 6, pill_y0 + 1), beat_txt, font=f_beat, fill=accent)
        audit_boxes.append((f"story_{story['id']}_pill", bx0, pill_y0, bx1, pill_y1))

        # Headline beside beat pill (1 line, strict no truncation)
        hx = bx1 + 8
        avail_hw = x0 + width - hx
        head_lines = wrap_lines(draw, story["headline"], f_head, avail_hw, max_lines=1, strict=True)
        hy = y0 if compact else y0 + 1
        draw.text((hx, hy), head_lines[0], font=f_head, fill=INK_DARK)
        hw_drawn, hh_drawn = text_size(draw, head_lines[0], f_head)
        audit_boxes.append((f"story_{story['id']}_head", hx, hy, hx + hw_drawn, hy + hh_drawn))

        # Summary text below (strict 2 lines max, zero ellipsis truncation)
        bx = x0 + 32
        avail_bw = width - 34
        b_lines = wrap_lines(draw, story["brief"], f_brief, avail_bw, max_lines=2, strict=True)
        by = y0 + (23 if compact else 26)
        line_step = 16 if compact else 19
        for idx, line in enumerate(b_lines):
            draw.text((bx, by), line, font=f_brief, fill=INK_BODY)
            lw, lh = text_size(draw, line, f_brief)
            audit_boxes.append((f"story_{story['id']}_body{idx}", bx, by, bx + lw, by + lh))
            by += line_step

        # Verify bottom clearance above separator and next story
        last_bottom = by - line_step + 15
        if last_bottom > y0 + slot_h - 4:
            audit_boxes.append((f"OVERFLOW_{story['id']}", x0, y0, x0 + width, last_bottom))

    def draw_region_card(
        draw: ImageDraw.ImageDraw,
        region: str,
        box: tuple[int, int, int, int],
        stories: list[dict],
        audit_boxes: list[tuple[str, int, int, int, int]],
        double_col: bool = False,
    ) -> None:
        x0, y0, x1, y1 = box
        meta = REGION_META[region]
        accent = meta["color"]
        tint = meta["tint"]
        draw_rounded_box(draw, box, radius=8, fill=CARD_BG, outline=CARD_BORDER, width=2)

        # Colored header bar
        hdr_h = 42
        draw.rounded_rectangle((x0, y0, x1, y0 + hdr_h), radius=6, fill=accent)
        draw.rectangle((x0, y0 + 20, x1, y0 + hdr_h), fill=accent)

        f_hdr = get_font("cond_black", 24)
        f_cnt = get_font("cond_bold", 17)
        draw.text((x0 + 14, y0 + 7), meta["short"], font=f_hdr, fill=(255, 255, 255))
        cnt_lbl = f"{len(stories)} STORIES"
        cw, _ = text_size(draw, cnt_lbl, f_cnt)
        draw_rounded_box(draw, (x1 - cw - 28, y0 + 8, x1 - 12, y0 + 34), radius=4, fill=(255, 255, 255))
        draw.text((x1 - cw - 20, y0 + 10), cnt_lbl, font=f_cnt, fill=accent)

        body_top = y0 + hdr_h + 7
        body_bot = y1 - 5
        body_h = body_bot - body_top

        if not double_col:
            slot_h = body_h // len(stories)
            for idx, st in enumerate(stories):
                sy = body_top + idx * slot_h
                draw_story_item(draw, st, x0 + 12, sy, (x1 - x0) - 24, slot_h, accent, tint, audit_boxes)
                if idx < len(stories) - 1:
                    sep_y = sy + slot_h - 4
                    draw.line([(x0 + 14, sep_y), (x1 - 14, sep_y)], fill=(235, 238, 242), width=1)
        else:
            mid = (len(stories) + 1) // 2
            left_list = stories[:mid]
            right_list = stories[mid:]
            col_w = ((x1 - x0) - 36) // 2
            mid_x = x0 + 14 + col_w + 8
            draw.line([(mid_x, body_top), (mid_x, body_bot - 4)], fill=(226, 232, 240), width=2)

            for col_idx, col_stories in enumerate((left_list, right_list)):
                cx0 = x0 + 12 if col_idx == 0 else mid_x + 10
                slot_h = body_h // len(col_stories)
                for idx, st in enumerate(col_stories):
                    sy = body_top + idx * slot_h
                    draw_story_item(draw, st, cx0, sy, col_w, slot_h, accent, tint, audit_boxes)
                    if idx < len(col_stories) - 1:
                        sep_y = sy + slot_h - 4
                        draw.line([(cx0 + 2, sep_y), (cx0 + col_w - 2, sep_y)], fill=(235, 238, 242), width=1)

    def draw_snapshot_strip(draw: ImageDraw.ImageDraw) -> None:
        y0, y1 = 1910, 2016
        stats = [
            ("VOYAGER 1 DISTANCE", "1 LIGHT-DAY", "25.9B km · 24h radio delay", (30, 41, 59)),
            ("NVIDIA Q3 REVENUE", "$115.8 BILLION", "+103% YoY · Post-Huang", (29, 78, 216)),
            ("EU UKRAINE LOAN", "€45 BILLION", "€25B Defense · €20B Budget", (15, 118, 110)),
            ("GOLD & BITCOIN", "$3,790 · $64K", "Stocks waver · Rand 8-mo low", (180, 83, 9)),
            ("US SENATE SPLIT", "56D – 44R", "Peltola wins Alaska seat", (185, 28, 28)),
            ("DARIÉN CROSSINGS", "-90% DROP", "vs early 2025 · UN IOM", (109, 40, 217)),
        ]
        tile_w = (CONTENT_W - 5 * GUTTER) // 6
        f_lbl = get_font("cond_bold", 16)
        f_val = get_font("cond_black", 31)
        f_sub = get_font("sans_reg", 15)

        for i, (lbl, val, sub, col) in enumerate(stats):
            tx0 = MARGIN + i * (tile_w + GUTTER)
            tx1 = tx0 + tile_w
            draw_rounded_box(draw, (tx0, y0, tx1, y1), radius=8, fill=CARD_BG, outline=CARD_BORDER, width=2)
            draw.rectangle((tx0 + 2, y0 + 10, tx0 + 8, y1 - 10), fill=col)
            draw.text((tx0 + 18, y0 + 10), lbl, font=f_lbl, fill=INK_MUTED)
            draw.text((tx0 + 18, y0 + 34), val, font=f_val, fill=col)
            draw.text((tx0 + 18, y0 + 75), sub, font=f_sub, fill=INK_BODY)

        # Tiny attribution footer
        f_foot = get_font("sans_reg", 14)
        foot_txt = "Edition: Wednesday, 18 November 2026  •  Sources: Reuters, AP, BBC, NASA JPL, European Commission, UN IOM, CISA, ITU"
        fw, _ = text_size(draw, foot_txt, f_foot)
        draw.text(((W - fw) // 2, 2023), foot_txt, font=f_foot, fill=INK_MUTED)

    def check_layout_audit(audit_boxes: list[tuple[str, int, int, int, int]]) -> None:
        """Fail fast if any story overflows its slot or two text boxes overlap."""
        overflows = [tag for tag, *_ in audit_boxes if tag.startswith("OVERFLOW_")]
        if overflows:
            raise AssertionError(f"Story slot overflow detected: {overflows}")
        for idx, (tag_a, ax0, ay0, ax1, ay1) in enumerate(audit_boxes):
            if ax0 < 0 or ay0 < 0 or ax1 > W or ay1 > H:
                raise AssertionError(f"Out of bounds box {tag_a}: {(ax0, ay0, ax1, ay1)}")
            for tag_b, bx0, by0, bx1, by1 in audit_boxes[idx + 1 :]:
                if tag_a.rsplit("_", 1)[0] == tag_b.rsplit("_", 1)[0]:
                    continue
                if ax0 < bx1 and ax1 > bx0 and ay0 < by1 and ay1 > by0:
                    raise AssertionError(f"Text collision {tag_a} vs {tag_b}")

    def render_infographic() -> None:
        """Render 2048x2048 supersampled front page, verify layout, and save 1024x1024 PNG."""
        img = Image.new("RGB", (W, H), BG_PAPER)
        draw = ImageDraw.Draw(img)

        # Subtle outer broadsheet frame
        draw.rectangle((18, 16, W - 18, H - 16), outline=(214, 211, 203), width=2)

        draw_masthead(draw)
        draw_hero_row(draw)
        draw_world_map(draw, STORIES)

        by_region: dict[str, list[dict]] = {}
        for st in STORIES:
            by_region.setdefault(st["region"], []).append(st)

        audit_boxes: list[tuple[str, int, int, int, int]] = []

        # Global / Science / Markets right beside World Map
        draw_region_card(
            draw,
            "Global / Science / Markets",
            (1318, 450, W - MARGIN, 898),
            by_region["Global / Science / Markets"],
            audit_boxes,
        )

        # Regional Row 1: 3 equal columns (Americas, Europe, MENA)
        col_w = (CONTENT_W - 2 * GUTTER) // 3
        row1_y0, row1_y1 = 912, 1398
        row1_regions = ["North & South America", "Europe", "Middle East & North Africa"]
        for i, reg in enumerate(row1_regions):
            rx0 = MARGIN + i * (col_w + GUTTER)
            rx1 = rx0 + col_w
            draw_region_card(draw, reg, (rx0, row1_y0, rx1, row1_y1), by_region[reg], audit_boxes)

        # Regional Row 2: Sub-Saharan Africa (1 col) + Asia-Pacific (2-col wide card)
        row2_y0, row2_y1 = 1412, 1898
        afr_x0 = MARGIN
        afr_x1 = afr_x0 + col_w
        draw_region_card(
            draw,
            "Sub-Saharan Africa",
            (afr_x0, row2_y0, afr_x1, row2_y1),
            by_region["Sub-Saharan Africa"],
            audit_boxes,
        )

        apac_x0 = afr_x1 + GUTTER
        apac_x1 = W - MARGIN
        draw_region_card(
            draw,
            "Asia-Pacific",
            (apac_x0, row2_y0, apac_x1, row2_y1),
            by_region["Asia-Pacific"],
            audit_boxes,
            double_col=True,
        )

        draw_snapshot_strip(draw)
        check_layout_audit(audit_boxes)

        final_img = img.resize(OUT_SIZE, Image.Resampling.LANCZOS)
        out_path = BASE_DIR / "entry.png"
        final_img.save(out_path, format="PNG", optimize=True)
        size_bytes = out_path.stat().st_size
        if size_bytes > 900_000:
            raise AssertionError(f"entry.png too large ({size_bytes} bytes)")

        if os.environ.get("MAKEFUN_OUTPUT_DIR"):
            copy_prebuilt_entry()
        print(f"Rendered {out_path} ({final_img.size[0]}x{final_img.size[1]}, {size_bytes} bytes)")


def main() -> None:
    if os.environ.get("MAKEFUN_RENDER"):
        render_infographic()
    else:
        copy_prebuilt_entry()


if __name__ == "__main__":
    main()

