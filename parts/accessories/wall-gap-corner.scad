// Wall-gap corner. One L-shaped piece for the back-left corner of top A, where the gap along
// the back wall meets the gap along the side wall. Same profile, lip, screws and pockets as
// the strip. Each leg is 230 mm from the wall corner: with the desk 30 mm off the wall the
// leg ends at desk 20.0 cm, where the 80 mm filler starts. One screw per leg.
// The file is in PRINT orientation: top face down, lips up, no supports.

include <wall-gap-common.scad>
leg = 230;
w = gap + ontop;

module hole_x(y) { translate([gap - lip_t - 1, y, hole_z]) rotate([0, 90, 0]) { cylinder(d = screw, h = lip_t + 2, $fn = 24); translate([0, 0, 1 - 0.01]) cylinder(d1 = csk, d2 = screw, h = (csk - screw) / 2 + 0.01, $fn = 24); } }
module corner() {
    difference() {
        union() {
            cube([leg, w, th]);                                                  // along the back wall (x), wall side at y = 0
            cube([w, leg, th]);                                                  // along the side wall (y), wall side at x = 0
            translate([w, gap - lip_t, -lip]) cube([leg - w, lip_t, lip]);      // lip along the back-wall leg
            translate([gap - lip_t, w, -lip]) cube([lip_t, leg - w, lip]);      // lip along the side-wall leg
        }
        // chamfers: the two exposed desk-side top edges beyond the inner corner, and the two wall-side top edges
        translate([w + (leg - w) / 2 + 1, w, th]) rotate([45, 0, 0]) cube([leg - w + 2, chamf * 1.5, chamf * 1.5], center = true);
        translate([w, w + (leg - w) / 2 + 1, th]) rotate([0, 45, 0]) cube([chamf * 1.5, leg - w + 2, chamf * 1.5], center = true);
        translate([leg / 2, 0, th]) rotate([45, 0, 0]) cube([leg + 2, chamf * 1.5, chamf * 1.5], center = true);
        translate([0, leg / 2, th]) rotate([0, 45, 0]) cube([chamf * 1.5, leg + 2, chamf * 1.5], center = true);
        lip_holes([leg - 30]);
        hole_x(leg - 30);
        // connector pocket at the end of each leg
        translate([leg - pocket_l, pocket_y - pocket_w / 2, -1]) cube([pocket_l + 1, pocket_w, pocket_d + 1]);
        translate([leg - pin_from_end, pocket_y, -1]) cylinder(d = pin_hole, h = pocket_d + pin_depth + 1, $fn = 20);
        translate([pocket_y - pocket_w / 2, leg - pocket_l, -1]) cube([pocket_w, pocket_l + 1, pocket_d + 1]);
        translate([pocket_y, leg - pin_from_end, -1]) cylinder(d = pin_hole, h = pocket_d + pin_depth + 1, $fn = 20);
    }
}
translate([0, 0, th]) mirror([0, 0, 1]) corner();   // flipped for printing
