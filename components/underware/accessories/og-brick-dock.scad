// Power-brick dock on openGrid: a tray that hangs under the tile, the brick slides in from the
// open end over a 6 mm lip and a Velcro strap through the two slots holds it. Cable notches at
// both ends. Sized by the brick: set `brick` to its measured length, width, height in mm
// (MEASURE: the defaults are catalogue guesses) and render:
//   openscad -D 'brick=[95,47,28]' -D 'tag="DELL 65W"' -o og-brick-dock-dell65-x1.stl og-brick-dock.scad
//   openscad -D 'brick=[100,48,32]' -D 'tag="G5"'      -o og-brick-dock-g5-x1.stl     og-brick-dock.scad
// Print plate down, snaps up, PETG, 3 walls, 20 %. The plate covers whole cells (2 x 4 for the
// Dell brick); snap it in with the open end toward where the cord goes.
include <og-lib.scad>

brick = [95, 47, 28];   // length (along the cord), width, height; MEASURE
tag = "DELL 65W";
clr = 1.0; wall = 2.4; floor_t = 2.4; lip = 6; notch = 14; strap = [20, 3];
f = "DejaVu Sans:style=Bold";

plate_t = 3;
W = brick[1] + 2 * clr + 2 * wall; L = brick[0] + 2 * clr + 2 * wall; H = plate_t + brick[2] + clr + floor_t;   // from the tile face to the tray's floor
nx = ceil(W / cell); ny = ceil(L / cell);
ox = (nx * cell - W) / 2; oy = (ny * cell - L) / 2;   // tray centred under the plate

difference() {
    union() {
        og_plate(nx, ny);
        translate([ox, oy, -H]) cube([W, L, H]);
    }
    translate([ox + wall, oy + wall, -H + floor_t]) cube([W - 2 * wall, L - 2 * wall, H - floor_t - plate_t]);   // the cavity, up to the plate's underside
    translate([ox + wall, oy - 1, -H + floor_t + lip]) cube([W - 2 * wall, wall + 2, H - floor_t - lip - plate_t]);   // open end above the lip (y = oy)
    translate([ox + (W - notch) / 2, oy + L - wall - 1, -H + floor_t]) cube([notch, wall + 2, H - floor_t - plate_t]);   // cord notch, closed end
    for (y = [oy + L * 0.3, oy + L * 0.7]) translate([ox - 1, y - strap[0] / 2, -H - 1]) cube([W + 2, strap[0], floor_t + strap[1] + 1]);   // strap slots across the floor and up both walls
    translate([ox + W / 2, oy + L / 2, -H - 0.01]) mirror([0, 0, 1]) mirror([1, 0, 0]) linear_extrude(0.8) text(tag, size = 6, font = f, halign = "center", valign = "center");   // read from below
}
