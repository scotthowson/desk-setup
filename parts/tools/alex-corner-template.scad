// ALEX corner template. Drop it over any corner of an ALEX top: the two fences sit against
// the two edges, and the holes give you the ring centre (5 cm in from both edges) and the
// ring's three screw holes in one go. Same template for all eight corners; just turn it.
// Turned over against the two edges of the BOTTOM, it marks the optional ALEX feet
// (accessories/alex-foot.scad): same centre, and their three screws are the inner holes.
// The ring's outline is engraved so you can see it will land where you expect.
//
// The file is in PRINT orientation: flat face on the bed, fences pointing up, no supports.
// In use you turn it over so the fences hang down against the ALEX edges and the labels
// face you. Any filament.

inset   = 50;      // ring centre from each edge
plate_t = 2.5;   // halved to save material
size    = 92;      // square plate
fence_h = 6; fence_t = 4;
centre_d = 2.5;    // scriber only
bit     = 2.3;     // 5/64 in bit (1.98) + 0.3 for the #6 screws, prints as a running fit
screw_r = 33;      // the ring's screw circle, fixed at 33 in structure/foot-ring.scad
n_screws = 3;
foot_r  = 14.5;      // the ALEX foot's screw circle (accessories/alex-foot.scad), same angles
ring_od = 58; ring_bore = 52;

module ring_line(d) { translate([inset, inset, plate_t - 0.5]) difference() { cylinder(d = d + 0.9, h = 1, $fn = 96); translate([0, 0, -1]) cylinder(d = d - 0.9, h = 3, $fn = 96); } }
module template() {   // use orientation: plate on the ALEX top, fences hanging down over two edges
    difference() {
        union() {
            cube([size, size, plate_t]);
            translate([-fence_t, -fence_t, -fence_h]) cube([size + fence_t, fence_t, fence_h + plate_t]);   // fence along one edge
            translate([-fence_t, -fence_t, -fence_h]) cube([fence_t, size + fence_t, fence_h + plate_t]);   // fence along the other
        }
        translate([inset, inset, -1]) cylinder(d = centre_d, h = plate_t + 2, $fn = 24);               // ring centre, scriber
        for (i = [0 : n_screws - 1])
            translate([inset, inset, -1]) rotate([0, 0, i * 360 / n_screws + 45])
                translate([screw_r, 0, 0]) cylinder(d = bit, h = plate_t + 2, $fn = 32);              // ring screws, 5/64 in drill holes
        for (i = [0 : n_screws - 1])
            translate([inset, inset, -1]) rotate([0, 0, i * 360 / n_screws + 45])
                translate([foot_r, 0, 0]) cylinder(d = bit, h = plate_t + 2, $fn = 32);               // ALEX foot screws (underside), 5/64 in drill holes
        ring_line(ring_od); ring_line(ring_bore);
        translate([0, 0, plate_t - 0.6]) labels();   // labels on the face you see in use
    }
}
module labels(top = false) {
    translate([inset, 11.6, 0]) mirror([0, top ? 0 : 1, 0]) linear_extrude(1) text("ring + foot centre 50 / 50", size = 3.2, halign = "center", valign = "center");
    translate([inset, 5.3, 0]) mirror([0, top ? 0 : 1, 0]) linear_extrude(1) text("trace must sit inside the inner circle   .   inner 3 = ALEX feet (bottom), drill", size = 2.4, halign = "center", valign = "center");
    translate([size - 5, size / 2, 0]) mirror([0, top ? 0 : 1, 0]) rotate([0, 0, 90]) linear_extrude(1) text("fences on the ALEX edges", size = 3.0, halign = "center", valign = "center");
    translate([inset, size - 7, 0]) mirror([0, top ? 0 : 1, 0]) linear_extrude(1) text("ALEX CORNER", size = 5, halign = "center", valign = "center");
}
difference() {
    translate([0, 0, plate_t]) mirror([0, 0, 1]) template();   // flipped for printing
    translate([0, 0, plate_t - 0.6]) labels(top = true);   // print-top labels read as written; the use-face ones above are mirrored in y so they read after the flip
}
