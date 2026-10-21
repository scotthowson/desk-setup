// Wall-gap corner. One L-shaped piece for the back-left corner of top A, where the gap
// along the back wall meets the gap along the side wall. Same profile as the strip; the
// two legs are 120 mm long and the strips butt against their ends. Print flat, top face up.

leg   = 120;
gap   = 31;    // keep equal to the strip's gap
ontop = 12;
th    = 3;
chamf = 1.5;
lip   = 16;    // locating lip, hangs into the gap against the desk's edge; the screws go through it
lip_t = 3;
screw = 3.2;   // #4 screw clearance; countersunk on the wall side
csk   = 6.5;
w = gap + ontop;

difference() {
    union() {
        cube([leg, w, th]);                                   // along the back wall (x), wall side at y = 0
        cube([w, leg, th]);                                   // along the side wall (y), wall side at x = 0
    }
    // chamfers on the two exposed desk-side edges, only beyond the inner corner
    translate([w + (leg - w) / 2 + 1, w, th]) rotate([45, 0, 0]) cube([leg - w + 2, chamf * 1.5, chamf * 1.5], center = true);
    translate([w, w + (leg - w) / 2 + 1, th]) rotate([0, 45, 0]) cube([chamf * 1.5, leg - w + 2, chamf * 1.5], center = true);
}
difference() {
    union() {
        translate([w, gap - lip_t, -lip]) cube([leg - w, lip_t, lip]);   // lip along the back-wall leg, only where the desk edge is
        translate([gap - lip_t, w, -lip]) cube([lip_t, leg - w, lip]);   // lip along the side-wall leg
    }
    translate([leg - 30, gap - lip_t - 1, -lip / 2 - 2]) rotate([-90, 0, 0]) { cylinder(d = screw, h = lip_t + 2, $fn = 24); cylinder(d1 = csk, d2 = screw, h = (csk - screw) / 2 + 0.01, $fn = 24); }
    translate([gap - lip_t - 1, leg - 30, -lip / 2 - 2]) rotate([0, 90, 0]) { cylinder(d = screw, h = lip_t + 2, $fn = 24); cylinder(d1 = csk, d2 = screw, h = (csk - screw) / 2 + 0.01, $fn = 24); }
}
