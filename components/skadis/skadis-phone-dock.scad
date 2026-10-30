// Phone dock for the SKÅDIS board: the phone stands in a 14 mm channel 20 mm out from the
// board and leans back on it (about 10° for a 150 mm phone), with a 14 mm notch under it
// for the charging plug and a groove behind for the lead to run down. 90 wide takes any
// phone in a case. Two hangers. Print on the side, as saved, PETG, 4 walls, 25 %. x1
//   openscad -o skadis-phone-dock-x1.stl skadis-phone-dock.scad

include <skadis-lib.scad>

W = 90; D = 36; t = 6; spine_t = 4; chan0 = 20; chan1 = 34; lip = 14; notch = 14; gusset = 30;
v_top = -50;
hx = [W / 2 - 20, W / 2 + 20];

module piece() {
    difference() {
        union() {
            hangers(hx);
            spine(0, W, v_top - t - gusset, 8, spine_t);
            translate([0, 0, v_top - t]) cube([W, spine_t + D, t]);                       // the plate
            translate([0, spine_t + chan1, v_top - t]) cube([W, D - chan1, t + lip]);      // the lip in front of the channel
            translate([0, spine_t, v_top - t]) cube([W, chan0, t + 4]);                    // a 4 mm step behind the channel: the phone's foot sits on it, the lead runs under
            for (x = [W / 2 - 32, W / 2 + 32]) translate([x - 2, 0, 0]) rotate([90, 0, 90]) linear_extrude(4)
                polygon([[spine_t - 0.01, v_top - t + 0.01], [spine_t + gusset, v_top - t + 0.01], [spine_t - 0.01, v_top - t - gusset]]);
        }
        translate([W / 2 - notch / 2, spine_t + chan0 - 6, v_top - t - 1]) cube([notch, chan1 - chan0 + 6, t + 6]);   // plug notch, through the plate, into the step
    }
}
as_print() piece();
