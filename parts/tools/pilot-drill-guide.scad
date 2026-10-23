// Pilot drill guide with built-in depth stops. No tape flags, no measuring.
//
// How it works: the SET tower has two blind holes, 45 mm deep for the 1/8 in bit and 35 mm
// deep for the 5/64 in bit. Loosen the chuck, drop the bit in tip-first, let the chuck nose
// rest on the tower, tighten. The bit now sticks out of the chuck by exactly that much.
// Each depth puck is a bore through a block whose height is chosen so that when the chuck
// nose lands on the puck, the hole below is exactly the depth written on it. Stand the puck
// flat on the surface (or on the plate, or on the rail's flat leg), drill until the chuck
// stops. The bore also keeps the bit square. The pucks are separate pieces, printed together,
// so the chuck can overhang any side and nothing stands next to the one you are using.
//   12 PLATE 1/8 in, 12 mm: joining plates into an EKBACKEN top
//   15 LEG   1/8 in, 15 mm: OLOV and feet plates into an EKBACKEN top
//   10 EDGE  5/64 in, 10 mm: the wall-gap trim's #4 screws sideways into the raw back edge (hold the step's base against the edge, bit horizontal)
//   12 ALEX  5/64 in, 12 mm: the locating rings into the ALEX tops, and the optional ALEX feet into the bottoms
//   25 RAIL  1/8 in, 25 mm: through the 4.8 mm angle into the top, 20 mm into the wood
// Print as saved (all six pieces standing, one job), 100% infill, any filament. Never scale.
// If your chuck nose is domed rather than flat, drill one test hole in scrap and measure it.

puck_w = 18; depth_y = 10; gap = 4;
P8 = 45;   // protrusion for the 1/8 in bit, set by the tower hole
P64 = 35;  // protrusion for the 5/64 in bit (shorter bit, less sticks out)
bore_8th = 3.3; bore_64th = 2.2; set_8th = 3.5; set_64th = 2.4;
steps = [ [P8 - 12, bore_8th, "12 PLATE"], [P8 - 15, bore_8th, "15 LEG"], [P64 - 10, bore_64th, "10 EDGE"], [P64 - 12, bore_64th, "12 ALEX"], [P8 - 25, bore_8th, "25 RAIL"] ];
tower_w = 16; tower_h = P8 + 2;

module puck(h, bore, name) {
    difference() {
        cube([puck_w, depth_y, h]);
        translate([puck_w / 2, depth_y / 2, -1]) cylinder(d = bore, h = h + 2, $fn = 32);
        translate([puck_w / 2, 1.0, h - 5]) rotate([90, 0, 0]) linear_extrude(1.2) text(name, size = 2.2, halign = "center");
    }
}
difference() {   // SET tower
    cube([tower_w, depth_y, tower_h]);
    translate([tower_w / 2 - 4, depth_y / 2, tower_h - P8]) cylinder(d = set_8th, h = P8 + 1, $fn = 32);       // 45 mm setting hole
    translate([tower_w / 2 + 4, depth_y / 2, tower_h - P64]) cylinder(d = set_64th, h = P64 + 1, $fn = 32);    // 35 mm setting hole
    translate([tower_w / 2, 1.0, tower_h - 6]) rotate([90, 0, 0]) linear_extrude(1.2) text("SET", size = 3.6, halign = "center");
    translate([tower_w / 2 - 4, 1.0, tower_h - 11]) rotate([90, 0, 0]) linear_extrude(1.2) text("1/8", size = 2.4, halign = "center");
    translate([tower_w / 2 + 4, 1.0, tower_h - 11]) rotate([90, 0, 0]) linear_extrude(1.2) text("5/64", size = 2.4, halign = "center");
}
// five pucks in two rows beside the tower; separate pieces on the bed
for (i = [0 : len(steps) - 1]) translate([tower_w + gap + (i % 3) * (puck_w + gap), (i < 3 ? 0 : depth_y + gap), 0]) puck(steps[i][0], steps[i][1], steps[i][2]);
