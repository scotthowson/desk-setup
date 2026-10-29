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

Keys sit at cell corners (40, 120, 200 mm along each edge), where the pattern leaves 2 mm of solid on each side.

The keys also keep the pattern true across the joint. The pockets are cut in the same print as the slots, on the same 40 mm grid, so a seated key holds the two tiles within 0.1 mm of each other along the joint, and butting the edges fixes them across it. The neighbour's first slot then lands exactly 40 mm from this tile's last, row after row, however many tiles you add. The key is 13 × 11 mm with a 5 mm waist, 3.4 mm thick. A 0.1 mm slop is built in; if a key is tight, a tap with a mallet seats it; if loose, a drop of CA glue.

## The desk mount (MakerWorld 2780289, measured from its 3MF)

The board rests on the foot frame's ledge, 12 mm above the desk, with the frame's 40 × 12 mm upright behind it and its 60 × 4 mm foot plate on the desk. The frame screw's 4.8 × 14 mm shank goes through any slot of the bottom row into the frame's window, nut behind. So the slots need no change, and bottom tiles get a 12 mm **skirt** with a straight bottom edge that sits flush in the clamps and reaches the desk. No notches by default; if a frame's foot plate ever needs clearance, `notches = [x, x, ...]` (mm from the tile's left edge) cuts a 40 wide notch for the upright and a 60 × 4 one for the plate. `lift = 0` removes the skirt.

## Pieces

| File | Where | Outside edges |
| --- | --- | --- |
| `skadis-TL-x1.stl` `skadis-T-x1.stl` `skadis-TR-x1.stl` | top row | top (+ left / right) |
| `skadis-L-x1.stl` `skadis-C-x1.stl` `skadis-R-x1.stl` | middle rows | left / none / right |
| `skadis-BL-x1.stl` `skadis-B-x1.stl` `skadis-BR-x1.stl` | bottom row, with the skirt, straight bottom edge | bottom (+ left / right) |
| `skadis-L1-x1.stl` `skadis-M1-x1.stl` `skadis-R1-x1.stl` | single-row board, with the skirt | top and bottom (+ left / right) |
| `skadis-key-x24.stl` | every joint, 3 each | |
| `skadis-cross-x4.stl` | every inside corner where four tiles meet, on the back, glued | |

Outside edges are chamfered 1.5 mm on the front and have no pockets. Joint edges have the pockets. A tile is 331 g (346 g with the skirt), a key 0.7 g.

Boards and what to print:

| Board | Tiles | Keys |
| --- | --- | --- |
| 2 wide × 1 tall (48 × 25 cm) | L1, R1 | 3 |
| 3 wide × 1 tall (72 × 25 cm) | L1, M1, R1 | 6 |
| 2 × 2 (48 × 49 cm) | TL, TR, BL, BR | 12 |
| 3 × 2 (72 × 49 cm) | TL, T, TR, BL, B, BR | 21 |
| 3 × 3 (72 × 73 cm) | TL, T, TR, L, C, R, BL, B, BR | 36 |

Two frames hold a 2-wide board, three a 3-wide one, one under each bottom tile.

## Print

Tiles: **front face down, as saved**, 0.2 mm layers, 3 to 4 walls, 3 top and bottom layers, 15 to 20 % gyroid, PETG; the textured plate becomes the front. No supports. Keys: flat as saved, same profile (a 13 × 10 × 3.4 key is nearly all walls anyway), print the whole `-x24` plate; spares weigh nothing.

    openscad -D 'pos="BL"' -o skadis-BL-x1.stl skadis-tile.scad      # TL T TR L C R BL B BR L1 M1 R1
    openscad -o skadis-key-x24.stl skadis-key.scad

Assembly: lay the tiles face down on a flat surface, butted, pattern lined up by eye (the pockets line up when the slots do), push a key into each pocket pair until it clicks, turn the board over. Stand it on the frames, frame screw through a bottom-row slot, nut behind.

First print: one BL tile and three keys. Hang an IKEA hook on it, click a key in and out, set it in a clamp. Then print the rest. A 2 × 2 board takes about 1.35 kg.

## The corner cross (back brace where four tiles meet)

`skadis-cross-x4.stl` (source `skadis-bracket.scad`): a 73 × 42 × 2 mm plate with four pegs, one into a slot of each of the four tiles that meet at an inside corner. It goes on the back and is glued in. The keys hold the tiles together. The cross stops the corner from hinging and makes the board one stiff panel.

- **Pegs** are 4.8 × 14.8 mm, 0.1 mm smaller all round than the slot so CA glue has room. They are 5 mm tall, the board's thickness, so they finish flush with the front and the corner reads as solid board.
- **Where they go**, relative to the corner: 10 left and 10 down, 10 right and 10 up, 30 right and 10 down, 30 left and 10 up. These are the four slots nearest the corner, one per tile. The cross fits either way round. It cannot go in sideways because the slots only take it upright.
- **What it costs**: its own four slots. The plate stays 1.5 mm clear of every other slot, so the rest of the corner still takes hooks.
- **How many**: one per inside corner. A 2 × 2 board needs 1, a 3 × 2 needs 2, and a 3 × 3 needs 4. The file is named for a 3 × 3.

Fitting:

1. Assemble the board face down with all keys in.
2. Dry-fit the cross over the corner and check the pegs are flush on the front.
3. If a peg stands proud, set `proud = -0.1` and reprint.
4. Lift the cross out, put a thin line of CA glue (or a dot on each peg) on the plate, and press it home.
5. Hold it for 30 s and leave the board flat for an hour.

Print the cross plate down, pegs up, as saved, in PETG. Use 100 % infill, because it is 3 g and should be solid. No supports.

    openscad -D 'type="cross"' -o skadis-cross-x4.stl skadis-bracket.scad

The same source also draws two-peg bridges (`bridge-h` across an upright joint, `bridge-v` across a level one), for a single-row board that has no inside corner.

## Should you use a generator online instead?

Not for the board. The pattern is four numbers that every generator shares; what the generators do not give you is the seamless joint, the lock, the finished edges and the skirt for the mount. For accessories (bins, hooks, holders) use the published ones: `makerworld.com/en/models/799571` (parametric bins and shelves), the Printables "Parametric Skadis Board" family, and openGrid's SKÅDIS adapter if you want openGrid parts on it.

## openGrid, bigger tiles

The biggest openGrid Lite tile a 256 mm bed takes is 9 × 9 cells (252 × 252 mm). `components/underware/` carries `tile-9x9-lite.stl` and `tile-8x9-lite.stl` for a wall or a cabinet side; the Underware plan under the desk stays on 8 × 4 tiles.
