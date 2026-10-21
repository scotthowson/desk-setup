# Build manual

Every number you need, in build order. Coordinates are (x, y) in cm measured from the back-left corner of top A: x runs along the back wall, y along the side wall. Work on the undersides with the tops face down on a blanket; a helper is needed for steps 6 and 7. Budget a weekend: steel prep on day one, assembly on day two.

The interactive 3D model is at `index.html` (open it in a browser, or enable GitHub Pages on this repo and open the site). The full design review with the structural reasoning is in `design-review.md`.

## 0. Before you start

- [ ] Both EKBACKEN tops measure 28 mm thick (calipers). If 27 mm, shorten every screw into the top by 1 mm.
- [ ] Six OLOV legs on hand. Plate is 11 cm across: keep that in mind at every mark below.
- [ ] Eight of your twelve round 4 in feet (four per ALEX, four spare). Plate 6 × 6 cm, body and pad 5 cm, 10 cm tall.
- [ ] Printed tools from `parts/tools/` (see `parts/README.md`) before any marking: the edge T-square (50/85/100/150 mm offsets and the feet-plate holes), the ALEX corner template (ring centre and screw holes in one placement), the rail marking gauge (19 and 29 mm lines) and the pilot drill guide. Optional, from `parts/cables/` and `parts/accessories/`: rail end caps, cable hooks and clips, power-bar cradles, cable tray, wall-gap strip, phone stand.
- [ ] Eight printed locating rings for the pads (`parts/structure/foot-ring.stl`, source beside it): 51 mm bore, 3 mm wall, 10 mm ring on a 75 mm × 2.5 mm flange with three countersunk holes for #6 × ⅝ in flat-head screws, open bottom. PETG or ABS, printed flange-down. Plus 24 × #6 × ⅝ in flat-head screws.
- [ ] Two lengths of 2 × 2 × 3/16 in hot-rolled steel angle, cut to 213 cm (84 in) by Metal Supermarkets, ends deburred.
- [ ] Four 10 × 3 in mending plates, 19 × #10 × 1 in pan-head screws, 16 × #10 × ⅝ in screws with washers, two 5 mm gusseted 90° strut fittings (1-5/8 in channel size, two holes per leg), 4 × 3/8-16 × 1 in bolts, 2 × 3/8-16 × 1½ in bolts, 6 × 3/8 nylon-insert nuts, 12 × 3/8 flat washers.
- [x] VIVO crossbar measured 21¼ in (54.0 cm) outer edge to outer edge, collars about 4 cm: poles 50.0 cm apart, clamps at 40 cm from the corner.
- [ ] Room cleared: the desk needs 252 × 317 cm of floor including the 3 cm wall gaps.

## 1. Drill the steel (bench)

| Piece | Length | Holes | Where |
| --- | --- | --- | --- |
| Rail A | 213 cm | 9 × 7/32 in in the flat leg | 19 mm from the leg's free edge; at 2.5, 28, 54, 80, 106, 132, 158, 184, 210.5 cm from one end (call it the wall end) |
| Rail B | 213 cm | 10 × 7/32 in in the flat leg | same offset; at 2.5, 7.5, 28, 54, 80, 106, 132, 158, 184, 210.5 cm from one end (call it the corner end) |
| Both rails | | 7/16 in bolt holes for the corner fittings, in the vertical leg, 29 mm down from the heel edge | on the bench, using one fitting as the template. Rail A: clamp the fitting to the vertical leg with its heel on the 52.0 cm mark from the wall end, legs pointing toward the far end; punch through both holes. Clamp it again with its heel on the 51.5 cm mark, legs pointing toward the wall end; punch. Rail B: heel on the corner end itself (0 cm), legs toward the far end; punch. Drill all six 7/16 in. The fittings' 9/16 in holes give 2 mm of play at assembly |

Centre-punch every mark, drill at low speed with oil, deburr with the file. Degrease, scuff, two coats of flat black enamel, dry 24 h.

## 2. Mark top A (face down)

Measure from the end that will go against the side wall (x = 0) and the edge that will go against the back wall (y = 0).

