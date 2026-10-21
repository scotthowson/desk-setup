# Printed parts

Every part is an OpenSCAD source (`.scad`) with its rendered `.stl` and a `-preview.png` beside it. Change a number at the top of the source and re-render with `openscad -o name.stl name.scad`. Measurements in mm.

**Printers:** everything fits the Bambu P1S and A1 (256 × 256 mm bed; the longest part is 240 mm). Every STL is saved in its print orientation, flat face on the bed, and none needs supports. The three lipped marking tools print lip-up and are turned over to use; their labels are on the bed face so they read correctly in use. Bambu defaults (0.2 mm layers, 3 walls) are fine; PETG where the table says so, PLA for the rest. Do not scale anything in the slicer: the tools' distances are the tool.

**Fastening rules that every part obeys:** nothing is ever screwed into the top *face* of a desk top. Screws into the underside are #6 × 5/8 in flat head, 13 mm in, well inside the 21 mm rule, and every screw-on part has its countersinks on the flat face that points at the floor. Parts on the desk surface sit by their own shape (lips, fences, gravity), by magnets on the steel, or, for the wall-gap trim, by small screws driven sideways into the desk's raw back edge inside the gap, where nothing shows.

## Print list

| Part | Print | Filament |
| --- | --- | --- |
| tools: edge-t-square, alex-corner-template, rail-marking-gauge, pilot-drill-guide | 1 each | any |
| structure: foot-ring | 8 | PETG or ABS |
| structure: rail-end-cap | 4 | PETG or ABS |
| cables: rail-cable-hook (plus 2 magnets each) | 4 | PETG |
| cables: cable-clip | 6 | PETG |
| cables: power-bar-cradle | 2 per bar | PETG or ABS |
| cables: cable-tray | 3 | PETG or ABS |
| accessories: wall-gap-corner | 1 | walnut-ish or black |
| accessories: wall-gap-strip, 240 mm | 19 full, 3 short (see the cut list); 2 × #4 × 1/2 in screws each | same |
| accessories: wall-gap-strip-slot | 4 (counted inside the 19) | same |
| accessories: phone-stand | 1 | any |

**Wall-gap cut list.** The gap runs 249 cm along the back wall and 314 cm along the side wall, minus the corner piece's two 120 mm legs and the two VIVO clamp zones (x 36–44 on the back wall, y 36–44 on the side). Set `seg` in the source for the short pieces so nothing is cut by hand:

| Run | From | To | Pieces |
| --- | --- | --- | --- |
| back wall, corner to clamp 1 | 12 | 36 | 1 × 240 |
| back wall, clamp 1 to the far end | 44 | 249 | 8 × 240 + 1 × 130 (put a slotted one behind the Y60, around x 200–224) |
| side wall, corner to clamp 2 | 12 | 36 | 1 × 240 |
| side wall, clamp 2 to the far end | 44 | 314 | 11 × 240 + 1 × 60 (a slotted one behind the left speaker, around y 96–120) |

Where a cable needs to go down, swap a plain segment for a slotted one; the slot is centred, so it lands in the middle of that 240 mm.

## tools/ · print these before you mark or drill anything

