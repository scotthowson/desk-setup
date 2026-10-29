// J-hook for the SKÅDIS board (headset, cables, bags), hung the IKEA way: a tab through a
// slot with a lip behind the board, plus a short peg in the slot 40 mm below so it
// cannot tip or swing. Lift, push in, drop 6 mm; lift to take it off.
//
// Side profile, u out from the front face, v up from the upper slot's centre:
//   tab   u -5.2..0, v -5.9..-1  (rests on the slot's rounded bottom)
//   lip   u -8.2..-5.2, v -11.8..-1  (6 mm behind solid board below the slot)
//   peg   u -3..0, v -45.6..-40.6  (in the slot below; 5.9 mm drop leaves it inside)
// Raised 5.9 mm for fitting, tab and lip (v -5.9..5) pass the slot, whose straight width for a
// 4.6 mm tab is about 12 mm because of the rounded ends; the peg stays inside its slot.
//
// Print on its side, as saved, PETG, 4 walls, 40 % infill: the layers run along the arm.
//   openscad -o skadis-hook-x4.stl skadis-hook.scad

reach = 40;     // clear space from the board to the tip
tip = 14;       // tip height above the arm
w = 4.6;        // width; the tab, lip and peg must stay 4.6 to pass the 5 mm slot
arm = 7;        // arm and spine depth
spine_u = 4;    // spine thickness on the front face

module mount2d() {
    translate([-5.2, -5.9]) square([5.2 + 0.01, 4.9]);    // tab
    translate([-8.2, -11.8]) square([3, 10.8]);            // lip
    translate([-3, -45.6]) square([3 + 0.01, 5]);          // peg in the slot below
}
module body2d() {
    v0 = -48 - arm / 2;
    offset(r = 1.5, $fn = 24) offset(delta = -1.5) union() {
        translate([0, v0]) square([spine_u, 2 - v0]);                          // spine up the front
        translate([0, v0]) square([spine_u + reach + arm, arm]);               // arm
        translate([spine_u + reach, v0]) square([arm, arm + tip]);             // tip
    }
}
linear_extrude(w) { mount2d(); body2d(); }
