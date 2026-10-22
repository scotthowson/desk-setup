// TPU pad for the ALEX foot: 52 mm disc, 4 mm thick, rounded bottom edge, with a 40 x 2 mm
// plug that presses into the pocket in the foot's floor end. One per foot. Print as saved
// (plug up), TPU 95A, 100% infill, slow. Numbers match alex-foot.scad.

pad_d = 52; pad_t = 4; plug_d = 40; plug_h = 2; r = 1.5;
hull() {
    translate([0, 0, r]) rotate_extrude($fn = 120) translate([pad_d / 2 - r, 0]) circle(r = r, $fn = 24);
    translate([0, 0, pad_t - 0.5]) cylinder(d = pad_d, h = 0.5, $fn = 120);
}
translate([0, 0, pad_t]) cylinder(d = plug_d, h = plug_h, $fn = 96);
