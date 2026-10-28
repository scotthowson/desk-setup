// SKÅDIS-compatible pegboard tiles that assemble into one board of any size, with finished
// outer edges, a skirt that closes the gap to the desk, and a lock at every joint.
//
// Pattern (community-measured IKEA SKÅDIS; check one IKEA hook on the first tile): board
// 5 mm thick, vertical obround slots 5 wide x 15 tall, 40 mm apart along a row, rows 20 mm
// apart and every other row shifted 20 mm. The pattern sits 10 mm in from every tile edge,
// so the neighbour's first slot is exactly 40 mm from this tile's last: one board, no seam
// in the pattern. All tiles are the same size; `outer_*` says which edges are the board's
// outside (chamfered, no pockets) and which are joints (lock pockets).
//
// The lock: at each joint, three bow-tie keys (skadis-key.scad) sit in pockets cut from
// the BACK of both tiles, 3.5 mm deep, leaving a 1.5 mm skin on the front. The dovetail
// shape stops the tiles pulling apart; the pocket floor holds the two faces flush; the
// skin stops the key coming out the front; a 0.3 mm lip round the back of the pocket
// snaps over the key so it cannot fall out the back. Push a key in with a thumb until it
// clicks; nothing shows on the front. The keys sit at cell corners (40, 120, 200 mm along
// a 240 edge), where the pattern leaves 2.5 mm of solid each side.
//
// Desk mount (makerworld 2780289, measured from its 3MF): the board rests on the foot
// frame's ledge, `lift` mm above the desk, with the frame's 40 x 12 mm upright behind it
// and the frame screw (4.8 x 14 shank) through any slot of the bottom row. Bottom tiles get
// a `lift` mm skirt so the board reaches the desk with a straight bottom edge that sits
// flush in the clamps. `notches` is empty; if a frame's foot plate ever needs clearance,
// add notch centres (mm from the tile's left edge) and the `clamp_w` / `base_w` x `base_h`
// cuts come back. Set lift = 0 for no skirt.
//
// Positions, rendered as skadis-<pos>.stl: TL T TR / L C R / BL B BR for a board of two or
// more rows; L1 M1 R1 for a single-row board (top and bottom both outside).
//   openscad -D 'pos="BL"' -o skadis-BL-x1.stl skadis-tile.scad
// Print FRONT FACE DOWN (as saved), 0.2 mm layers, 4 walls, PETG. 240 x 252 with the skirt.

pos = "C";                 // TL T TR L C R BL B BR, or L1 M1 R1 (single row)
cols = 6; rows = 6;        // cells of 40 mm: 240 x 240
pitch = 40; th = 5;
slot_w = 5; slot_h = 15;
chamfer = 1.5;             // on the front face along outer edges
lift = 12;                 // skirt below the bottom row: the frame lifts the board this much off the desk
clamp_w = 40; base_w = 60; base_h = 4;   // the mount's upright, and its foot plate
notches = [];                            // no notches: the bottom edge is straight and sits flush in the clamps; add centres (mm from the left) if a frame's foot needs one
key_at = [40, 120, 200];   // key centres along each joint, mm from the tile's left or bottom edge
key_len = 13; key_neck = 6; key_tip = 10; key_depth = 3.5; slop = 0.1; lip = 0.3; lip_h = 0.5;

outer_top    = pos == "TL" || pos == "T" || pos == "TR" || pos == "L1" || pos == "M1" || pos == "R1";
outer_bottom = pos == "BL" || pos == "B" || pos == "BR" || pos == "L1" || pos == "M1" || pos == "R1";
outer_left   = pos == "TL" || pos == "L" || pos == "BL" || pos == "L1";
outer_right  = pos == "TR" || pos == "R" || pos == "BR" || pos == "R1";

W = cols * pitch; H = rows * pitch;
skirt = outer_bottom ? lift : 0;

module slot() { hull() for (s = [-1, 1]) translate([0, s * (slot_h - slot_w) / 2, 0]) cylinder(d = slot_w, h = th + 2, $fn = 24); }
key_poly = [[-key_len / 2, -key_tip / 2], [-key_len / 2, key_tip / 2], [0, key_neck / 2], [key_len / 2, key_tip / 2], [key_len / 2, -key_tip / 2], [0, -key_neck / 2]];
module pocket() {   // centred on the joint line, cut from the back; the lip is the last lip_h
    translate([0, 0, th - key_depth]) linear_extrude(key_depth - lip_h + 0.01) offset(delta = slop) polygon(key_poly);
    translate([0, 0, th - lip_h]) linear_extrude(lip_h + 1) offset(delta = slop - lip) polygon(key_poly);
}
module front_chamfer(len) { rotate([45, 0, 0]) cube([len + 2, chamfer * 1.4142, chamfer * 1.4142], center = true); }

difference() {
    translate([0, -skirt, 0]) cube([W, H + skirt, th]);
    for (i = [0 : cols - 1], j = [0 : rows - 1]) {
        translate([i * pitch + 10, j * pitch + 10, -1]) slot();
        translate([i * pitch + 30, j * pitch + 30, -1]) slot();
    }
    // lock pockets on the joint edges (a key straddles the edge, half in each tile)
    if (!outer_right)  for (y = key_at) translate([W, y, 0]) pocket();
    if (!outer_left)   for (y = key_at) translate([0, y, 0]) pocket();
    if (!outer_top)    for (x = key_at) translate([x, H, 0]) rotate([0, 0, 90]) pocket();
    if (!outer_bottom) for (x = key_at) translate([x, 0, 0]) rotate([0, 0, 90]) pocket();
    // front chamfers on the outside edges
    if (outer_top)    translate([W / 2, H, 0]) front_chamfer(W);
    if (outer_bottom) translate([W / 2, -skirt, 0]) front_chamfer(W);
    if (outer_left)   translate([0, (H - skirt) / 2, 0]) rotate([0, 0, 90]) front_chamfer(H + skirt);
    if (outer_right)  translate([W, (H - skirt) / 2, 0]) rotate([0, 0, 90]) front_chamfer(H + skirt);
    // notches in the skirt for the mount's upright and foot plate
    if (outer_bottom && lift > 0) for (nx = notches) {
        translate([nx - clamp_w / 2 - 1, -skirt - 1, -1]) cube([clamp_w + 2, skirt + 1, th + 2]);
        translate([nx - base_w / 2 - 1, -skirt - 1, -1]) cube([base_w + 2, base_h + 1, th + 2]);
    }
}
