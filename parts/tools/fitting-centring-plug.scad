// Fitting centring plug. The strut fittings have 9/16 in holes and the rails get 7/16 in
// holes, so a punch or bit put through the fitting's hole can sit anywhere in 4.8 mm of
// slack. This plug drops into the fitting's hole and has a 1/8 in bore dead centre: clamp
// the fitting on its heel mark, drop the plug in, drill the 1/8 in pilot through it, move
// the plug to the next hole. Then take the fitting off and open each pilot to 7/16 in; the
// bit follows the pilot and the hole lands on the fitting's centre, not somewhere in its
// slack. Print two. PRINT orientation: head on the bed, plug up, no supports. Any filament.

hole_d = 14.29;   // 9/16 in
fit    = 0.25;    // clearance so it drops in
plug_h = 5;       // the fitting is 5 mm thick
head_d = 20; head_t = 3;
bore   = 3.3;     // 1/8 in bit
difference() {
    union() {
        cylinder(d = head_d, h = head_t, $fn = 96);
        translate([0, 0, head_t]) cylinder(d = hole_d - fit, h = plug_h, $fn = 96);
    }
    translate([0, 0, -1]) cylinder(d = bore, h = head_t + plug_h + 2, $fn = 32);
    translate([0, 5, -0.01]) linear_extrude(0.6) text("FIT", size = 2.6, halign = "center", valign = "center");
    translate([0, -5, -0.01]) linear_extrude(0.6) text("PLUG", size = 2.6, halign = "center", valign = "center");
}
