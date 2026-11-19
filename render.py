"""Composite relevant supplied editorial artwork into Image 1 without retypesetting it."""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "assets" / "entry-source.webp"
REF2 = ROOT / "assets" / "reference-2.webp"
REF3 = ROOT / "assets" / "reference-3.webp"
OUT = ROOT / "assets" / "entry.png"


def paste_art(canvas, source, source_box, target_box, resample=Image.Resampling.LANCZOS):
    art = source.crop(source_box).resize(
        (target_box[2] - target_box[0], target_box[3] - target_box[1]), resample
    )
    canvas.paste(art, target_box[:2])


def render():
    page = Image.open(BASE).convert("RGB")
    ref2 = Image.open(REF2).convert("RGB")
    ref3 = Image.open(REF3).convert("RGB")

    # Image 1's editorial layout and all its typography remain the base layer.
    # Only the illustration windows are adapted, and only from matching stories.
    # Start to the right of each source illustration's old story-number badge.
    paste_art(page, ref2, (535, 439, 654, 487), (15, 461, 207, 526))    # Crimea bridge
    riyadh_box = (837, 439, 974, 487)
    riyadh = ref2.crop(riyadh_box)
    # Remove the source card's old red 9 marker; Image 1 supplies the correct 5.
    riyadh_fill = ref2.getpixel((875, 442))
    ImageDraw.Draw(riyadh).ellipse((857 - riyadh_box[0] - 11, 450 - riyadh_box[1] - 11,
                                    857 - riyadh_box[0] + 11, 450 - riyadh_box[1] + 11), fill=riyadh_fill)
    page.paste(riyadh.resize((193, 65), Image.Resampling.LANCZOS), (215, 461))
    paste_art(page, ref3, (426, 429, 604, 482), (416, 461, 610, 526))  # Cyclone Akvan

    # Reuse the matching market plot, with no extra labels, in the existing ANT panel.
    paste_art(page, ref3, (860, 248, 982, 305), (83, 619, 204, 658))

    # Add a cinematic city/car strip from the GTA VI art while retaining Image 1's
    # original GTA VI and 13 years lettering above and below it.
    paste_art(page, ref2, (420, 254, 710, 298), (238, 632, 399, 656))

    # Use the matching Bogotá march crowd in the lower part of its existing art
    # window; preserve Image 1's own PARO NACIONAL lettering and card number.
    paste_art(page, ref2, (690, 628, 814, 655), (416, 648, 610, 678))

    page.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(
        OUT, format="PNG", optimize=True, compress_level=9
    )
    return OUT


if __name__ == "__main__":
    print(render())
