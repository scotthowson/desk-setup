// Bow-tie key for the SKÅDIS tiles (skadis-tile.scad): one per pocket pair, three per
// joint. 13 x 10 x 3.4 mm, dovetail waist 6 mm. Push it into the back of the joint with a
// thumb until the pocket's lip clicks over it; the chamfer on its top edge cams it past
// the lip. Print flat, as saved, PETG, 100% infill. Print spares: they are 0.4 g each.

key_len = 13; key_neck = 6; key_tip = 10; key_depth = 3.5; cham = 0.5;
h = key_depth - 0.1;
key_poly = [[-key_len / 2, -key_tip / 2], [-key_len / 2, key_tip / 2], [0, key_neck / 2], [key_len / 2, key_tip / 2], [key_len / 2, -key_tip / 2], [0, -key_neck / 2]];
hull() {
    linear_extrude(h - cham) polygon(key_poly);
    translate([0, 0, h - cham]) linear_extrude(cham) offset(delta = -cham) polygon(key_poly);
}