| Mark | Centre (x, y) | Purpose |
| --- | --- | --- |
| L1 | (15, 42) | OLOV, under VIVO clamp 2; its 11 cm plate ends 5 mm short of rail A |
| L2 | (65, 10) | OLOV |
| L3 | (140, 10) | OLOV |
| F1–F4 | (214.5, 8.5), (240.5, 8.5), (214.5, 56.5), (240.5, 56.5) | round feet for ALEX 1; 5 cm in from each ALEX corner, the 6 cm plates 5 mm clear of rail A |
| Rail A line | y = 53, from x = 1 to 214 | the vertical leg's outer face goes on this line, flat leg toward y = 48 |
| Clamp zone 1 | x 36–44, y 0–9 | keep clear |
| Clamp zone 2 | x 0–9, y 36–44 | keep clear |
| Plates P1, P2 | centred (15, 65) and (35, 65), long axis along y | span y 52–78, so 13 cm of each plate is on top A |

## 3. Mark top B (face down)

Measure from the end that butts against top A (y = 65) and the edge that goes against the side wall (x = 0).

| Mark | Centre (x, y) | Purpose |
| --- | --- | --- |
| L4 | (10, 85) | OLOV, 20 cm from the joint end |
| L5 | (10, 160) | OLOV |
| L6 | (10, 235) | OLOV |
| F5–F8 | (8.5, 279.5), (56.5, 279.5), (8.5, 305.5), (56.5, 305.5) | round feet for ALEX 2 |
| Rail B line | x = 53, from y = 65 to 266 | the vertical leg's outer face on this line, flat leg toward x = 48 |

## 4. Fit legs and feet to both tops

1. Pilot every leg plate hole 1/8 in, 15 mm deep, then drive the IKEA M4 × 16 mm screws (about 13 mm into the top). Pre-set every OLOV to 80.2 cm (measure plate face to foot).
2. Pilot the feet plate holes 1/8 in, 15 mm deep; screw each plate to the top, pad pointing away from the top. Wind each pad out until the foot measures 10.2 cm overall.
3. Rail A: clamp it on its line, flat leg against the top, wall end flush with x = 0. Through each rail hole, drill a 1/8 in pilot 20 mm into the top: the printed drill guide's 25 RAIL step on the flat leg, or a tape flag on the bit 25 mm from the tip (4.8 mm steel plus 20 mm). Drive #10 × 1 in screws with the Robertson #2 bit on the 3 in extension (the chuck would hit the vertical leg otherwise) until the head seats. Nine screws.
4. Rail B: clamp it on its line with the corner end projecting 12 cm past the top's joint end. Pilot and screw holes 3 to 10 only (eight screws). Holes 1 and 2 wait for step 7.

## 5. Place the ALEX units

| Unit | Footprint (x, y) | Faces |
| --- | --- | --- |
| ALEX 1 drawers | x 209.5–245.5, y 3.5–61.5 | drawers toward you (+y) |
| ALEX 2 storage | x 3.5–61.5, y 274.5–310.5 | door toward you (+x) |

Stand them 3 cm off the walls like the tops. A strip of painter's tape on the floor at x = 209.5 and y = 274.5 saves guessing.

Screw a locating ring to each ALEX top at the four foot positions: ring centres 5 cm in from each corner of the ALEX top (the same F1–F8 centres, now measured on the ALEX). The printed corner template gives the centre and the three screw holes in one placement; drop it over each corner, fences against the edges, punch through. Pilot 5/64 in, 12 mm deep; #6 × ⅝ in flat-head screws. The pads drop into the rings when the tops go on, which is what stops the desk sliding on the ALEX units; the ALEX units themselves then hold the whole desk against racking.

## 6. Stand top A (two people)

