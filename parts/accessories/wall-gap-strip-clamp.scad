// Wall-gap strip with a clamp notch: the piece that runs from desk 28 cm to 52 cm along each
// wall edge, with an enclosed notch in its middle that wraps round the VIVO clamp's back.
// The clamp back is 80 mm long along the edge and projects 17.5 mm behind the desk edge
// (measured 21 Oct 2026). The notch is 82 mm wide (1 mm each side) and 19.5 mm deep from the
// desk's edge, and its centre is exactly 120 mm from the piece's start, so butted against
// the 80 mm filler and the corner piece the notch centres on desk 40.0 cm: the clamp position.
// A 9.5 mm bridge along the wall side still closes the gap behind the clamp. The lip runs
// either side of the notch with one screw each side. Two needed, one per wall; it is the same
// part turned round. If the notch does not centre on a clamp, adjust the 80 mm filler, not this.
// The file is in PRINT orientation: top face down, lip up, no supports.

seg = 240; gap = 29; ontop = 12; th = 3; lip = 20; lip_t = 3; chamf = 1.5; screw = 3.2; csk = 6.5; hole_z = -14;
clamp_len  = 80;    // clamp back along the edge, measured
clamp_proj = 17.5;  // clamp back behind the desk edge, measured
clear      = 1;     // per side
margin     = 2;
notch_w = clamp_len + 2 * clear;
notch_d = clamp_proj + margin;              // from the desk's edge toward the wall
notch_c = 120;                              // notch centre from the piece's start = desk 40.0 when the piece starts at 28
n0 = notch_c - notch_w / 2; n1 = notch_c + notch_w / 2;

module profile() { polygon([[0, 0], [gap + ontop, 0], [gap + ontop, th - chamf], [gap + ontop - chamf, th], [chamf, th], [0, th - chamf]]); }
module lip_holes(xs) { for (x = xs) translate([x, gap - lip_t - 1, hole_z]) rotate([-90, 0, 0]) { cylinder(d = screw, h = lip_t + 2, $fn = 24); translate([0, 0, 1 - 0.01]) cylinder(d1 = csk, d2 = screw, h = (csk - screw) / 2 + 0.01, $fn = 24); } }
module strip() {
    difference() {
        union() {
            rotate([90, 0, 90]) linear_extrude(seg) profile();
            translate([0, gap - lip_t, -lip]) cube([seg, lip_t, lip]);
        }
        lip_holes([40, seg - 40]);
        translate([n0, gap - notch_d, -lip - 1]) cube([notch_w, ontop + notch_d + 1, lip + th + 2]);   // the notch, through plate and lip
    }
}
translate([0, 0, th]) mirror([0, 0, 1]) strip();   // flipped for printing
