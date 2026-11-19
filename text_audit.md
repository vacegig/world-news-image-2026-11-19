# Text and output audit

## Content source

Audited against `reference_transcription.md`, which records the latest supplied Image 1 (the 19-story edition).

## Counts checked

- Edition date: Thursday 19 November 2026.
- Numbered stories: 1–11, each with its location/category, headline, and description.
- Additional briefs: 8, all included in the original order.
- Total stories: 19.
- Statistics: 6.
- Date-check exclusions: all 6 entries retained, including Qeshm Island (17 Nov).
- Publication footer and source list: included.
- Map title and both legend lines: included.

## Visual review

Inspected the rendered PNG at full size. Headlines, brief labels, descriptions, map, date check, and footer are visible without clipping. All article headlines use the same serif family at a fixed 16.2 px size; story descriptions and briefs use the same serif family at a fixed 12.2 px size. All story artwork is cropped only from the three supplied WebP references. The summit, game, court, cyclone, climate, exam, Iran, Gaza and Australia graphics come from reference 1; the ANT market panel comes from reference 2; the Colombia protest panel comes from reference 3. No standalone PNG illustration assets are loaded by the renderer.

The page keeps the supplied image’s content and masthead wording, with the grid, typography and map placement refreshed for a cleaner, more readable mix of the three visual references.

## Output checks

Run `python3 render.py` to regenerate `assets/entry.png`; the renderer uses only local assets and fonts. `main.ts` copies the bundled PNG to `/output/entry.png`.

## Final artifact

- `assets/entry.png`: valid 1024 × 1024 indexed-color PNG.
- Byte count: 202,210.
- SHA-256: `78c1ed45b39a4e025da64fe50ac74886eca293ef37b6bb40cae39944ed4d9fa5`.
- Two consecutive renders produced the same SHA-256.
- `out/entry.png` was refreshed through `main.ts` and matches `assets/entry.png` byte-for-byte.
- Repeated `python3 render.py` runs produced the same SHA-256.
- The Node entrypoint copied the same PNG successfully to `/tmp/entry-output/entry.png` using `MAKEFUN_OUTPUT_DIR`.
- The default `/output/entry.png` destination could not be created in this container; the host returned `EACCES` for `/output`, including when retried with elevated execution. The entrypoint itself works with its supported output-directory override.
