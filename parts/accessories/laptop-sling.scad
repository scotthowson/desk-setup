// Laptop sling under top B, between the ALEX 2 feet F5-F8, for the Dell Pro 16 Plus (PB16250:
// 358 x 251.4 x 21.35 mm, 1.84 kg). The laptop lies flat, lid closed, and slides in from top B's
// far end (z = 314, open floor there) with a SHORT side leading, so its 251 width runs between
// the feet (43 cm clear between the pads) and its 358 length runs along the wall, z 272 to 308
// when docked. Two C-rails screwed to the underside carry its long edges on 12 mm lips; a
// carriage at the inner end holds the dock's USB-C plug so the port on the leading side mates
// as the laptop reaches its stops: the stops take the push, the plug floats 1 mm in its clip.
//
// Rails: inner faces 253.4 apart (laptop + 2), centred on x = 31.5 cm, so at x 18.83 and 44.17
// cm; flange out toward the feet; #6 x 5/8 screws (3/4 through a 4 mm openGrid tile), 13 mm in.
// Four 230 mm segments make the two 46 cm rails (z 268 to 314, two per side, butted), the
// outer segment of each side flared at the mouth. Felt strip on the lips.
//
// MEASURE before printing the carriage (the rails need nothing measured):
//   which side leads (the side with the Thunderbolt ports), port centre from the laptop's
//   HINGE edge (port_from_hinge), port centre height above the laptop's underside (port_h),
//   the dock plug's overmould width, height and length (plug_body), how far the metal tongue
//   sticks out of the overmould (plug_tongue).
//   openscad -D part=\"rail\"     -o laptop-sling-rail-x2.stl       laptop-sling.scad
//   openscad -D part=\"mouth\"    -o laptop-sling-mouth-x2.stl      laptop-sling.scad
//   openscad -D part=\"carriage\" -o laptop-sling-carriage-x1.stl   laptop-sling.scad
//   openscad -D part=\"clip\"     -o laptop-sling-usbc-clip-x1.stl  laptop-sling.scad   (set port_h and plug_body first; x is set on the slots)
// Print rails and mouths standing on the flange face (as saved), PETG, 4 walls, 30 %; the
// carriage flat on its back. Nothing here is test-printed; the rails are safe to print now.

part = "rail";
lap_w = 251.4; lap_t = 21.35; lap_l = 358;        // Dell Pro 16 Plus, SHI listing (MEASURE the thickness at the port side)
gap = 2;                                          // side play, total
clear_t = 24;                                     // under the flange to the lip: 2.65 over the laptop
wall = 4; flange = 18; flange_t = 4; lip = 12; lip_t = 3;
seg = 230; mouth_len = 60; flare = 6;
hole_d = 4.0; head_d = 8.5;                       // #6 clearance, countersink
port_from_hinge = 60;   // MEASURE: port centre from the hinge (back) edge, mm
port_h = 8.5;           // MEASURE: port centre above the laptop's underside, mm
plug_body = [22, 11, 35];   // MEASURE: the dock plug's overmould, width x height x length
plug_tongue = 8;        // MEASURE: metal tongue beyond the overmould (USB-C inserts about 6.5)
play = 1.0;             // the plug floats this much each way in its clip
stop_t = 6; carr_t = 6;

inner = lap_w + gap;                 // 253.4
H = flange_t + clear_t + lip_t;      // rail height, 31