| Part | What it does | Settings |
| --- | --- | --- |
| `edge-t-square` | Head hooks over any edge (desk top, ALEX top, the steel); the blade lies square to it with punch holes at the four offsets this build uses: **50** ring centres on the ALEX, **85** feet on the top (with the plate's four screw holes round it), **100** legs L2–L6, **150** leg L1. Slide to the tape station, punch. The blade's edge squares the station lines across a rail. | as saved (lip up), 3 mm plate, 6 mm lip; turn over to use. `plate_hole_spacing` is 45; measure your feet plates. |
| `alex-corner-template` | Drops over any corner of an ALEX top, fences against both edges: ring centre at 50/50 plus the ring's three screw holes in one placement. Same template for all eight corners. | as saved (fences up), 2.5 mm plate, 6 mm fences; turn over to use. |
| `rail-marking-gauge` | Hooks over an edge of the angle. Pencil in the **19** notch along the flat leg's free edge gives the screw line; **29** along the heel edge gives the bolt line. | as saved (hook up), 5 mm body, 4 mm hook; turn over to use. |
| `pilot-drill-guide` | Two jobs. The bores keep the bit square: hold the block flat and drill through it (1/8 in for the tops, 5/64 in for the ALEX). The grooves set the tape flag: bit tip on the bench against the block, wrap the tape level with the 12, 15 or 20 groove, or the 25 top face. | standing on its base, 100% infill. 30 × 16 × 25; it must stay 25 tall. |

## structure/ · part of the desk

| Part | What it does | Where and how it attaches | Settings |
| --- | --- | --- | --- |
| `foot-ring` | Locating ring for the ALEX feet: 51 mm bore, 3 mm wall, 10 mm ring on a 75 mm flange, open bottom so the pad bears on the ALEX laminate. Stops the desk sliding on the cabinets. | ALEX tops, 5 cm in from each corner (the corner template marks them). Three #6 × 5/8 in flat heads into the ALEX top. | flange down, PETG or ABS, 3 perimeters, 30% infill. `pad_d` is 50; measure your pad. |
| `rail-end-cap` | Covers each cut end of the rails. 15 mm socket, 2 mm walls, open on the face that sits against the desk. | Slides onto the four rail ends; friction, a dab of hot glue if loose. | closed end down, PETG or ABS. |

## cables/ · cable management

| Part | What it does | Where and how it attaches | Settings |
| --- | --- | --- | --- |
| `rail-cable-hook` | J hook for a bundle up to 24 mm. | Two 10 × 3 mm neodymium discs glued into the pockets; sticks to the front face of either rail's vertical leg, anywhere. Light runs only. | on its side as rendered, PETG. |
| `cable-clip` | Saddle for one cable (`bundle` = 8) or a small bundle (14). | One #6 × 5/8 in into the underside, wherever a cable runs. | on its side as rendered, PETG. |
| `power-bar-cradle` | Two cradles hold a power bar; a cable tie through the slots keeps it in. Set `bar_w` and `bar_h`. | Under top A over ALEX 1, between the feet and rail A: y 15–25, at x about 215 and 240, 25 cm apart. Two #6 × 5/8 in each into the underside. | open side up, PETG or ABS. |
| `cable-tray` | 240 mm trough, 80 wide, 50 deep, screw tabs both sides, drain slots. Chain end to end for bricks and slack. | Under top A between legs L2 and L3, y 18–30, x 72–132: three segments. Four #6 × 5/8 in per segment into the underside. | open side up, PETG or ABS. |

## accessories/ · nice to have

| Part | What it does | Where and how it attaches | Settings |
| --- | --- | --- | --- |
| `wall-gap-corner` | One L piece for the back-left corner where the two wall gaps meet; 120 mm legs. | Sits on the desk's two edges at the corner; the 16 mm lip drops into the gap against the desk's edge, the outer edges touch the walls. One #4 × 1/2 in flat-head screw per leg through the lip into the desk's back edge, hidden in the gap (stubby or right-angle driver). | flat, top face up. |
| `wall-gap-strip` | 240 mm strip covering the 3 cm wall gap: rests 12 mm on the desk, lip into the gap, reaches the wall. `gap` is 31 (design gap 30 plus 1); measure your gap after the desk is in and set it to the largest value. | Lip against the desk edge, pushed to the wall; two #4 × 1/2 in flat heads per segment through the lip into the desk's back edge, 40 mm from each end. Butt the segments end to end. 3M VHB tape under the flat is the no-screw alternative. | flat, top face up. |
| `wall-gap-strip-slot` | The same strip with a 60 × 18 mm rounded slot over the gap, for leads to drop straight down. | Same. One behind the VIVO clamps for the monitor leads, one behind the Y60, one behind each speaker. | flat, top face up. |
| `phone-stand` | Phone leans back 25° against the plate, bottom edge in a groove behind a lip, cable notch through the base. Cases up to 15 mm. | Anywhere on the top; nothing fixed. | flat on its base, any filament. |

## Not printed, on purpose

- The pads under the VIVO clamp jaws stay as the two spare 10 × 3 in steel mending plates; plastic creeps under the clamp load.
- The corner joint stays the bought 5 mm steel strut fittings.
- The HYTE Y60 pedestal is MakerWorld model 679012.
