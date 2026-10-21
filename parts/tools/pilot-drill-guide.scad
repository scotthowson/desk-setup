// Pilot drill guide with built-in depth stops. No tape flags, no measuring.
//
// How it works: the SET tower has two blind holes, 45 mm deep for the 1/8 in bit and 35 mm
// deep for the 5/64 in bit. Loosen the chuck, drop the bit in tip-first, let the chuck nose
// rest on the tower, tighten. The bit now sticks out of the chuck by exactly that much.
// Each step is a bore at a height chosen so that when the chuck nose lands on the step, the
// hole below is exactly the depth written on it. Hold the step flat on the surface (or on the
// plate, or on the rail's flat leg), drill until the chuck stops. The bore also keeps the bit
// square.
//   12       1/8 in, 12 mm: joining plates
//   15       1/8 in, 15 mm: OLOV and feet plates
//   25 RAIL  1/8 in, 25 mm: through the 4.8 mm angle into the top, 20 mm into the wood
//   12 RING  5/64 in, 12 mm: the locating rings into the ALEX tops
// Print standing on its base, 100% infill, any filament. Fits any drill whose chuck nose is
// flat; if yours has a domed nose, measure the first hole and shim the step with tape.

step_w = 16; depth_y = 18;
P8 = 45;   // protrusion for the 1/8 in bit, set by the tower hole
P64 = 35;  // protrusion for the 5/64 in bit (shorter bit, less sticks out)
bore_8th = 3.3; bore_64th = 2.2; set_8th = 3.5; set_64th = 2.4;
steps = [ [P8 - 12, bore_8th, "12"], [P8 - 15, bore_8th, "15"], [P8 - 25, bore_8th, "25 RAIL"], [P64 - 12, bore_64th, "12 RING"] ];
tower_h = P8 + 2;

difference() {
    union() {
        translate([0, 0, 0]) cube([step_w, depth_y, tower_h]);                                   // SET tower
        for (i = [0 : len(steps) - 1]) translate([step_w * (i + 1), 0, 0]) cube([step_w, depth_y, steps[i][0]]);
    }
    translate([step_w / 2 - 4, depth_y / 2, tower_h - P8]) cylinder(d = set_8th, h = P8 + 1, $fn = 32);       // 45 mm setting hole
    translate([step_w / 2 + 4, depth_y / 2, tower_h - P64]) cylinder(d = set_64th, h = P64 + 1, $fn = 32);    // 35 mm setting hole
    for (i = [0 : len(steps) - 1]) translate([step_w * (i + 1.5), depth_y / 2, -1]) cylinder(d = steps[i][1], h = steps[i][0] + 2, $fn = 32);
    // labels on the front face of each step and the tower
    translate([step_w / 2, 1.0, tower_h - 6]) rotate([90, 0, 0]) linear_extrude(1.2) text("SET", size = 3.6, halign = "center");
    translate([step_w / 2 - 4, 1.0, tower_h - 11]) rotate([90, 0, 0]) linear_extrude(1.2) text("1/8", size = 2.4, halign = "center");
    translate([step_w / 2 + 4, 1.0, tower_h - 11]) rotate([90, 0, 0]) linear_extrude(1.2) text("5/64", size = 2.4, halign = "center");
    for (i = [0 : len(steps) - 1]) translate([step_w * (i + 1.5), 1.0, steps[i][0] - 6]) rotate([90, 0, 0]) linear_extrude(1.2) text(steps[i][2], size = 2.8, halign = "center");
}
