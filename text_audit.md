# Text and graphics audit — Image 1 recreation

## Text preservation

Image 1 is the base layer. Its masthead, edition line, date, subtitle, seven region labels and counts, six statistics, all 33 story items, map, date-check sentence, footer, and every article headline, description, and source reference remain in their original positions. No text was retyped, rewritten, or added to the art panels. The complete visible copy is transcribed in `reference_transcription.md`.

The source clips part of the first lead card's final source line at the lower card edge. The image was preserved as supplied; the transcription notes this clipping rather than silently correcting it.

## Graphics adapted from Images 2 and 3

- Story 4, Crimea bridge: bridge strike scene from Image 2.
- Story 5, Riyadh missile: night skyline and interception scene from Image 2.
- Story 6, Cyclone Akvan: cyclone symbol from Image 3.
- Story 9, Anthropic: chart detail from Image 3, without its labels.
- Story 10, GTA VI: city and car strip from Image 2, without its labels.
- Story 11, Bogotá: march crowd from Image 2, retaining Image 1's own banner.

Image 1 has no France story, so Image 3's French political graphic was not placed on an unrelated item. Other cards retain Image 1's original topic-matched art.

## Output checks

- PNG: valid, 1024 × 1024 pixels
- Size: 426,030 bytes (under 1 MiB)
- SHA-256: `467c2c993a30d09195f327144c13c9103b795d74bdcfadef4b9b6e5ddfea96ff`
- Renderer: deterministic Pillow compositing; source text remains from Image 1
- Main runtime: existing `main.ts`; Node built-ins only, copies the bundled `assets/entry.png`
- No commit, push, or submission performed

## Changed files

- `render.py` — reproducible composition of relevant supplied art into Image 1's artwork panels
- `assets/entry.png` — final image
- `assets/reference-2.webp` and `assets/reference-3.webp` — bundled art references used by the renderer
- `reference_transcription.md` — Image 1 copy transcription
- `text_audit.md` — this report
