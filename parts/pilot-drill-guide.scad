// Pilot drill guide and tape-flag gauge.
// Two bores keep the bit square to the top: 1/8 in for every pilot into the EKBACKEN tops,
// 5/64 in for the ring screws into the ALEX tops. Grooves round the block at 12, 15, 20 mm
// from the base, and the top face at 25 mm, set the tape flag: hold the bit tip on the bench
// against the block's base and wrap the tape level with the groove you need.
// Print standing on its base. Any filament, 100% infill is fine, it is small.

L = 44; W = 22; H = 25;
bore_8th  = 3.3;   // 1/8 in bit is 3.175 mm
bore_64th = 2.2;   // 5/64 in bit is 1.98 mm
grooves   = [12, 15, 20];

difference() {
    cube([L, W, H]);
    translate([13, W / 2, -1]) cylinder(d = bore_8th, h = H + 2, $fn = 32);
    translate([31, W / 2, -1]) cylinder(d = bore_64th, h = H + 2, $fn = 32);
    for (g = grooves) {
        translate([-1, -1, g - 0.5]) cube([L + 2, 1.6, 1]);           // front
        translate([-1, W - 0.6, g - 0.5]) cube([L + 2, 1.6, 1]);      // back
        translate([-1, -1, g - 0.5]) cube([1.6, W + 2, 1]);           // left end
        translate([L - 0.6, -1, g - 0.5]) cube([1.6, W + 2, 1]);      // right end
        translate([L - 3.5 - (g - 12) * 1.6, 1.0, g + 1.2]) rotate([90, 0, 0]) linear_extrude(1.2) text(str(g), size = 3, halign = "right", valign = "bottom");  // staggered so the labels never overlap
    }
    translate([L - 24, 1.0, H - 4]) rotate([90, 0, 0]) linear_extrude(1.2) text("25", size = 3, halign = "right", valign = "bottom");
    translate([13, 2.5, H - 0.6]) linear_extrude(1) text("1/8", size = 3.5, halign = "center");
    translate([31, 2.5, H - 0.6]) linear_extrude(1) text("5/64", size = 3.5, halign = "center");
}
