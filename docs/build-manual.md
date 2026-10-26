# Build manual

Every number you need, in build order. Coordinates are (x, y) in cm measured from the back-left corner of top A: x runs along the back wall, y along the side wall. Work on the undersides with the tops face down on a blanket; a helper is needed for steps 6 and 7. Budget a weekend: steel prep on day one, assembly on day two.

The interactive 3D model is at `index.html` (open it in a browser, or enable GitHub Pages on this repo and open the site). The full design review with the structural reasoning is in `design-review.md`.

## 0. Before you start

- [ ] Both EKBACKEN tops measure 28 mm thick (calipers). If a top measures 27 mm, nothing changes: the deepest screw (the rail's #10 × 1 in, 20.6 mm in) still stops 6 mm short of the laminate. If it measures less than 27, stop and ask before drilling.
- [ ] Six OLOV legs on hand. Plate is 10.5 cm across with five 5.5 mm holes on an 85 mm circle, neighbouring holes 50 mm apart (22 Oct 2026); the printed leg jig marks all five. Count the M4 screws in the boxes: five per leg, 30 in all.
- [ ] Eight of your twelve round 4 in feet (four per ALEX, four spare). Plate 59.5 × 59.5 mm with four holes 46.8 mm apart (measured 23 Oct 2026: 41.6 mm between two neighbouring holes with the inside jaws, 52.0 across them with the outside jaws, so 5.2 mm holes), body and pad 5 cm, 10 cm tall.
- [ ] Printed tools from `parts/tools/` (see `parts/README.md`) before any marking: the edge T-square (50/85/100/150 mm offsets and the feet-plate holes), the leg jig (an OLOV's centre and five plate holes at 10 or 15 cm from the edge), the feet corner jig (a far-corner foot and its four plate holes in one placement), the foot height gauge (102 mm), the wall gauge (65 and 30 mm), the ALEX corner template (ring centre and screw holes in one placement), the rail marking gauge (19 and 29 mm lines), the rail drill jig (1/8 in bore on the 19 mm line), two fitting centring plugs, two rail setback gauges (120 mm from the front edge to the rail's outer face) and the pilot drill guide. Optional, from `parts/cables/` and `parts/accessories/`: rail end caps, cable hooks and clips, power-bar cradles, cable tray, wall-gap strip, phone stand, ALEX feet (2, 4 or 6 cm under the cabinets; height table before step 5).
- [ ] Eight printed locating rings for the pads (`parts/structure/foot-ring.stl`, source beside it): 52 mm bore for the 50 mm pad, 3 mm wall, 10 mm ring on a 75 mm × 2.5 mm flange with three countersunk holes for #6 × ⅝ in flat-head screws, open bottom. PETG or ABS, printed flange-down. Plus 24 × #6 × ⅝ in flat-head screws.
- [ ] Two lengths of 2 × 2 × 3/16 in hot-rolled steel angle, cut to 213 cm (84 in) by Metal Supermarkets, ends deburred.
- [ ] Four 10 × 3 in mending plates, 19 × #10 × 1 in pan-head screws (rails), 32 × #8 × ⅝ in pan-head screws (feet plates), 8 × #10 × ⅝ in screws with #10 washers (joining plates), two 5 mm gusseted 90° strut fittings (1-5/8 in channel size, legs 100.5 × 41 mm, two 21 × 12 mm slots per leg), 6 × 3/8-16 × 1½ in hex bolts, grade 5 (one length for both rails), 6 × 3/8 nylon-insert nuts, 12 × 3/8 flat washers. Buy a few spares of each screw.
- [x] VIVO crossbar measured 19¾ in (50.2 cm) centre to centre of its end collars: clamps at 40 cm from the corner put the poles exactly that far apart.
- [ ] An automatic centre punch and cutting oil for the steel; a 5/64, 1/8, 7/32 and 7/16 in bit (the 7/16 cobalt).
- [ ] Room cleared: the desk needs 252 × 317 cm of floor including the 3 cm wall gaps, plus the side wall running at least 322 cm (top B is stood 5 cm out in step 7 and pushed home) and 40 cm of free floor on the desk's open sides (the desk is pulled into the room in step 8b). If the side wall is shorter than 322 cm, stop and ask before step 7.

## 1. Drill the steel (bench)

| Piece | Length | Holes | Where |
| --- | --- | --- | --- |
| Rail A | 213 cm | 9 × 7/32 in in the flat leg | 19 mm from the leg's free edge; at 3.5, 28, 54, 80, 106, 132, 158, 184, 210.5 cm from one end (call it the wall end). The first is at 3.5, not 2.5, so it sits 4.5 cm from top A's end, so it stays 4 cm from top A's end |
| Rail B | 213 cm | 10 × 7/32 in in the flat leg | same offset; at 2.5, 7.5, 28, 54, 80, 106, 132, 158, 184, 210.5 cm from one end (call it the corner end) |
| Both rails | | 7/16 in bolt holes for the corner fittings, in the vertical leg, 29 mm down from the heel edge | on the bench, using one fitting as the template. Rail A: clamp the fitting to the vertical leg with its heel on the 52.0 cm mark from the wall end, legs pointing toward the far end; a slot plug in each slot, 1/8 in pilot through the plug. Clamp it again with its heel on the 51.5 cm mark, legs pointing toward the wall end; plug and pilot. Rail B: heel on the corner end itself (0 cm), legs toward the far end; plug and pilot. Fitting off, open all six to 7/16 in. Mark the 51.5 and 52.0 cm heel positions on rail A's vertical leg with a scribe, not pencil, and after painting (step 1 end) put a strip of tape at 52.0 and re-label both ends, because step 7 checks rail B's outer face against that 52.0 mark. The holes land at the fittings' slot centres, 29.15 and 78.45 mm from each heel (measured 23 Oct 2026): rail A at 54.9 and 59.8 cm from the wall end (outside fitting) and 48.6 and 43.7 (inside fitting); rail B at 2.9 and 7.8 from the corner end. At assembly the bolts have 1.6 mm of play in the rail holes and, in the fittings' 21 × 12 mm slots, 2.5 across and 11.5 along; that is why step 7 tightens them fully, the corner holds by friction |

Centre-punch every mark, drill at low speed with oil, deburr with the file. Degrease, scuff, two coats of flat black enamel, dry 24 h.

## 2. Mark top A (face down)

Each top has one rounded, laminated long edge and one square, unfinished long edge. The unfinished edge goes against the wall: it is y = 0 on top A and x = 0 on top B. The rounded edge is the front edge. Either short end can be the side-wall end; pick one and tape it. Measure from the taped end (x = 0) and the unfinished long edge (y = 0). If it is 27 mm, nothing changes: the deepest screw still stops 6 mm short of the laminate; under 27, stop and ask.

| Mark | Centre (x, y) | Purpose |
| --- | --- | --- |
| L1 | (15, 42) | OLOV, under VIVO clamp 2; its 10.5 cm plate ends 6.5 mm short of rail A |
| L2 | (65, 10) | OLOV |
| L3 | (140, 10) | OLOV |
| F1–F4 | (214.5, 8.5), (240.5, 8.5), (214.5, 56.5), (240.5, 56.5) | round feet for ALEX 1; 5 cm in from each ALEX corner, the 6 cm plates 5 mm clear of rail A. F2 and F4: feet corner jig over the far corners (8.5 from both edges). F1 and F3: T-square's 85 hole, tape hooked on the far end, at 34.5 cm from the far end |
| Rail A line | y = 53, from x = 1 to 214 | the vertical leg's outer face goes on this line, flat leg toward y = 47.9 (the leg is 5.08 wide) |
| Clamp zone 1 | x 36–44, y 0–9 | keep clear |
| Clamp zone 2 | x 0–9, y 36–44 | keep clear |
| Pad plates (draw the outline only) | x 20.0–45.4, y 0.5–8.1 and x 0.5–8.1, y 20.0–45.4 | the two spare mending plates go here, loose, under the clamp jaws in step 8; 2.5 cm clear of rail A |
| Plates P1, P2 | centred (15, 66) and (35, 66), long axis along y | span y 53.3–78.7 (3 mm clear of rail A). The plates are 10 × 3 × 0.12 in with four holes along the length at 0.79, 2.76, 7.26 and 9.21 in from one end (2.0, 7.0, 18.4, 23.4 cm). Laid across the joint those land at y 55.3 and 60.3 in top A, 71.7 and 76.7 in top B: all four get a screw |

## 3. Mark top B (face down)

Measure from the end that butts against top A (y = 65) and the edge that goes against the side wall (x = 0).

| Mark | Centre (x, y) | Purpose |
| --- | --- | --- |
| L4 | (10, 85) | OLOV, 20 cm from the joint end |
| L5 | (10, 160) | OLOV |
| L6 | (10, 235) | OLOV |
| F5–F8 | (8.5, 279.5), (56.5, 279.5), (8.5, 305.5), (56.5, 305.5) | round feet for ALEX 2. F7 and F8: feet corner jig over the far corners. F5 and F6: T-square's 85 hole, tape hooked on the far end, at 34.5 cm from the far end |
| Rail B line | x = 53, from y = 65 to 266 | the vertical leg's outer face on this line, flat leg toward x = 48 |

## 4. Fit legs and feet to both tops

1. Legs: start the five pilots through the leg jig with the 1/8 in bit, lift the jig, finish 15 mm deep with the 15 LEG puck, then drive the IKEA M4 × 16 mm screws (about 13 mm into the top). Pre-set every OLOV to 80.2 cm (measure plate face to foot), or the table's number if you fit the optional ALEX feet.
2. Feet: first, with each foot loose in your hand, wind its pad out until the printed foot height gauge (102.0 mm inside) just slides over it from the side with no rock; all eight then match without a ruler. Then the plates: start the four pilots through the jig's holes with the 1/8 in bit, lift the jig, finish 15 mm deep with the 15 LEG puck; screw each plate to the top, pad pointing away from the top. (The gauge sits against the plate face, so it cannot be used once the plate is screwed on.)
3. Rail A: clamp it on its line, flat leg against the top, wall end at x = 1 (1 cm in from the taped end). Hook a rail setback gauge over the front edge near each end and push the rail against both (12 cm from the front edge to the vertical leg's outer face), check the middle with one, or measure 12 cm at both ends and in the middle, before drilling; drill and drive the two end screws first, re-check, then the rest. Through each rail hole, drill a 1/8 in pilot 20 mm into the top: the printed drill guide's 25 RAIL step on the flat leg, or a tape flag on the bit 25 mm from the tip (4.8 mm steel plus 20 mm). Drive #10 × 1 in screws with the Robertson #2 bit on the 3 in extension (the chuck would hit the vertical leg otherwise) until the head seats. Nine screws.
4. Rail B: clamp it on its line with the corner end projecting 12 cm past the top's joint end. Pilot and screw holes 3 to 10 only (eight screws). Holes 1 and 2 wait for step 7.

**Optional ALEX feet.** The desk is built at 83.0 cm as planned. If you want it higher, print four solid round feet per ALEX (`parts/accessories/alex-foot.scad`, 2, 4 or 6 cm, three #6 × 5/8 in screws each driven down wells in the column, TPU pad) and screw them under the ALEX bottom corners before step 5: the corner template marks them exactly where the rings go on top, screws in its inner three holes. Everything on the desk stays where it is; only these four numbers move, all by the foot height:

| ALEX feet | Underside of the tops | Top surface | Every OLOV set to | Rail lower edge |
| --- | --- | --- | --- | --- |
| none (as planned) | 80.2 | 83.0 | 80.2 | 75.1 |
| 2 cm | 82.2 | 85.0 | 82.2 | 77.1 |
| 4 cm | 84.2 | 87.0 | 84.2 | 79.1 |
| 6 cm | 86.2 | 89.0 | 86.2 (OLOV max 90) | 81.1 |

Decide before step 4, because the OLOV pre-set in step 4 is the table's number. Seat height goes up by the same amount: about 52 cm without feet, 58 cm with the 6 cm feet.

## 5. Place the ALEX units

| Unit | Footprint (x, y) | Faces |
| --- | --- | --- |
| ALEX 1 drawers | x 209.5–245.5, y 3.5–61.5 | drawers toward you (+y) |
| ALEX 2 storage | x 3.5–61.5, y 274.5–310.5 | door toward you (+x) |

The tops are not up yet, so set the units by the walls: ALEX 1's back 6.5 cm off the back wall (the printed wall gauge's 65 leg just fits) and its near side 212.5 cm from the side wall; ALEX 2's side 6.5 cm off the side wall and, for now, its near end 282.5 cm from the back wall, 5 cm short of its final 277.5, so that top B can be lowered onto it with rail B's end clear of rail A's flat leg; it is pushed home in step 7. Top B's far end then reaches 319 cm from the back wall for a moment, so the side wall must run at least 322 cm; if it does not, stop and ask before standing top B. That is 3.5 cm inside the tops' edges all round once the tops are on, 3 cm off the walls. Painter's tape on the floor saves guessing.Do not fit the locating rings yet. A pad is 50 mm and a ring's bore 52, so a ring has to sit within a millimetre of where its pad lands, closer than a cabinet can be placed by measuring. The rings are fitted in steps 6 and 7 by tracing the pads: stand the top on the bare cabinet, trace round each pad, lift the top off, screw the rings on the traces. The printed corner template (ring centre 5 cm in from each corner, three screw holes) is then only a check that the traces landed where the plan says. The ALEX top panel is 5/8 in (15.9 mm, measured 23 Oct 2026): the #6 × ⅝ in screws reach 13.4 mm into it and the 12 ALEX pilot 12, so 2.5 mm of panel stays under every screw.

## 6. Stand top A (two people)

Top A already has its legs and feet on it; the ALEX has no rings yet. With a helper, turn it over and stand it on its legs with its four pads on the bare ALEX top, lowering the ALEX end first, then the leg end. Push the ALEX unit, never the top, until the top shows 3.5 cm all round the cabinet and the wall gauge's 65 leg just fits between the wall and the ALEX. Now the rings: trace round each pad with a sharp pencil; lift the top off onto the blanket (two people); set a ring on each circle and look down through its open bottom until the pencil line shows all the way round the bore; start the three 5/64 pilots through the ring's own holes 3–4 mm, lift the ring, finish 12 mm deep with the 12 ALEX puck; drive the #6 × ⅝ in screws. Stand the top up again: the pads drop into the rings. From here never push the top: push the ALEX unit with the pads sitting in its rings and the top comes with it. Put a level on the top along x and along y; adjust the OLOV feet and the round feet until it reads flat and all four pads bear with no rock. Target: top surface 83.0 cm above the floor at every corner.

## 7. Stand top B and make the joint

1. Wind top B's OLOV legs 2–3 mm short so rail B's corner end can slide under top A. ALEX 2 has no rings yet and stands 5 cm further from the back wall than its final place (its near end at 282.5 cm from the back wall, step 5), so rail B's corner end comes down clear of rail A's flat leg. Turn top B over onto its legs with its pads on the bare ALEX 2 top; push the cabinet, never the top, until 3.5 cm of top shows all round it and the wall gauge's 65 leg fits at the side wall; then fit the rings exactly as in step 6 (pencil round each pad, lift top B off, rings on the circles, pilots through the rings, screws) and stand top B back on with its pads in the rings. Now push ALEX 2 toward the back wall, with the pads in the rings so top B comes with it, until rail B's end touches rail A's vertical leg and its end meets A's front edge, 3 cm off the side wall. Then wind the legs up to flush.
2. Bring the two surfaces level at the joint by turning the OLOV feet and the round feet, never by packing anything under the joining plates. A fingertip across the joint should find no step.
   Check under the corner before going on: rail B's end must touch the face of rail A's vertical leg with no gap, and rail B's outer face must line up with the 52.0 mark on rail A. If not, push ALEX 2 with the pads in its rings so top B moves with it; never lift or push the top alone. Only then screw the plates.
3. From below, hold plate P1 on the outline you drew (y 53.3–78.7, 3 mm clear of rail A; it is not centred on the joint), scribe through its four holes, take the plate away, and pilot each hole 1/8 in, 12 mm deep, with the 12 PLATE puck standing on the wood (two holes land in each top). Put the plate back and drive #10 × ⅝ in screws with washers. Same for P2.
4. Drill rail B's holes 1 and 2 into top A (the drill guide's 25 RAIL step, or a 25 mm tape flag) and screw.
5. Bolt on the two gusseted fittings (their holes and the rails' holes were drilled to match in step 1). Outside fitting: heel at the outside corner, one leg on rail A's vertical leg toward the far end, the other on rail B's outer face, gusset facing the open space under the knee corner, web at the top edge (on the outside nothing is in the way either way; the drawings show it up). Inside fitting: heel at the inside corner, one leg on rail A's vertical leg toward the wall, the other on the inner face of rail B's vertical leg, with its gusset pointing at the floor (the hole pattern is symmetric, so the bench-drilled holes still line up; gusset-up it would sit 1 mm under the head of rail B's screw 1). Rail A: four 3/8-16 × 1½ in bolts from the fitting side, washer under each head, washer and nylon-insert nut on the inside of the leg. Rail B: two 3/8-16 × 1½ in bolts through outside fitting, leg and inside fitting, washer each end, nylon-insert nut. Tight, not snug: these six bolts hold the corner by friction. The fittings' 21 × 12 mm slots leave 2.5 mm of play across and 11.5 along each bolt, and the rails' 7/16 in holes 1.6 mm, so only the clamping force keeps rail B's corner from settling. With a torque wrench, 25 N·m (18 ft·lb), under the standard dry torque even for a grade 2 bolt, the weakest sold; without one, pull as hard as one hand can on a 15 cm wrench, then stop. Never an impact wrench or impact driver on these bolts: a 1/2 in impact wrench delivers many times this and will strip the 3/8 thread or shear the bolt; run the nuts down by hand and finish with a hand ratchet or torque wrench, 9/16 in socket. Tighten them only after the two surfaces are flush and rail B's end touches rail A. The mending plates from step 3 align the tops; they do not carry the corner. If the corner ever drops a millimetre, retighten these bolts.

## 8. Monitors, PC and the rest

| Item | Position | Note |
| --- | --- | --- |
| VIVO clamp 1 | centred x 40 on A's back edge; finger-tight until the crossbar is on | a spare mending plate flat between the jaw and the top, long side along the edge on the outline from step 2; 28 mm top plus plate is under 60 mm, so use the manual's Option 1 (holes 2 and 4 on the lower clamp) |
| VIVO clamp 2 | centred y 40 on A's left end edge | same; both clamps sit in the 3 cm wall gap |
| Crossbar | diagonal between the poles | fit it first as the spacing guide (manual step 3), then refit it at monitor height (step 6). Poles 50.2 cm apart (crossbar measured centre to centre); the bar on the poles sets the last millimetre, so tighten the clamps with it fitted |
| Samsung Odyssey G5 32 in (1000R, landscape) | centre bracket (VESA 75), screen centred (36.5, 36.5) on the diagonal, 20 cm in front of the crossbar; the curve brings its ends 6.5 cm toward you | bottom edge 23 cm above the top (13 cm over the ELLOVEN), top edge 66.9, inside the mount's 26.5 in (67.3 cm) centre-screen limit. Only 4 mm spare: if the assembled mount will not reach, lower the G5; a bottom edge anywhere down to 12 cm still clears the ELLOVEN |
| ELLOVEN | centred (36, 36), turned 45°, drawer toward you | under the G5; its back corners clear the clamp plates and poles by over 2 cm (at (33, 33) they would sit on the clamps) |
| Acer right (landscape) | along the back wall, centred about (99, 19), toed 15° toward you; its near end about 12 cm from the G5's curved end | bottom edge 26 cm above the top; the arm runs along the wall behind the panel, then forward into the VESA plate |
| Acer left | along the side wall, centred about (19, 99), toed 15° | same |
| Edifiers | centred (108, 22) and (22, 108), grilles toward you | under the outer half of each Acer |
| HYTE Y60 | x 197.5–246.5, y 4.5–35.5, standing on its I/O end on the MakerWorld pedestal (model 679012), long axis along the back wall, side glass facing you, front glass facing up | over ALEX 1 |
| Deskmat and NuPhy | mat centred (55, 55) turned 45°; keyboard centred (58.5, 58.5); mouse (74, 45) | on the corner square, its back edge touching the ELLOVEN's front feet, its front edge at the inside corner |
| Lamp | base centred (183, 20), arm reaching toward the keyboard | on top A beside the Y60 |
| Headset stand | base centred (28, 140), hook toward you | on top B |
| Plant | centred (32, 298) | far end of top B, over ALEX 2 |

### 8b. Wall-gap trim, before the final push to the walls

1. With the desk in place against both walls, measure the gap between each top's raw back edge and the wall at five or six points along each wall. Set `gap` in `parts/accessories/wall-gap-common.scad` from the smallest reading with this table: 27 mm → 26, 28 → 27, 29 → 28, 30 → 29 (as saved), 31 → 30, 32 → 31, 33 → 32; under 27 or over 33, measure again and ask before printing and print the trim (cut list in `parts/README.md`).
2. Take the screens, the PC and everything loose off the desk first. Then two people, one at each ALEX unit: slide the whole desk 40 cm away from both walls. The ALEX units slide on their feet and the pads stay in their rings. Nothing comes apart.
3. Build each chain on the edge from the corner outward: corner piece, 80 mm filler, clamp piece with its notch round the clamp back (the clamps are already tight from step 8), then the 240 mm segments, slotted ones where the cut list says, ending with the short piece. Butt every joint and push a connector tile up into the pockets. Push an end cap into the last piece's end pocket on each wall, end wall flush with the trim's end, so the gap is closed at the far end.
4. Through each lip hole, pilot 5/64 in, 10 mm deep, with the drill horizontal and the drill guide's **10 EDGE** step held against the raw edge. Drive a #4 × 1/2 in flat head into each. Two per segment, one per corner leg, one each side of a clamp notch.
5. Slide the desk back until the wall gauge's 65 leg just fits between the wall and each ALEX again. The trim's outer edge stops 1 mm short of the wall.

Retighten every screw after two weeks.

## 9. Checks before you call it done

- [ ] Top surface 83.0 cm at all six corners of the L (± 3 mm; with optional ALEX feet, 83.0 plus their height). Adjust: corner (0, 0) by L1 and L2, (249, 0) and (249, 65) by the ALEX 1 feet, (0, 314) and (65, 314) by the ALEX 2 feet, (0, 65) by L4; the inside corner (65, 65) has no support of its own, it follows the joint, so check it last.
- [ ] A level across the joint reads flat both ways.
- [ ] Corner load test, a known weight rather than a shove: set 20 kg (a case of water plus a few books) on top B's inside corner, the case's two near faces 10 cm from the corner's two edges. Lay a straightedge flat on the surface from above leg L1 toward the inside corner, hold it down over L1, and read the gap under its far end at the corner before and after the weight goes on: it should drop no more than 2 mm (the estimate for 20 kg is about 1). Lift the weight off: the corner returns to where it was, nothing creaks, no screw or bolt has moved. Do not stand or sit on the corner; that is not what the beam was sized for.
- [ ] All eight feet pads bear in their rings: try to rock each pad sideways by hand (do not turn it, that changes its height); none should rock or lift.
- [ ] Lay a straightedge across the joint at the inside corner and write down any step. Check it again after two weeks and after the first month: if the corner has settled, retighten the six fitting bolts.
- [ ] Push the desk sideways along each wall: no sway at the top beyond a few millimetres.
- [ ] No screw tip visible or felt as a bump on either laminate face.
- [ ] Knees clear: sit at the corner, slide in, nothing within reach of a knee or thigh.
- [ ] Both ALEX fronts open fully without touching a foot or a leg.
