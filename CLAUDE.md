# desk-setup — agent handoff

You are continuing work on Scott's L-shaped PC desk build. Everything here is a snapshot exported from a Claude doc; the numbers are final unless Scott says otherwise.

## What exists

| File | What it is | Edit? |
| --- | --- | --- |
| `index.html` | Interactive Three.js (r128, loaded from cdnjs) 3D model of the finished desk. Single file, no build step. Open it in a browser or via GitHub Pages. | Yes, this is the main thing you will touch |
| `docs/design-review.md` | Engineering review: verified IKEA specs, load paths, bill of materials, hole schedule, structural assessment, purchasing decision, open measurements | Only to correct a measured fact |
| `docs/build-manual.md` | Build order with every measurement and the final checks | Only to correct a measured fact |
| `docs/plan.svg` | Static top-down plan | Regenerate if leg or clamp positions change |

## The design in one paragraph

Two IKEA EKBACKEN tops (249 × 65 × 2.8 cm, brown walnut) form an L. Top A runs along the back wall and keeps the corner square; top B butts into A's front edge. Both tops stand 5 cm off their walls. The tops sit on two ALEX units (centred under the far ends, 3.5 cm of top showing all round) via four round 4 in adjustable feet per unit, and on seven IKEA OLOV legs set to 80.2 cm, so the surface is 83.0 cm. Two 2 × 2 × 3/16 in steel angle rails run under the front edges 12 cm back and are bolted together at the inside corner. Scott sits at the inside corner facing the diagonal; a VIVO STAND-V300CU clamps to top A's two wall edges at 35 cm from the corner with the crossbar on the diagonal, carrying a Samsung Smart M7 32 in (centre, flat) and two Acer XZ320QU 31.5 in 1500R curved monitors along the walls, an Edifier R1280DBs under each Acer, an IKEA ELLOVEN drawer under the M7, an 80 × 30 cm deskmat with a NuPhy Air75 V2 centred on the diagonal, a HYTE Y60 standing on its I/O end on a printed pedestal over ALEX 1, and an ELYONA swing-arm lamp on top B.

## Coordinate convention (do not change)

Scene units are centimetres. x runs along the back wall from top A's left end; z (y in the docs) runs along the side wall from top A's back edge; y is up. Top A: x 0–249, z 0–65. Top B: x 0–65, z 65–314. Walls are at x = −5 and z = −5. Top surface Y1 = 83.0; underside Y0 = 80.2.

Fixed positions (cm): OLOV legs L1 (14, 14), L2 (14, 43), L3 (65, 10), L4 (140, 10), L5 (10, 85), L6 (10, 160), L7 (10, 235). ALEX 1 x 209.5–245.5, z 3.5–61.5. ALEX 2 x 3.5–61.5, z 274.5–310.5. VIVO clamps centred (35, 0) and (0, 35). Rails: A x 1–214 at z 48–53, B z 54–267 at x 48–53. Change these only if Scott measures something different; then update all three docs and the plan.

## How `index.html` is built

- `box(x0,x1,y0,y1,z0,z1,mat)` and `cyl(r0,r1,h,mat,x,y,z)` are the two helpers; `box()` positions the mesh at the centre of the given extents. When you rotate a part, build it inside a `THREE.Group`, position the group, rotate the group.
- `setup` group holds everything that is not structure (chair, monitors, PC, speakers, lamp, mat); the "Chair & setup" toggle hides it.
- Labels are canvas sprites made with `label(text, x, y, z, scale)` and live in `labels`.
- Camera presets are in `views`; the orbit is hand-rolled (drag rotate, wheel zoom, right-drag pan).
- The Acers are slices of a 150 cm radius cylinder (1500R). Their side arms run from the pole along the wall to the panel centre's x (or z), then turn forward into the VESA plate; keep them behind the panels.
- Theme: CSS tokens on `:root`, dark by default, light under `prefers-color-scheme: light`.

## Known open items (ask Scott, do not guess)

1. VIVO pole spacing is assumed 42 cm but is really fixed by the crossbar (part B, the spec's 23 in "base"; the manual uses it as the spacing guide and shows this exact corner mounting). Expect 54–58 cm. Measure collar centre to collar centre on the crossbar, and the pole centre to the desk edge (model assumes 4.5 cm). Clamps move together: clamp centre = pole inset + spacing ÷ 1.414 from the corner.
2. Round feet: the plan uses four per ALEX (eight). Confirm their load rating and plate size.
3. Closed 19 Oct 2026: Scott keeps the 83 cm surface (chair at ~52 cm or a footrest).
4. Steel price from Acier Terrebonne for 2 × 2 × 3/16 in angle, two 7 ft pieces plus a 1 ft offcut.
5. Measured 19 Oct 2026: OLOV plate is 11 cm in diameter (docs assumed ≤ 7 cm), screws M4 × 16 mm fully threaded (IKEA part 108443). An 11 cm plate at L2 (14, 43) overlaps rail A's flat leg by 5 mm and the clamp-2 jaw by 4 mm; moving L2 to (15, 42) clears both, pending Scott's OK. ALEX side-panel thickness still open.

## Rules

- Keep every number in the docs and the model consistent; if you move a part in the model, change the same coordinate in `docs/build-manual.md`.
- Never put a fastener deeper than 21 mm into the 28 mm tops; the docs explain why.
- Commit small, descriptive changes to `main`. GitHub Pages serves `index.html` from the repo root.
