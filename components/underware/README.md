# Underware on openGrid under the desk (optional)

Our own addition, not in the assembly manual. One continuous cable channel that runs from the PC end of top A, round the inside corner, and down top B, snapped into openGrid tiles screwed to the undersides. File names carry the print count: `-x11` means print eleven. The 3D model shows the plan: tick **Underware** and **See-through tops** under Show in `index.html`, then **Under the corner** or **Plan**.

## Sources (third party, included for reproducibility)

| File | What | Author, licence |
| --- | --- | --- |
| `openGrid.scad` | openGrid tile generator (Full / Lite, screw holes, chamfers), the same generator as makerworld.com/en/models/1304337 | design David D, OpenSCAD by BlackjackDuck, CC-BY-NC-SA 4.0; derived tiles CC-BY. From github.com/suddhu/open-grid-studio |
| `monokini_I/L/S/T/X_channel.scad` | Underware for openGrid, one-piece channels with grip snaps (makerworld.com/en/models/1175037) | Hands on Katie and BlackjackDuck, CC-BY-NC-SA 4.0. From github.com/openGrid-3D/openGrid-openSCAD, `beta/monokini` |

Both need the BOSL2 library in OpenSCAD's library path (`git clone https://github.com/BelfrySCAD/BOSL2 ~/.local/share/OpenSCAD/libraries/BOSL2`). Nothing in `parts/` needs a library.

## Print list

