// ALEX corner template. Drop it over any corner of an ALEX top: the two fences sit against
// the two edges, and the holes give you the ring centre (5 cm in from both edges) and the
// ring's three screw holes in one go. Same template for all eight corners; just turn it.
// The ring's outline is engraved so you can see it will land where you expect.
// Print with the fences pointing up (flat face on the bed), any filament, no supports.

inset   = 50;      // ring centre from each edge
plate_t = 5;
size    = 100;     // square plate
fence_h = 12; fence_t = 4;
hole_d  = 4;       // scriber or pencil tip
screw_r = (57 / 2 + 75 / 2) / 2;   // the ring's screw circle, from foot-ring.scad
n_screws = 3;
ring_od = 57; ring_bore = 51;

difference() {
    union() {
        cube([size, size, plate_t]);
        translate([-fence_t, -fence_t, 0]) cube([size + fence_t, fence_t, plate_t + fence_h]);   // fence along one edge
        translate([-fence_t, -fence_t, 0]) cube([fence_t, size + fence_t, plate_t + fence_h]);   // fence along the other
    }
    translate([inset, inset, -1]) cylinder(d = hole_d, h = plate_t + 2, $fn = 24);                 // ring centre
    for (i = [0 : n_screws - 1])
        translate([inset, inset, -1]) rotate([0, 0, i * 360 / n_screws + 45])
            translate([screw_r, 0, 0]) cylinder(d = hole_d, h = plate_t + 2, $fn = 24);           // ring screws
    translate([inset, inset, plate_t - 0.5]) difference() { cylinder(d = ring_od + 0.6, h = 1, $fn = 96); translate([0, 0, -1]) cylinder(d = ring_od - 0.6, h = 3, $fn = 96); }   // ring outline
    translate([inset, inset, plate_t - 0.5]) difference() { cylinder(d = ring_bore + 0.6, h = 1, $fn = 96); translate([0, 0, -1]) cylinder(d = ring_bore - 0.6, h = 3, $fn = 96); } // bore outline
    translate([inset, 10, plate_t - 0.6]) linear_extrude(1) text("ring centre 50 / 50", size = 4, halign = "center");
    translate([size - 6, size / 2, plate_t - 0.6]) rotate([0, 0, 90]) linear_extrude(1) text("fences against the ALEX edges", size = 3.5, halign = "center");
}
