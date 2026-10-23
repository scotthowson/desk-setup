// EKB leg jig, for the OLOV legs. Hook the lip over the edge named in the manual's table,
// slide to the station, punch the centre and the five plate holes: the leg's plate then
// lands exactly on its mark, square to the edge, and every leg's five screws sit the same
// way round. Two patterns: 100 (legs L2 to L6, 10 cm from the wall edges) with one hole
// pointing at the wall, and 150 (leg L1, 15 cm from the side-wall end) turned 36 degrees so
// its holes clear the 100 pattern. OLOV plate: 105 mm diameter, five 5.5 mm holes on a
// 42.5 mm radius (85 mm circle; neighbouring holes 50 mm apart), from a shared OLOV template
// (schablone.stp) and Scott's 49 mm hole-to-hole measurement, 22 Oct 2026. The T-square's 100 and 150 holes are the centres only.
// PRINT orientation: flat on the bed, lip up; turn over to use. Any filament.

t = 3; lip_h = 6; lip_t = 4; len = 215; w = 110; hole_d = 4;
r = 42.5; n = 5;
module pattern(cx, rot) {
    translate([cx, 0, -1]) cylinder(d = hole_d, h = t + 2, $fn = 24);
    for (i = [0 : n - 1]) translate([cx + r * cos(rot + i * 360 / n), r * sin(rot + i * 360 / n), -1]) cylinder(d = hole_d, h = t + 2, $fn = 24);
}
module jig() {
    difference() {
        union() {
            translate([0, -w / 2, 0]) cube([len, w, t]);
            translate([-lip_t, -w / 2, -lip_h]) cube([lip_t, w, lip_h + t]);
        }
        pattern(100, 180);   // one hole toward the edge
        pattern(150, 0);     // one hole away from the edge
        translate([0, 0, t - 0.6]) labels();   // labels on the face you see in use
    }
}
module labels(top = false) {
    translate([30, 0, 0]) mirror([0, top ? 0 : 1, 0]) rotate([0, 0, 90]) linear_extrude(1) text("EKB LEG  .  OLOV 5 holes", size = 3.6, halign = "center", valign = "center");
    translate([100, -12, 0]) mirror([0, top ? 0 : 1, 0]) linear_extrude(1) text("100  L2 L3 L4 L5 L6", size = 3.4, halign = "center", valign = "center");
    translate([150, 10, 0]) mirror([0, top ? 0 : 1, 0]) linear_extrude(1) text("150  L1", size = 3.4, halign = "center", valign = "center");
    if (!top) translate([-lip_t / 2 - 0.2, 0, 0]) mirror([0, 1, 0]) rotate([0, 0, 90]) linear_extrude(1) text("edge", size = 2.4, halign = "center", valign = "center");
}
difference() {
    translate([0, 0, t]) mirror([0, 0, 1]) jig();   // flipped for printing
    translate([0, 0, t - 0.6]) labels(top = true);   // print-top labels read as written; the use-face ones above are mirrored in y so they read after the flip
}
