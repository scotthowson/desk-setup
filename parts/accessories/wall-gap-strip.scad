// Wall-gap strip, optional. Covers the 3 cm gap between a top's wall edge and the wall so
// nothing falls down it. A 200 mm segment; print as many as the run needs (top A's back edge
// and top B's wall edge are 249 cm each; leave the VIVO clamp zones uncovered). It rests on
// the desk's surface with a lip that drops into the gap against the desk's edge, and reaches
// to the wall. Print flat, top face up. A colour near the walnut, or black.

seg   = 200;   // segment length
gap   = 30;    // wall gap
ontop = 8;     // how far it rests on the desk surface
th    = 3;     // thickness
lip   = 6;     // locating lip, hangs into the gap against the desk's edge
chamf = 2;     // chamfer on the edge that faces you

module profile() {   // across the strip: 0 is the wall, gap is the desk's edge
    polygon([[0, 0], [gap + ontop, 0], [gap + ontop, th - chamf], [gap + ontop - chamf, th], [0, th]]);
}
rotate([90, 0, 90]) linear_extrude(seg) profile();   // length along x, across along y, thickness up z
translate([0, gap - 2, -lip]) cube([seg, 2, lip]);    // the lip