Lift top A onto L1–L3 with the four feet pads dropping into their rings on ALEX 1. Push it to 3 cm off both walls (the rings allow no slide once the pads are in, so lift and set, don't push). Put a level on the top along x and along y; adjust the OLOV feet and the round feet until it reads flat and all four pads bear with no rock. Target: top surface 83.0 cm above the floor at every corner.

## 7. Stand top B and make the joint

1. Lift top B onto L4–L6 with its pads in the rings on ALEX 2, its end against A's front edge, 3 cm off the side wall.
2. Adjust its legs and feet until the two surfaces are flush at the joint (run a fingertip across; shim the legs, never the plates).
3. From below, screw plates P1 and P2 across the joint: #10 × ⅝ in with washers, 1/8 in pilots 12 mm deep, 4 screws per plate, two in each top.
4. Push rail B's corner end against rail A's vertical leg. Drill its holes 1 and 2 into top A (pilots 20 mm, same 25 mm flag) and screw.
5. Bolt on the two gusseted fittings (their holes and the rails' holes were drilled to match in step 1). Outside fitting: heel at the outside corner, one leg on rail A's vertical leg toward the far end, the other on rail B's outer face, gusset facing the open space under the knee corner. Inside fitting: heel at the inside corner, one leg on rail A's vertical leg toward the wall, the other on the inner face of rail B's vertical leg, gusset tucked under rail B's flat leg (it clears the flat leg above and the heads of screws 1 and 2 by about 1 mm each). Rail A: four 3/8-16 × 1 in bolts from the fitting side, washer under each head, washer and nylon-insert nut on the inside of the leg. Rail B: two 3/8-16 × 1½ in bolts through outside fitting, leg and inside fitting, washer each end, nylon-insert nut. Snug, not cranked.

## 8. Monitors, PC and the rest

| Item | Position | Note |
| --- | --- | --- |
| VIVO clamp 1 | centred x 40 on A's back edge | a spare mending plate flat between the jaw and the top; 28 mm top plus plate is under 60 mm, so use the manual's Option 1 (holes 2 and 4 on the lower clamp) |
| VIVO clamp 2 | centred y 40 on A's left end edge | same; both clamps sit in the 3 cm wall gap |
| Crossbar | diagonal between the poles | fit it first as the spacing guide (manual step 3), then refit it at monitor height (step 6). Poles 50.0 cm apart (crossbar measured); the bar on the poles sets the last millimetre, so tighten the clamps with it fitted |
| Samsung M7 | centre bracket, screen centred (34, 34) on the diagonal, 20 cm in front of the crossbar | bottom edge 24 cm above the top, clears the ELLOVEN |
| ELLOVEN | centred (33, 33), turned 45°, drawer toward you | under the M7 |
| Acer right | along the back wall, centred about (99, 19), toed 15° toward you; its near end about 6 cm from the M7's end | bottom edge 26 cm above the top; the arm runs along the wall behind the panel, then forward into the VESA plate |
| Acer left | along the side wall, centred about (19, 99), toed 15° | same |
| Edifiers | centred (108, 22) and (22, 108), grilles toward you | under the outer half of each Acer |
| HYTE Y60 | x 197.5–246.5, y 4.5–35.5, standing on its I/O end on the MakerWorld pedestal (model 679012), long axis along the back wall, side glass facing you, front glass facing up | over ALEX 1 |
| Deskmat and NuPhy | mat centred (53, 53) turned 45°; keyboard centred (56.5, 56.5); mouse (72, 43) | on the corner square, centred in front of the ELLOVEN |
| Lamp | base centred (183, 20), arm reaching toward the keyboard | on top A beside the Y60 |
| Headset stand | base centred (28, 140), hook toward you | on top B |
| Plant | centred (32, 298) | far end of top B, over ALEX 2 |

Retighten every screw after two weeks.

## 9. Checks before you call it done

- [ ] Top surface 83.0 cm at all six outer corners (± 3 mm).
- [ ] A level across the joint reads flat both ways.
- [ ] Push the inside corner down hard: it should give 2–3 mm and spring back, no creak.
- [ ] Push the desk sideways along each wall: no sway at the top beyond a few millimetres.
- [ ] No screw tip visible or felt as a bump on either laminate face.
- [ ] Knees clear: sit at the corner, slide in, nothing within reach of a knee or thigh.
- [ ] Both ALEX fronts open fully without touching a foot or a leg.
