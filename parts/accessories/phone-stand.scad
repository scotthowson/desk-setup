// Phone stand for the desk, with a notch for the charging cable. The phone leans back at
// 25 degrees against the back plate, its bottom edge in a groove behind a lip. Takes a
// phone in a case up to 15 mm thick. Print flat on its base, any filament, no supports.

width  = 70;
base_l = 60; base_t = 6;
back_t = 6;  back_h = 95; lean = 25;   // degrees back from vertical
lip_x  = 20; lip_t = 5; lip_h = 14;    // the front lip
groove_depth = 2;
cable  = 10;

difference() {
    union() {
        cube([base_l, width, base_t]);
        translate([48, 0, 0]) rotate([0, lean, 0]) translate([-back_t, 0, 0]) cube([back_t, width, back_h]);   // back plate, leaning away
        translate([lip_x, 0, 0]) cube([lip_t, width, lip_h]);                                               // front lip
    }
    translate([lip_x + lip_t, -1, base_t - groove_depth]) cube([42 - lip_x - lip_t, width + 2, 30]);         // groove the phone stands in
    translate([lip_x + lip_t - 1, width / 2 - cable / 2, -1]) cube([base_l - lip_x - lip_t + 22, cable, base_t + 2]);   // cable tunnel from the groove out through the back
    translate([-1, -1, -1]) cube([base_l + 20, width + 2, 1]);                                               // trim below the bed
}
