# Quality-control report · assembly manual

Built 23 Oct 2026 from the repository at commit 459465afdf429f88e9928482752b118f5d7cdea3 (the measured facts since a2e99ea are included; see `manual/facts.json` `source_commit`). The brief named a2e99ea; the facts measured after it (feet plate 46.8, OLOV pattern on the 85 mm circle, VIVO pole inset 43.7 and pad, strut fitting slots, 1½ in bolts everywhere, the printed drill jigs) are in this manual and in the repository documents, so the two agree.

## Deliverables
| File | Pages | Content |
| --- | --- | --- |
| `manual/IKEA-Style-Assembly-Manual.pdf` | 72 | cover, contents, chapters A–K, appendix |
| `manual/Drilling-and-Placement-Templates.pdf` | 25 | T0 index, T1 ring (1:1), T2 feet plate (1:1), T3a/b OLOV (1:1), T4-A/B rail strips (1:1, 9 landscape sheets each), T5 fittings (reference 1:2 with VERIFIED rail hole positions), T6 clamp pads (reference 1:4) |
| `manual/Assembly-Verification-Checklist.pdf` | 3 | measurements before you start, gates at each step, final checks, two-week and one-month items |
| Source: `manual/src/` (chapter HTML and figure scripts), `manual/figures/` (162 SVG), `manual/lib/draw.py`, `manual/build.py`, `manual/facts.json`, `manual/data.json` | | rebuild with `python3 manual/build.py` |

Illustrations in the manual: 133 inline vector figures (plus 25 template sheets and the checklist icons). All vector; pages are A4 with 16 mm margins.

