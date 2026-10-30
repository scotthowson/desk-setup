// Cable comb for the SKÅDIS board: five 8 mm fingers with a 6.5 mm neck, so a charging lead
// clips in from the front and stays. 100 wide, two hangers. Print on the side, as saved,
// PETG, 4 walls, 30 %. x1
//   openscad -o skadis-cable-comb-x1.stl skadis-cable-comb.scad

include <skadis-lib.scad>

W = 100; D = 26; t = 10; spine_t = 4; n = 5; hole = 8; neck = 6.5;
v_top = -50;
hx = [W / 2 - 20, W / 2 + 20];

module piece() {
    difference() {
        union() {
            hangers(hx);
            spine(0, W, v_top - t, 8, spine_t);
            translate([0, 0, v_top - t]) cube([W, spine_t + D, t]);
        }
        for (i = [0 : n - 1]) let (x = W / (2 * n) * (2 * i + 1)) {
            translate([x, spine_t + D - 11, v_top - t - 1]) cylinder(d = hole, h = t + 2, $fn = 32);
            translate([x - neck / 2, spine_t + D - 11, v_top - t - 1]) cube([neck, 12, t + 2]);
        }
    }
}
as_print() piece();
