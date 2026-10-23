# Manual conventions (read before writing a chapter)

The deliverables are three PDFs built by `python3 manual/build.py` from HTML page fragments with inline SVG figures. Several people write chapters in parallel; these rules keep the result one booklet.

## Files
- `manual/data.json`: every coordinate, extracted from the guide's `D` object (cm). `manual/facts.json`: everything else, with provenance. **Print no number that is not in one of these two files or in `docs/build-manual.md`.** If you need a number that is missing, it is a MEASURE ON HARDWARE callout, not a guess.
- `manual/lib/draw.py`: SVG helper (mm page units; `Canvas`, `dim`, `hole`, `balloon`, `hatch`, `iso_box`, `warning_panel`, `badge`). Import with `sys.path.insert(0, 'manual')` then `from lib.draw import Canvas, badge, warning_panel`.
- Your chapter: `manual/src/chapters/NN-name.html` (fragment, no html/head) and `manual/src/figures_NN.py` that writes SVGs into `manual/figures/`. Run your figures script, then `python3 manual/build.py manual --render --dpi=60` and look at your pages in `manual/build/png/manual/`. Fix overlaps and cropping before you finish.
- Do not edit another chapter's files, `build.py`, `style.css`, `data.json` or `facts.json`. If a shared file needs a change, say so in your report.

## Page fragments
```html
<section class="page" data-chapter="E" data-title="Steel rails" data-toc="E · Steel rail fabrication and drilling">
  <h1>E · Steel rail fabrication and drilling</h1>
  ... content that fits one A4 page with 16 mm margins (content area 178 × 263 mm) ...
</section>
```
One `<section class="page">` per printed page. `data-toc` only on the first page of a chapter (or a major sub-part). The builder adds header, footer and page numbers; never write page numbers yourself. Chapters are lettered A–K as in the brief; the cover is `<section class="page cover">`.

Figures: `<img class="fig" src="../../figures/name.svg">` is inlined by the builder (add `style="width:178mm"` or `width="120mm"` to size it). Keep figure text at 3 mm or larger on the page (3.2 is the default), line weights 0.25 / 0.5 / 0.8 mm. Put each figure in a `<div class="figbox">` with a `<div class="cap">` caption that names the figure number, e.g. `Fig. E-3`.

Steps: `<div class="step"><div class="num">4</div><div class="body">...</div></div>`. One primary operation per step. Prefer a drawing to text.

## Units and arithmetic (binding)
- **cm for anything a tape measure reads**: positions on the desk (x, y), stations along a rail or an edge, lengths of tops and rails, distances from the walls, heights from the floor, the wall gap, the rail setback, the feet and ring insets. Write them as the build manual does: `214.5 cm`, `3.5 cm`, `83.0 cm`. One decimal where the manual has one; no trailing noise.
- **mm for anything calipers or a drill read**: thicknesses, hole diameters, screw lengths and depths, plate and ring sizes, slot sizes, the 19 / 29 lines on the steel, the hole spacings on the plates.
- Say the unit every time a number stands alone in text; in a table or on a drawing, say it once in the heading or caption ("all cm" / "mm").
- **No arithmetic for the reader.** Print the number the builder will read on the tool: if the tape is hooked on the joint end, print that reading, not a formula; if a depth depends on a thickness, print the depth. A page that needs the reader to add or subtract is a defect.
- Drawings may carry mm (CAD habit) but every label the builder measures with a tape gets its cm value too, in brackets if the mm must stay.

## Style
IKEA: white page, black line art, greys for fills, no meaning carried by colour. Isometric views use `Canvas.iso` (30°). Callouts are numbered balloons that use the part numbers (P01…P21) and hardware numbers (H01…H11) from `facts.json`; a page that uses a balloon shows the legend for it. Every dimension in mm (cm in brackets where the build manual uses cm). Hole symbols: circle plus centre mark, diameter written as `⌀3.2 (1/8 in)`. Arrows for insertion, rotation and alignment. Zoomed detail views in their own figbox.

Confidence labels: use `badge('VERIFIED')`, `badge('SOURCE')`, `badge('MEASURE')`, `badge('ASSUMPTION')` from `lib.draw` next to the dimension or table row they qualify, with the wording from `facts.json`. A source-defined dimension is never called verified. Any dimension not in the data files gets a `warning_panel(...)` **at the point of use**, not in an appendix.

Orientation words: back (wall side) / front (you), left / right as the user sits at the inside corner facing the diagonal; top face = laminate up; underside = face down while marking. The coordinate datum is top A's back-left corner (x along the back wall, y along the side wall); say it on every drawing that uses it.

## What the drawings must not show
- A rail resting on a cabinet. Rail ends load the top; the top loads the feet plates; the feet load the rings on the cabinets.
- Any part mirrored. Top B is top A rotated, not mirrored; the rail end caps are handed; the inside fitting is gusset-down.
- A person on the desk. The load test is 20 kg of water and books.
- Clamp jaw geometry beyond what `facts.json` says is measured.
