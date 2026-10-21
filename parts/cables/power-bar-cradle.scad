// Power bar cradle. Two of these screw to the underside of the top (behind the rail, near
// the Y60) and the power bar drops into them; a cable tie through the slots holds it if
// the bar is light. Measure your bar's width and height and set them below.
// Screws: #6 x 5/8 in into the desk top, two per cradle, 13 mm penetration (under the
// 21 mm rule). The countersinks are on the flat face that points at the floor.
// Print with the open side up, PETG or ABS.

bar_w = 60;    // power bar width
bar_h = 42;    // power bar height
slack = 1.5;
wall  = 3;
depth = 25;    // how much of the bar's length each cradle holds
tab   = 14;    // screw tabs either side, against the desk underside
hole  = 3.8;   // #6 clearance
csk   = 7.5;

W = bar_w + slack + 2 * wall;
difference() {
    union() {
        translate([-tab, 0, 0]) cube([W + 2 * tab, depth, wall]);                     // mounting plate against the underside
        cube([W, depth, bar_h + slack + wall]);                                        // the U
    }
    translate([wall, -1, wall]) cube([bar_w + slack, depth + 2, bar_h + slack + 1]);    // the bar's pocket
    for (x = [-tab / 2, W + tab / 2]) translate([x, depth / 2, -1]) {
        cylinder(d = hole, h = wall + 2, $fn = 24);
        translate([0, 0, 1 - 0.01]) cylinder(d1 = csk, d2 = hole, h = (csk - hole) / 2 + 0.01, $fn = 24);   // countersink on the underside face
    }
    translate([-1, depth / 2 - 6, bar_h + slack + wall - 10]) cube([W + 2, 12, 4]);   // cable-tie slot through both side walls, near the top
}
