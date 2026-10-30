// Shelf for the SKÅDIS board: 120 wide x 70 deep with a 12 mm front lip, two hangers and two
// gussets under it, on the shared hanger (skadis-lib.scad). Holds a couple of kilos.
// Print on the side, as saved, PETG, 4 walls, 25 % infill, no supports: every wall is
// upright in the print, which is why it has gussets rather than end walls. x2
//   openscad -o skadis-shelf-120-x2.stl skadis-shelf.scad

include <skadis-lib.scad>

W = 120; D = 70; lip = 12; t = 6; spine_t = 4; gusset = 50;
v_top = -50;                 // the shelf's top surface (just under the hanger pegs)
hx = [W / 2 - 20, W / 2 + 20];

module piece() {
    hangers(hx);
    spine(0, W, v_top - t - gusset, 8, spine_t);
    translate([0, 0, v_top - t]) cube([W, spine_t + D, t]);                           // the plate
    translate([0, spine_t + D - t, v_top - t]) cube([W, t, t + lip]);                  // the lip
    for (x = hx) translate([x - 2, 0, 0]) rotate([90, 0, 90]) linear_extrude(4)        // gussets under the hangers
        polygon([[spine_t - 0.01, v_top - t + 0.01], [spine_t + gusset, v_top - t + 0.01], [spine_t - 0.01, v_top - t - gusset]]);
}
as_print() piece();
