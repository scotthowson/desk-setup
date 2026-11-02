// Snap-in hook on openGrid, one cell: headset, a coiled lead, a bag strap, under the front
// edge of the desk. 40 mm drop, 30 mm reach, the tip turns up 12. Print plate down, snaps up,
// PETG, 4 walls (the hook is 6 thick). Two cells of snaps if you want it stronger: nx = 2.
//   openscad -o og-hook-x2.stl og-hook.scad
include <og-lib.scad>
nx = 1; drop = 40; reach = 30; tip = 12; t = 6; w = 16; r = 6;

og_plate(nx, 1);
// the J: a stem down from the plate, a bottom run out to the tip, the tip up
translate([nx * cell / 2 - w / 2, cell / 2, 0]) rotate([90, 0, 90]) linear_extrude(w) {
    translate([-t / 2, -drop]) square([t, drop]);                                   // stem
    translate([-t / 2, -drop]) square([reach + t / 2, t]);                           // run
    translate([reach - t / 2, -drop]) square([t, tip + t]);                          // tip
    translate([reach, -drop + tip + t]) circle(d = t);                               // rounded tip end
}
