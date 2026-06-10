from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"
FALLBACK_LOGO_PATH = ASSETS_DIR / "generated_logo.png"


BRAND_BLUE = "#101130"
GOLD = "#B58A45"
PAPER = "#F7F4EF"


def get_logo_path() -> Path:
    if LOGO_PATH.exists():
        return LOGO_PATH

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    if not FALLBACK_LOGO_PATH.exists():
        image = Image.new("RGBA", (640, 220), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        draw.rounded_rectangle((12, 12, 628, 208), radius=26, fill=PAPER, outline=GOLD, width=5)
        draw.ellipse((44, 44, 176, 176), fill=BRAND_BLUE, outline=GOLD, width=5)

        try:
            monogram_font = ImageFont.truetype("arialbd.ttf", 56)
            name_font = ImageFont.truetype("arialbd.ttf", 30)
            subtitle_font = ImageFont.truetype("arial.ttf", 19)
        except OSError:
            monogram_font = ImageFont.load_default()
            name_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()

        draw.text((110, 111), "LB", anchor="mm", fill=GOLD, font=monogram_font)
        draw.text((205, 72), "Lobo Baddini", fill=BRAND_BLUE, font=name_font)
        draw.text((207, 112), "Advocacia", fill=BRAND_BLUE, font=name_font)
        draw.line((206, 153, 545, 153), fill=GOLD, width=3)
        draw.text((207, 164), "Propostas jurídicas empresariais", fill=BRAND_BLUE, font=subtitle_font)
        image.save(FALLBACK_LOGO_PATH)

    return FALLBACK_LOGO_PATH
