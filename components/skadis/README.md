# SKÅDIS-compatible pegboard tiles (optional, our own)

Printed pegboard that takes IKEA's SKÅDIS hooks, clips and containers, in tiles that join edge to edge and keep IKEA's hole pitch across every joint. Not in the assembly manual. File names carry the print count (`-x4`: print four).

## Geometry

IKEA does not publish the hole pattern; these are the community measurements every compatible design uses (pegboardly's SKÅDIS reference, the Printables parametric board, the OpenSCAD tower on GitHub), so check one IKEA hook on the first tile before printing a wall:

| | mm |
| --- | --- |
| Board thickness | 5 |
| Slot | 5 wide × 15 tall, vertical, rounded ends |
| Pitch along a row | 40 |
| Row spacing | 20, every other row shifted 20 (a 40 × 40 grid plus a second one at its centres) |
| Stand-off from the wall | 20, on spacers, so the hooks can pass behind (IKEA's own spacers or any 20 mm tube) |

## The tile

`skadis-board.scad`, plain OpenSCAD, no library. `cols × rows` cells of 40 mm; 6 × 6 = 240 × 240 mm fills a P1S or A1 bed. The pattern sits 10 mm in from every edge, which is the widest solid band the pattern allows, and the next tile's first slot is exactly 40 mm from this one's last, so a wall of tiles reads as one board.

Joints: dovetail tabs on the right and top edges, sockets on the left and bottom. Lay the next tile over the tabs, face on; the joint cannot pull apart in the plane. Every tile is identical, so there is no handed piece; outer tiles keep their tabs behind the board, or render with `tabs = false`.

Screws: countersunk for #8 or M4 at every second cell corner (an 80 mm grid, always in solid), through 20 mm spacers into the wall or a batten. Four per 6 × 6 tile.

## Print

| File | Print | Grams (PETG) | Print |
| --- | --- | --- | --- |
| `skadis-6x6-x4.stl` (240 × 240 × 5, 36 + 36 slots) | 4 for a 48 × 48 cm board; add tiles for any size | about 190 | flat, as saved, 0.2 mm layers, 4 walls, PETG |

    openscad -D cols=6 -D rows=6 -o skadis-6x6-x4.stl skadis-board.scad

Any other size: set `cols` and `rows`; a 3 × 6 half tile (120 × 240) finishes an odd width.

## Should you use a generator online instead?

For the board itself, no: this file is 50 lines, needs no library, and the only thing that matters is the four numbers above, which every generator shares. For accessories (bins, hooks, holders) use the published ones; `makerworld.com/en/models/799571` (parametric bins and shelves) and the Printables "Parametric Skadis Board" are the usual starting points, and openGrid has a SKÅDIS adapter if you want to hang openGrid parts on it.

## openGrid, bigger tiles

The biggest openGrid Lite tile a 256 mm bed takes is 9 × 9 cells (252 × 252 mm). `components/underware/` carries `tile-9x9-lite.stl` for a wall or a cabinet side, and `tile-8x9-lite.stl` for a deeper run behind rail A (the Underware plan stays on 8 × 4 tiles; a deeper tile there only adds hanging space, it does not change the channel).
