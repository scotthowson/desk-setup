// Magnetic cable hook for the rails. The rail's flat leg is flush against the desk, so
// nothing can clip over it; instead this hook holds itself to the steel with two 10 x 3 mm
// neodymium disc magnets (glued into the pockets) and sticks anywhere on the vertical leg's
// front face. A J below holds a bundle up to 24 mm. For light cable runs; use the screw-on
// clips or the tray for anything heavy. Print on its side as rendered, PETG.

w       = 16;    // width along the rail
plate_h = 40;    // the plate against the vertical leg (which is 50.8 tall)
wall    = 2.4;
plate_t = 4;     // the plate against the steel, thick enough for the magnet pockets plus 0.8 mm of backing
loop    = 24;    // inside width of the J
drop    = 26;    // how far the J hangs below the plate
mag_d   = 10.3;  // magnet pocket, for 10 x 3 mm discs
mag_t   = 3.2;

module profile() {
    translate([0, -drop]) square([plate_t, drop + plate_h]);              // the plate on the steel, continuing down as the J's spine
    translate([0, -drop]) square([plate_t + loop + wall, wall]);          // bottom of the J
    translate([plate_t + loop, -drop]) square([wall, drop - 8]);          // up-stand, 8 mm short of the plate so cables drop in
}
difference() {
    linear_extrude(w) profile();
    // magnet pockets in the plate, opening on the steel side (x = 0), one near the top and one near the bottom
    for (y = [8, plate_h - 8]) translate([-1, y, w / 2]) rotate([0, 90, 0]) cylinder(d = mag_d, h = mag_t + 1, $fn = 32);   // 3.2 deep into a 4 mm plate
}