module rail_profile(fl = flare) {    // x across (0 = inner face of the wall), y down from the top's underside
    translate([-fl, 0]) square([wall + flange + fl, flange_t]);                 // flange, out toward the feet
    translate([-fl, 0]) square([wall, H]);                                      // wall
    translate([-fl - lip, H - lip_t]) square([lip + wall, lip_t]);              // lip, in under the laptop
}
module rail(len, mouth = false) {    // along z; the mouth flares out over its last 30 mm
    difference() {
        union() {
            if (!mouth) linear_extrude(len) rail_profile(0);
            else {
                linear_extrude(len - 30) rail_profile(0);
                hull() { translate([0, 0, len - 30]) linear_extrude(0.01) rail_profile(0); translate([0, 0, len - 0.01]) linear_extrude(0.01) rail_profile(flare); }
            }
        }
        for (z = holes_z(len, mouth)) translate([wall + flange / 2 + 2, -1, z]) rotate([-90, 0, 0]) cylinder(d = hole_d, h = flange_t + 2, $fn = 24);   // through holes; the heads are countersunk from the flange's underside in rail_part()
    }
}
// The flange is against the top, so the heads must be on its underside: countersink from below.
module rail_part(len, mouth = false) difference() {
    rail(len, mouth);
    for (z = holes_z(len, mouth)) translate([wall + flange / 2 + 2, flange_t + 0.01, z]) rotate([90, 0, 0]) cylinder(d1 = head_d, d2 = hole_d, h = (head_d - hole_d) / 2 + 0.2, $fn = 24);
}
function holes_z(len, mouth) = mouth ? [20] : [25, len - 25];   // a mouth piece gets one screw, clear of its flare
module carriage() {   // x along the bay (0 at the hinge-side rail's inner face), y toward the laptop (0 = the bar's back), z up from the lip top
    // A bar across the bay with a stop pad each end: the laptop's leading edge lands on the stops. A window in the bar, 50 wide and open
    // at the bottom, takes the USB-C clip (separate part), which screws to the bar's laptop-side face on four M3 screws through its slots,
    // so the plug can be set 10 mm either way along the bay once the port is measured. Two tabs screw the bar up to the top.
    bar_h = clear_t;
    difference() {
        union() {
            cube([inner, carr_t, bar_h]);
            for (x = [0, inner - 25]) translate([x, carr_t, 0]) cube([25, stop_t, bar_h]);                 // stops
            for (x = [0, inner - 30]) translate([x, -12, bar_h]) cube([30, 12 + carr_t, flange_t]);        // screw tabs, up to the top
        }
        translate([port_x - 25, -1, -1]) cube([50, carr_t + 2, bar_h - 7]);                                // the window, open underneath, an 8 mm bridge left over it
        for (dx = [-28, 28], z = [5, 20]) translate([port_x + dx, -1, z]) rotate([-90, 0, 0]) cylinder(d = 2.8, h = carr_t + 2, $fn = 20);   // M3 self-tapping, for the clip
        for (x = [15, inner - 15]) translate([x, -6, bar_h - 1]) cylinder(d = hole_d, h = flange_t + 2, $fn = 24);
    }
}
module usbc_clip() {   // screws to the carriage's laptop-side face: plate with four slots, cradle for the plug's overmould, zip-tie slots
    pw = plug_body[0] + 1; ph = plug_body[1] + 1; pl = plug_body[2];
    front = stop_t + 6.5 - plug_tongue;          // overmould face beyond the plate when the tongue is 6.5 into the port
    cw = 3; cf = 3;                               // cradle wall and floor
    difference() {
        union() {
            cube([76, 3, 24]);                                                                            // the plate, bottom at the lip top
            translate([38 - pw / 2 - cw, front - pl, port_h - ph / 2 - cf]) cube([pw + 2 * cw, pl + 3, ph + cf]);   // cradle, open on top, through the window behind the plate
        }
        translate([38 - pw / 2, front - pl - 1, port_h - ph / 2]) cube([pw, pl + 5, 30]);               // the overmould's pocket
        translate([38 - pw / 2 - cw - 1, -1, port_h - ph / 2]) cube([pw + 2 * cw + 2, 5, ph + 2]);     // the plate opens where the plug passes; continuous above
        for (dx = [-28, 28], z = [5, 20]) hull() for (sx = [-6, 6]) translate([38 + dx + sx, -1, z]) rotate([-90, 0, 0]) cylinder(d = 3.4, h = 5, $fn = 20);   // slots, 12 long: 6 mm of adjustment each way
        for (y = [front - pl + 6, front - 6]) translate([38 - pw / 2 - cw - 1, y - 2, port_h - ph / 2 - cf - 1]) cube([pw + 2 * cw + 2, 4, cf + 2]);         // zip-tie slots through the floor
    }
}
port_x = port_from_hinge;   // hinge edge at x = 0 of the bay (hinge toward the wall); set port_from_hinge from the other edge if the hinge faces the room

if (part == "rail") rail_part(seg);
else if (part == "mouth") rail_part(mouth_len, true);
else if (part == "carriage") carriage();
else if (part == "clip") usbc_clip();
