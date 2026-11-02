// Cable exit comb on openGrid, one cell: where leads leave a channel run or drop to the floor,
// four 7 mm slots with 3 mm fingers hold them apart and off the tile. Print plate down, snaps
// up, PETG. Snap it in the cell past the channel's open end.
//   openscad -o og-cable-exit-x2.stl og-cable-exit.scad
include <og-lib.scad>
slot = 7; finger = 3; depth = 14; t = 8;

og_plate(1, 1);
difference() {
    translate([0.4, cell / 2 - t / 2, -depth - 3]) cube([cell - 0.8, t, depth + 3]);
    for (i = [0 : 3]) translate([0.4 + finger + i * (slot + finger), cell / 2 - t / 2 - 1, -depth - 4]) cube([slot, t + 2, depth + 1]);
}
