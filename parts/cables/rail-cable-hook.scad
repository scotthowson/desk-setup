// Cable hook that snaps over the vertical leg of either rail. No holes, no screws; slide it
// wherever a cable run needs holding, and flip it so the J hangs on the side away from your
// knees. Holds a bundle up to about 24 mm. Print on its side (the profile is what you see
// from the end), PETG so the clip has some spring. Print as many as you need.

leg_t = 4.8;   // angle thickness
slack = 0.3;
w     = 16;    // width along the rail
jaw   = 22;    // how far the clip reaches down the leg
wall  = 2.4;
loop  = 24;    // inside width of the J
drop  = 26;    // how far the J hangs below the clip

slot = leg_t + slack;
module profile() {
    square([wall, jaw]);                                        // inner jaw (x 0..wall), the leg sits beside it
    translate([wall, 1.5]) polygon([[0,0],[0.5,1.5],[0,3]]);    // snap bump
    translate([0, jaw]) square([2*wall + slot, wall]);          // bridge over the heel edge
    translate([wall + slot, -drop]) square([wall, drop + jaw + wall]);   // outer jaw, continuing down as the J's spine
    translate([wall + slot, -drop]) square([wall + loop + wall, wall]);  // bottom of the J
    translate([wall + slot + wall + loop, -drop]) square([wall, drop - 8]); // up-stand, 8 mm short of the clip so cables drop in
}
linear_extrude(w) profile();
