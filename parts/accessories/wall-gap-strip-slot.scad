// Wall-gap strip with a cable slot. Same strip as wall-gap-strip.scad, with a 60 x 18 mm
// rounded slot over the gap so monitor, speaker and PC leads can drop straight down behind
// the desk. Put one behind the VIVO clamps for the monitor leads, one behind the Y60 for
// the PC and lamp, one behind each speaker. Print flat, top face up.

seg   = 240; gap = 31; ontop = 12; th = 3; chamf = 1.5;
lip   = 16;    // locating lip, hangs into the gap against the desk's edge; the screws go through it
lip_t = 3;
screw = 3.2;   // #4 screw clearance; countersunk on the wall side
csk   = 6.5;
slot_l = 60; slot_w = 18;

// two screw holes through the lip, into the desk's back edge, heads toward the wall
module lip_holes(x_list) { for (x = x_list) translate([x, gap - lip_t - 1, -lip / 2 - 2]) rotate([-90, 0, 0]) { cylinder(d = screw, h = lip_t + 2, $fn = 24); cylinder(d1 = csk, d2 = screw, h = (csk - screw) / 2 + 0.01, $fn = 24); } }
module profile() { polygon([[chamf, 0], [gap + ontop, 0], [gap + ontop, th - chamf], [gap + ontop - chamf, th], [0, th], [0, chamf]]); }
difference() {
    union() {
        rotate([90, 0, 90]) linear_extrude(seg) profile();
        translate([0, gap - lip_t, -lip]) cube([seg, lip_t, lip]);
    }
    lip_holes([40, seg - 40]);
    // stadium slot centred on the segment, over the gap (between the wall and the lip)
    translate([seg / 2, (gap - 2) / 2, -1]) hull() {
        translate([-(slot_l - slot_w) / 2, 0, 0]) cylinder(d = slot_w, h = th + 2, $fn = 48);
        translate([ (slot_l - slot_w) / 2, 0, 0]) cylinder(d = slot_w, h = th + 2, $fn = 48);
    }
}
