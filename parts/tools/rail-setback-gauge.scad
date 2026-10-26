// Rail setback gauge. The rails sit 12 cm back from the tops' front edges (the vertical leg's
// outer face on the rail line). With the top face down, hook the lip over the front edge and
// slide the rail until its vertical leg touches the gauge's end: 120.0 mm, no tape. Use two,
// one near each end, while you clamp the rail; check the middle with one. The underside
// corner of the front edge is square (the rounding is on the top face), so the lip registers
// on a true face. Labelled on both faces. Print 2, as saved (on its side), any filament.

setback = 120; w = 20; th = 6; lip = 15;
module gauge() {
    difference() {
        union() { cube([setback, w, th]); translate([-th, 0, -lip]) cube([th, w, lip + th]); }   // body on the underside, lip down the front edge
        translate([setback / 2, w / 2, th - 0.6]) linear_extrude(1) text("RAIL 120", size = 5, halign = "center", valign = "center");
        translate([setback / 2, w / 2, 0.6]) mirror([0, 0, 1]) mirror([0, 1, 0]) linear_extrude(1) text("RAIL 120", size = 5, halign = "center", valign = "center");   // reads right when turned over
    }
}
rotate([90, 0, 0]) gauge();   // on its side for printing: the L profile stands, no supports
