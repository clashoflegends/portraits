# Default portrait set

Eight original portraits are included at **107 × 151 pixels**:

- Male and female commander
- Male and female rogue
- Male and female wizard
- Male and female diplomat

Every portrait has four associated assets:

- `default_<gender>_<class>.jpg` — immediate drop-in JPEG.
- `default_<gender>_<class>.png` — lossless production portrait.
- `default_<gender>_<class>_house_mask.png` — aligned grayscale recolor mask.
- `default_<gender>_<class>_targaryen_preview.png` — purple/black example.

## Shared house-color mask contract

- Black (`0`): preserve the original pixel.
- White (`255`): apply the house recolor completely.
- Intermediate gray: blend source and house colors for antialiased edges.

The masks cover navy backgrounds and major blue clothing. Skin, hair, eyes, ink,
leather, parchment, weapons, armor, and neutral metal remain fixed.

For Java/Swing, load the portrait and mask as `BufferedImage`s. Build a house-colored
version of each source pixel by replacing its HSB hue and optionally scaling saturation
and brightness. Interpolate between source and house-colored pixels using
`maskGray / 255.0`.

The supplied Targaryen previews use a target hue of approximately 281 degrees and
reduce brightness to roughly 72 percent. PNG is recommended for runtime recoloring;
JPG versions are provided for immediate compatibility.

`build_full_set.py` reproduces the exports and preview sheets from the generated
masters.
