// Wall standoff for the SKÅDIS board: if the board stands with its back toward a wall, two
// of these at its top corners rest on the wall and the sway is gone, because the board is
// then held at the top as well as at the clamps. A 12 x 40 mm foot glues to the back in one
// of the solid bands (x = 20, 40, 60 ... from a tile's edge, where there are no slots), a
// 14 mm stem reaches `reach` mm, and a 24 mm disc takes a felt pad. Measure the gap from the
// board's back to the wall at the top, subtract 3 for the pad, set `reach` (30 or more).
// Print standing on the disc, as saved, PETG, 100 %, brim if you like. x2
//   openscad -D reach=60 -o skadis-wall-standoff-x2.stl skadis-wall-standoff.scad

reach = 60;
foot = [12, 40, 3]; stem = 14; disc = 24; disc_t = 3; flare = 13;   // the 45° flare under the foot

cylinder(d = disc, h = disc_t, $fn = 64);
cylinder(d = stem, h = reach - foot[2] - flare + 0.01, $fn = 48);
hull() {
    translate([0, 0, reach - foot[2] - flare]) cylinder(d = stem, h = 0.01, $fn = 48);
    translate([-foot[0] / 2, -foot[1] / 2, reach - foot[2] - 0.01]) cube([foot[0], foot[1], 0.01]);
}
translate([-foot[0] / 2, -foot[1] / 2, reach - foot[2]]) cube(foot);
