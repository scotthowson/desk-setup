// ALEX foot, optional. Solid round foot screwed under each corner of an ALEX to lift the
// whole desk by `h`: 20, 40 or 60 mm (the desk surface becomes 85.0, 87.0 or 89.0 cm and
// every OLOV is set to 80.2 + h). Four per unit, centred 50 mm in from both edges of the
// bottom, exactly where the rings sit on top. The three screws go up through the column
// itself: each sits at the top of a 10 mm well bored from the floor end, so the screw head
// bears on 6 mm of solid plastic in the core of the foot and nothing can pry. Drive them
// with a long screwdriver or a bit holder down the well. The ALEX corner template marks the
// centre and the three screws (its inner holes) with the unit on its back. Unscrew the IKEA
// stock feet first. Three #6 x 5/8 in flat heads per foot, 10 mm into the panel.
// A TPU pad (alex-foot-pad.scad) presses into the floor end so it neither slips nor scratches.
// Render each height:  openscad -D h=60 -o alex-foot-60.stl alex-foot.scad
// PRINT orientation: top face (the one against the ALEX) on the bed, wells open upward, no
// supports. PETG, 5 walls, 50% infill (the wells make it mostly wall anyway).

h = 60;                        // total height from the floor to the ALEX, pad included
col_top = 56; col_bot = 52;    // round column, slight taper toward the floor
screw_r = 14.5; n_screws = 3; screw = 3.6; csk = 7.0;   // screw circle, same angles as the ring pattern so the template carries both
roof = 6;                      // solid plastic between the screw head and the ALEX
well_d = 10;                   // clears a 6 mm screwdriver shank or a 1/4 in bit holder
pad_t = 4; plug_d = 40; plug_h = 2;   // the TPU pad's plug fits this pocket
col_h = h - pad_t;
assert(col_h >= 14, "h too small");

difference() {
    cylinder(d1 = col_top, d2 = col_bot, h = col_h, $fn = 120);
    for (i = [0 : n_screws - 1]) rotate([0, 0, i * 360 / n_screws + 45]) translate([screw_r, 0, 0]) {
        translate([0, 0, -1]) cylinder(d = screw, h = roof + 2, $fn = 24);                                   // screw hole through the roof
        translate([0, 0, roof]) cylinder(d1 = screw, d2 = well_d, h = (well_d - screw) / 2, $fn = 32);      // countersink at the well floor
        translate([0, 0, roof + (well_d - screw) / 2 - 0.01]) cylinder(d = well_d, h = col_h, $fn = 32);    // well, open at the floor end
    }
    translate([0, 0, col_h - plug_h - 0.2]) cylinder(d = plug_d + 0.4, h = plug_h + 1, $fn = 96);           // pad pocket
    translate([0, 0, col_h / 2]) rotate([90, 0, 180 + 45]) translate([0, 0, col_top / 2 - 0.6]) linear_extrude(2) text(str("ALEX ", h / 10, " cm"), size = 3.5, halign = "center", valign = "center");   // height on the side, between two wells
}
