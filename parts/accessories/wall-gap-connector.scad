// Connector tile for the wall-gap trim. Butt two pieces end to end, then push this up into
// the pockets on their undersides: the two pins press-fit into the pin holes (a drop of CA
// glue if you want it permanent). One per joint; print a couple of spares. Print pins up.

include <wall-gap-common.scad>
tile_l = 2 * pocket_l - 1;   // 39: 1 mm total slack in the two pockets
tile_w = pocket_w - 0.4;
pin_d = pin_hole - 0.1;      // press fit in a printed hole, which comes out slightly small
cube([tile_l, tile_w, pocket_d]);
for (x = [tile_l / 2 - pin_from_end, tile_l / 2 + pin_from_end]) translate([x, tile_w / 2, pocket_d]) cylinder(d = pin_d, h = pin_depth - 0.1, $fn = 20);
