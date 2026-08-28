from pathlib import Path
import colorsys

from PIL import Image, ImageDraw, ImageFont, ImageOps


OUTPUT_DIR = Path(__file__).resolve().parent

SOURCES = {
    "male_commander": Path(r"C:\Users\John\.codex\generated_images\01a036d4-2bd7-7d12-bbe1-47d41fb01731\exec-e3f1e368-c7c9-45ad-9d72-121d1f3126e3.png"),
    "female_commander": Path(r"C:\Users\John\.codex\generated_images\01a036d4-2bd7-7d12-bbe1-47d41fb01731\exec-0632808a-5d9d-4705-8bef-dc4580d3bcdb.png"),
    "male_rogue": Path(r"C:\Users\John\.codex\generated_images\01a036d4-2bd7-7d12-bbe1-47d41fb01731\exec-3fadeea6-a150-4e75-80f1-d6318b1bc471.png"),
    "female_rogue": Path(r"C:\Users\John\Google Drive\RPG\2026 Ed Forgotten\Default Portraits 107x151\Female Rogue Prototype\default_female_rogue.png"),
    "male_wizard": Path(r"C:\Users\John\.codex\generated_images\01a036d4-2bd7-7d12-bbe1-47d41fb01731\exec-2ada7b4e-86da-48b9-a915-4e5c74572018.png"),
    "female_wizard": Path(r"C:\Users\John\.codex\generated_images\01a036d4-2bd7-7d12-bbe1-47d41fb01731\exec-e5d6c8f2-80f8-4bca-9960-354d635eda8b.png"),
    "male_diplomat": Path(r"C:\Users\John\.codex\generated_images\01a036d4-2bd7-7d12-bbe1-47d41fb01731\exec-5d526e67-a520-4dfa-b77e-89fe0acf93ce.png"),
    "female_diplomat": Path(r"C:\Users\John\.codex\generated_images\01a036d4-2bd7-7d12-bbe1-47d41fb01731\exec-5724f2ff-1073-4a5b-880f-c27eeffe5190.png"),
}

ORDER = [
    "male_commander",
    "male_rogue",
    "male_wizard",
    "male_diplomat",
    "female_commander",
    "female_rogue",
    "female_wizard",
    "female_diplomat",
]


def fit_portrait(source: Path) -> Image.Image:
    image = Image.open(source).convert("RGB")
    if image.size == (107, 151):
        return image
    return ImageOps.fit(
        image,
        (107, 151),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )


def make_house_mask(image: Image.Image) -> Image.Image:
    mask = Image.new("L", image.size, 0)
    source = image.load()
    target = mask.load()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue = source[x, y]
            hue, saturation, _ = colorsys.rgb_to_hsv(
                red / 255.0, green / 255.0, blue / 255.0
            )
            hue_weight = max(
                0.0,
                min(1.0, (hue - 0.50) / 0.06, (0.75 - hue) / 0.06),
            )
            saturation_weight = max(0.0, min(1.0, (saturation - 0.10) / 0.20))
            target[x, y] = round(255 * hue_weight * saturation_weight)
    return mask


def recolor_targaryen(image: Image.Image, mask: Image.Image) -> Image.Image:
    result = image.copy()
    source = image.load()
    target = result.load()
    mask_pixels = mask.load()
    for y in range(image.height):
        for x in range(image.width):
            amount = mask_pixels[x, y] / 255.0
            if amount <= 0.0:
                continue
            red, green, blue = source[x, y]
            _, saturation, value = colorsys.rgb_to_hsv(
                red / 255.0, green / 255.0, blue / 255.0
            )
            new_red, new_green, new_blue = colorsys.hsv_to_rgb(
                0.78,
                min(1.0, max(0.42, saturation * 0.95)),
                max(0.02, value * 0.72),
            )
            target[x, y] = (
                round(red * (1.0 - amount) + new_red * 255 * amount),
                round(green * (1.0 - amount) + new_green * 255 * amount),
                round(blue * (1.0 - amount) + new_blue * 255 * amount),
            )
    return result


def save_contact_sheet(
    portraits: dict[str, Image.Image], filename: str, title: str
) -> None:
    gutter = 8
    label_height = 18
    title_height = 24
    cell_width = 107
    cell_height = 151 + label_height
    width = 4 * cell_width + 5 * gutter
    height = title_height + 2 * cell_height + 3 * gutter
    sheet = Image.new("RGB", (width, height), (235, 235, 232))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=12)
    title_font = ImageFont.load_default(size=15)
    draw.text((gutter, 5), title, fill=(24, 27, 34), font=title_font)

    for index, key in enumerate(ORDER):
        column = index % 4
        row = index // 4
        x = gutter + column * (cell_width + gutter)
        y = title_height + gutter + row * (cell_height + gutter)
        sheet.paste(portraits[key], (x, y))
        label = key.replace("_", " ").title()
        box = draw.textbbox((0, 0), label, font=font)
        label_width = box[2] - box[0]
        draw.text(
            (x + (cell_width - label_width) // 2, y + 154),
            label,
            fill=(24, 27, 34),
            font=font,
        )
    sheet.save(OUTPUT_DIR / filename, optimize=True)


def main() -> None:
    defaults: dict[str, Image.Image] = {}
    targaryens: dict[str, Image.Image] = {}

    for key, source in SOURCES.items():
        portrait = fit_portrait(source)
        mask = make_house_mask(portrait)
        targaryen = recolor_targaryen(portrait, mask)

        portrait.save(OUTPUT_DIR / f"default_{key}.png", optimize=True)
        portrait.save(
            OUTPUT_DIR / f"default_{key}.jpg",
            "JPEG",
            quality=95,
            subsampling=0,
            optimize=True,
        )
        mask.save(OUTPUT_DIR / f"default_{key}_house_mask.png", optimize=True)
        targaryen.save(
            OUTPUT_DIR / f"default_{key}_targaryen_preview.png", optimize=True
        )
        defaults[key] = portrait
        targaryens[key] = targaryen
        print(f"{key}: JPG, PNG, mask, Targaryen preview")

    save_contact_sheet(defaults, "default_set_preview.png", "Default Navy Set")
    save_contact_sheet(
        targaryens,
        "targaryen_set_preview.png",
        "Targaryen Purple/Black Preview",
    )


if __name__ == "__main__":
    main()
