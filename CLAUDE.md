# desk-setup — agent handoff

You are continuing work on Scott's L-shaped PC desk build. Everything here is a snapshot exported from a Claude doc; the numbers are final unless Scott says otherwise.

## What exists

| File | What it is | Edit? |
| --- | --- | --- |
| `index.html` | Interactive Three.js (r128, loaded from cdnjs) 3D model of the finished desk. Single file, no build step. Open it in a browser or via GitHub Pages. | Yes, this is the main thing you will touch |
| `docs/design-review.md` | Engineering review: verified IKEA specs, load paths, bill of materials, hole schedule, structural assessment, purchasing decision, open measurements | Only to correct a measured fact |
| `docs/build-manual.md` | Build order with every measurement and the final checks | Only to correct a measured fact |
| `docs/plan.svg` | Static top-down plan | Regenerate if leg or clamp positions change |
| `parts/` | Printed parts, each an OpenSCAD source with its rendered STL and preview; `parts/README.md` lists them. Needed: foot-ring (8), rail-marking-gauge, pilot-drill-guide. Optional: rail-end-cap, rail-cable-hook, wall-gap-strip. Re-render with `openscad -o name.stl name.scad`. | Yes, when a measured dimension changes (pad diameter, angle size, wall gap) |
| `guide.html` | Print-ready build guide: every measurement, dimensioned drawings of each top face down, rails, ALEX rings, the corner joint and the desk layout. All numbers live in the `D` object at the top of its script and every table and drawing is rendered from it. | Yes: change `D` whenever `docs/build-manual.md` changes |

## The design in one paragraph

Two IKEA EKBACKEN tops (249 × 65 × 2.8 cm, brown walnut) form an L. Top A runs along the back wall and keeps the corner square; top B butts into A's front edge. Both tops stand 3 cm off their walls (was 5; the VIVO clamp back needs about 1.5 cm). The tops sit on two ALEX units (centred under the far ends, 3.5 cm of top showing all round) via four round 4 in adjustable feet per unit (plates screwed to the top, 5 cm pads sitting in printed locating rings screwed to the ALEX tops, 5 cm in from each ALEX corner), and on six IKEA OLOV legs set to 80.2 cm, so the surface is 83.0 cm. Two 2 × 2 × 3/16 in hot-rolled steel angle rails (cut to 213 cm by the supplier) run under the front edges 12 cm back and are joined at the inside corner by two 5 mm gusseted 90° strut fittings (1-5/8 in channel size, two holes per leg), one each side of rail B's end, bolted to the vertical legs with 3/8-16 bolts. Scott sits at the inside corner facing the diagonal; a VIVO STAND-V300CU clamps to top A's two wall edges at 35 cm from the corner with the crossbar on the diagonal, carrying a Samsung Smart M7 32 in (centre, flat) and two Acer XZ320QU 31.5 in 1500R curved monitors along the walls, an Edifier R1280DBs under each Acer, an IKEA ELLOVEN drawer under the M7, an 80 × 30 cm deskmat with a NuPhy Air75 V2 centred on the diagonal, a HYTE Y60 standing on its I/O end on a printed pedestal over ALEX 1, an ELYONA swing-arm lamp beside the Y60 at (183, 20), a wooden headset stand at (28, 140) and a plant at (32, 298) on top B.

## Coordinate convention (do not change)

Scene units are centimetres. x runs along the back wall from top A's left end; z (y in the docs) runs along the side wall from top A's back edge; y is up. Top A: x 0–249, z 0–65. Top B: x 0–65, z 65–314. Walls are at x = −3 and z = −3. Top surface Y1 = 83.0; underside Y0 = 80.2.

