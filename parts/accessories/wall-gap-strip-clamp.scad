// Wall-gap strip with a clamp notch: the piece that runs from desk 28 cm to 52 cm along each
// wall edge, with an enclosed notch in its middle that wraps round the VIVO clamp's back.
// The clamp back is 80 mm long along the edge and projects 17.5 mm behind the desk edge
// (measured 21 Oct 2026). The notch is 82 mm wide (1 mm each side) and 19.5 mm deep from the
// desk's edge; its centre is exactly 120 mm from the piece's start, so butted against the
// 80 mm filler and the corner piece it sits on desk 40.0 cm, and the clamp itself locates it.
// A 9.5 mm bridge along the wall side still closes the gap behind the clamp. One screw each
// side of the notch; connector pockets at both ends. Two needed, one per wall (same part,
// turned round). The file is in PRINT orientation: top face down, lip up, no supports.

include <wall-gap-common.scad>
seg = 240;
clamp_len = 80; clamp_proj = 17.5; clear = 1; margin = 2;
notch_w = clamp_len + 2 * clear; notch_d = clamp_proj + margin; notch_c = 120;
translate([0, 0, th]) mirror([0, 0, 1]) difference() {
    plain_strip(seg);
    translate([notch_c - notch_w / 2, gap - notch_d, -lip - 1]) cube([notch_w, ontop + notch_d + 1, lip + th + 2]);
}
