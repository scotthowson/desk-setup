// Shared pieces for the SKÅDIS accessories. Not printed on its own.
//
// Frame for an accessory: the board's FRONT face is the plane y = 0 (the board fills
// y -5..0), x runs across the board, z up, and z = 0 is the centre of the slot the upper
// hanger uses. Every accessory is built in this frame and saved with as_print(), which lays
// it on its side (x becomes the print's z), so the hangers print with their layers running
// along the lip and nothing needs support.
//
// The hanger is IKEA's own way of holding on, proven on skadis-hook.scad: a 4.6 mm wide tab
// goes through a slot and a lip behind the board drops 5.9 mm below the slot; a short peg
// sits in the slot 40 mm below so the piece cannot tip, swing or lift by accident. Lift it
// 6 mm to take it off. Two hangers 40 mm apart (two slots of one row) carry anything heavy.
//
// Profile (u out from the front face, v up from the upper slot's centre), dropped position:
//   tab  u -5.2..0,    v -5.9..-1    rests on the slot's rounded bottom (-5.98 for a 4.6 tab)
//   lip  u -8.2..-5.2, v -11.8..-1   5.8 mm of board behind it
//   peg  u -3..0,      v -45.6..-40.6
// Raised 5.9 for fitting, the tab and lip (10.8 tall) pass the slot, whose straight height
// for a 4.6 mm part is 11.96; the peg stays inside the lower slot (usable -45.98..-34.02).

hanger_w = 4.6;
hanger_drop = 5.9;
hanger_bottom = -45.6;        // the lowest point of a hanger (the peg's bottom)
key_len = 13; key_neck = 5; key_tip = 11; key_depth = 3.5;
key_poly = [[-key_len / 2, -key_tip / 2], [-key_len / 2, key_tip / 2], [0, key_neck / 2], [key_len / 2, key_tip / 2], [key_len / 2, -key_tip / 2], [0, -key_neck / 2]];

module hanger2d() {
    translate([-5.2, -5.9]) square([5.2 + 0.01, 4.9]);
    translate([-8.2, -11.8]) square([3, 10.8]);
    translate([-3, -45.6]) square([3 + 0.01, 5]);
}
// extrude a 2D (u, v) profile along x, from x0 to x0 + w
module along_x(x0, w) multmatrix([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]]) linear_extrude(w) children();
module hanger(x) along_x(x - hanger_w / 2, hanger_w) hanger2d();
module hangers(xs) for (x = xs) hanger(x);
// a slab from the front face: u 0..t, v v0..v1, x x0..x1 (the spine that sits on the board)
module spine(x0, x1, v0, v1, t = 4) translate([x0, 0, v0]) cube([x1 - x0, t, v1 - v0]);
// lay the finished accessory on its side for printing: x up, lying on its x = 0 face
module as_print() rotate([0, -90, 0]) children();
// rounded 2D rectangle, for arms and lips
module rr(w, h, r) offset(r = r, $fn = 24) offset(delta = -r) square([w, h]);
