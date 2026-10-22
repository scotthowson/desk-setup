// ALEX corner template. Drop it over any corner of an ALEX top: the two fences sit against
// the two edges, and the holes give you the ring centre (5 cm in from both edges) and the
// ring's three screw holes in one go. Same template for all eight corners; just turn it.
// Turned over against the two edges of the BOTTOM, it marks the optional ALEX feet
// (accessories/alex-foot.scad), which use the same centre and screw pattern.
// The ring's outline is engraved so you can see it will land where you expect.
//
// The file is in PRINT orientation: flat face on the bed, fences pointing up, no supports.
// In use you turn it over so the fences hang down against the ALEX edges and the labels
// face you. Any filament.

inset   = 50;      // ring centre from each edge
plate_t = 2.5;   // halved to save material
size    = 100;     // square plate
fence_h = 6; fence_t = 4;
hole_d  = 4;       // scriber or pencil tip
screw_r = (57 / 2 + 75 / 2) / 2;   // the ring's screw circle: (ring_od/2 + flange_od/2)/2 from structure/foot-ring.scad. If pad_d changes there, change ring_od here too
n_screws = 3;
ring_od = 57; ring_bore = 51;

module ring_line(d) { translate([inset, inset, plate_t - 0.5]) difference() { cylinder(d = d + 0.9, h = 1, $fn = 96); translate([0, 0, -1]) cylinder(d = d - 0.9, h = 3, $fn = 96); } }
module template() {   // use orientation: plate on the ALEX top, fences hanging down over two edges
    difference() {
        union() {
            cube([size, size, plate_t]);
            translate([-fence_t, -fence_t, -fence_h]) cube([size + fence_t, fence_t, fence_h + plate_t]);   // fence along one edge
            translate([-fence_t, -fence_t, -fence_h]) cube([fence_t, size + fence_t, fence_h + plate_t]);   // fence along the other
        }
        translate([inset, inset, -1]) cylinder(d = hole_d, h = plate_t + 2, $fn = 24);                 // ring centre
        for (i = [0 : n_screws - 1])
            translate([inset, inset, -1]) rotate([0, 0, i * 360 / n_screws + 45])
                translate([screw_r, 0, 0]) cylinder(d = hole_d, h = plate_t + 2, $fn = 24);           // ring screws
        ring_line(ring_od); ring_line(ring_bore);
        translate([inset, 10, plate_t - 0.6]) linear_extrude(1) text("ring / foot centre 50 / 50", size = 4, halign = "center");
        translate([size - 6, size / 2, plate_t - 0.6]) rotate([0, 0, 90]) linear_extrude(1) text("fences against the ALEX edges", size = 3.5, halign = "center");
    }
}
translate([0, 0, plate_t]) mirror([0, 0, 1]) template();   // flipped for printing
