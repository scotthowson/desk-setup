// openGrid snap-in library for our own under-desk accessories. The snap is the Underware
// channel's own grip (monokiniGrip in ../monokini_I_channel.scad, CC-BY-NC-SA, needs BOSL2 to
// render; the STLs here are already rendered), so anything built on it clicks into an openGrid
// Lite tile exactly like a channel does: two 2 mm tabs 26.4 mm apart, 15 mm long, 3.4 mm tall,
// one pair per 28 mm cell, lips into the cell's groove. Build the part hanging from z = 0 (the
// tile's face) with og_plate() as its top, and print it plate down, snaps up, no supports.
use <../monokini_I_channel.scad>

cell = 28;              // openGrid pitch
snap_w = 26.4;          // tab outer faces, the channel's width
snap_h = 3.4;           // tab height above the plate (baseHeight in the channel source)
grip_z = 22 - 3.4;      // monokiniGrip draws its tab at z 18.6..22 for a 22 mm channel

module og_snap_pair() {   // one cell, centred at x = 0, running y 0..cell
    translate([0, 0, -grip_z]) { monokiniGrip(widthMM = snap_w); mirror([1, 0, 0]) monokiniGrip(widthMM = snap_w); }
}
module og_snaps(nx, ny) for (i = [0 : nx - 1], j = [0 : ny - 1]) translate([i * cell + cell / 2, j * cell, 0]) og_snap_pair();
module og_plate(nx, ny, t = 3, inset = 0.4) {   // the flat top, a hair inside the cells' outline
    translate([inset, inset, -t]) cube([nx * cell - 2 * inset, ny * cell - 2 * inset, t]);
    og_snaps(nx, ny);
}
module rr(w, h, r) offset(r) offset(-r) square([w, h]);
