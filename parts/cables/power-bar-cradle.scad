// Power bar cradle. Two of these screw to the underside of the top near the Y60; the bar
// slides in endwise and sits in the U, open side against the desk, and a cable tie through
// the rim notches keeps it there. Measure your bar's width and height and set them below.
// Two #6 x 5/8 in flat heads per cradle, countersunk on the face that points at the floor.
// The file is in PRINT orientation: the U profile face down (25 mm tall), no supports. PETG or ABS.

bar_w = 60;    // power bar width
bar_h = 42;    // power bar height
slack = 1.5;
wall  = 3;
depth = 25;    // how much of the bar's length each cradle holds
tab   = 14;    // screw tabs either side, at the rim, against the desk underside
hole  = 3.8;
csk   = 7.5;

W = bar_w + slack + 2 * wall; H = bar_h + slack + wall;
module cradle() {   // use orientation: U floor at z = 0, rim and tabs at z = H - wall .. H against the desk
    difference() {
        union() {
            cube([W, depth, H]);                                                    // the U
            translate([-tab, 0, H - wall]) cube([W + 2 * tab, depth, wall]);         // tabs at the rim
        }
        translate([wall, -1, wall]) cube([bar_w + slack, depth + 2, H]);             // the bar's pocket, open at the rim
        for (x = [-tab / 2, W + tab / 2]) translate([x, depth / 2, H - wall - 1]) {
            cylinder(d = hole, h = wall + 2, $fn = 24);
            translate([0, 0, 1 - 0.01]) cylinder(d1 = csk, d2 = hole, h = (csk - hole) / 2 + 0.01, $fn = 24);   // countersink on the tab's lower face
        }
        translate([-1, depth / 2 - 6, H - 5]) cube([W + 2, 12, 6]);                 // cable-tie notches at the rim, both walls
    }
}
rotate([90, 0, 0]) cradle();   // U profile face down for printing: 25 mm tall, no overhangs
