// ALEX foot, optional. Round foot screwed under each corner of an ALEX to lift the whole
// desk by `h`: 20, 40 or 60 mm (the desk surface becomes 85.0, 87.0 or 89.0 cm and every
// OLOV is set to 80.2 + h). Four per unit, centred 50 mm in from both edges of the bottom,
// exactly where the rings sit on top, with the same three-screw pattern, so the ALEX corner
// template marks them (turn the unit on its back, fences against the two edges). Unscrew
// the IKEA stock feet first. Three #6 x 5/8 in flat heads per foot, 12 mm into the panel.
// A TPU pad (alex-foot-pad.scad) presses into the bottom so it neither slips nor scratches.
// Render each height:  openscad -D h=60 -o alex-foot-60.stl alex-foot.scad
// PRINT orientation: flange on the bed, column up, no supports. PETG, 4 walls, 40% infill.

h = 60;                        // total height from the floor to the ALEX, pad included
flange_d = 75; flange_t = 4;   // same flange as the locating ring
screw_r = 33; screw = 3.6; csk = 7.0; n_screws = 3;
col_top = 40; col_bot = 36;    // round column, slight taper
pad_t = 4; plug_d = 30; plug_h = 2;   // the TPU pad's plug fits this pocket
col_h = h - flange_t - pad_t;
assert(col_h >= 10, "h too small for a column");

difference() {
    union() {
        cylinder(d = flange_d, h = flange_t, $fn = 120);
        translate([0, 0, flange_t]) cylinder(d1 = col_top + 6, d2 = col_top, h = 3, $fn = 96);                     // fillet cone into the flange
        translate([0, 0, flange_t]) cylinder(d1 = col_top, d2 = col_bot, h = col_h, $fn = 96);
    }
    for (i = [0 : n_screws - 1]) rotate([0, 0, i * 360 / n_screws + 45]) translate([screw_r, 0, 0]) {
        translate([0, 0, -1]) cylinder(d = screw, h = flange_t + 2, $fn = 24);
        translate([0, 0, flange_t - (csk - screw) / 2]) cylinder(d1 = screw, d2 = csk, h = (csk - screw) / 2 + 0.01, $fn = 24);   // countersink on the floor side
    }
    translate([0, 0, h - pad_t - plug_h - 0.2]) cylinder(d = plug_d + 0.4, h = plug_h + 1, $fn = 64);              // pad pocket
    translate([0, 0, flange_t - 0.6]) rotate([0, 0, 225]) translate([30, 0, 0]) rotate([0, 0, 90]) linear_extrude(1) text(str(h / 10, " cm"), size = 3.5, halign = "center", valign = "center");   // height, engraved on the floor side of the flange between two screws
}
