// Rail marking gauge. Hooks over any edge of the 2 x 2 x 3/16 in angle and gives a pencil
// notch at 19 mm (the screw line, hooked over the flat leg's free edge) and at 29 mm (the
// bolt line, hooked over the heel edge). Slide it along the rail with a pencil in the notch.
// Print flat, the hook pointing up. Any filament.

leg_t    = 4.8;   // angle thickness
slack    = 0.4;   // hook clearance over the leg
hook_h   = 8;     // how far the hook reaches down the leg
body_t   = 10;    // gauge thickness
w        = 30;    // width along the rail
d19      = 19;
d29      = 29;
notch    = 2.4;   // pencil notch width

module notch_at(x, y0, y1) {               // V notch cut into an end face, through the full thickness
    translate([x, (y0 + y1) / 2, body_t / 2])
        rotate([0, 0, 45]) cube([notch, notch, body_t + 2], center = true);
}

difference() {
    union() {
        // body: left half reaches 19 mm, right half reaches 29 mm from the hook's inner face
        translate([0, 0, 0]) cube([d19, w / 2, body_t]);
        translate([0, w / 2, 0]) cube([d29, w / 2, body_t]);
        // hook: a lip that drops over the edge; its inner face is x = 0
        translate([-(leg_t + slack + 3), 0, -hook_h]) cube([3, w, hook_h + body_t]);
        translate([-(leg_t + slack + 3), 0, body_t]) cube([leg_t + slack + 3, w, 0]);
        translate([-(leg_t + slack), 0, 0]) cube([leg_t + slack, w, body_t]);   // bridge over the edge
    }
    // the slot the leg sits in
    translate([-(leg_t + slack), -1, -hook_h - 1]) cube([leg_t + slack, w + 2, hook_h + 1]);
    // pencil notches on the two end faces
    notch_at(d19, 0, w / 2);
    notch_at(d29, w / 2, w);
    // labels
    translate([d19 / 2, w / 4, body_t - 0.6]) linear_extrude(1) text("19", size = 5, halign = "center", valign = "center");
    translate([d29 / 2, 3 * w / 4, body_t - 0.6]) linear_extrude(1) text("29", size = 5, halign = "center", valign = "center");
}