| File | Print | Grams each (PETG) | Print |
| --- | --- | --- | --- |
| `tile-8x4-lite-x11.stl` (224 × 112 × 4 mm, corner screw holes for #6) | 11 | 27 | flat, as saved, 0.2 mm layers |
| `tile-2x9-lite-x2.stl` (56 × 252 × 4 mm) | 2 | 15 | flat, as saved |
| `channel-I-8-x11.stl` (224 mm straight) | 11 | 33 | as saved, open side up, no supports |
| `channel-I-4-x1.stl` (112 mm) | 1 | 17 | same |
| `channel-I-3-x2.stl` (84 mm) | 2 | 13 | same |
| `channel-T-x2.stl` (3 × 2 cells, branch) | 2 | 16 | same |
| `channel-L-x1.stl` (2 × 2 cells, corner) | 1 | 11 | same |

Total about 0.85 kg. Also here, not in the plan: `tile-8x9-lite.stl` (224 × 252, the deepest tile behind rail A, 60 g) and `tile-9x9-lite.stl` (252 × 252, the biggest a 256 mm bed takes, 68 g) for a wall, a cabinet side or anywhere you want more openGrid; print as many as you need. Black PETG for the tiles. Channels black too, or one accent colour if you want the run to show.

Re-render with the parameters the STLs were made with:

    openscad -D 'Full_or_Lite="Lite"' -D Board_Width=8 -D Board_Height=4 -D 'Screw_Mounting="Corners"' -D Screw_Diameter=3.8 -D Screw_Head_Diameter=7.0 -o tile-8x4-lite-x11.stl openGrid.scad
    openscad -D 'Full_or_Lite="Lite"' -D Board_Width=2 -D Board_Height=9 -D 'Screw_Mounting="Corners"' -D Screw_Diameter=3.8 -D Screw_Head_Diameter=7.0 -o tile-2x9-lite-x2.stl openGrid.scad
    openscad -D Channel_Length_Units=8 -o channel-I-8-x11.stl monokini_I_channel.scad     # 4 and 3 the same way
    openscad -o channel-T-x2.stl monokini_T_channel.scad
    openscad -o channel-L-x1.stl monokini_L_channel.scad

The screw hole is 3.8 mm with a 7.0 mm countersink, for the #6 × 5/8 in flat heads (H06) the rings use.

## The plan

Desk cm: x along the back wall from top A's corner, y along the side wall. One grid for everything: cells are 28 mm, counted from the origin (16.0, 16.0), so cell k starts at 16 + 2.8 k. Channels are one cell wide and 22 mm tall; "row 2" is y 18.8 to 21.6, "column 4" is x 24.4 to 27.2.

Tiles (13), all 4 mm Lite:

| Tiles | Where (cm) | Clear of |
| --- | --- | --- |
| 8 × (8×4) in a row behind rail A | x 27.2 to 206.4, y 16.0 to 27.2 | L2 and L3 plates (end at y 15.25), rail A's flat leg (y 47.9), ALEX 1 (x 209.5), clamp plate 1 (y to 8.1) |
| 1 × (2×9), corner column | x 21.6 to 27.2, y 21.6 to 46.8 | L1 plate (ends at x 20.25), clamp plate 2 (ends at x 8.1), rail A's flat leg (y 47.9) |
| 1 × (2×9), under the hop | x 21.6 to 27.2, y 55.2 to 80.4 | joining plate P1 (ends at x 18.8), P2 (starts at x 31.2), rail A's vertical leg (y 53) |
| 3 × (8×4) in a column behind rail B | x 16.0 to 27.2, y 80.4 to 147.6 | L4 to L6 plates (end at x 15.25), rail B's flat leg (x 47.9) |

The run, from the PC end:

1. Row 2 behind rail A from x 206.4 (open end at ALEX 1, where the power bar is) back to x 30.0: I-8, I-8, I-8, I-8, then the **T** at x 108.4 to 116.8 with its stem toward the wall, under the wall-gap slot at x 100 to 124 (the G5, the right Acer and the right speaker drop here), then I-8, I-8, I-8, I-4.
2. **L** at the corner, x 24.4 to 30.0, y 18.8 to 24.4: row 2 turns into column 4.
3. Column 4 down to rail A: I-8, y 24.4 to 46.8, open end facing the rail.
4. **The hop**: rail A's vertical leg hangs 5 cm below the top at y 53, between the two channel ends (y 46.8 and 55.2). The bundle dips under the leg and comes back up, 8.4 cm of free cable. One rail cable hook on the leg if it ever sags. This is the only place a cable leaves a channel.
5. Column 4 behind rail B from y 55.2: I-8, I-8, I-3, then the **T** at y 108.4 to 116.8 with its stem toward the wall under the slot at y 100 to 124 (the left Acer and the left speaker), then I-8, I-3, open end at y 147.6.

Power bar: on ALEX 1's top panel between the rings, in the 10 cm cavity under the top, fed straight down the Y60 slot at x 220 to 244. The Y60 is right above it. Nothing powered lives at the ALEX 2 end.

Why it is laid out this way: every lead on the desk goes down through one of the three wall-gap slots, hangs 16 cm to the channel, and rides the channel to the ALEX 1 end. The corner is the only obstacle course (clamps, L1, joining plates, the rails' ends) and the column at x 24.4 to 27.2 is the one lane that threads it: 1.35 cm from L1's plate, between the joining plates, 20 mm short of each rail's flat leg.

## Fixing the tiles (same rules as every part under the tops)

- Screws: #6 × 5/8 in flat head (H06), four per tile, 52 in all. Through a 4 mm tile the screw reaches 12 mm into the top, inside the 21 mm limit.
- When: after the rails are screwed on and before the tops are stood up, tops still face down (between chapters F and G of the manual).
- Mark the tile rectangles on the undersides with the tape, then lay the tiles on the lines and check the air to every plate circle with a ruler: 7.5 mm to L2 and L3, 13.5 mm to L1, 7.5 mm to L4 to L6, 28 mm to P1 and 40 mm to P2.
- Pilot: the tile is the template, like a ring. Hold it on its outline, scribe through its four corner holes, lift it, pilot 5/64 in with the **12 ALEX** puck standing on the wood, put the tile back, drive the screws. Never drill through the tile with the puck on it: the hole would end 4 mm short.
- Tiles butt end to end on the grid; the channels bridge the joints, so no connectors are needed. Snap the channels in after the desk is standing, from below.

## What it replaces in `parts/cables/`

The cable clips, the power-bar cradles and the cable tray. Keep the rail cable hooks (magnets on the steel) for the drop from the desk surface to rail A and for the hop.
