// Foot height gauge. Every one of the eight 4 in feet has to be wound out to exactly 10.2 cm
// from the plate face that touches the top to the bottom of the pad, so the underside of the
// desk ends at 80.2 and the tops sit flat. Instead of measuring eight times: stand the foot on
// its pad, slide this C over it from the side, and wind the pad until the gauge just slides on
// with no rock. The inside height is 102.0 mm. Print flat, any filament, 100% infill.

inside_h = 102.0; inside_w = 64;   // the 59.5 mm plate passes through
arm = 6; th = 5;
difference() {
    cube([inside_w + 2 * arm, inside_h + 2 * arm, th]);
    translate([arm, arm, -1]) cube([inside_w + 1, inside_h, th + 2]);   // open on the +x side
    translate([arm / 2, arm + inside_h / 2, th - 0.6]) rotate([0, 0, 90]) linear_extrude(1) text("EKB FOOT 10.2 cm", size = 2.6, halign = "center", valign = "center");
}
