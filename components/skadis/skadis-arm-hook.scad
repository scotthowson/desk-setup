// Wide hooks for the SKÅDIS board, on the shared hanger (skadis-lib.scad).
//   kind = "headset"     60 wide, two hangers, 55 mm reach, the arm crowned 9 mm across its
//                        width so a headband sits centred and the pads hang free. x1
//   kind = "controller"  24 wide, one hanger, 60 mm reach, 25 mm tip: the pad goes between
//                        the grips and the controller hangs face out. x1
// Print on the side, as saved, PETG, 4 walls, 30 % infill, no supports.
//   openscad -D 'kind="headset"' -o skadis-headset-hook-x1.stl skadis-arm-hook.scad

include <skadis-lib.scad>

kind = "headset";
W     = kind == "headset" ? 60 : 24;
reach = kind == "headset" ? 55 : 60;
tip   = kind == "headset" ? 22 : 25;
crown = kind == "headset" ? 9 : 0;     // how much the arm's centre stands above its edges
arm = 7; spine_t = 4;
v_arm = -52;                            // the arm's top at the edges (below the lower peg)
hx = kind == "headset" ? [W / 2 - 20, W / 2 + 20] : [W / 2];

R = crown > 0 ? (pow(W / 2, 2) + crown * crown) / (2 * crown) : 0;   // crown circle through the edges
module crowned_arm() {   // the arm as a curved plate, constant 7 thick, running out along y
    if (crown > 0) intersection() {
        translate([W / 2, 0, v_arm + crown - R]) rotate([-90, 0, 0]) difference() { cylinder(r = R, h = spine_t + reach, $fn = 240); translate([0, 0, -1]) cylinder(r = R - arm, h = spine_t + reach + 2, $fn = 240); }
        translate([0, 0, v_arm - arm - 1]) cube([W, spine_t + reach, arm + crown + 2]);
    } else translate([0, 0, v_arm - arm]) cube([W, spine_t + reach, arm]);
}
module piece() {
    hangers(hx);
    spine(0, W, v_arm - arm - crown, 8, spine_t);
    crowned_arm();
    translate([0, spine_t + reach - arm, v_arm - arm - crown]) cube([W, arm, arm + crown + tip]);   // the tip, full width
}
as_print() piece();
