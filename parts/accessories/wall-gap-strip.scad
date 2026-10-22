// Wall-gap strip. Covers the 3 cm gap between a top's wall edge and the wall so nothing
// falls in. Rests 12 mm on the desk; a 20 mm lip hangs into the gap against the desk's raw
// back edge, and two #4 x 1/2 in flat-head screws through the lip go sideways into that edge,
// 14 mm below the surface. Connector pockets at both ends (see wall-gap-common.scad).
// 240 mm segments, butted end to end; set `seg` for the short pieces (README cut list):
//   openscad -D seg=80 -o wall-gap-strip-80.stl wall-gap-strip.scad
// Measure the real gap after the desk is in and set `gap` in wall-gap-common.scad to the
// SMALLEST value minus 1. The file is in PRINT orientation: top face down, lip up, no supports.

include <wall-gap-common.scad>
seg = 240;
translate([0, 0, th]) mirror([0, 0, 1]) plain_strip(seg);
