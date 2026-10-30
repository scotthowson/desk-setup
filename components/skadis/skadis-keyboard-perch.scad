// Keyboard perch, a pair: two 60 mm ledges that park a keyboard on the board, on edge,
// leaning back against it (the NuPhy Air75 V2 when the controller is out). Each ledge is
// 30 deep with a 16 mm lip, so a board up to 26 mm thick sits in it; two hangers each.
// Hang the two in one slot row, 5 columns apart (200 mm) for a 75 % keyboard, further for
// a full size. Print on the side, as saved, PETG, 4 walls, 30 % infill. x2 (one pair)
//   openscad -o skadis-keyboard-perch-x2.stl skadis-keyboard-perch.scad

include <skadis-lib.scad>

W = 60; D = 30; lip = 16; t = 6; spine_t = 4; gusset = 24;
v_top = -50;
hx = [W / 2 - 20, W / 2 + 20];

module piece() {
    hangers(hx);
    spine(0, W, v_top - t - gusset, 8, spine_t);
    translate([0, 0, v_top - t]) cube([W, spine_t + D, t]);
    translate([0, spine_t + D - 4, v_top - t]) cube([W, 4, t + lip]);
    translate([W / 2 - 2, 0, 0]) rotate([90, 0, 90]) linear_extrude(4)
        polygon([[spine_t - 0.01, v_top - t + 0.01], [spine_t + gusset, v_top - t + 0.01], [spine_t - 0.01, v_top - t - gusset]]);
}
as_print() piece();
