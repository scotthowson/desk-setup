# Printed parts

Every part is an OpenSCAD source (`.scad`) with its rendered `.stl` and a `-preview.png` beside it. Change a number at the top of the source and re-render with `openscad -o name.stl name.scad`. Measurements in mm. Every screw-on part has its countersinks on the flat face that points at the floor, and every screw into the desk top is a #6 × 5/8 in flat head, 13 mm penetration, well inside the 21 mm rule.

**Printers:** everything fits the Bambu P1S and A1 (256 × 256 mm bed; the longest part is 200 mm). Every STL is saved in its print orientation, flat face on the bed, and none needs supports. The three lipped marking tools print lip-up and are turned over to use; their labels are on the bed face so they read correctly in use. Bambu defaults (0.2 mm layers, 3 walls) are fine; use PETG where the table says so, PLA is fine for the rest.

## tools/ · print these before you mark or drill anything

| Part | Print | What it does | Settings |
| --- | --- | --- | --- |
| `edge-t-square` | 1 | Head hooks over any edge (desk top, ALEX top, the steel); the blade lies square to it with punch holes at the four offsets this build uses: **50** ring centres on the ALEX, **85** feet on the top (with the plate's four screw holes round it), **100** legs L2–L6, **150** leg L1. Slide to the tape station, punch. The blade's edge squares the station lines across a rail. | as saved (lip up), turn over to use. `plate_hole_spacing` is 45; measure your feet plates. |
| `alex-corner-template` | 1 | Drops over any corner of an ALEX top, fences against both edges: ring centre at 50/50 plus the ring's three screw holes in one placement. Same template for all eight corners. | as saved (fences up), turn over to use. |
| `rail-marking-gauge` | 1 | Hooks over an edge of the angle. Pencil in the **19** notch along the flat leg's free edge gives the screw line; **29** along the heel edge gives the bolt line. | as saved (hook up), turn over to use. |
| `pilot-drill-guide` | 1 | 1/8 in and 5/64 in bores keep the bit square. Grooves at 12, 15, 20 mm and the top face at 25 mm set the tape flag: bit tip on the bench against the block, tape level with the groove. | standing on its base, 100% infill. |

## structure/ · part of the desk

| Part | Print | What it does | Settings |
| --- | --- | --- | --- |
| `foot-ring` | 8 | Locating ring for the ALEX feet: 51 mm bore, 3 mm wall, 10 mm ring on a 75 mm flange with three countersunk #6 holes, open bottom so the pad bears on the ALEX laminate. Stops the desk sliding on the cabinets. | flange down, PETG or ABS, 3 perimeters, 30% infill. `pad_d` is 50; measure your pad. |
| `rail-end-cap` | 4 | Slips over each cut end of the rails. 15 mm socket, 2 mm walls. | closed end down, PETG or ABS. Hot glue if loose. |

## cables/ · cable management

| Part | Print | What it does | Settings |
| --- | --- | --- | --- |
| `rail-cable-hook` | 4–6 | Snaps over the vertical leg of either rail, J underneath holds a bundle up to 24 mm. No holes; slide it anywhere; turn the J away from your knees. | on its side as rendered, PETG. |
| `cable-clip` | as needed | Screw-on saddle for one cable (set `bundle` = 8) or a small bundle (14), one #6 screw into the underside. | on its side as rendered, PETG. |
| `power-bar-cradle` | 2 per bar | Two cradles under the top near the Y60; the bar drops in, a cable tie through the slots holds it. Two #6 screws each. Set `bar_w` and `bar_h` to your bar. | open side up, PETG or ABS. |
| `cable-tray` | by the segment | 200 mm under-desk trough, 80 wide, 50 deep, screw tabs along both sides, drain slots. Chain segments end to end behind the rail for bricks and slack. | open side up, PETG or ABS. |

## accessories/ · nice to have

| Part | Print | What it does | Settings |
| --- | --- | --- | --- |
| `wall-gap-strip` | by the segment | 200 mm strip covering the 3 cm wall gap so nothing falls in: rests 8 mm on the desk, a lip drops into the gap, reaches the wall. About 12 per wall edge; leave the VIVO clamp zones open. | flat, a colour near the walnut or black. |
| `phone-stand` | 1 | Phone leans back 25° against the plate, bottom edge in a groove behind a lip, cable notch through the base. Cases up to 15 mm. | flat on its base, any filament. |

## Not printed, on purpose

- The pads under the VIVO clamp jaws stay as the two spare 10 × 3 in steel mending plates; plastic creeps under the clamp load.
- The corner joint stays the bought 5 mm steel strut fittings.
- The HYTE Y60 pedestal is MakerWorld model 679012.
