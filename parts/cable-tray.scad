// Under-desk cable tray, a 200 mm segment. Screws to the underside of the top behind the
// rail (it fits in the 35 cm between the rail and the wall edge, or anywhere under the
// wings) and takes the power bricks and slack. Chain segments end to end. Open top, drain
// slots in the floor so dust does not collect, two screw tabs.
// Screws: #6 x 5/8 in into the desk top, 13 mm penetration. Print open side up, PETG or ABS.

seg  = 200;   // length
w    = 80;    // inside width
h    = 50;    // inside depth
wall = 2.4;
tab  = 16;
hole = 3.8;
csk  = 7.5;

difference() {
    union() {
        cube([seg, w + 2 * wall, h + wall]);
        translate([0, -tab, 0]) cube([seg, w + 2 * wall + 2 * tab, wall]);    // tabs run the full length, screw anywhere along them
    }
    translate([-1, wall, wall]) cube([seg + 2, w, h + 1]);                     // the trough
    for (x = [30, seg - 30], y = [-tab / 2, w + 2 * wall + tab / 2]) translate([x, y, -1]) {
        cylinder(d = hole, h = wall + 2, $fn = 24);
        translate([0, 0, 1 - 0.01]) cylinder(d1 = csk, d2 = hole, h = (csk - hole) / 2 + 0.01, $fn = 24);
    }
    for (x = [20 : 40 : seg - 20]) translate([x - 4, wall + 10, -1]) cube([8, w - 20, wall + 2]);   // drain slots
}
