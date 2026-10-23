// Edge T-square. The head hooks over any edge (a desk top, an ALEX top, the steel angle);
// the blade lies on the surface at a right angle to that edge. Punch holes down the blade
// at the offsets this build uses, measured from the edge:
//   50  ring centres on the ALEX tops            (5 cm in)
//   85  feet centres on the desk tops            (8.5 cm in), with the plate's four screw holes round it
//  100  OLOV legs L2 to L6                       (10 cm in)
//  150  OLOV leg L1                              (15 cm from the side-wall end)
// Slide the head along the edge to the station you measured with the tape, then punch
// through the hole. The blade's straight edge also squares the station lines across a rail.
//
// The file is in PRINT orientation: flat face on the bed, lip pointing up, no supports.
// In use you turn it over: the lip hangs down over the edge and the labels read correctly.
// 162 x 110 mm. Any filament.

head_l = 110; head_w = 20;
t      = 3;                               // plate thickness, head and blade alike, so the tool lies flat (halved to save material; 3 mm still guides a scriber)
lip_h  = 6;   lip_t  = 4;                 // the lip that hooks over the edge; its inner face is the zero line
blade_l = 162; blade_w = 24;
hole_d  = 4;                              // fits a scriber, a pencil tip or a 1/8 in bit
plate_hole_spacing = 36.6;                // the feet plates' screw holes, centre to centre: measured 22 Oct 2026 (59.5 mm plate, 5.4 mm holes)
pad = 48;                                 // square pad round the 85 mm hole (holes at ±18.3)

module tool() {   // use orientation: plate at z 0..t on the surface, lip hanging below
    difference() {
        union() {
            translate([-lip_t, -head_l / 2, 0]) cube([lip_t + head_w, head_l, t]);           // head
            translate([-lip_t, -head_l / 2, -lip_h]) cube([lip_t, head_l, lip_h]);           // lip
            translate([0, -blade_w / 2, 0]) cube([blade_l, blade_w, t]);                     // blade, from the zero line outward
            translate([85 - pad / 2, -pad / 2, 0]) cube([pad, pad, t]);                      // pad for the foot plate pattern
        }
        for (x = [50, 85, 100, 150]) translate([x, 0, -1]) cylinder(d = hole_d, h = t + 2, $fn = 24);
        for (sx = [-1, 1], sy = [-1, 1])
            translate([85 + sx * plate_hole_spacing / 2, sy * plate_hole_spacing / 2, -1]) cylinder(d = hole_d, h = t + 2, $fn = 24);
        translate([head_w, -0.45, t - 0.5]) cube([blade_l - head_w, 0.9, 1]);                // scribe line down the blade's centre
        translate([0, 0, t - 0.6]) labels();   // labels on the face you see in use
    }
}
module labels(top = false) {
    module label(x, s, side, al = "left") { translate([x + (al == "left" ? 3.5 : -3.5), side > 0 ? 5.8 : -7.2, 0]) mirror([0, top ? 0 : 1, 0]) linear_extrude(1) text(s, size = 3.6, halign = al, valign = "center"); }
    label(50, "50 ALEX ring", 1); label(100, "100 leg", 1); label(150, "150 L1", 1, "right"); label(85, "85 foot + plate holes 36.6", -1);
    translate([head_w / 2 + 2, 0, 0]) mirror([0, top ? 0 : 1, 0]) rotate([0, 0, 90]) linear_extrude(1) text("edge", size = 4, halign = "center", valign = "center");
    translate([head_w / 2 + 2, 36, 0]) mirror([0, top ? 0 : 1, 0]) rotate([0, 0, 90]) linear_extrude(1) text("EKB T-SQUARE", size = 3.6, halign = "center", valign = "center");
}
difference() {
    translate([0, 0, t]) mirror([0, 0, 1]) tool();   // flipped for printing
    translate([0, 0, t - 0.6]) labels(top = true);   // print-top labels read as written; the use-face ones above are mirrored in y so they read after the flip
}
