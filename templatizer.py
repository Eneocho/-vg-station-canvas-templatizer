from PIL import Image
import json
import sys
from pathlib import Path

TRANSPARENCY_COLOR = "#aaaaaa"


def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"


def image_to_template(image_path):
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size

    if not ((w == 24 and h == 24) or (w == 32 and h == 32)):
        raise ValueError("Image must be 24x24 or 32x32")

    pixels = img.load()

    palette = []
    color_index = {}
    bmp = []

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]

            if a == 0:
                hex_color = TRANSPARENCY_COLOR
            else:
                hex_color = rgb_to_hex(r, g, b)

            if hex_color not in color_index:
                color_index[hex_color] = len(palette)
                palette.append({
                    "clr": hex_color,
                    "txt": ""
                })

            bmp.append(color_index[hex_color])

    return {
        "w": w,
        "h": h,
        "rgn": palette,
        "bmp": bmp
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python image_to_template.py <image.png>")
        sys.exit(1)

    image_path = Path(sys.argv[1])
    output_path = image_path.with_suffix(".txt")

    template = image_to_template(image_path)

    with open(output_path, "w", encoding="utf-8") as f:
        # Write palette, one hex per line (no #)
        for entry in template["rgn"]:
            f.write(entry["clr"][1:] + "\n")

        # Write JSON on the next line
        json.dump(template, f, separators=(",", ":"))

    print(f"Template written to {output_path}")


if __name__ == "__main__":
    main()
