"""Write the supplied square newspaper artwork as the project PNG asset."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'assets' / 'entry-source.webp'
OUTPUT = ROOT / 'assets' / 'entry.png'

image = Image.open(SOURCE).convert('RGB')
if image.size != (1024, 1024):
    raise ValueError(f'Expected 1024x1024 source art, found {image.size}')
image.save(OUTPUT, format='PNG', optimize=True, compress_level=9)
