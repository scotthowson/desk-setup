// End cap for the 2 x 2 x 3/16 in angle rails. Slips over a cut end so nothing sharp faces
// the wall gap or the cabinet. Four needed. Print with the closed end down. PETG or ABS;
// a dab of hot glue if it is loose.

leg    = 50.8;
t      = 4.8;
slack  = 0.3;   // per side
wall   = 2;
depth  = 15;

module L2d(l, th) { polygon([[0, 0], [l, 0], [l, th], [th, th], [th, l], [0, l]]); }

difference() {
    linear_extrude(depth + wall) offset(r = wall) L2d(leg + 2 * slack, t + 2 * slack);
    translate([0, 0, wall]) linear_extrude(depth + 1) L2d(leg + 2 * slack, t + 2 * slack);
}
