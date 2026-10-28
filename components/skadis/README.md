# SKÅDIS-compatible pegboard tiles for the desk (optional, our own)

Printed pegboard tiles that take IKEA's SKÅDIS hooks, clips and containers, assemble into one board of any size with finished outer edges, lock together at every joint, and stand on the desk in the MakerWorld clamp mount (model 2780289). Not in the assembly manual. File names carry the print count (`-x1`: one per board of that shape; `-x24`: keys).

## Geometry

IKEA does not publish the hole pattern; these are the community measurements every compatible design uses. Check one IKEA hook on the first tile before printing the rest.

| | mm |
| --- | --- |
| Board thickness | 5 |
| Slot | 5 wide × 15 tall, vertical, rounded ends |
| Pitch along a row | 40 |
| Rows | 20 apart, every other row shifted 20 (a 40 × 40 grid plus one at its centres) |
| Tile | 6 × 6 cells = 240 × 240 (252 tall with the skirt); a P1S or A1 bed is 256 |

The pattern sits 10 mm in from every tile edge, so across a joint the neighbour's first slot is exactly 40 mm from this tile's last, in both directions: one board, no seam in the pattern.

## The lock (so nothing falls out, front or back)

Three bow-tie keys per joint, in pockets cut from the **back** of both tiles, 3.5 mm deep, leaving a 1.5 mm skin on the front.

- The dovetail stops the tiles pulling apart.
- The pocket floor holds the two faces flush, so a hook never catches a step.
- The front skin means nothing shows and nothing can come out the front.
- A 0.3 mm lip round the back of each pocket snaps over the key: push it in with a thumb until it clicks, and it cannot fall out the back.

Keys sit at cell corners (40, 120, 200 mm along each edge), where the pattern leaves 2.5 mm of solid on each side. A 0.1 mm slop is built in; if a key is tight, a tap with a mallet seats it; if loose, a drop of CA glue.

## The desk mount (MakerWorld 2780289, measured from its 3MF)

The board rests on the foot frame's ledge, 12 mm above the desk, with the frame's 40 × 12 mm upright behind it and its 60 × 4 mm foot plate on the desk. The frame screw's 4.8 × 14 mm shank goes through any slot of the bottom row into the frame's window, nut behind. So the slots need no change, and bottom tiles get a 12 mm **skirt** that reaches the desk, notched 40 wide for the upright and 60 × 4 for the foot plate. One notch per bottom tile, centred, by default; move or add notches with `notches = [x, x, ...]` (mm from the tile's left edge) and set `clamp_w`, `base_w`, `base_h`, `lift` if your measurements differ. `lift = 0` removes the skirt.

## Pieces

| File | Where | Outside edges |
| --- | --- | --- |
| `skadis-TL-x1.stl` `skadis-T-x1.stl` `skadis-TR-x1.stl` | top row | top (+ left / right) |
| `skadis-L-x1.stl` `skadis-C-x1.stl` `skadis-R-x1.stl` | middle rows | left / none / right |
| `skadis-BL-x1.stl` `skadis-B-x1.stl` `skadis-BR-x1.stl` | bottom row, with the skirt | bottom (+ left / right) |
| `skadis-L1-x1.stl` `skadis-M1-x1.stl` `skadis-R1-x1.stl` | single-row board, with the skirt | top and bottom (+ left / right) |
| `skadis-key-x24.stl` | every joint, 3 each | |

Outside edges are chamfered 1.5 mm on the front and have no pockets. Joint edges have the pockets. A tile is 331 g (346 g with the skirt), a key 0.6 g.

Boards and what to print:

| Board | Tiles | Keys |
| --- | --- | --- |
| 2 wide × 1 tall (48 × 25 cm) | L1, R1 | 3 |
| 3 wide × 1 tall (72 × 25 cm) | L1, M1, R1 | 6 |
| 2 × 2 (48 × 49 cm) | TL, TR, BL, BR | 12 |
| 3 × 2 (72 × 49 cm) | TL, T, TR, BL, B, BR | 21 |
| 3 × 3 (72 × 73 cm) | TL, T, TR, L, C, R, BL, B, BR | 36 |

Two frames hold a 2-wide board, three a 3-wide one, one under each bottom tile's notch.

## Print

Tiles: **front face down, as saved**, 0.2 mm layers, 4 walls, PETG; the textured plate becomes the front. No supports. Keys: flat as saved, 100 % infill, print the whole `-x24` plate; spares weigh nothing.

    openscad -D 'pos="BL"' -o skadis-BL-x1.stl skadis-tile.scad      # TL T TR L C R BL B BR L1 M1 R1
    openscad -o skadis-key-x24.stl skadis-key.scad

Assembly: lay the tiles face down on a flat surface, butted, pattern lined up by eye (the pockets line up when the slots do), push a key into each pocket pair until it clicks, turn the board over. Stand it on the frames, frame screw through a bottom-row slot, nut behind.

First print: one BL tile and three keys. Hang an IKEA hook on it, click a key in and out, set a frame under the notch. Then print the rest.

## Should you use a generator online instead?

Not for the board. The pattern is four numbers that every generator shares; what the generators do not give you is the seamless joint, the lock, the finished edges and the skirt for the mount. For accessories (bins, hooks, holders) use the published ones: `makerworld.com/en/models/799571` (parametric bins and shelves), the Printables "Parametric Skadis Board" family, and openGrid's SKÅDIS adapter if you want openGrid parts on it.

## openGrid, bigger tiles

The biggest openGrid Lite tile a 256 mm bed takes is 9 × 9 cells (252 × 252 mm). `components/underware/` carries `tile-9x9-lite.stl` and `tile-8x9-lite.stl` for a wall or a cabinet side; the Underware plan under the desk stays on 8 × 4 tiles.
