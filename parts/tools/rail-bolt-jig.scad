// Rail bolt jig. Hooks over the heel of the angle (the top corner of the vertical leg, the
// same datum as template T7) and puts a 1/8 in bore exactly 29 mm down the vertical leg's
// outer face: the bolt line of the corner fittings. Mark each station along the heel with the
// tape (rail A from the wall end: 43.7, 48.6, 54.9, 59.8 cm; rail B from the corner end: 2.9,
// 7.8 cm), slide the jig to the mark using the sight grooves, hold it down and drill the 1/8 in
// pilot through the bore. Pull the jig off and open the hole to 7/16 in: the bit follows the
// pilot. Six holes, one jig; T7 is the paper check of the same positions. Body 6 mm, bore 3.5.
// PRINT orientation: body on the bed, lip up, no supports. PETG (the bore lasts longer).

d29    = 29;     // bolt line from the heel (facts.json steel.bolt_line_below_heel)
body_t = 6; lip_h = 8; lip_t = 4;
w      = 24;     // along the rail
len    = 40;     // from the heel down the leg (the leg is 50.8)
bore   = 3.5;    // 1/8 in bit (3.18) + 0.3, prints as a running fit
f = "DejaVu Sans:style=Bold";
module jig() {   // use orientation: body on the vertical leg's outer face, lip over the heel onto the flat leg's top face
    difference() {
        union() {
            cube([len, w, body_t]);
            translate([-lip_t, 0, -lip_h]) cube([lip_t, w, lip_h + body_t]);
        }
        translate([d29, w / 2, -1]) cylinder(d = bore, h = body_t + 2, $fn = 32);
        for (y = [-1, w - 0.6]) translate([d29 - 0.4, y, -1]) cube([0.8, 1.6, body_t + 2]);   // sight grooves down both sides, on the bore's centre line
        translate([0, 0, body_t - 1.0]) labels();   // labels on the face you see in use
    }
}
module labels(top = false) {   // bold, 4.5-5 mm, 1 mm deep; run a marker over the engraving if it reads poorly
    translate([8, w / 2, 0]) mirror([0, top ? 0 : 1, 0]) rotate([0, 0, 90]) linear_extrude(1.2) text("BOLT", size = 4.5, font = f, halign = "center", valign = "center");
    translate([15, w / 2, 0]) mirror([0, top ? 0 : 1, 0]) rotate([0, 0, 90]) linear_extrude(1.2) text("1/8", size = 4.5, font = f, halign = "center", valign = "center");
    translate([35.5, w / 2, 0]) mirror([0, top ? 0 : 1, 0]) rotate([0, 0, 90]) linear_extrude(1.2) text("29", size = 5, font = f, halign = "center", valign = "center");
}
difference() {
    translate([0, 0, body_t]) mirror([0, 0, 1]) jig();   // flipped for printing
    translate([0, 0, body_t - 1.0]) labels(top = true);   // print-top labels read as written; the use-face ones above are mirrored in y so they read after the flip
}
