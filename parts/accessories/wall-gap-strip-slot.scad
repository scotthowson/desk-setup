// Wall-gap strip with a cable slot: the plain strip with a 60 x 18 mm rounded slot over the
// gap so monitor, speaker and PC leads drop straight down behind the desk. Three places; see
// the README cut list. Everything else is in wall-gap-common.scad.

include <wall-gap-common.scad>
seg = 240; slot_l = 60; slot_w = 18;
translate([0, 0, th]) mirror([0, 0, 1]) difference() {
    plain_strip(seg);
    translate([seg / 2, (gap - lip_t) / 2, -1]) hull() {
        translate([-(slot_l - slot_w) / 2, 0, 0]) cylinder(d = slot_w, h = th + 2, $fn = 48);
        translate([ (slot_l - slot_w) / 2, 0, 0]) cylinder(d = slot_w, h = th + 2, $fn = 48);
    }
}
