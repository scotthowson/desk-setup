// Stiffening ribs for the back of the SKÅDIS board. This is what stops the board being
// flimsy: a 5 mm printed tile is bendier than IKEA's fibreboard, every joint between tiles
// is a hinge, and the whole board stands on clamps at its bottom edge. A rib glued along
// each upright joint makes that joint rigid for its whole length, and ribs down the middle
// of each tile, crossing the level joints, stiffen the board top to bottom. Together they
// make the 3 x 3 board about 20 times stiffer against a push on its top edge.
//
// Where they go, and why nothing is lost: the slots sit in columns at x = 10 and 30 (mod 40),
// so the back of a tile is solid, full height, in 15 mm bands centred on every x = 20, 40,
// 60 ... and on the joint lines themselves. A 12 mm rib in such a band covers no slot and
// stays 1.5 mm clear of the slots either side, where IKEA's hook tabs drop behind the board.
// Level (horizontal) ribs are impossible: the solid band between rows is 5 mm and sits
// right under a row of slots, where the hook tabs hang.
//
// Keys: the rib carries the bow-tie keys of the pockets it covers, built in (same shape as
// skadis-key.scad, the original fit, clipped to the rib's width: the dovetail still flares
// from 5 to 10.5). So a joint rib drops into the three pockets of that joint instead of
// three loose keys, is located by them, and is then glued (CA, a bead each side). keys = []
// gives a flat rib to glue over keys that are already in.
//
// Pieces (print count for a 3 x 3 board):
//   rib-240-k3-x4   L 240, keys at 40 120 200   upright joints, 80..320 and 320..560
//   rib-80-k1-x2    L 80,  key at 40             upright joints, 0..80
//   rib-160-k2-x2   L 160, keys at 40 120        upright joints, 560..720
//   rib-240-k1-x6   L 240, key at 120, along     tile-centre bands x 120 360 600, 120..360 and 360..600
//   rib-240-k0      L 240, no keys               flat, for joints whose keys are already in
// The upright-joint ribs are staggered (ends at 80, 320, 560) so every level joint is
// crossed by a rib, and the rib ends never fall on a pocket. The centre-band ribs start at
// 120 so they clear the clamp frames' uprights (113 mm tall) at the bottom.
//
// Print on the outer face (as saved: keys up), PETG, 3 walls, 15-20 % gyroid. 240 x 12 x 20.
//   openscad -D L=240 -D 'keys=[40,120,200]' -o rib-240-k3-x4.stl skadis-rib.scad
//   openscad -D L=240 -D 'keys=[120]' -D along=true -o rib-240-k1-x6.stl skadis-rib.scad

include <skadis-lib.scad>

L = 240;
keys = [40, 120, 200];   // key centres, mm from the rib's start (an empty list for a flat rib)
along = false;           // false: keys run across the rib (an upright joint); true: along it (a centre-band rib crossing a level joint)
width = 12;              // across the band: 15 is solid, 12 leaves 1.5 mm to the slots
depth = 20;              // out from the board; stiffness grows with the cube of this
cham = 1;                // on the outer edges
key_h = key_depth - 0.1; key_cham = 0.5;

module key_up() {   // original key, clipped to the rib's width, chamfer on top (the camming face)
    steps = 5;
    intersection() {
        union() {
            linear_extrude(key_h - key_cham) polygon(key_poly);
            for (i = [0 : steps - 1]) translate([0, 0, key_h - key_cham + i * key_cham / steps]) linear_extrude(key_cham / steps + 0.01) offset(delta = -key_cham * (i + 1) / steps) polygon(key_poly);
        }
        translate([-width / 2, -10, -1]) cube([width, 20, 10]);   // clip across the rib (x); nothing to clip along it
    }
}
// y along the rib, x across it, z out from the board: the face at z = 0 sits on the board
module body() hull() {
    translate([-width / 2, 0, 0]) cube([width, L, depth - cham]);
    translate([-width / 2 + cham, 0, 0]) cube([width - 2 * cham, L, depth]);
}
// keys on the board face: an upright joint's pockets run their 13 across the joint (across
// the rib); a level joint's pockets run their 13 along the rib. Both are 180° symmetric, so
// the rib fits either way round. `along` = true for the centre-band ribs. The clip to the
// rib's width only touches the across keys (13 long on a 12 rib). Saved keys up, the outer
// face on the bed.
translate([0, 0, depth]) mirror([0, 0, 1]) {
    body();
    for (k = keys) translate([0, k, 0]) mirror([0, 0, 1]) rotate([0, 0, along ? 90 : 0]) key_up();
}
