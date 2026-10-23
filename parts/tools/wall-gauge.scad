// Wall gauge. An L with two legs: 65 mm for the ALEX units (their backs stand 6.5 cm off
// the walls: 3 cm gap plus 3.5 cm of top overhang) and 30 mm for the tops themselves (3 cm
// off the walls). Hold the 65 leg between the wall and a cabinet while you place it (manual
// step 5) and again when you slide the desk back after fitting the trim (step 8b); the 30 leg
// checks a top's raw edge against the wall before the trim goes on. Print flat, any filament.

long = 65; short = 30; w = 14; h = 18;
difference() {
    union() { cube([long, w, h]); cube([w, short, h]); }
    translate([long / 2 + 6, w / 2, h - 0.6]) linear_extrude(1) text("ALEX 65", size = 4, halign = "center", valign = "center");
    translate([w / 2, short / 2 + 7, h - 0.6]) rotate([0, 0, 90]) linear_extrude(1) text("EKB 30", size = 3.2, halign = "center", valign = "center");
}
