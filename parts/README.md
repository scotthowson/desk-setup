# Printed parts

Every part is an OpenSCAD source (`.scad`) with its rendered `.stl` and a `-preview.png` beside it. Change a number at the top of the source and re-render with `openscad -o name.stl name.scad`. Measurements in mm.

**Printers:** everything fits the Bambu P1S and A1 (256 × 256 × 256 mm; the longest part is 240 mm, the tallest 200). **Every STL is saved in its print orientation**: put it on the bed as it opens, no rotating, no supports. Every tool is named on both faces: the face you see in the slicer reads as printed, and the face you see in use (the lipped tools are turned over) reads after the flip. Bambu defaults (0.2 mm layers, 3 walls) are fine; PETG where the table says so, PLA for the rest. **Never scale anything in the slicer**: the tools' distances are the tool.

**Fastening rules every part obeys:** nothing is ever screwed into the top *face* of a desk top. Screws into the underside are #6 × 5/8 in flat head (13 mm in, well inside the 21 mm rule), and every screw-on part has its countersinks on the face that points at the floor. Parts on the desk surface hold by their own shape, by magnets on the steel, or, for the wall-gap trim, by #4 × 1/2 in screws driven sideways into the desk's raw back edge inside the gap, 14 mm below the surface, where nothing shows.

## Print list

| Part | Print | Filament |
| --- | --- | --- |
| tools: edge-t-square, alex-corner-template, rail-marking-gauge, pilot-drill-guide, rail-drill-jig | 1 each | any (PETG for the jig) |
| tools: leg-jig, feet-corner-jig, foot-height-gauge, wall-gauge | 1 each | any |
| tools: fitting-centring-plug | 2 | any |
| structure: foot-ring | 8 | PETG or ABS |
| structure: rail-end-cap-A | 2 | PETG or ABS |
| structure: rail-end-cap-B | 1 | PETG or ABS |
| cables: rail-cable-hook (plus two 10 × 3 mm magnets each) | 4 | PETG |
| cables: cable-clip | 6 | PETG |
| cables: power-bar-cradle | 2 per bar | PETG or ABS |
| cables: cable-tray | 3 | PETG or ABS |
| accessories: wall-gap-corner | 1 | walnut-ish or black |
| accessories: wall-gap-strip, 240 mm | 15 | same |
| accessories: wall-gap-strip-slot, 240 mm | 3 | same |
| accessories: wall-gap-strip-clamp, 240 mm | 2 | same |
| accessories: wall-gap-strip, short (set `seg`) | 2 × 80 (fillers), 1 × 50, 1 × 220 | same |
| accessories: wall-gap-connector | 26 (24 joints + 2 spare) | same |
| accessories: phone-stand | 1 | any |
| accessories: alex-foot (optional, one height: 20, 40 or 60) | 8 | PETG, 5 walls, 50% infill |
| accessories: alex-foot-pad (optional, with the feet) | 8 | TPU 95A |

Screws to buy for the printed parts: 46 × #6 × 5/8 in flat head (24 rings, 6 clips, 4 cradles, 12 trays) and 48 × #4 × 1/2 in flat head (wall-gap trim, two per piece). The optional ALEX feet take 24 more #6 × 5/8 in.

**Wall-gap cut list.** The gap runs 249 cm along the back wall and 314 cm along the side wall. The corner piece covers the first 20 cm of each wall. Then an 80 mm filler (20–28), then the clamp piece (28–52) whose enclosed notch wraps round the VIVO clamp's back at 36–44 (the clamp back is 80 mm long and projects 17.5 mm; the notch is 82 × 19.5 and still leaves a 9.5 mm bridge along the wall). Because the notch is centred 120 mm into the piece, butting the chain together puts it on desk 40.0, the clamp position, on both walls alike. If a wall is out and the notch misses the clamp, change the filler's `seg`, nothing else. Segments are 240 mm, butted end to end; set `seg` for the short pieces so nothing is cut by hand. **Every joint clicks:** each piece, the corner included, has a 20 × 12 mm pocket on its underside at every end, over the gap. Butt two pieces, then push a connector tile up into both pockets; its two pins press into the pin holes and the joint cannot step, bow or drift. Nothing shows on top. 11 joints on the back wall, 13 on the side wall, 24 tiles.

