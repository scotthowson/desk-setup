// End cap for the wall-gap trim. The chain's last piece ends at the top's far end and the
// gap is open there: from the side you see the raw back edge. This clips into the connector
// pocket of ANY strip end (one pin, like half a connector tile), so it works on either wall
// and either end, no handed parts. A 3 mm slab sits under the plate across the gap, between
// the wall side and the lip, and an end wall drops the full top thickness (28 mm) flush with
// the strip's end, closing the gap. Nothing shows on top. Print 2. A drop of CA glue if loose.
// Print as saved: end wall flat on the bed, slab and tile standing, pin horizontal.

include <wall-gap-common.scad>
drop = 28;                        // EKBACKEN thickness: the wall ends at the top's underside
tile_l = pocket_l - 0.5; tile_w = pocket_w - 0.4; pin_d = pin_hole - 0.1;
cap_w = gap - lip_t - 1;          // across the gap part, 0.5 mm clear of the wall side and the lip
slab_t = 3;
// use orientation: x along the strip, outer end at x = 0, plate underside at z = 0, wall side at y = 0
module cap() {
    cy = (gap - lip_t) / 2;                                               // = pocket_y, centre line of the gap part
    translate([0, cy - tile_w / 2, 0]) cube([tile_l, tile_w, pocket_d]);  // tile up into the pocket
    translate([pin_from_end, cy, pocket_d]) cylinder(d = pin_d, h = pin_depth - 0.1, $fn = 20);
    translate([0, cy - cap_w / 2, -slab_t]) cube([tile_l, cap_w, slab_t]);  // slab under the plate
    translate([0, cy - cap_w / 2, -drop]) cube([th, cap_w, drop]);          // end wall, flush with the strip's end
}
rotate([0, -90, 0]) cap();   // end wall onto the bed, slab and tile standing
