// Wall-gap strip with a cable slot: the same strip as wall-gap-strip.scad with a 60 x 18 mm
// rounded slot over the gap so monitor, speaker and PC leads drop straight down behind the
// desk. Everything else (lip, screws, gap rule, print orientation) is identical; keep the
// numbers below equal to the plain strip's.

seg = 240; gap = 29; ontop = 12; th = 3; lip = 20; lip_t = 3; chamf = 1.5; screw = 3.2; csk = 6.5; hole_z = -14;
slot_l = 60; slot_w = 18;

module profile() { polygon([[0, 0], [gap + ontop, 0], [gap + ontop, th - chamf], [gap + ontop - chamf, th], [chamf, th], [0, th - chamf]]); }
module lip_holes(xs) { for (x = xs) translate([x, gap - lip_t - 1, hole_z]) rotate([-90, 0, 0]) { cylinder(d = screw, h = lip_t + 2, $fn = 24); translate([0, 0, 1 - 0.01]) cylinder(d1 = csk, d2 = screw, h = (csk - screw) / 2 + 0.01, $fn = 24); } }
module strip() {
    difference() {
        union() {
            rotate([90, 0, 90]) linear_extrude(seg) profile();
            translate([0, gap - lip_t, -lip]) cube([seg, lip_t, lip]);
        }
        lip_holes([40, seg - 40]);
        translate([seg / 2, (gap - lip_t) / 2, -1]) hull() {                   // stadium slot over the gap, between the wall and the lip
            translate([-(slot_l - slot_w) / 2, 0, 0]) cylinder(d = slot_w, h = th + 2, $fn = 48);
            translate([ (slot_l - slot_w) / 2, 0, 0]) cylinder(d = slot_w, h = th + 2, $fn = 48);
        }
    }
}
translate([0, 0, th]) mirror([0, 0, 1]) strip();   // flipped for printing
