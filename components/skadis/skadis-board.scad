// SKÅDIS-compatible pegboard tile that joins to its neighbours and keeps IKEA's hole pitch
// across the joint, so IKEA's own hooks, clips and containers fit anywhere on the wall.
//
// IKEA SKÅDIS geometry (community-measured, IKEA publishes none; check one hook on the
// first print): board 5 mm thick; every opening is a vertical obround slot 5 mm wide and
// 15 mm tall; along a row the slots are 40 mm apart, rows are 20 mm apart, and every other
// row is shifted 20 mm, so it is a 40 x 40 grid plus a second 40 x 40 grid at its centres.
//
// Tile: cols x rows cells of 40 mm, so 6 x 6 is 240 x 240 (a P1S / A1 bed is 256). The
// pattern sits 10 mm in from the edges, so the solid band at every edge is the widest the
// pattern allows and the pitch continues across a joint: the neighbour's first slot is
// exactly 40 mm from this tile's last, in both directions. All tiles are identical.
// Edges: dovetail tabs on the right and top edges, matching sockets on the left and bottom;
// lay the next tile over the tabs (they drop in from the face) and the joint cannot pull
// apart in the plane. Outer tiles keep their tabs (hidden behind the board) or print with
// tabs = false. Screw holes: countersunk for a #8 / M4 at every second cell corner (80 mm
// grid), always in solid, for screws into the wall or a batten through 20 mm spacers,
// as IKEA mounts its board (hooks need the space behind).
//
//   openscad -D cols=6 -D rows=6 -o skadis-6x6.stl skadis-board.scad
// Print flat, as saved, 0.2 mm layers, 4 walls, PETG (the dovetails).

cols = 6; rows = 6;        // cells of 40 mm
pitch = 40; th = 5;
slot_w = 5; slot_h = 15;
tabs = true;               // dovetails on the right and top edges
screw_d = 4.5; csk_d = 9;
tab_w = 8; tab_d = 4; tab_slop = 0.15;

W = cols * pitch; H = rows * pitch;

module slot() { hull() { translate([0,  (slot_h - slot_w) / 2, 0]) cylinder(d = slot_w, h = th + 2, $fn = 24);
                         translate([0, -(slot_h - slot_w) / 2, 0]) cylinder(d = slot_w, h = th + 2, $fn = 24); } }
tab_poly = [[-tab_w / 2, 0], [tab_w / 2, 0], [tab_w / 2 + 1, tab_d], [-tab_w / 2 - 1, tab_d]];   // 8 at the root, 10 at the tip
module tab() { linear_extrude(th) polygon(tab_poly); }
module socket() { translate([0, 0, -1]) linear_extrude(th + 2) offset(delta = tab_slop) polygon(tab_poly); }
module board() {
    difference() {
        union() {
            cube([W, H, th]);
            if (tabs) {
                for (j = [0 : rows - 1]) translate([W, j * pitch + pitch / 2, 0]) rotate([0, 0, -90]) tab();   // right edge, points +x
                for (i = [0 : cols - 1]) translate([i * pitch + pitch / 2, H, 0]) tab();                        // top edge, points +y
            }
        }
        for (i = [0 : cols - 1], j = [0 : rows - 1]) {
            translate([i * pitch + 10, j * pitch + 10, -1]) slot();   // rows at y = 10 + 40 j
            translate([i * pitch + 30, j * pitch + 30, -1]) slot();   // rows at y = 30 + 40 j, shifted 20
        }
        for (j = [0 : rows - 1]) translate([0, j * pitch + pitch / 2, 0]) rotate([0, 0, -90]) socket();   // left edge, cut 4 mm into the board
        for (i = [0 : cols - 1]) translate([i * pitch + pitch / 2, 0, 0]) socket();                        // bottom edge
        for (i = [2 : 2 : cols - 1], j = [2 : 2 : rows - 1])   // cell corners are solid: the nearest slot edge is 7.5 mm away
            translate([i * pitch, j * pitch, -1]) { cylinder(d = screw_d, h = th + 2, $fn = 24); translate([0, 0, th + 1 - (csk_d - screw_d) / 2]) cylinder(d1 = screw_d, d2 = csk_d, h = (csk_d - screw_d) / 2 + 0.01, $fn = 24); }
    }
}
board();
