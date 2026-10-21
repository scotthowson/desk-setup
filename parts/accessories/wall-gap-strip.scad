// Wall-gap strip. Covers the 3 cm gap between a top's wall edge and the wall so nothing
// falls in. Rests 12 mm on the desk; a 20 mm lip hangs into the gap against the desk's raw
// back edge, and two #4 x 1/2 in flat-head screws through the lip go sideways into that edge,
// 14 mm below the surface (the middle of the 28 mm board). Hidden in the gap. 3M VHB tape
// under the flat is the no-screw alternative.
// 240 mm segments, butted end to end; set `seg` for the short end pieces (README cut list).
// After the desk is in, measure the gap in several places and set `gap` to the SMALLEST
// value minus 1: a strip 1-2 mm short of the wall is invisible, one too long will not seat.
//
// The file is in PRINT orientation: top face down on the bed, lip pointing up, no supports.
// A colour near the walnut, or black.

seg   = 240;   // segment length (240 fits the P1S / A1 bed)
gap   = 29;    // reach from the desk's edge to the wall: design gap 30 minus 1
ontop = 12;    // how far it rests on the desk surface
th    = 3;     // thickness
lip   = 20;    // lip hanging into the gap against the desk's edge
lip_t = 3;
chamf = 1.5;   // chamfer on the exposed top edges
screw = 3.2;   // #4 clearance
csk   = 6.5;   // countersunk on the wall side of the lip
hole_z = -14;  // screw centre below the desk surface: the board's mid-plane

module profile() {   // across the strip: 0 is the wall, gap is the desk's edge; both top edges chamfered
    polygon([[0, 0], [gap + ontop, 0], [gap + ontop, th - chamf], [gap + ontop - chamf, th], [chamf, th], [0, th - chamf]]);
}
module lip_holes(xs) { for (x = xs) translate([x, gap - lip_t - 1, hole_z]) rotate([-90, 0, 0]) { cylinder(d = screw, h = lip_t + 2, $fn = 24); translate([0, 0, 1 - 0.01]) cylinder(d1 = csk, d2 = screw, h = (csk - screw) / 2 + 0.01, $fn = 24); } }
module strip() {   // use orientation: top face at z = th, lip hanging below
    difference() {
        union() {
            rotate([90, 0, 90]) linear_extrude(seg) profile();                 // length along x, across along y, thickness up z
            translate([0, gap - lip_t, -lip]) cube([seg, lip_t, lip]);         // the lip, outer face against the desk's edge
        }
        lip_holes([40, seg - 40]);
    }
}
translate([0, 0, th]) mirror([0, 0, 1]) strip();   // flipped for printing
