// Feet corner jig. Drop it over a corner of a desk top (face down): the two fences sit against
// the two edges, and the holes give you a foot's centre 8.5 cm from both edges plus its four
// plate screw holes, square to the edges, in one placement. That is F2 and F4 at top A's far
// corners and F7 and F8 at top B's far corners: no measuring at all for those four. The other
// four feet (F1, F3, F5, F6) are 34.5 cm from the end: the T-square's 85 hole does those.
// The plate is the measured 59.5 x 59.5 mm with 5.4 mm holes 47.0 mm apart (23 Oct 2026: 41.6 inner to inner).
// The file is in PRINT orientation: flat face on the bed, fences up, no supports. Turn it
// over to use. Any filament.

inset   = 85;      // foot centre from each edge
hole_sp = 47.0;    // plate holes, centre to centre, measured
plate   = 59.5;    // feet plate, engraved so you can see where it lands
plate_t = 2.5; size = 125; fence_h = 6; fence_t = 4; hole_d = 4;

module square_line(s) { translate([inset, inset, plate_t - 0.5]) difference() { translate([-s / 2 - 0.45, -s / 2 - 0.45, 0]) cube([s + 0.9, s + 0.9, 1]); translate([-s / 2 + 0.45, -s / 2 + 0.45, -1]) cube([s - 0.9, s - 0.9, 3]); } }
module jig() {
    difference() {
        union() {
            cube([size, size, plate_t]);
            translate([-fence_t, -fence_t, -fence_h]) cube([size + fence_t, fence_t, fence_h + plate_t]);
            translate([-fence_t, -fence_t, -fence_h]) cube([fence_t, size + fence_t, fence_h + plate_t]);
        }
        translate([inset, inset, -1]) cylinder(d = hole_d, h = plate_t + 2, $fn = 24);
        for (sx = [-1, 1], sy = [-1, 1]) translate([inset + sx * hole_sp / 2, inset + sy * hole_sp / 2, -0.01]) cylinder(d1 = 2.4, d2 = 5.4, h = plate_t + 0.02, $fn = 32);   // 5.4 at the face like the plate's holes (calipers read 41.6 inner to inner), tapering so a scriber self-centres
        square_line(plate);
        translate([0, 0, plate_t - 0.6]) labels();   // labels on the face you see in use
    }
}
module labels(top = false) {
    translate([inset, 9.8, 0]) mirror([0, top ? 0 : 1, 0]) linear_extrude(1) text("foot 8.5 / 8.5  .  holes 47.0", size = 3.6, halign = "center", valign = "center");
    translate([size - 6, size / 2, 0]) mirror([0, top ? 0 : 1, 0]) rotate([0, 0, 90]) linear_extrude(1) text("fences against the EKB edges", size = 3.4, halign = "center", valign = "center");
    translate([inset, size - 5, 0]) mirror([0, top ? 0 : 1, 0]) linear_extrude(1) text("EKB FEET CORNER", size = 5, halign = "center", valign = "center");
}
difference() {
    translate([0, 0, plate_t]) mirror([0, 0, 1]) jig();   // flipped for printing
    translate([0, 0, plate_t - 0.6]) labels(top = true);   // print-top labels read as written; the use-face ones above are mirrored in y so they read after the flip
}
