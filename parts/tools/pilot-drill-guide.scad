// Pilot drill guide and tape-flag gauge. Two jobs:
//  1. The bores keep the bit square: hold the block flat on the top and drill through it.
//     1/8 in for every pilot into the EKBACKEN tops, 5/64 in for the ring screws into the ALEX.
//  2. The grooves set the tape flag: stand the bit tip on the bench against the block's base
//     and wrap masking tape round the bit level with the groove you need (12, 15, 20) or
//     with the top face (25). When the tape touches the surface, the hole is that deep.
// Slim version: 30 x 16 x 25 mm. It must stay 25 mm tall, that height is the 25 mm measurement.
// Print standing on its base, 100% infill. Any filament.

L = 30; W = 16; H = 25;
bore_8th  = 3.3;   // 1/8 in bit is 3.175 mm
bore_64th = 2.2;   // 5/64 in bit is 1.98 mm
grooves   = [12, 15, 20];

difference() {
    cube([L, W, H]);
    translate([8, W / 2, -1]) cylinder(d = bore_8th, h = H + 2, $fn = 32);
    translate([22, W / 2, -1]) cylinder(d = bore_64th, h = H + 2, $fn = 32);
    for (g = grooves) {
        translate([-1, -1, g - 0.5]) cube([L + 2, 1.6, 1]);           // front
        translate([-1, W - 0.6, g - 0.5]) cube([L + 2, 1.6, 1]);      // back
        translate([-1, -1, g - 0.5]) cube([1.6, W + 2, 1]);           // left end
        translate([L - 0.6, -1, g - 0.5]) cube([1.6, W + 2, 1]);      // right end
        translate([L - 2 - (g - 12) * 1.1, 1.0, g + 1.0]) rotate([90, 0, 0]) linear_extrude(1.2) text(str(g), size = 2.6, halign = "right", valign = "bottom");  // staggered labels
    }
    translate([L - 20, 1.0, H - 3.6]) rotate([90, 0, 0]) linear_extrude(1.2) text("25", size = 2.6, halign = "right", valign = "bottom");
    translate([8, 2.2, H - 0.6]) linear_extrude(1) text("1/8", size = 2.8, halign = "center");
    translate([22, 2.2, H - 0.6]) linear_extrude(1) text("5/64", size = 2.8, halign = "center");
}
