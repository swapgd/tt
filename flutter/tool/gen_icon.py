#!/usr/bin/env python3
"""Generate the Table Tennis Ratings iOS app icon set from a source PNG.

Flattens any transparency onto white (Apple requires the marketing icon to be
opaque/square; iOS applies the rounded-corner mask itself), then resamples to
every size the asset catalog needs.
"""
from pathlib import Path
from PIL import Image

SRC = Path("/Users/s.deshmukh/Documents/icon_for_app.png")
ICON_DIR = Path(__file__).resolve().parent.parent / "ios/Runner/Assets.xcassets/AppIcon.appiconset"

TARGETS = {
    "Icon-App-20x20@1x.png": 20, "Icon-App-20x20@2x.png": 40, "Icon-App-20x20@3x.png": 60,
    "Icon-App-29x29@1x.png": 29, "Icon-App-29x29@2x.png": 58, "Icon-App-29x29@3x.png": 87,
    "Icon-App-40x40@1x.png": 40, "Icon-App-40x40@2x.png": 80, "Icon-App-40x40@3x.png": 120,
    "Icon-App-60x60@2x.png": 120, "Icon-App-60x60@3x.png": 180,
    "Icon-App-76x76@1x.png": 76, "Icon-App-76x76@2x.png": 152,
    "Icon-App-83.5x83.5@2x.png": 167,
    "Icon-App-1024x1024@1x.png": 1024,
}


def load_flattened() -> Image.Image:
    img = Image.open(SRC).convert("RGBA")
    # square-crop centered if not already square
    w, h = img.size
    if w != h:
        side = min(w, h)
        left, top = (w - side) // 2, (h - side) // 2
        img = img.crop((left, top, left + side, top + side))
    # flatten alpha onto white
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    bg.alpha_composite(img)
    return bg.convert("RGB")


def main():
    master = load_flattened()
    for name, px in TARGETS.items():
        master.resize((px, px), Image.LANCZOS).save(ICON_DIR / name)
        print(f"wrote {name} ({px}x{px})")


if __name__ == "__main__":
    main()
