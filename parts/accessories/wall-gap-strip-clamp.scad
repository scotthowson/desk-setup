// Wall-gap strip with a clamp notch: the piece that runs from the corner piece (desk 20 cm)
// to the far side of a VIVO clamp (desk 44 cm). Its last 80 mm has a notch cut from the desk
// side so the clamp's back (7.6 cm wide, projecting `clamp_proj` behind the edge) sits in it,
// while a narrow bridge along the wall side still closes the gap behind the clamp. The lip
// and its screws stop where the notch starts. Two needed: one on the back wall (clamp 1), one
// on the side wall (clamp 2); the side-wall one is the same part turned round.
// Measure how far the clamp's back projects behind the desk edge once a clamp is on, and set
// `clamp_proj` to that (the manual's construction suggests about 16 mm). The bridge that is
// left must be at least 8 mm wide, or print the piece without the bridge (set bridge = false).
// The file is in PRINT orientation: top face down, lip up, no supports.

seg = 240; gap = 29; ontop = 12; th = 3; lip = 20; lip_t = 3; chamf = 1.5; screw = 3.2; csk = 6.5; hole_z = -14;
notch_w    = 84;    // clamp 76 wide plus 4 each side
clamp_proj = 16;    // clamp back behind the desk edge, measured; see above
margin     = 3;
bridge     = true;
notch_d = clamp_proj + margin;              // notch depth from the desk's edge toward the wall
n0 = seg - notch_w;                         // the notch starts here and runs to the end

module profile() { polygon([[0, 0], [gap + ontop, 0], [gap + ontop, th - chamf], [gap + ontop - chamf, th], [chamf, th], [0, th - chamf]]); }
module lip_holes(xs) { for (x = xs) translate([x, gap - lip_t - 1, hole_z]) rotate([-90, 0, 0]) { cylinder(d = screw, h = lip_t + 2, $fn = 24); translate([0, 0, 1 - 0.01]) cylinder(d1 = csk, d2 = screw, h = (csk - screw) / 2 + 0.01, $fn = 24); } }
module strip() {
    difference() {
        union() {
            rotate([90, 0, 90]) linear_extrude(seg) profile();
            translate([0, gap - lip_t, -lip]) cube([n0, lip_t, lip]);              // lip only where there is a desk edge
        }
        lip_holes([40, n0 - 40]);
        // the notch: from the desk-side edge inward by notch_d, over the last notch_w of the length
        translate([n0, bridge ? gap - notch_d : -1, -lip - 1]) cube([notch_w + 1, bridge ? ontop + notch_d + 1 : gap + ontop + 2, lip + th + 2]);
    }
}
translate([0, 0, th]) mirror([0, 0, 1]) strip();   // flipped for printing