Fixed positions (cm): OLOV legs L1 (15, 42), L2 (65, 10), L3 (140, 10), L4 (10, 85), L5 (10, 160), L6 (10, 235). Six legs by Scott's decision (19 Oct 2026); the corner leg at (14, 14) was dropped and the leg under clamp 2 moved from (14, 43) to (15, 42) so its 11 cm plate clears rail A and the clamp jaw. ALEX 1 x 209.5–245.5, z 3.5–61.5. ALEX 2 x 3.5–61.5, z 274.5–310.5. VIVO clamps centred (35, 0) and (0, 35). Rails: A x 1–214 at z 48–53, B z 53–266 at x 48–53 (B's corner end touches A's front face). Change these only if Scott measures something different; then update all three docs and the plan.

## How `index.html` is built

- `box(x0,x1,y0,y1,z0,z1,mat)` and `cyl(r0,r1,h,mat,x,y,z)` are the two helpers; `box()` positions the mesh at the centre of the given extents. When you rotate a part, build it inside a `THREE.Group`, position the group, rotate the group.
- `setup` group holds everything that is not structure (chair, monitors, PC, speakers, lamp, mat); the "Chair & setup" toggle hides it.
- Labels are canvas sprites made with `label(text, x, y, z, scale)` and live in `labels`.
- Camera presets are in `views`; the orbit is hand-rolled (drag rotate, wheel zoom, right-drag pan).
- The Acers are slices of a 150 cm radius cylinder (1500R). Their side arms run from the pole along the wall to the panel centre's x (or z), then turn forward into the VESA plate; keep them behind the panels.
- Theme: CSS tokens on `:root`, dark by default, light under `prefers-color-scheme: light`.

## Known open items (ask Scott, do not guess)

1. VIVO pole spacing is assumed 42 cm but is really fixed by the crossbar (part B, the spec's 23 in "base"; the manual uses it as the spacing guide and shows this exact corner mounting). Expect 54–58 cm. Measure collar centre to collar centre on the crossbar, the pole centre to the desk edge (model assumes 4.5 cm), and how far the clamp projects behind the desk edge (the 3 cm wall gap assumes under 2.5 cm). Clamps move together: clamp centre = pole inset + spacing ÷ 1.414 from the corner.
2. Round feet: Scott has twelve 4 in feet (listing: 10 cm tall, 5 cm stainless body and pad, 6 × 6 cm plate); the plan uses four per ALEX (eight), four spare; pad diameter 5 cm, so the printed locating rings have a 51 mm bore. Load rating still unknown (design wants ≥ 50 kg each).
3. Closed 19 Oct 2026: Scott keeps the 83 cm surface (chair at ~52 cm or a footrest).
4. Closed 19 Oct 2026: two 2 × 2 × 0.188 in hot-rolled angle, 84 in each, ordered from Metal Supermarkets Ottawa (2275 Stevenage Dr) for pickup, $142.68 plus tax = $161.22, cutting included. No offcut, so the corner bracket is two 5 mm gusseted 90° strut fittings (1-5/8 in channel, 9/16 in holes, two per leg), one each side of rail B's end, centred 29 mm below the top (the inside fitting's top edge then clears rail B's first two screw heads by 1 mm): four 3/8-16 × 1 in bolts through rail A's vertical leg, two 3/8-16 × 1½ in bolts through rail B's leg with a fitting on each side, all in 7/16 in holes template-drilled on the bench (rail A: fitting heel at 52.0 cm from the wall end facing the far end, and at 51.5 cm facing the wall end; rail B: heel at the corner end). Rail screws #10 × 1 in.
5. Measured 19 Oct 2026: OLOV plate is 11 cm in diameter (docs assumed ≤ 7 cm), screws M4 × 16 mm fully threaded (IKEA part 108443). The plate clash at (14, 43) is resolved by L1 at (15, 42). ALEX side-panel thickness still open.

## Rules

- Keep every number in the docs and the model consistent; if you move a part in the model, change the same coordinate in `docs/build-manual.md`.
- Never put a fastener deeper than 21 mm into the 28 mm tops; the docs explain why.
- Commit small, descriptive changes to `main`. GitHub Pages serves `index.html` from the repo root.
