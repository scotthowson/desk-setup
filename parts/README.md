# Printed parts

Every part is an OpenSCAD source (`.scad`) with its rendered `.stl` next to it. Change a number in the source and re-render with `openscad -o name.stl name.scad`. Measurements in mm. Previews are the `-preview.png` files.

## Needed

| Part | Print | What it does | Settings |
| --- | --- | --- | --- |
| `foot-ring` | 8 | Locating ring for the ALEX feet. The 5 cm pad of each adjustable foot drops into the 51 mm bore and bears on the ALEX laminate through the open bottom; the 75 mm flange takes three #6 × 5/8 in flat-head screws into the ALEX top. Stops the desk sliding on the cabinets. | flange down, PETG or ABS, 3 perimeters, 30% infill, no supports. Measure your pad first; `pad_d` in the source is 50. |
| `rail-marking-gauge` | 1 | Hooks over an edge of the steel angle. Pencil notch at 19 mm for the screw line (hook over the flat leg's free edge) and at 29 mm for the bolt line (hook over the heel edge). Slide it along with a pencil in the notch. | flat, hook up, any filament, no supports. |
| `pilot-drill-guide` | 1 | Block with a 1/8 in bore (every pilot into the tops) and a 5/64 in bore (ring screws into the ALEX). Keeps the bit square. Grooves at 12, 15 and 20 mm from the base and the top face at 25 mm are the tape-flag gauge: stand the bit tip on the bench against the block and wrap the tape level with the groove you need. | standing on its base, any filament, 100% infill. |

## Optional

| Part | Print | What it does | Settings |
| --- | --- | --- | --- |
| `rail-end-cap` | 4 | Slips over each cut end of the two rails so nothing sharp faces the wall gap or the cabinets. 15 mm deep socket, 2 mm walls. | closed end down, PETG or ABS, no supports. A dab of hot glue if loose. |
| `rail-cable-hook` | 4 to 6 | Snaps over the vertical leg of either rail; a J below it holds a cable bundle up to 24 mm. No holes, no screws, slide it anywhere. Turn it so the J hangs on the side away from your knees. | on its side as rendered, PETG (the clip needs some spring), 3 perimeters. |
| `wall-gap-strip` | by the metre | 200 mm segment that covers the 3 cm gap between a top's wall edge and the wall so pens and cables stop falling in. Rests 8 mm on the desk, a lip drops into the gap against the desk's edge, the far edge touches the wall. Leave the two VIVO clamp zones uncovered (x 31–39 on the back edge, y 31–39 on the left end). About 12 segments per wall edge. | flat, top face up, a colour near the walnut or black. |

## Not printed, on purpose

- The pads under the VIVO clamp jaws stay as the two spare 10 × 3 in steel mending plates. A printed pad would creep under the clamp load over months.
- The corner joint uses bought 5 mm steel strut fittings; a printed bracket would not hold rail B's end.
- The HYTE Y60 pedestal is MakerWorld model 679012.
