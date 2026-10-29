// Bow-tie key for the SKÅDIS tiles (skadis-tile.scad): one per pocket pair, three per
// joint. 13 x 11 x 3.4 mm, dovetail waist 5 mm. Push it into the back of the joint with a
// thumb until the pocket's lip clicks over it; the chamfer on its top edge cams it past
// the lip. Both faces are chamfered, so either way up works. Print flat, as saved, PETG,
// same profile as the tiles. Print spares: 0.7 g each. Fit: see `fit` below.

key_len = 13; key_neck = 5; key_tip = 11; key_depth = 3.5; cham = 0.5; foot = 0.3;
fit = 0.1;   // the key is drawn this much smaller all round than the pocket's nominal shape: the lip then holds it by 0.1 mm a side. Tight: raise it. Loose: lower it.
h = key_depth - 0.1;
key_poly = [[-key_len / 2, -key_tip / 2], [-key_len / 2, key_tip / 2], [0, key_neck / 2], [key_len / 2, key_tip / 2], [key_len / 2, -key_tip / 2], [0, -key_neck / 2]];
module key2d(d = 0) { offset(delta = -fit + d) polygon(key_poly); }
steps = 5;   // chamfers as shrinking slices, so the waist is kept (a hull would fill it)
for (i = [0 : steps - 1]) translate([0, 0, i * foot / steps]) linear_extrude(foot / steps + 0.01) key2d(-foot * (steps - i) / steps);   // bottom: counters first-layer squish
translate([0, 0, foot]) linear_extrude(h - cham - foot) key2d();
for (i = [0 : steps - 1]) translate([0, 0, h - cham + i * cham / steps]) linear_extrude(cham / steps + 0.01) key2d(-cham * (i + 1) / steps);   // top: cams past the lip
