// Wall-gap strip. Covers the 3 cm gap between a top's wall edge and the wall so nothing
// falls in. Rests on the desk with a lip that drops into the gap against the desk's edge,
// and reaches to the wall. 240 mm segments, butted end to end; set `seg` for the short
// end pieces so nothing needs cutting (the README has the cut list). Leave the two VIVO
// clamp zones open. Print flat, top face up. A colour near the walnut, or black.
//
// Attach: two #4 x 1/2 in flat-head screws per segment through the lip into the desk's raw back
// edge, hidden in the gap, driven with a stubby or right-angle driver. Or 3M VHB tape under
// the flat if you would rather not screw anything.
//
// After the desk is in, measure the real gap in a few places and set `gap` to the largest
// value: a strip 1-2 mm short of the wall is invisible, one that is too long will not seat.

seg   = 240;   // segment length (240 fits the P1S / A1 bed)
gap   = 31;    // reach from the desk's edge to the wall; the design gap is 30, 1 mm added
ontop = 12;    // how far it rests on the desk surface
th    = 3;     // thickness
lip   = 16;    // locating lip, hangs into the gap against the desk's edge; the screws go through it
lip_t = 3;
screw = 3.2;   // #4 screw clearance; countersunk on the wall side
csk   = 6.5;
chamf = 1.5;   // chamfer on the exposed edges

module profile() {   // across the strip: 0 is the wall, gap is the desk's edge
    polygon([[chamf, 0], [gap + ontop, 0], [gap + ontop, th - chamf], [gap + ontop - chamf, th], [0, th], [0, chamf]]);
}
// two screw holes through the lip, into the desk's back edge, heads toward the wall
module lip_holes(x_list) { for (x = x_list) translate([x, gap - lip_t - 1, -lip / 2 - 2]) rotate([-90, 0, 0]) { cylinder(d = screw, h = lip_t + 2, $fn = 24); cylinder(d1 = csk, d2 = screw, h = (csk - screw) / 2 + 0.01, $fn = 24); } }
difference() {
    union() {
        rotate([90, 0, 90]) linear_extrude(seg) profile();   // length along x, across along y, thickness up z
        translate([0, gap - lip_t, -lip]) cube([seg, lip_t, lip]);    // the lip, its outer face against the desk's edge
    }
    lip_holes([40, seg - 40]);
}