| Run | From | To | Pieces | Slotted segment |
| --- | --- | --- | --- | --- |
| back wall, filler then clamp 1 | 20 | 52 | 1 × 80 filler + 1 × clamp piece | |
| back wall, clamp 1 to the far end | 52 | 249 | 8 × 240 + 1 × 50 | the 3rd (100–124, behind the right speaker) and the 8th (220–244, behind the Y60) |
| side wall, filler then clamp 2 | 20 | 52 | 1 × 80 filler + 1 × clamp piece | |
| side wall, clamp 2 to the far end | 52 | 314 | 10 × 240 + 1 × 220 | the 3rd (100–124, behind the left speaker) |

Totals: 20 full-length pieces (15 plain, 3 slotted, 2 clamp), 4 short (two 80 mm fillers, 50, 220), 1 corner, 24 connector tiles. All the shared numbers (gap, lip, screw holes, pockets) live in `wall-gap-common.scad`; change them there and re-render every piece.

## tools/ · print these before you mark or drill anything

| Part | What it does | Settings |
| --- | --- | --- |
| `edge-t-square` | The head hooks over any edge (desk top, ALEX top, the steel); the blade lies square to it with punch holes at the four offsets this build uses: **50** ring centres on the ALEX, **85** feet on the top (with the plate's four screw holes round it), **100** legs L2–L6, **150** leg L1. Slide to the tape station, punch. The blade's edge squares the station lines across a rail. | as saved (lip up), 3 mm plate, 6 mm lip; turn over to use. `plate_hole_spacing` is 46.9, measured (59.5 mm plate, 5.4 mm holes). |
| `alex-corner-template` | Drops over any corner of an ALEX top, fences against both edges: ring centre at 50/50 plus the ring's three screw holes in one placement. Same template for all eight corners; the ring pattern is symmetric so which way the unit faces does not matter. Turned over against the two edges of the **bottom**, it marks the optional ALEX feet: same centre, and the inner three holes are their screws. | as saved (fences up), 2.5 mm plate, 6 mm fences; turn over to use. |
| `leg-jig` | Hooks over the wall edge like the T-square and marks an OLOV's centre and its five plate holes (105 mm plate, 5.5 mm holes on an 85 mm circle, 50 mm apart) in one punch set: the 100 pattern for L2–L6, the 150 pattern for L1 from the side-wall end. One hole points at the wall on every leg, so the plates all sit the same way. On the use face the 100 pattern has a solid plate circle and plain holes, the 150 pattern a dashed circle and ringed holes, so they cannot be mixed up. The five positions match the shared OLOV template (schablone.stp, printed and test-fitted on an OLOV) to 0.01 mm. | as saved (lip up), 3 mm plate; turn over to use. 215 × 110. |
| `feet-corner-jig` | Drops over a far corner of a top (face down), fences against both edges: a foot's centre 8.5 cm from each edge and its four plate holes, square to the edges, in one placement. F2, F4, F7, F8 need no measuring; F1, F3, F5, F6 (34.5 cm from the end) use the T-square's 85 hole. | as saved (fences up), 2.5 mm plate; turn over to use. |
| `wall-gauge` | An L with a 65 mm leg (ALEX back to wall) and a 30 mm leg (top's raw edge to wall). Hold it in the gap while you place a cabinet or slide the desk back; no tape. | flat, any filament. |
| `foot-height-gauge` | A C with a 102.0 mm inside height. Stand a foot on its pad, slide the gauge over it from the side, wind the pad until the gauge just slides on without rocking. All eight feet identical, no ruler. | flat, 100% infill. |
| `rail-marking-gauge` | Sits on a face of the angle with its lip over the edge. Pencil in the **19** notch along the flat leg's free edge gives the screw line; **29** along the vertical leg's heel edge gives the bolt line. The notches put a 0.8 mm pencil point on exactly 19.0 and 29.0. | as saved (lip up), 3 mm body 20 mm wide, 6 mm lip; turn over to use. |
| `rail-drill-jig` | Hooks over the flat leg's free edge like the gauge and puts a 1/8 in bore exactly on the 19 mm screw line. Slide to a station line (sight grooves on both sides), hold, drill the pilot through it: square, no wandering. Pull it off and open the hole to 7/32 in; the bit follows the pilot. All 19 rail holes. | as saved (lip up), 28 × 24 × 6 mm body; turn over to use. PETG. |
| `fitting-centring-plug` | Drops into a strut fitting's 9/16 in hole with a 1/8 in bore dead centre, so the pilot lands on the hole's centre instead of somewhere in 4.8 mm of slack. Clamp the fitting on its heel mark, plug, drill, move the plug, repeat; then open each pilot to 7/16 in with the fitting off. | head down, any filament. Print 2. |
| `pilot-drill-guide` | Depth stops, no tape, no measuring. SET tower: drop the bit tip-first into its blind hole (45 mm for the 1/8 in bit, 35 mm for the 5/64), rest the chuck nose on the tower, tighten; the bit now sticks out exactly that far. Then stand the puck you need flat on the surface and drill until the chuck nose lands on it: **12 PLATE** joining plates, **15 LEG** leg and feet plates, **10 EDGE** (5/64) the wall-gap trim's screws sideways into the raw back edge (hold the step's base against the edge, bit horizontal), **12 ALEX** (5/64) rings into the ALEX tops and ALEX feet into the bottoms, **25 RAIL** through the angle into the top. The five pucks are separate pieces, so nothing stands next to the one you are using and any chuck clears. Re-set the bit every time you change it. | all six pieces as saved, standing, 100% infill, a brim; never scale them. | If your chuck nose is domed, drill one test hole in scrap and measure. |

## structure/ · part of the desk

| Part | What it does | Where and how it attaches | Settings |
| --- | --- | --- | --- |
| `foot-ring` | Locating ring for the ALEX feet: 51 mm bore, 3 mm wall, 10 mm ring on a 75 × 2.5 mm flange, open bottom so the pad bears on the ALEX laminate. Stops the desk sliding on the cabinets. | ALEX tops, 5 cm in from each corner (the corner template marks them). Three #6 × 5/8 in flat heads into the ALEX top, 13 mm in. It only fits one way round over its three pilot holes. | flange down, PETG or ABS, 3 perimeters, 30% infill. `pad_d` is 50; measure your pad. |
| `rail-end-cap-A`, `-B` | Covers a cut end of a rail: 15 mm socket, 2 mm walls, open on the face that sits against the desk. The two ends of one rail are mirror images, so there are two hands. A: rail A's far end and rail B's far end. B: rail A's wall end. Rail B's corner end is bolted to rail A and takes no cap. | Slides on; friction, a dab of hot glue if loose. A cap that will not go on is the other hand. | closed end down, PETG or ABS. |

## cables/ · cable management

| Part | What it does | Where and how it attaches | Settings |
| --- | --- | --- | --- |
| `rail-cable-hook` | J hook for a bundle up to 24 mm. | Two 10 × 3 mm neodymium discs glued into the pockets; sticks to the front face of either rail's vertical leg, anywhere. Light runs only. | as saved, PETG. |
| `cable-clip` | Saddle for one cable (`bundle` = 8) or a small bundle (14); the cable pushes in past a lip. | One #6 × 5/8 in into the underside, wherever a cable runs. | as saved (profile face down), PETG. |
| `power-bar-cradle` | Two cradles hold a power bar: the open side is against the desk, the bar slides in from the end, a cable tie through the rim notches keeps it in. Set `bar_w` and `bar_h`. | Under top A over ALEX 1, between the feet plates and rail A: y 15–25, at x about 215 and 240. Two #6 × 5/8 in each into the underside. | as saved (U face down, 25 mm tall), PETG or ABS. |
| `cable-tray` | 200 mm trough, 80 wide, 50 deep, open side against the desk, drain slots in the floor. A 150 mm entry slot under the rim on the wall-side wall takes the leads from the outlets; two notches in the front wall let leads out to the devices; bricks slide in from the ends. Chain end to end, slot toward the wall. | Under top A between legs L2 and L3, y 18–30, x 72–132: three segments. Four #6 × 5/8 in per segment through the rim tabs into the underside. | as saved (standing on one end, 200 mm tall), PETG or ABS. |

## accessories/ · nice to have

| Part | What it does | Where and how it attaches | Settings |
| --- | --- | --- | --- |
| `wall-gap-corner` | One L piece for the back-left corner where the two wall gaps meet; 230 mm legs from the wall corner, ending at desk 20.0 cm on each edge, where the 80 mm fillers start. Connector pocket at the end of each leg. | Sits on the desk's two edges; the 20 mm lip drops into the gap against the desk's raw edge, the outer edges touch the walls. One #4 × 1/2 in flat head per leg through the lip into the edge, 14 mm below the surface. | as saved (top face down, lips up). |
| `wall-gap-strip` | 240 mm strip covering the gap: rests 12 mm on the desk, lip into the gap, reaches the wall. `gap` is 29 (design gap 30 minus 1). After the desk is in, measure the gap in several places and set `gap` to the **smallest** value minus 1. | Lip against the desk's edge, pushed to the wall; two #4 × 1/2 in per segment through the lip, 40 mm from each end, driven with the desk pulled 40 cm off the walls (manual step 8b: measure the gap at the wall first, print, pull out, fit and screw with the drill horizontal and the **10 EDGE** step, push back). Butt segments end to end and click a connector tile into the pockets. 3M VHB tape under the flat is the no-screw alternative. | as saved (top face down, lip up). |
| `wall-gap-strip-slot` | The same strip with a 60 × 18 mm rounded slot over the gap, for leads to drop straight down. | Same. Three places: see the cut list. | as saved. |
| `wall-gap-strip-clamp` | The strip from desk 28 to 52 cm with an enclosed notch in its middle (82 × 19.5 mm) that wraps round the VIVO clamp's back (80 mm long, 17.5 mm projection, measured) and leaves a 9.5 mm bridge along the wall. The notch centre is 120 mm into the piece, so the chain locates it on desk 40.0, the clamp position. | Two: one per wall; the side-wall one is the same part turned round. One screw each side of the notch. | as saved (top face down, lip up). |
| `wall-gap-connector` | 39 × 11.6 × 1.2 mm tile with two 2.4 mm pins, 20 mm apart. Bridges the pockets of two butted pieces; the pins press-fit so the joint stays flush and cannot pull apart. | Underneath every joint in the trim, over the gap; push up until the pins seat. A drop of CA glue makes it permanent. | pins up, 100% infill, same filament as the trim. |
| `alex-foot-20`, `-40`, `-60` | Optional. Solid round foot, 56 mm across, that lifts an ALEX, and with it the whole desk, by 2, 4 or 6 cm. The three screws go up through the column itself: each sits at the top of a 10 mm well bored from the floor end, bearing on 6 mm of solid core, so nothing can pry. Pocket for the TPU pad; the height is engraved on the side. Desk heights with each: surface 85.0 / 87.0 / 89.0, OLOV set to 82.2 / 84.2 / 86.2 (the table in `docs/build-manual.md` before step 5). | Unscrew the IKEA stock feet. Lay the unit on its back, hook the ALEX corner template over each bottom corner and punch the centre and the **inner** three holes. Pilot with the **12 ALEX** step. Three #6 × 5/8 in flat heads per foot, driven down the wells with a long screwdriver or a bit holder in the drill. Four per unit, all the same height. | as saved (ALEX face down, wells up), PETG, 5 walls, 50% infill. |
| `alex-foot-pad` | TPU pad for the foot: 52 mm disc, rounded edge, 40 × 2 mm plug. Grips the floor and scratches nothing. | Press the plug into the pocket in the foot's bottom; a drop of CA glue if it ever works loose. | as saved (plug up), TPU 95A, 100% infill, slow. |
| `phone-stand` | Phone leans back 25° against the plate, bottom edge in a groove behind a lip, cable tunnel from the groove out through the back. Cases up to 15 mm. | Anywhere on the top; nothing fixed. | flat on its base, any filament. |

## Not printed, on purpose

- The pads under the VIVO clamp jaws stay as the two spare 10 × 3 in steel mending plates; plastic creeps under the clamp load.
- The corner joint stays the bought 5 mm steel strut fittings.
- The HYTE Y60 pedestal is MakerWorld model 679012.
