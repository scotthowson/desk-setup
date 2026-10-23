// Rail marking gauge. Sits on a face of the 2 x 2 x 3/16 in angle with its lip hanging over
// the edge; the lip's inner face bears on the edge and is the zero. Pencil in the 19 notch,
// slide along the flat leg's free edge: the screw line. Pencil in the 29 notch along the
// vertical leg's heel edge: the bolt line. The V notches are sized so a 0.8 mm pencil point
// sits exactly on 19.0 and 29.0.
//
// The file is in PRINT orientation: flat face on the bed, lip pointing up, no supports.
// In use you turn it over so the lip hangs over the edge; the labels then read correctly.
// Any filament.

lip_h  = 6;     // how far the lip hangs down over the edge
lip_t  = 3;
body_t = 3;
w      = 20;    // width along the rail
d19 = 19; d29 = 29;
notch = 2.4;    // V notch side; the V is 90 degrees
pencil_tip = 0.8;
apex = pencil_tip / 2 * sqrt(2);   // a round point of radius r sits r*sqrt(2) from the apex of a 90-degree V
over = notch * 0.7071 - apex;      // body extends past the distance by this so the V has a full mouth

module notch_at(x, y0, y1) {
    translate([x - apex + notch * 0.7071, (y0 + y1) / 2, body_t / 2]) rotate([0, 0, 45]) cube([notch, notch, body_t + 2], center = true);
}
module gauge() {   // use orientation: body on the steel face, lip hanging over the edge; lip inner face at x = 0
    difference() {
        union() {
            cube([d19 + over, w / 2, body_t]);
            translate([0, w / 2, 0]) cube([d29 + over, w / 2, body_t]);
            translate([-lip_t, 0, -lip_h]) cube([lip_t, w, lip_h + body_t]);
        }
        notch_at(d19, 0, w / 2);
        notch_at(d29, w / 2, w);
        translate([0, 0, body_t - 0.6]) labels();   // labels on the face you see in use
    }
}
module labels(top = false) {
    translate([d19 / 2, w / 4, 0]) mirror([0, top ? 0 : 1, 0]) linear_extrude(1) text("19", size = 3.6, halign = "center", valign = "center");
    translate([d29 / 2, 3 * w / 4, 0]) mirror([0, top ? 0 : 1, 0]) linear_extrude(1) text("29", size = 3.6, halign = "center", valign = "center");
    translate([24, 3 * w / 4, 0]) mirror([0, top ? 0 : 1, 0]) rotate([0, 0, 90]) linear_extrude(1) text("RAIL", size = 2.6, halign = "center", valign = "center");
}
difference() {
    translate([0, 0, body_t]) mirror([0, 0, 1]) gauge();   // flipped for printing
    translate([0, 0, body_t - 0.6]) labels(top = true);   // print-top labels read as written; the use-face ones above are mirrored in y so they read after the flip
}
