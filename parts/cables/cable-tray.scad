// Under-desk cable tray, a 200 mm segment. The rim screws to the underside of the top and
// the trough hangs below it, open side against the desk; bricks and slack slide in from the
// ends. Chain segments end to end. Drain slots in the floor. Four #6 x 5/8 in flat heads
// per segment, countersunk on the face that points at the floor.
// The file is in PRINT orientation: standing on one end (200 mm tall), no overhangs, no
// supports. PETG or ABS.

seg  = 200;   // length
w    = 80;    // inside width
h    = 50;    // inside depth
wall = 2.4;
tab  = 16;
hole = 3.8;
csk  = 7.5;

module tray() {   // use orientation: floor at z = 0, rim and tabs at z = h .. h + wall, against the desk
    difference() {
        union() {
            cube([seg, w + 2 * wall, h + wall]);
            translate([0, -tab, h]) cube([seg, w + 2 * wall + 2 * tab, wall]);    // tabs at the rim
        }
        translate([-1, wall, wall]) cube([seg + 2, w, h + 1]);                     // the trough, open at the rim
        for (x = [30, seg - 30], y = [-tab / 2, w + 2 * wall + tab / 2]) translate([x, y, h - 1]) {
            cylinder(d = hole, h = wall + 2, $fn = 24);
            translate([0, 0, 1 - 0.01]) cylinder(d1 = csk, d2 = hole, h = (csk - hole) / 2 + 0.01, $fn = 24);   // countersink on the tab's lower face
        }
        for (x = [20 : 40 : seg - 20]) translate([x - 4, wall + 10, -1]) cube([8, w - 20, wall + 2]);   // drain slots
    }
}
rotate([0, -90, 0]) tray();   // standing on one end for printing
