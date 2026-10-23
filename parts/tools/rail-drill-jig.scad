// Rail drill jig. Hooks over the flat leg's free edge of the angle (the lip's inner face is
// the zero, same as the marking gauge) and puts a 1/8 in bore exactly 19 mm in: the screw
// line. Slide it to a station line, line the scribe marks up with it, hold it down and drill
// the 1/8 in pilot through the bore. The bore keeps the bit square and it cannot wander on
// the steel. Pull the jig off and open the hole to 7/32 in: the bit follows the pilot. Nineteen
// holes, one jig. The body is 6 mm thick, enough to start the bit square.
// PRINT orientation: body on the bed, lip up, no supports. PETG (the bore lasts longer).

d19    = 19;     // screw line from the leg's free edge
body_t = 6; lip_h = 6; lip_t = 4;
w      = 30;     // along the rail
len    = 40;     // from the lip across the leg
bore   = 3.3;    // 1/8 in bit, running fit
module jig() {   // use orientation: body on the leg's top face, lip hanging over the free edge
    difference() {
        union() {
            cube([len, w, body_t]);
            translate([-lip_t, 0, -lip_h]) cube([lip_t, w, lip_h + body_t]);
        }
        translate([d19, w / 2, -1]) cylinder(d = bore, h = body_t + 2, $fn = 32);
        for (y = [-1, w - 0.6]) translate([d19 - 0.4, y, -1]) cube([0.8, 1.6, body_t + 2]);                     // sight grooves down both sides, on the bore's centre line
        translate([d19 + 9, w / 2, body_t - 0.6]) rotate([0, 0, 90]) linear_extrude(1) text("19", size = 5, halign = "center", valign = "center");
        translate([len - 6, w / 2, body_t - 0.6]) rotate([0, 0, 90]) linear_extrude(1) text("RAIL JIG  1/8 pilot", size = 3, halign = "center", valign = "center");
    }
}
translate([0, 0, body_t]) mirror([0, 0, 1]) jig();   // flipped for printing: lip up
