// Rail marking gauge. Hooks over any edge of the 2 x 2 x 3/16 in angle and gives a pencil
// notch at 19 mm (the screw line, hooked over the flat leg's free edge) and at 29 mm (the
// bolt line, hooked over the heel edge). Slide it along the rail with a pencil in the notch.
//
// The file is in PRINT orientation: flat face on the bed, hook pointing up, no supports.
// In use you turn it over so the hook drops over the edge; the labels then read correctly.
// Any filament.

leg_t  = 4.8;   // angle thickness
slack  = 0.4;   // hook clearance over the leg
hook_h = 4;     // how far the hook reaches down the leg (the leg edge is 4.8 mm thick)
body_t = 5;     // gauge thickness (halved to save material)
w      = 30;    // width along the rail
d19    = 19;
d29    = 29;
notch  = 2.4;   // pencil notch width
pencil_tip = 0.8;   // the pencil's point diameter; the V's apex sits this far short of the distance so the pencil centre lands on it

module notch_at(x, y0, y1) {               // V notch cut into an end face, through the full thickness, apex at x - pencil_tip/2
    translate([x - pencil_tip / 2 + notch * 0.7071, (y0 + y1) / 2, body_t / 2])
        rotate([0, 0, 45]) cube([notch, notch, body_t + 2], center = true);
}
module gauge() {   // use orientation: body on the leg's face, hook hanging over the edge below
    difference() {
        union() {
            cube([d19, w / 2, body_t]);                                             // left half reaches 19 mm from the hook's inner face
            translate([0, w / 2, 0]) cube([d29, w / 2, body_t]);                    // right half reaches 29 mm
            translate([-(leg_t + slack + 3), 0, -hook_h]) cube([3, w, hook_h + body_t]);   // the hook's lip
            translate([-(leg_t + slack), 0, 0]) cube([leg_t + slack, w, body_t]);  // bridge over the edge
        }
        notch_at(d19, 0, w / 2);
        notch_at(d29, w / 2, w);
        translate([d19 / 2, w / 4, body_t - 0.6]) linear_extrude(1) text("19", size = 5, halign = "center", valign = "center");
        translate([d29 / 2, 3 * w / 4, body_t - 0.6]) linear_extrude(1) text("29", size = 5, halign = "center", valign = "center");
    }
}
translate([0, 0, body_t]) mirror([0, 0, 1]) gauge();   // flipped for printing