## How it was checked
- Every chapter was written from `facts.json` and `data.json` (extracted from the guide's `D` object) and `docs/build-manual.md`; no number was allowed from anywhere else. Each author rendered its pages to PNG at 60 and 100 dpi and read them; then every page of all three PDFs was rendered and read again at integration, with the dense pages (face-down marking diagrams, both rail fabrication drawings, the underside layout, the joint plan, the clamp section) re-read at 110 dpi.
- Built text audited for stale values (47.0 / 47.4 / 36.6 feet spacing, 9/16 in holes, 1¼ in bolts, 11 cm plate, 4.5 cm pole inset, the M7, the old drill-guide step names): none remain. Required values present: 46.8, 2130, 29.15 / 78.45, rail holes 549.2 / 598.5 / 485.9 / 436.6 / 29.2 / 78.5, 25 N·m, 830 / 802 / 751, 43.7, 502, 105, 59.5, 5.2, 21 × 12, 20 kg / 2 mm, 2520 × 3170, every leg and foot coordinate as in data.json.
- Templates: every hole recomputed from the source numbers and compared with the SVG coordinates (43 holes, max error 0.002 mm); 100 mm rulers measured on the rendered PDF at 254 dpi (1000.0 px landscape, 999.5 px portrait); all sheets A4.
- Geometry rules verified on the drawings: no rail rests on a cabinet (rail A's end is 5 mm from feet F1/F3, rail B's 135 mm from F5/F6, the top bridges it); top B is top A turned, never mirrored; the inside fitting is gusset-down; the load test shows a case of water, never a person; the fittings go on after the plates and rail B's screws 1 and 2.

## Dimensions independently checked (source → manual → drawings)
Footprint 2490 × 650 per top, 2490 × 3140 overall, 30 mm wall gaps, 2520 × 3170 floor · six legs (150,420) (650,100) (1400,100) (100,850) (100,1600) (100,2350) · ALEX 1 x 2095–2455 y 35–615, ALEX 2 x 35–615 y 2745–3105, 35 all round, 65 off the walls · eight feet 85 in from the edges, F1 F3 F5 F6 345 from the far ends · rails 2130 long, 120 back, A x 10–2140 at y 479–530, B y 530–2660 at x 479–530, B's 120 overlap under A · screw line 19, bolt line 29, stations 35 … 2105 (A) and 25 … 2105 (B) · fitting heels 520 and 515 on A, corner end on B; slot centres 29.15 / 78.45 · hole sizes 5.56 / 11.1 / 3.2 / 2.0, screw lengths and depths per the fastener table, 21 mm limit · heights 830 / 802 / 751, foot 102, ALEX feet table · clamps at 400, zones 360–440, pad plates 200–454 × 5–81, pole 43.7 in, crossbar 502, pad 13.5–63.5 · monitor heights 230 / 669 / 673 · part and hardware quantities (H01 30, H02 32, H03 19, H04/H05 8, H06 24, H07 48, H08 6, H09 12, H10 6, H11 8).

## Outstanding physical measurements (each is flagged where it is used)
1. EKBACKEN thickness (expect 28; if 27, every screw into the top loses 1 mm).
2. Delivered rail lengths and angle thickness (design 2130 from the labelled end; bought as 84 in = 2133.6).
3. Feet pad diameter (rings bored 52 for the 50 mm pad).
4. ALEX bottom panel thickness (only for the optional ALEX feet). The top panel is measured: 15.9 mm, screws 13.4 in, 2.5 remains.
5. ALEX height with and without its stock feet (docs assume 700).
6. VIVO top arm reach (about 89) and maximum opening (31 or more).
7. Room: wall to wall 2520 and 3170, baseboard thickness.
8. Feet load rating (design wants 50 kg or more each).

## Contradictions found in the sources and resolved during the build
- Feet plate hole spacing stated as 47.0 in `parts/README.md` and in the engraved labels of two printed jigs while the geometry was 46.8: README and labels corrected.
- `data.json` (from the guide) still said leg L1's plate ends 4 mm short of rail A (11 cm plate); the build manual's 6.5 (105 plate) is right: guide and data corrected.
- The build manual's step 7 said the joining plates come "in the next step" while they are fitted before the fittings: corrected to the manual's own order (plates → rail B's screws 1 and 2 → fittings).
- Strut fittings were assumed to have 9/16 in round holes at about 25 and 65 from the heel; measured 23 Oct: 21 × 12 mm slots at 29.15 and 78.45; every document, the 3D model's bolts and the printed plug (now a slot plug) updated.
- The guide's tool list said a 3/8 in wrench; the 3/8-16 bolt takes a 9/16 in wrench: corrected.
- The guide's floor test said rail B's flat leg covers 47–52 cm; it is 46.9–52: corrected.
- The build manual said rail A's first hole stays 4 cm from the top's end; it sits 4.5 cm: corrected.
- The design review's sag estimate (2–3 mm worst case) and the acceptance limit (2 mm) read as a conflict; the review now says the 20 kg test alone gives about 1 mm.
- The load test did not say where the case sits or how the straightedge is held; the manual and guide now do.
- The paper ring template and the printed corner template drilled the ring's three holes at different angles (both valid on a round ring); the paper template now uses the printed tool's angles so both give the same holes.
- Three authors reported the handoff file as saying 1¼ in bolts; it does not (the 21¼ in crossbar figure was misread). No change.

## Assumptions retained from the design review (labelled ASSUMPTION / FIELD CHECK in the manual)
ALEX height 700 · VIVO top arm reach about 89 · feet load rating · the 3-4-5 squareness field check (not in the build manual) · corner sag about 1 mm under the 20 kg test (estimate, not a measured capacity) · bolt preload and friction margin (torque, not measured preload) · the lower jaw pad oval drawn centred on the clamp.

## Second build (same day): what changed and what was re-verified
- Units: cm for everything a tape reads, mm for calipers and drills, on every page; no page asks the reader to add or subtract (the two former cases, a 27 mm top and the trim gap, are now a plain statement and a lookup table).
- Tools: chapter B gained five pages, one panel per printed jig drawn in use with its steps and first-print check; chapter E gained the panel and drawing "why the holes on both rails meet without a jig".
- Rings: fitted by tracing the pads with the top standing on the bare cabinet (chapters G and H, build manual steps 5–7, checklist); bore 52 / OD 58 for the 50 mm pad; screw circle pinned at r 33 in `foot-ring.scad`, `alex-corner-template.scad`, `facts.json` and template T1, and asserted equal by `figures_T.py` (which reads the pinned value instead of deriving it).
- Measured on the hardware 23 Oct 2026 and now VERIFIED throughout: strut fittings (legs 100.5 × 41 × 5, slots 21 × 12 at 29.15 / 78.45 from the heel; rail holes 54.9 / 59.8 / 48.6 / 43.7 cm on A, 2.9 / 7.8 cm on B), ALEX top panel 15.9 mm (screws 13.4 in, 2.5 remains), feet plate 59.5 with 46.8 centres, VIVO pole inset 43.7 and pad. Defined by CAD / the documents (SOURCE): every coordinate, the rail layout, the ring and foot geometry, heights. Still ASSUMPTION or MEASURE: see the list above (the ALEX top panel is removed from it; the bottom panel remains, for the optional feet only).
- Verification run on this build: all three PDFs built from a clean clone of the repository (same page counts); built text searched for stale ring (51 / 57), panel-rule (16 mm) and earlier-geometry strings: none; the templates' 43 holes re-derived from the sources (0.002 mm) and the 100 mm rulers re-measured at 254 dpi; every page rendered and read again after the rebuild.

## Not done
No paper print was measured (the 100 mm rulers were measured on the rendered PDF). The desk has not been load-tested; the manual's chapter J is the acceptance test, not a structural certification.
