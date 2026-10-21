// Wall-gap corner. One L-shaped piece for the back-left corner of top A, where the gap along
// the back wall meets the gap along the side wall. Same profile, lip, screws and gap rule as
// the strip. Each leg is 151 mm from the wall corner, so it ends 12.0 cm along each desk edge
// and the first strip butts against it there. One screw per leg.
// The file is in PRINT orientation: top face down, lips up, no supports.

leg = 151; gap = 29; ontop = 12; th = 3; lip = 20; lip_t = 3; chamf = 1.5; screw = 3.2; csk = 6.5; hole_z = -14;
w = gap + ontop;

module hole_y(x) { translate([x, gap - lip_t - 1, hole_z]) rotate([-90, 0, 0]) { cylinder(d = screw, h = lip_t + 2, $fn = 24); translate([0, 0, 1 - 0.01]) cylinder(d1 = csk, d2 = screw, h = (csk - screw) / 2 + 0.01, $fn = 24); } }
module hole_x(y) { translate([gap - lip_t - 1, y, hole_z]) rotate([0, 90, 0]) { cylinder(d = screw, h = lip_t + 2, $fn = 24); translate([0, 0, 1 - 0.01]) cylinder(d1 = csk, d2 = screw, h = (csk - screw) / 2 + 0.01, $fn = 24); } }
module corner() {   // use orientation
    difference() {
        union() {
            cube([leg, w, th]);                                                  // along the back wall (x), wall side at y = 0
            cube([w, leg, th]);                                                  // along the side wall (y), wall side at x = 0
            translate([w, gap - lip_t, -lip]) cube([leg - w, lip_t, lip]);      // lip along the back-wall leg, where the desk edge is
            translate([gap - lip_t, w, -lip]) cube([lip_t, leg - w, lip]);      // lip along the side-wall leg
        }
        // chamfers: the two exposed desk-side top edges, beyond the inner corner, and the two wall-side top edges
        translate([w + (leg - w) / 2 + 1, w, th]) rotate([45, 0, 0]) cube([leg - w + 2, chamf * 1.5, chamf * 1.5], center = true);
        translate([w, w + (leg - w) / 2 + 1, th]) rotate([0, 45, 0]) cube([chamf * 1.5, leg - w + 2, chamf * 1.5], center = true);
        translate([leg / 2, 0, th]) rotate([45, 0, 0]) cube([leg + 2, chamf * 1.5, chamf * 1.5], center = true);
        translate([0, leg / 2, th]) rotate([0, 45, 0]) cube([chamf * 1.5, leg + 2, chamf * 1.5], center = true);
        hole_y(leg - 30);
        hole_x(leg - 30);
    }
}
translate([0, 0, th]) mirror([0, 0, 1]) corner();   // flipped for printing
