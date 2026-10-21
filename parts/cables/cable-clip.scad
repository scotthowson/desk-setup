// Screw-on cable clip for the underside of the top: a saddle for one or two cables with a
// single countersunk #6 x 5/8 in screw (13 mm into the top). Two sizes in one file: set
// `bundle` to the cable diameter you want to hold. The cable pushes in past the lip, which
// flexes 1.5 mm. The file is in PRINT orientation: profile face down, no overhangs. PETG.

bundle = 8;     // cable or bundle diameter: 8 for a monitor lead, 14 for a small bundle
wall   = 2.4;
w      = 10;    // clip width along the cable
hole   = 3.8;
csk    = 7.5;
foot   = 12;    // screw foot length

module clip() {
  difference() {
    union() {
        translate([-foot, 0, 0]) cube([foot, w, wall]);                               // screw foot, against the underside
        translate([0, 0, 0]) cube([bundle + 2 * wall, w, wall]);                      // top of the saddle
        translate([0, 0, 0]) cube([wall, w, bundle + wall]);                          // one side
        translate([bundle + wall, 0, 0]) cube([wall, w, bundle + 2 * wall]);          // other side, longer, with a lip
        translate([bundle + wall - 1.5, 0, bundle + wall]) cube([1.5 + wall, w, wall]);  // the lip that keeps the cable in
    }
    translate([-foot / 2, w / 2, -1]) { cylinder(d = hole, h = wall + 2, $fn = 24); translate([0, 0, 1 - 0.01]) cylinder(d1 = csk, d2 = hole, h = (csk - hole) / 2 + 0.01, $fn = 24); }
  }
}
translate([0, w, 0]) rotate([90, 0, 0]) clip();   // profile face down for printing
