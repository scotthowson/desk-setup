// Fitting slot plug. The strut fittings have 21 x 12 mm slots (measured 23 Oct 2026) and the
// rails get 7/16 in holes, so a bolt could sit anywhere along 11.5 mm of slot. This plug fills
// the slot and has a 1/8 in bore dead centre: clamp the fitting on its heel mark, drop the plug
// into each slot, drill the 1/8 in pilot through it, move the plug to the next slot. Then take
// the fitting off and open each pilot to 7/16 in; the bit follows the pilot and every hole lands
// on a slot centre, 29.15 and 78.45 mm from the fitting's heel. Print two. PRINT orientation:
// head on the bed, plug up, no supports. Any filament.

slot_l = 21; slot_w = 12;   // measured
fit    = 0.3;               // clearance so it drops in
plug_h = 5;                 // the fitting is 5 mm thick
head_l = 30; head_w = 18; head_t = 3;
bore   = 3.5;               // 1/8 in bit (3.18) + 0.3, prints as a running fit
module stadium(l, w, h) { hull() { for (x = [-(l - w) / 2, (l - w) / 2]) translate([x, 0, 0]) cylinder(d = w, h = h, $fn = 48); } }
difference() {
    union() {
        stadium(head_l, head_w, head_t);
        translate([0, 0, head_t]) stadium(slot_l - fit, slot_w - fit, plug_h);
    }
    translate([0, 0, -1]) cylinder(d = bore, h = head_t + plug_h + 2, $fn = 32);
    translate([0, 6, -0.01]) mirror([1, 0, 0]) linear_extrude(0.6) text("FIT", size = 2.6, halign = "center", valign = "center");
    translate([0, -6, -0.01]) mirror([1, 0, 0]) linear_extrude(0.6) text("PLUG", size = 2.6, halign = "center", valign = "center");
}
