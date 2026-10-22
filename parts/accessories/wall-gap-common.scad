// Shared numbers and modules for every wall-gap trim piece. Change a number here and
// re-render all of them. Measurements in mm.
//
// Cross-section (across the strip): 0 is the wall, `gap` is the desk's edge, the strip
// rests `ontop` on the desk beyond that. A `lip` hangs into the gap against the desk's raw
// back edge and takes the #4 screws, 14 mm below the surface. Every end has a pocket on the
// underside, over the gap, for a connector tile (wall-gap-connector.scad) with two press-fit
// pins: butt two pieces together, push a tile up into both pockets, and the joint cannot
// step or bow. The pin holes are blind, so nothing shows on top.

gap   = 29;    // reach from the desk's edge to the wall: design gap 30 minus 1. Set to the smallest measured gap minus 1.
ontop = 12;    // how far it rests on the desk surface
th    = 3;     // plate thickness
lip   = 20;    // lip hanging into the gap
lip_t = 3;
chamf = 1.5;   // chamfer on the two long top edges (never on the ends, so butt joints stay hairlines)
screw = 3.2;   // #4 clearance
csk   = 6.5;
hole_z = -14;  // screw centre below the desk surface: the board's mid-plane

// connector pocket: on the underside of the gap part, at each end
pocket_l = 20; pocket_w = 12; pocket_d = 1.2;
pin_hole = 2.5; pin_depth = 1.0; pin_from_end = 10;
pocket_y = (gap - lip_t) / 2;   // centred across the gap part (between the wall edge and the lip)

module profile() { polygon([[0, 0], [gap + ontop, 0], [gap + ontop, th - chamf], [gap + ontop - chamf, th], [chamf, th], [0, th - chamf]]); }
module lip_holes(xs) { for (x = xs) translate([x, gap - lip_t - 1, hole_z]) rotate([-90, 0, 0]) { cylinder(d = screw, h = lip_t + 2, $fn = 24); translate([0, 0, 1 - 0.01]) cylinder(d1 = csk, d2 = screw, h = (csk - screw) / 2 + 0.01, $fn = 24); } }
// pockets at x = 0 (the start) and x = len (the end) of a piece running along x
module end_pockets(len) {
    for (e = [0, 1]) {
        x0 = e == 0 ? -1 : len - pocket_l;
        translate([x0, pocket_y - pocket_w / 2, -1]) cube([pocket_l + 1, pocket_w, pocket_d + 1]);
        xp = e == 0 ? pin_from_end : len - pin_from_end;
        translate([xp, pocket_y, -1]) cylinder(d = pin_hole, h = pocket_d + pin_depth + 1, $fn = 20);
    }
}
module plain_strip(len) {
    difference() {
        union() {
            rotate([90, 0, 90]) linear_extrude(len) profile();
            translate([0, gap - lip_t, -lip]) cube([len, lip_t, lip]);
        }
        lip_holes(len >= 120 ? [40, len - 40] : [len / 2]);
        end_pockets(len);
    }
}
