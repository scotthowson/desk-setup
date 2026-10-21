// End cap for the 2 x 2 x 3/16 in angle rails. Slips onto a cut end so nothing sharp faces
// the wall gap or the cabinet. The flat leg of the angle is flush against the underside of
// the top, so the cap has NO wall on that face: it covers the end, the underside and free
// edge of the flat leg, and both faces and the bottom edge of the vertical leg. Four needed.
// Print with the closed end down. PETG or ABS; a dab of hot glue if it is loose.

leg   = 50.8;
t     = 4.8;
slack = 0.3;   // per side
wall  = 2;
depth = 15;

// The angle seen end-on: flat leg along the top (its top face is y = leg, against the desk),
// vertical leg down the left side (x 0..t).
module L2d(l, th) { polygon([[0, 0], [th, 0], [th, l - th], [l, l - th], [l, l], [0, l]]); }

difference() {
    linear_extrude(depth + wall) offset(r = wall) L2d(leg + 2 * slack, t + 2 * slack);
    translate([0, 0, wall]) linear_extrude(depth + 1) L2d(leg + 2 * slack, t + 2 * slack);   // the socket
    translate([-wall - 1, leg + 2 * slack, -1]) cube([leg + 2 * wall + 4, wall + 2, depth + wall + 2]);   // open on the desk-side face
}
