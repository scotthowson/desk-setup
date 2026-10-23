// Locating ring for the ALEX feet.
// Screws to the ALEX top; the 5 cm pad of each adjustable foot drops into the bore and
// bears directly on the ALEX laminate through the open bottom. The ring only stops the
// desk sliding sideways on the cabinets. Eight needed (four per ALEX).
//
// Print flange-down, flat on the bed, no supports. PETG or ABS, 3+ perimeters, 30% infill.
// Render:  openscad -o foot-ring.stl foot-ring.scad

pad_d      = 50;    // measured pad diameter, mm. Re-measure yours with calipers before printing.
clearance  = 2.0;   // added to the pad: bore 52 for a 50 pad, so a ring placed on a pencil trace of the pad (within 1 mm) still takes it
wall       = 3;     // ring wall thickness
ring_h     = 10;    // ring height above the flange
flange_t   = 2.5;   // flange thickness (the screws go through this)
flange_od  = 75;    // flange outside diameter
screw_hole = 3.8;   // clearance for a #6 screw
csk_d      = 7.0;   // countersink diameter at the surface (#6 flat head); 7.0 keeps 1 mm of flange outside it
n_screws   = 3;
lead_in    = 1.0;   // chamfer at the top of the bore so the pad finds its way in

bore_d  = pad_d + clearance;      // 52 for a 50 mm pad
ring_od = bore_d + 2 * wall;      // 58
screw_r = (ring_od / 2 + flange_od / 2) / 2;   // screws centred in the flange band
$fn = 128;

difference() {
    union() {
        cylinder(d = flange_od, h = flange_t);
        cylinder(d = ring_od, h = flange_t + ring_h);
    }
    // name on the flange, between two screws
    rotate([0, 0, 150]) translate([screw_r, 0, flange_t - 0.6]) rotate([0, 0, 90]) linear_extrude(1) text("ALEX RING", size = 2.8, halign = "center", valign = "center");
    // the open bore, right through
    translate([0, 0, -1]) cylinder(d = bore_d, h = flange_t + ring_h + 2);
    // lead-in chamfer at the top of the bore
    translate([0, 0, flange_t + ring_h - lead_in])
        cylinder(d1 = bore_d, d2 = bore_d + 2 * lead_in, h = lead_in + 0.01);
    // countersunk screw holes
    for (i = [0 : n_screws - 1])
        rotate([0, 0, i * 360 / n_screws + 90])
            translate([screw_r, 0, 0]) {
                translate([0, 0, -1]) cylinder(d = screw_hole, h = flange_t + 2, $fn = 48);
                csk_depth = (csk_d - screw_hole) / 2;           // 90 degree countersink
                translate([0, 0, flange_t - csk_depth])
                    cylinder(d1 = screw_hole, d2 = csk_d, h = csk_depth + 0.01, $fn = 48);
            }
}
