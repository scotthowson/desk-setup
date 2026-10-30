// Back brackets for the SKÅDIS tiles (skadis-tile.scad): a thin plate on the back of a
// joint with pegs that fill slots in each tile, glued in. The pegs run the full board
// thickness, so they finish flush with the front, and the plate stiffens the joint so it
// cannot hinge. The keys hold the tiles together; the brackets make the board one panel.
//
//   type = "cross"     where four tiles meet: 73 x 42 plate, four pegs, one in each tile.
//                      Centre it on the corner. It fits either way up (180° symmetric).
//   type = "bridge-h"  across an upright joint: 61 x 21 stadium, two pegs side by side 40 apart
//                      (the shape in Scott's picture).
//   type = "bridge-v"  across a level joint: 21 x 71, two pegs one above the other 40 apart.
//
// Where: a cross on every corner where four tiles meet. A bridge on every joint where it
// reaches the board's outside edge, centred on the 4th slot row (or column) in from that
// edge; a single-row board's joints reach two edges, so two bridges each. Each bracket
// fills only its own slots and leaves at least 1 mm to every other slot.
//
// IKEA's hooks drop a tab behind the board below their slot, so the plates are notched clear
// of the zone 12 mm under every slot they would otherwise cover (hook_zone below): the cross
// loses two bites from each long edge, bridge-h one from each long edge, and every slot
// around a bracket still takes a hook.
//
// Peg positions, from the pattern (slots at 10 + 40 i and 30 + 40 i, every tile edge on a
// multiple of 40): cross, relative to the corner: (-10,-10) (+10,+10) (+30,-10) (-30,+10).
// Bridges: two slots 40 apart in the same row (h) or the same column (v).
//
// Print plate down, pegs up, as saved, PETG, 100 % (they are small), no supports.
//   openscad -D 'type="cross"' -o skadis-cross-x4.stl skadis-bracket.scad     # bridge-h, bridge-v the same, -x4 each (3 x 3)

type = "cross";            // cross, bridge-h, bridge-v
th = 5;                    // board thickness: the pegs are this tall, so they end flush with the front
proud = 0;                 // + makes the pegs longer, - shorter; -0.1 if a peg stands proud of the front
plate = 2;                 // plate thickness, behind the board
slot_w = 5; slot_h = 15;   // SKÅDIS slot
fit = 0.1;                 // pegs are drawn this much smaller all round than the slot: room for CA glue

peg_w = slot_w - 2 * fit; peg_l = slot_h - 2 * fit;
module peg2d() { hull() for (s = [-1, 1]) translate([0, s * (peg_l - peg_w) / 2]) circle(d = peg_w, $fn = 32); }
module slot2d() { hull() for (s = [-1, 1]) translate([0, s * (slot_h - slot_w) / 2]) circle(d = slot_w, $fn = 32); }
module rrect(w, h, r) { offset(r = r, $fn = 48) square([w - 2 * r, h - 2 * r], center = true); }

pegs = type == "cross"    ? [[-10, -10], [10, 10], [30, -10], [-30, 10]]
     : type == "bridge-h" ? [[-20, 0], [20, 0]]
     :                      [[0, -20], [0, 20]];

module outline() {
    if (type == "cross")         rrect(73, 42, 6);                                              // 1.5 mm clear of the slots above and below
    else if (type == "bridge-h") hull() for (p = pegs) translate(p) circle(r = 10.5, $fn = 64);  // 2 mm clear of the slots above and below
    else                         hull() for (p = pegs) translate(p) offset(r = 8, $fn = 48) slot2d();
}

hook_drop = 12;   // how far an IKEA hook's tab reaches below its slot, behind the board
module hook_zones() for (i = [-3 : 3], j = [-3 : 3], o = [10, 30]) let (c = [40 * i + o, 40 * j + o])
    if (len([for (q = pegs) if (q == c) 1]) == 0) translate([c[0] - slot_w / 2 - 1, c[1] - slot_h / 2 - hook_drop]) square([slot_w + 2, hook_drop]);
linear_extrude(plate) difference() { outline(); hook_zones(); rotate(180) hook_zones(); }   // and the zones of the piece turned 180°, so it still fits either way up
for (p = pegs) translate([p[0], p[1], plate]) linear_extrude(th + proud) peg2d();
