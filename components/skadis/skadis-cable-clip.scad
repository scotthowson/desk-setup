// Cable clip for the BACK of the SKÅDIS board: a split peg pushes into any slot from behind
// and grips by spring (nothing shows on the front), and an open ring holds the cables of
// whatever hangs on the board, running down the back to the desk's wall gap.
//
// Section, z out of the back face (board z 0..5, front at 5), x across the slot:
//   two prongs 1.8 wide with a 1.2 gap, 4.5 long, a 0.25 bump each side at 2..3.5 deep, so
//   the peg is 5.3 at the bump in a 5 mm slot and squeezes to fit; tips chamfered to lead in.
//   10 mm along the slot, inside its straight part, so the rounded ends never touch.
// Ring behind the 2 mm plate: `cable` inside, opening to one side.
//
// Print standing on an end, as saved (everything is an extrusion along the slot), PETG.
//   openscad -o skadis-cable-clip-x6.stl skadis-cable-clip.scad

cable = 8;      // ring inside diameter: a bundle of 2 or 3 thin leads, or one power cord
wall = 2;
gap = 0.7;      // ring opening as a fraction of `cable`
len = 10;       // along the slot (straight part of a 15 mm slot is 10)
plate = 2;

module prong2d(s) {   // s = +1 right, -1 left
    mirror([s < 0 ? 1 : 0, 0])
    polygon([[0.6, 0], [2.4, 0], [2.4, 2], [2.65, 2.5], [2.65, 3.2], [2.2, 4.5], [0.6, 4.5]]);
}
module section2d() {
    prong2d(1); prong2d(-1);
    translate([-8, -plate]) square([16, plate + 0.01]);                       // plate on the back face
    r = cable / 2 + wall;
    translate([0, -plate - cable / 2 + 0.01]) difference() {                  // ring
        circle(r = r, $fn = 64);
        circle(d = cable, $fn = 64);
        translate([0, -cable * gap / 2]) square([r + 1, cable * gap]);       // opening to the side
    }
}
linear_extrude(len) section2d();
