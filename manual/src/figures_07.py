#!/usr/bin/env python3
"""Figures for chapter G (legs and cabinet support). Numbers from manual/data.json and manual/facts.json only."""
import math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figures_01 import (D, F, LAY, FIG, Canvas, mm, cm, ptext, pline, dim, leader, pballoon, plan_items,  # noqa: E402
                        wall_hatch, Z0, Z1, ALEX_H, RAIL_LOW)

A, B = D["A"], D["B"]
FE, RG, OL = F["feet"], F["rings"], F["olov"]


def save(c, name):
    c.save(os.path.join(FIG, name))


def person(c, p, facing=(0, -1), label="you"):
    """Top-view person symbol at page point p, facing a page direction."""
    x, y = p
    c.raw(f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="5" ry="2.4" fill="#e6e6e6" stroke="#000" stroke-width="0.5" '
          f'transform="rotate({math.degrees(math.atan2(facing[1], facing[0])) + 90:.1f} {x:.2f} {y:.2f})"/>')
    c.raw(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2" fill="#fff" stroke="#000" stroke-width="0.5"/>')
    ptext(c, x, y + 6.5, label, size=3.2, weight="bold")


def tape(c, p, rot=0):
    x, y = p
    c.raw(f'<rect x="{x - 5:.2f}" y="{y - 1.6:.2f}" width="10" height="3.2" fill="#bfbfbf" stroke="#000" stroke-width="0.25" transform="rotate({rot} {x:.2f} {y:.2f})"/>')
    ptext(c, x, y + 0.1, "TAPE", size=2.6 if False else 3.0, weight="bold", rotate=rot)


# ---------------- G-1 orientation of the two tops, face down ----------------
def fig_orient():
    c = Canvas(178, 134)
    s = 0.40
    # top A face down: back edge away from you (page top), side-wall end on the right
    ax, ay = 22, 16
    W, H = A["x1"] * s, A["y1"] * s
    c.raw(f'<rect x="{ax}" y="{ay}" width="{W:.2f}" height="{H:.2f}" fill="#f2f2f2" stroke="#000" stroke-width="0.5"/>')
    pline(c, (ax, ay), (ax + W, ay), lw=1.2)
    ptext(c, ax + W / 2, ay + H / 2, "A", size=8, weight="bold")
    ptext(c, ax + W / 2, ay - 7.5, "back edge: square, unfinished (goes to the wall) · y = 0", size=3.2)
    ptext(c, ax + W / 2, ay - 3.2, "measure y from here", size=3.2, weight="bold")
    ptext(c, ax + W / 2, ay + H + 4, "front edge: rounded, laminated", size=3.2)
    ptext(c, ax + W + 4.5, ay + H / 2, "side-wall end · x = 0", size=3.2, rotate=90)
    ptext(c, ax - 4.5, ay + H / 2, "far end · x = 249 cm", size=3.2, rotate=-90)
    tape(c, (ax + W - 12, ay + 2.2)); tape(c, (ax + W - 2.2, ay + H / 2 + 9), rot=90)
    c.raw(f'<circle cx="{ax + W:.2f}" cy="{ay:.2f}" r="1.4" fill="#000"/>')
    ptext(c, ax + W - 1, ay + 7.6, "datum", size=3.2, anchor="end", weight="bold")
    # x / y arrows
    c.arrow((ax + W - 4, ay + H + 9), (ax + W - 22, ay + H + 9)); ptext(c, ax + W - 25, ay + H + 9, "x", size=3.4, weight="bold", anchor="end")
    person(c, (ax + W / 2, ay + H + 13.5), label="stand here")
    # top B face down: joint end away from you, side-wall edge on the right
    bx, by = 150, 14
    BW, BH = B["x1"] * s, (B["y1"] - B["y0"]) * s
    c.raw(f'<rect x="{bx}" y="{by}" width="{BW:.2f}" height="{BH:.2f}" fill="#f2f2f2" stroke="#000" stroke-width="0.5"/>')
    pline(c, (bx + BW, by), (bx + BW, by + BH), lw=1.2)
    ptext(c, bx + BW / 2, by + BH / 2, "B", size=8, weight="bold")
    ptext(c, bx + BW / 2, by - 3.5, "joint end (tape 0)", size=3.2, weight="bold")
    ptext(c, bx + BW + 4.5, by + BH / 2, "side-wall edge: unfinished (to the wall) · x = 0", size=3.2, rotate=90)
    ptext(c, bx - 4.5, by + BH / 2, "front edge: rounded, laminated · x = 65 cm", size=3.2, rotate=-90)
    tape(c, (bx + BW / 2, by + 2.2)); tape(c, (bx + BW - 2.2, by + 22), rot=90)
    c.raw(f'<circle cx="{bx + BW:.2f}" cy="{by:.2f}" r="1.4" fill="#000"/>')
    c.arrow((bx + 6, by + 62), (bx + 6, by + 80)); ptext(c, bx + 8.5, by + 80, "y", size=3.4, weight="bold", anchor="start")
    ptext(c, bx + BW / 2, by + BH + 4, "far end", size=3.2)
    person(c, (bx + BW / 2, by + BH + 10), facing=(0, -1), label="stand here")
    # B is A turned a quarter turn (face up, seen from above, as installed)
    k = 0.15; ox, oy = 14, 84
    c.raw(f'<rect x="{ox}" y="{oy}" width="{A["x1"] * k:.2f}" height="{A["y1"] * k:.2f}" fill="#fff" stroke="#000" stroke-width="0.5"/>')
    pline(c, (ox, oy), (ox + A["x1"] * k, oy), lw=1.2)
    ptext(c, ox + A["x1"] * k / 2, oy + A["y1"] * k / 2, "A", size=4, weight="bold")
    ox2, oy2 = 70, 78
    c.raw(f'<rect x="{ox2}" y="{oy2}" width="{B["x1"] * k:.2f}" height="{(B["y1"] - B["y0"]) * k:.2f}" fill="#fff" stroke="#000" stroke-width="0.5"/>')
    pline(c, (ox2, oy2), (ox2, oy2 + (B["y1"] - B["y0"]) * k), lw=1.2)
    ptext(c, ox2 + B["x1"] * k / 2, oy2 + 18, "B", size=4, weight="bold")
    cx, cy, r = 60, 92, 5
    c.raw(f'<path d="M {cx + r:.2f} {cy:.2f} A {r} {r} 0 1 0 {cx:.2f} {cy + r:.2f}" fill="none" stroke="#000" stroke-width="0.5"/>')
    c._head(cx - 1.5, cy + r + 0.1, cx, cy + r, 1.6)   # anticlockwise: A's wall edge (top) turns to B's wall edge (left)
    for i, (t, w) in enumerate((("Face up, as installed:", "bold"), ("heavy line = unfinished edge,", "normal"), ("always to a wall.", "normal"),
                                ("B is A turned a quarter turn:", "bold"), ("B's drawings are not a", "bold"), ("mirror of A's.", "bold"),
                                ("Either short end of A can be", "normal"), ("its side-wall end: tape one.", "normal"))):
        ptext(c, 86, 79 + i * 4.4 + (2 if i >= 3 else 0) + (2 if i >= 6 else 0), t, size=3.2, anchor="start", weight=w)
    save(c, "07-orient.svg")


# ---------------- G-2 / G-3 underside support layout, face down ----------------
def layout_top(top, name, s, margin, size, rail_line=True):
    """Face-down view of one top. A: back edge at the page top, x grows to the left. B: joint end at the top."""
    if top == "A":
        T = lambda x, y: (A["x1"] - x, y)
        reg = (A["x1"], A["y1"])
    else:
        T = lambda x, y: (B["x1"] - x, y - B["y0"])
        reg = (B["x1"], B["y1"] - B["y0"])
    l, t = margin
    c = Canvas(size[0], size[1], scale=s, origin=(-l / s, -t / s))
    c.rect(0, 0, reg[0], reg[1], fill="#f2f2f2")
    if top == "A":
        c.line((0, 0), (reg[0], 0), lw="heavy")
    else:
        c.line((reg[0], 0), (reg[0], reg[1]), lw="heavy")
    # rail line (reference only) and ALEX outline
    if top == "A" and not rail_line:
        a = D["alex1"]
    elif top == "A":
        r = D["railA"]
        c.line(T(r["x0"], r["y1"]), T(r["x1"], r["y1"]), lw="thin", dash="3 1 0.8 1")
        ptext(c, *c.P(*T(120, r["y1"] + 4.5)), "rail A line, y = 53 cm (step 4)", size=3.2)
        a = D["alex1"]
    else:
        r = D["railB"]
        c.line(T(r["x1"], B["y0"]), T(r["x1"], r["y1"]), lw="thin", dash="3 1 0.8 1")
        ptext(c, *c.P(*T(r["x1"] + 5.5, 170)), "rail B line, x = 53 cm (step 5)", size=3.2, rotate=-90)
        a = D["alex2"]
    p0 = T(a["x0"], a["y0"]); p1 = T(a["x0"] + a["w"], a["y0"] + a["d"])
    c.rect(min(p0[0], p1[0]), min(p0[1], p1[1]), abs(p1[0] - p0[0]), abs(p1[1] - p0[1]), lw="thin", dash="3 1.5")
    # clamp zones and pad outlines on A
    if top == "A":
        for p in D["pads"]:
            q0, q1 = T(p[0], p[2]), T(p[1], p[3])
            c.rect(min(q0[0], q1[0]), min(q0[1], q1[1]), abs(q1[0] - q0[0]), abs(q1[1] - q0[1]), lw="thin", dash="1 0.8")
        z, k = D["zoneIn"], D["clamp"]
        for (x0, x1, y0, y1), lab in (((k - 4, k + 4, 0, z), "C1"), ((0, z, k - 4, k + 4), "C2")):
            q0, q1 = T(x0, y0), T(x1, y1)
            c.rect(min(q0[0], q1[0]), min(q0[1], q1[1]), abs(q1[0] - q0[0]), abs(q1[1] - q0[1]), fill="#bfbfbf", lw="thin")
        q = c.P(*T(k, z)); ptext(c, q[0], q[1] + 2.6, "C1", size=3.2, weight="bold")
        q = c.P(*T(z / 2, 49.3)); ptext(c, q[0], q[1], "C2", size=3.2, weight="bold")
    # legs and feet (solid: you are looking at the underside)
    for n, x, y, t, *_ in D["legs"]:
        if t != top: continue
        c.circle(T(x, y), D["legPlate"] / 2, fill="#fff")
        base = 0 if n == "L1" else (-90 if top == "A" else 180)   # one hole at the wall (L1: away from the side-wall end)
        for i in range(5):
            ang = math.radians(base + 72 * i); rr = OL["hole_circle_radius"] / 10
            c.circle(T(x + rr * math.cos(ang), y + rr * math.sin(ang)), 0.55, fill="#000", lw="thin")
        c.centre_mark(T(x, y), 1.2)
    for n, x, y, t in D["feet"]:
        if t != top: continue
        h = FE["plate"] / 20
        q0, q1 = T(x - h, y - h), T(x + h, y + h)
        c.rect(min(q0[0], q1[0]), min(q0[1], q1[1]), abs(q1[0] - q0[0]), abs(q1[1] - q0[1]), fill="#fff", lw="outline")
        hs = FE["plate_hole_spacing"] / 20
        for sx in (-1, 1):
            for sy in (-1, 1):
                c.circle(T(x + sx * hs, y + sy * hs), 0.5, fill="#000", lw="thin")
        c.circle(T(x, y), D["footPad"] / 2, lw="thin")
    return c, T


def fig_layout_a():
    s = 0.62
    c, T = layout_top("A", "07-layout-A.svg", s, (10, 17), (178, 70))
    W, H = A["x1"], A["y1"]
    ptext(c, *c.P(W / 2, -10.5 / s), "back edge (unfinished, to the wall) · y = 0 · measure y from here", size=3.2, weight="bold")
    ptext(c, *c.P(W / 2, H + 4.5 / s), "front edge (rounded)", size=3.2)
    ptext(c, *c.P(-5 / s, H / 2), "far end", size=3.2, rotate=-90)
    ptext(c, *c.P(W + 4.5 / s, H / 2), "side-wall end · x = 0", size=3.2, rotate=90)
    q = c.P(W, 0); c.raw(f'<circle cx="{q[0]:.2f}" cy="{q[1]:.2f}" r="1.3" fill="#000"/>')
    ptext(c, q[0] - 1, q[1] - 4.2, "datum", size=3.2, anchor="end", weight="bold")
    for n, x, y, *_ in D["legs"]:
        if n in ("L2", "L3"):
            p = c.P(*T(x, y)); ptext(c, p[0], p[1] + 6.4, n, size=3.2, weight="bold")
        elif n == "L1":
            p = c.P(*T(x, y)); ptext(c, p[0] - 4.5, p[1], n, size=3.2, weight="bold", anchor="end")
    for n, x, y, t in D["feet"]:
        if t == "A":
            p = c.P(*T(x, y)); ptext(c, p[0], p[1] + (4.6 if y < 30 else -4.6), n, size=3.2, weight="bold")
    p = c.P(*T(227.5, 30.5)); ptext(c, p[0], p[1], "ALEX 1", size=3.2, weight="bold"); ptext(c, p[0], p[1] + 4, "below", size=3.2)
    L3 = D["legs"][2]
    dim(c, T(L3[1], 0), T(L3[1], L3[2]), "", 0, ext=False); q = c.P(*T(L3[1], 0)); ptext(c, q[0] + 1.5, q[1] - 2.4, "10 cm", size=3.2, anchor="start")                    # 100 from the back edge
    dim(c, T(A["x1"], 0), T(D["feet"][1][1], 0), "8.5 cm", 3.5, tside=2)                  # F2 85 from the far end
    dim(c, T(A["x1"], A["y1"]), T(D["feet"][0][1], A["y1"]), "34.5 cm", -3.5)   # F1/F3 345 from the far end
    dim(c, T(0, A["y1"]), T(15, A["y1"]), "15 cm", 3.5)                       # L1 150 from the side-wall end
    save(c, "07-layout-A.svg")


def fig_layout_b():
    s = 0.45
    c, T = layout_top("B", "07-layout-B.svg", s, (13, 9), (62, 131))
    W, H = B["x1"], B["y1"] - B["y0"]
    ptext(c, *c.P(W / 2, -4.5 / s), "joint end: tape 0", size=3.2, weight="bold")
    ptext(c, *c.P(W / 2, H + 4.5 / s), "far end", size=3.2)
    ptext(c, *c.P(W + 5 / s, H / 2), "side-wall edge (unfinished) · x = 0", size=3.2, rotate=90)
    ptext(c, *c.P(-5 / s, H / 2), "front edge (rounded)", size=3.2, rotate=-90)
    q = c.P(W, 0); c.raw(f'<circle cx="{q[0]:.2f}" cy="{q[1]:.2f}" r="1.3" fill="#000"/>')
    for n, x, y, t, *_ in D["legs"]:
        if t == "B":
            p = c.P(*T(x, y)); ptext(c, p[0] - 4.2, p[1], n, size=3.2, weight="bold", anchor="end")
    for n, x, y, t in D["feet"]:
        if t == "B":
            p = c.P(*T(x, y)); ptext(c, p[0] + (4.4 if x > 30 else -4.4), p[1], n, size=3.2, weight="bold")
    p = c.P(*T(32.5, 292.5)); ptext(c, p[0], p[1] - 2, "ALEX 2", size=3.2, weight="bold"); ptext(c, p[0], p[1] + 2, "below", size=3.2)
    save(c, "07-layout-B.svg")


# ---------------- G-4 leg jig ----------------
def fig_leg_jig():
    s = 0.5
    c = Canvas(178, 80, scale=s, origin=(-30 / s, -42 / s))   # object mm: x from the lip's inner face, y across
    L, Wd, r = 205, 100, OL["hole_circle_radius"]
    c.rect(-4, -Wd / 2, 4, Wd, fill="#808080")                 # lip
    c.rect(0, -Wd / 2, L, Wd, fill="#f2f2f2")
    for cx, rot, dashed in ((100, 180, False), (150, 0, True)):
        c.circle((cx, 0), OL["plate_diameter"] / 2, dash="2 1.2" if dashed else None, lw="outline")
    for cx, rot, dashed in ((100, 180, False), (150, 0, True)):
        c.circle((cx, 0), 1.25, lw="thin")
        for i in range(5):
            a = math.radians(rot + 72 * i)
            p = (cx + r * math.cos(a), r * math.sin(a))
            c.circle(p, 1.75, fill="#fff")
            if dashed:
                c.circle(p, 4, lw="thin")
    dim(c, (0, -Wd / 2), (100, -Wd / 2), "100 mm (10 cm)", 4)
    dim(c, (0, -Wd / 2), (150, -Wd / 2), "150 mm (15 cm)", 11)
    pline(c, c.P(100, -Wd / 2), c.P(100, -Wd / 2 - 9)) if False else None
    # left: wall side
    c.arrow((-10, 0), (-40, 0)); ptext(c, *c.P(-24, -8), "wall", size=3.2, weight="bold")
    ptext(c, *c.P(-2, Wd / 2 + 8), "lip hooks over the wall edge", size=3.2, anchor="start")
    leader(c, (100 - r - 1.8, 1.2), c.P(-16, 38), "", anchor="start")
    ptext(c, *c.P(-58, 34), "this hole", size=3.2, anchor="start"); ptext(c, *c.P(-58, 42), "at the wall", size=3.2, anchor="start")
    # right column
    X = L + 8
    leader(c, (150 + r + 4, 0), c.P(X, 0), "150: L1 only,", anchor="start")
    ptext(c, *c.P(X + 3, 8), "dashed circle,", size=3.2, anchor="start"); ptext(c, *c.P(X + 3, 16), "ringed holes", size=3.2, anchor="start")
    pp = (100 + 52.5 * math.cos(math.radians(225)), 52.5 * math.sin(math.radians(225)))
    leader(c, pp, c.P(-14, -40), "", anchor="start")
    ptext(c, *c.P(-58, -46), "100: L2–L6,", size=3.2, anchor="start"); ptext(c, *c.P(-58, -34), "solid circle", size=3.2, anchor="start")
    ptext(c, *c.P(X + 3, 32), "centres: scriber", size=3.2, anchor="start"); ptext(c, *c.P(X + 3, 40), "only", size=3.2, anchor="start")
    ptext(c, *c.P(L / 2, Wd / 2 + 8), "", size=3.2)
    ptext(c, *c.P(110, Wd / 2 + 18), "Each pattern, mm: plate ⌀105 outline, 5 holes for the 1/8 in bit on ⌀85 (neighbours 50 apart)", size=3.2)
    save(c, "07-leg-jig.svg")


# ---------------- G-5 leg steps ----------------
def fig_leg_steps():
    c = Canvas(178, 66)
    w = 44
    def top_slab(x0, y0, wid):
        c.raw(f'<rect x="{x0}" y="{y0}" width="{wid}" height="8" fill="#f2f2f2" stroke="#000" stroke-width="0.5"/>')
        c.hatch([(x0, y0), (x0 + wid, y0), (x0 + wid, y0 + 8), (x0, y0 + 8)], spacing=1.6)
    def drill(x, ytip, label=None):
        c.raw(f'<rect x="{x - 4}" y="{ytip - 30}" width="8" height="10" fill="#bfbfbf" stroke="#000" stroke-width="0.5"/>')
        c.raw(f'<rect x="{x - 0.6}" y="{ytip - 20}" width="1.2" height="20" fill="#808080" stroke="#000" stroke-width="0.25"/>')
    for i in range(4):
        x0 = 2 + i * w
        ptext(c, x0 + 3, 4, str(i + 1), size=4, weight="bold", anchor="start")
        c.raw(f'<rect x="{x0}" y="0.5" width="{w - 3}" height="65" fill="none" stroke="#000" stroke-width="0.25"/>')
    # 1: through the jig, 3-4 mm
    top_slab(4, 44, 36); c.raw('<rect x="6" y="41" width="32" height="3" fill="#e6e6e6" stroke="#000" stroke-width="0.5"/>')
    drill(22, 46.5); ptext(c, 22, 58, "chapter D: started", size=3.2); ptext(c, 22, 62, "3–4 mm through the jig", size=3.2)
    ptext(c, 30, 38, "jig", size=3.2, anchor="start")
    # 2: lift the jig, finish with the 15 LEG puck
    x = 46; top_slab(x + 2, 44, 36)
    drill(x + 22, 50)
    c.raw(f'<rect x="{x + 14}" y="30" width="16" height="14" fill="#e6e6e6" stroke="#000" stroke-width="0.5"/>')
    ptext(c, x + 22, 37, "15 LEG", size=3.0, weight="bold")

    ptext(c, x + 20, 58, "finish 15 mm deep", size=3.2); ptext(c, x + 20, 62, "chuck on the puck", size=3.2)
    # 3: plate on, M4 x 16
    x = 90; top_slab(x + 2, 44, 36)
    c.raw(f'<rect x="{x + 8}" y="41.5" width="24" height="2.5" fill="#bfbfbf" stroke="#000" stroke-width="0.5"/>')
    c.raw(f'<rect x="{x + 16}" y="22" width="8" height="19.5" fill="#e6e6e6" stroke="#000" stroke-width="0.5"/>')
    for sx in (x + 11, x + 29):
        c.raw(f'<rect x="{sx - 1.5}" y="39.5" width="3" height="2" fill="#000"/>')
        c.raw(f'<line x1="{sx}" y1="41.5" x2="{sx}" y2="50.5" stroke="#000" stroke-width="0.8"/>')
    pballoon(c, (0, 0), (x + 36, 30), "H01") if False else None
    c.raw(f'<circle cx="{x + 36}" cy="29" r="3.6" fill="#fff" stroke="#000" stroke-width="0.5"/>')
    ptext(c, x + 36, 29.1, "H01", size=3.0, weight="bold"); pline(c, (x + 34, 32), (x + 29.5, 40))
    ptext(c, x + 20, 58, "5 × M4 × 16,", size=3.2); ptext(c, x + 20, 62, "about 13 mm into the top", size=3.2)
    # 4: pre-set to 802
    x = 134; top_slab(x + 2, 52, 36)
    c.raw(f'<rect x="{x + 8}" y="49.5" width="24" height="2.5" fill="#bfbfbf" stroke="#000" stroke-width="0.5"/>')
    c.raw(f'<rect x="{x + 17}" y="9" width="6" height="40.5" fill="#e6e6e6" stroke="#000" stroke-width="0.5"/>')
    c.raw(f'<rect x="{x + 15}" y="7" width="10" height="2" fill="#808080" stroke="#000" stroke-width="0.25"/>')
    pline(c, (x + 30, 7), (x + 35, 7)); pline(c, (x + 30, 49.5), (x + 35, 49.5))
    c.arrow((x + 33, 28), (x + 33, 7.6)); c.arrow((x + 33, 28), (x + 33, 48.9))
    ptext(c, x + 37, 28, "80.2 cm", size=3.4, weight="bold", rotate=-90)
    ptext(c, x + 20, 63, "plate face to foot", size=3.2)
    save(c, "07-leg-steps.svg")


# ---------------- G-6 feet plate ----------------
def fig_feet_plate():
    s = 0.75
    c = Canvas(72, 68, scale=s, origin=(-34 / s, -34 / s))
    P, sp = FE["plate"], FE["plate_hole_spacing"]
    c.rect(-P / 2, -P / 2, P, P, fill="#e6e6e6")
    c.circle((0, 0), FE["body_and_pad_diameter"] / 2, dash="1.6 0.9", lw="thin")
    for sx in (-1, 1):
        for sy in (-1, 1):
            c.hole((sx * sp / 2, sy * sp / 2), FE["plate_hole_diameter"])
    c.centre_mark((0, 0), 2)
    dim(c, (P / 2, -P / 2), (-P / 2, -P / 2), "59.5", -4)
    dim(c, (-P / 2, -P / 2), (-P / 2, P / 2), "59.5", -4)
    dim(c, (-sp / 2, P / 2), (sp / 2, P / 2), "46.8", -4)
    dim(c, (P / 2, P / 2), (P / 2, -P / 2), "46.8", 0.01, ext=False) if False else None
    dim(c, (P / 2, sp / 2), (P / 2, -sp / 2), "46.8", -4)
    pline(c, c.P(sp / 2, -sp / 2), c.P(P / 2 + 1, -sp / 2)); pline(c, c.P(sp / 2, sp / 2), c.P(P / 2 + 1, sp / 2))
    pline(c, c.P(-sp / 2, sp / 2), c.P(-sp / 2, P / 2 + 1)); pline(c, c.P(sp / 2, sp / 2), c.P(sp / 2, P / 2 + 1))
    leader(c, (sp / 2 + 2, -sp / 2 - 2), (70, 3), "⌀5.2", anchor="end")
    ptext(c, *c.P(0, -11), "pad ⌀50", size=3.2); ptext(c, *c.P(0, 11), "(below)", size=3.2)
    save(c, "07-feet-plate.svg")


# ---------------- G-7 feet jigs ----------------
def fig_feet_jigs():
    c = Canvas(178, 72)
    s = 0.4
    ox, oy = 14, 12          # the far corner (top-left, as F2 in Fig. G-2)
    c.raw(f'<rect x="{ox}" y="{oy}" width="72" height="50" fill="#f2f2f2" stroke="none"/>')
    pline(c, (ox, oy), (ox + 72, oy), lw=0.5); pline(c, (ox, oy), (ox, oy + 50), lw=0.5)
    J = 125 * s
    c.raw(f'<rect x="{ox:.2f}" y="{oy:.2f}" width="{J:.2f}" height="{J:.2f}" fill="#fff" stroke="#000" stroke-width="0.5"/>')
    c.raw(f'<rect x="{ox - 1.6:.2f}" y="{oy - 1.6:.2f}" width="1.6" height="{J + 1.6:.2f}" fill="#808080"/>')
    c.raw(f'<rect x="{ox - 1.6:.2f}" y="{oy - 1.6:.2f}" width="{J + 1.6:.2f}" height="1.6" fill="#808080"/>')
    fx, fy = ox + 85 * s, oy + 85 * s
    Pp = FE["plate"] * s; hs = FE["plate_hole_spacing"] / 2 * s
    c.raw(f'<rect x="{fx - Pp / 2:.2f}" y="{fy - Pp / 2:.2f}" width="{Pp:.2f}" height="{Pp:.2f}" fill="none" stroke="#000" stroke-width="0.25" stroke-dasharray="1 0.6"/>')
    for sx in (-1, 1):
        for sy in (-1, 1):
            c.raw(f'<circle cx="{fx + sx * hs:.2f}" cy="{fy + sy * hs:.2f}" r="0.9" fill="#fff" stroke="#000" stroke-width="0.4"/>')
    c.raw(f'<circle cx="{fx:.2f}" cy="{fy:.2f}" r="0.5" fill="#000"/>')
    pline(c, (ox, fy), (fx, fy)); pline(c, (fx, oy), (fx, fy))
    ptext(c, ox + 85 * s / 2, fy - 2.4, "8.5 cm", size=3.2, weight="bold"); ptext(c, fx + 2.6, oy + 12, "8.5 cm", size=3.2, weight="bold", rotate=90)
    ptext(c, ox + J / 2, oy - 4.5, "fence on one edge", size=3.2); ptext(c, ox - 4.5, oy + J / 2, "fence", size=3.2, rotate=-90)
    ptext(c, ox + J + 2, oy + 30, "plate outline", size=3.2, anchor="start"); pline(c, (fx + Pp / 2, fy - 2), (ox + J + 1.6, oy + 30))
    ptext(c, ox + 36, 68, "(a) corner jig on a far corner: F2 F4 F7 F8", size=3.2, weight="bold")
    # (b) T-square
    bx0, by = 104, 12
    c.raw(f'<rect x="{bx0}" y="{by}" width="72" height="52" fill="#f2f2f2" stroke="none"/>')
    pline(c, (bx0, by), (bx0 + 72, by), lw=0.5)
    sx = 140; s2 = 0.32
    pline(c, (sx, by - 3), (sx, by + 54), lw=0.25, dash="3 1 0.8 1")
    ptext(c, sx, by - 9.5, "station 34.5 cm from the far end", size=3.2); ptext(c, sx, by - 5.2, "(tape hooked on the far end)", size=3.2)
    c.raw(f'<rect x="{sx - 55 * s2:.2f}" y="{by - 1.4:.2f}" width="{110 * s2:.2f}" height="1.4" fill="#808080"/>')
    c.raw(f'<rect x="{sx - 55 * s2:.2f}" y="{by:.2f}" width="{110 * s2:.2f}" height="{20 * s2:.2f}" fill="#fff" stroke="#000" stroke-width="0.5"/>')
    c.raw(f'<rect x="{sx - 12 * s2:.2f}" y="{by + 20 * s2:.2f}" width="{24 * s2:.2f}" height="{142 * s2:.2f}" fill="#fff" stroke="#000" stroke-width="0.5"/>')
    c.raw(f'<rect x="{sx - 28 * s2:.2f}" y="{by + (85 - 28) * s2:.2f}" width="{56 * s2:.2f}" height="{56 * s2:.2f}" fill="#fff" stroke="#000" stroke-width="0.5"/>')
    for off in (50, 85, 100, 150):
        c.raw(f'<circle cx="{sx:.2f}" cy="{by + off * s2:.2f}" r="0.8" fill="#fff" stroke="#000" stroke-width="0.4"/>')
    for ddx in (-1, 1):
        for ddy in (-1, 1):
            c.raw(f'<circle cx="{sx + ddx * 23.4 * s2:.2f}" cy="{by + (85 + ddy * 23.4) * s2:.2f}" r="0.8" fill="#fff" stroke="#000" stroke-width="0.4"/>')
    for off, t in ((50, "50 mm"), (100, "100 mm"), (150, "150 mm")):
        pline(c, (sx - 1, by + off * s2), (sx - 11, by + off * s2)); ptext(c, sx - 12, by + off * s2, t, size=3.2, anchor="end")
    pline(c, (sx + 1, by + 85 * s2), (sx + 11, by + 85 * s2)); ptext(c, sx + 12, by + 85 * s2 - 2.1, "85 mm +", size=3.2, anchor="start"); ptext(c, sx + 12, by + 85 * s2 + 2.1, "plate holes", size=3.2, anchor="start")
    ptext(c, bx0 + 1, by + 3.5, "lip over", size=3.2, anchor="start"); ptext(c, bx0 + 1, by + 7.5, "the edge", size=3.2, anchor="start")
    ptext(c, sx, 68, "(b) T-square, 85 hole: F1 F3 F5 F6", size=3.2, weight="bold")
    save(c, "07-feet-jigs.svg")


# ---------------- G-8 foot height gauge ----------------
def fig_foot_gauge():
    s = 0.29
    c = Canvas(56, 40, scale=s, origin=(-80, -8 / s))
    def R(x0, y0, w, h, fill="#e6e6e6", lw=0.5):
        p = c.P(x0, y0)
        c.raw(f'<rect x="{p[0]:.2f}" y="{p[1]:.2f}" width="{w * s:.2f}" height="{h * s:.2f}" fill="{fill}" stroke="#000" stroke-width="{lw}"/>')
    R(-29.75, 0, 59.5, 2.5, "#bfbfbf")
    R(-25, 2.5, 50, 62)
    R(-6, 64.5, 12, 27.5, "#fff")
    R(-25, 92, 50, 10)
    g = "#808080"
    R(-50, -6, 6, 114, g); R(-50, -6, 76, 6, g); R(-50, 102, 76, 6, g)
    a, b = c.P(-60, 0), c.P(-60, 102)
    pline(c, c.P(-60, 0), c.P(-50, 0)); pline(c, c.P(-60, 102), c.P(-50, 102))
    pline(c, a, b); c._head(b[0], b[1], a[0], a[1], 1.5); c._head(a[0], a[1], b[0], b[1], 1.5)
    ptext(c, a[0] - 2.6, (a[1] + b[1]) / 2, "102.0 mm", size=3.4, weight="bold", rotate=-90)
    c.arrow((70, 50), (36, 50)); ptext(c, *c.P(38, 40), "slide on", size=3.2, anchor="start")
    save(c, "07-foot-gauge.svg")


# ---------------- G-9 locating ring ----------------
def fig_ring():
    s = 0.8
    c = Canvas(178, 80, scale=s, origin=(-44 / s, -40 / s))
    fo, od, bo, sr = RG["flange_od"], RG["od"], RG["bore"], RG["screw_circle_radius"]
    c.circle((0, 0), fo / 2, fill="#e6e6e6")
    c.circle((0, 0), od / 2, fill="#bfbfbf")
    c.circle((0, 0), bo / 2, fill="#fff")
    c.centre_mark((0, 0), 2)
    c.circle((0, 0), sr, lw="thin", dash="3 1 0.8 1")
    for a in RG["screw_angles_deg"]:
        p = (sr * math.cos(math.radians(a)), -sr * math.sin(math.radians(a)))
        c.circle(p, RG["csk"] / 2, fill="#fff", lw="thin")
        c.hole(p, RG["screw_hole"], cross=False)
    ptext(c, *c.P(0, -9), f"⌀{bo:g} bore", size=3.2); ptext(c, *c.P(0, 9), f"⌀{od:g} ring", size=3.2)
    p330 = (sr * math.cos(math.radians(330)), -sr * math.sin(math.radians(330)))
    leader(c, (p330[0] + 2.6, p330[1] + 2.6), c.P(44, 36), "3 × ⌀3.8, csk ⌀7.0,", anchor="start")
    ptext(c, c.P(44, 36)[0] + 1.2, c.P(44, 36)[1] + 4.3, "on r 33 at 90°, 210°, 330°", size=3.2, anchor="start")
    dim(c, (-fo / 2, 0), (-fo / 2, 0), "", 0) if False else None
    pline(c, c.P(-fo / 2, -1), c.P(-fo / 2, -fo / 2 - 3)); pline(c, c.P(fo / 2, -1), c.P(fo / 2, -fo / 2 - 3))
    dim(c, (-fo / 2, -fo / 2 - 1), (fo / 2, -fo / 2 - 1), "⌀75 flange", 0.01, ext=False)
    # section A-A, true scale 1.0 page mm per mm, flange bottom on oy
    ox, oy, k = 128, 50, 1.0
    def S(xm, zm): return (ox + xm * k, oy - zm * k)
    ft, rh = RG["flange_t"], RG["ring_h"]
    for sg in (-1, 1):
        pts = [(sg * bo / 2, 0), (sg * fo / 2, 0), (sg * fo / 2, ft), (sg * od / 2, ft), (sg * od / 2, ft + rh), (sg * bo / 2, ft + rh)]
        pp = [S(*q) for q in pts]
        c.raw('<polygon points="' + " ".join(f"{x:.2f},{y:.2f}" for x, y in pp) + '" fill="#e6e6e6" stroke="#000" stroke-width="0.5"/>')
    cs = RG["csk"] / 2; hh = RG["screw_hole"] / 2
    pp = [S(sr - hh, 0), S(sr + hh, 0), S(sr + hh, 0.3), S(sr + cs, ft), S(sr - cs, ft), S(sr - hh, 0.3)]
    c.raw('<polygon points="' + " ".join(f"{x:.2f},{y:.2f}" for x, y in pp) + '" fill="#fff" stroke="#000" stroke-width="0.25"/>')
    pline(c, (ox, oy + 3), (ox, oy - (ft + rh) - 3), lw=0.25, dash="3 1 0.8 1")
    a, b = S(-fo / 2 - 3, ft), S(-fo / 2 - 3, ft + rh)
    pline(c, S(-od / 2 - 1, ft + rh), S(-fo / 2 - 5, ft + rh))
    pline(c, a, b); c._head(b[0], b[1], a[0], a[1], 1.4); c._head(a[0], a[1], b[0], b[1], 1.4)
    ptext(c, a[0] - 2, (a[1] + b[1]) / 2, "10", size=3.2, anchor="end", weight="bold")
    leader(c, (fo / 2 - 4 + 0, 0) if False else (0, 0), (0, 0), "") if False else None
    tx, ty = S(fo / 2, ft / 2)
    pline(c, (tx + 0.8, ty), (tx + 5, ty)); ptext(c, tx + 6, ty, "2.5", size=3.2, anchor="start", weight="bold")
    q = S(sr, ft); pline(c, q, (q[0] + 6, q[1] - 10)); ptext(c, q[0] + 6.5, q[1] - 11, "csk", size=3.2, anchor="start")
    ptext(c, ox, oy + 6, "open bottom: the pad bears on the ALEX top", size=3.2)
    ptext(c, ox, oy - (ft + rh) - 20, "Section through one screw hole", size=3.2, weight="bold")
    ptext(c, ox, oy - (ft + rh) - 15.5, "(full size)", size=3.2)
    save(c, "07-ring.svg")


# ---------------- G-10 ALEX top with rings and the corner template ----------------
def fig_alex_rings():
    c = Canvas(178, 78)
    s = 0.11
    ox, oy = 14, 8
    a = D["alex1"]
    W, H = a["w"] * 10 * s, a["d"] * 10 * s
    c.raw(f'<rect x="{ox}" y="{oy}" width="{W:.2f}" height="{H:.2f}" fill="#f2f2f2" stroke="#000" stroke-width="0.5"/>')
    for yy in (50, a["d"] * 10 - 50):
        for xx in (50, a["w"] * 10 - 50):
            cx, cy = ox + xx * s, oy + yy * s
            c.raw(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{RG["flange_od"] / 2 * s:.2f}" fill="#e6e6e6" stroke="#000" stroke-width="0.4"/>')
            c.raw(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{RG["bore"] / 2 * s:.2f}" fill="#fff" stroke="#000" stroke-width="0.4"/>')
    pline(c, (ox, oy + H), (ox + W, oy + H), lw=1.2)
    ptext(c, ox + W / 2, oy + H + 4, "drawer fronts", size=3.2, weight="bold")
    ptext(c, ox + W / 2, oy + H / 2 - 2, "ALEX 1", size=3.2, weight="bold")
    ptext(c, ox + W / 2, oy + H / 2 + 2.5, "from above", size=3.2)
    ptext(c, ox + W + 2, oy + H / 2, "36 × 58 cm", size=3.2, rotate=90)
    # corner template detail
    s2 = 0.45
    tx, ty = 92, 12
    c.raw(f'<rect x="{tx}" y="{ty}" width="56" height="58" fill="#f2f2f2" stroke="none"/>')
    pline(c, (tx, ty), (tx + 56, ty), lw=0.5); pline(c, (tx, ty), (tx, ty + 58), lw=0.5)
    T = 92 * s2
    c.raw(f'<rect x="{tx:.2f}" y="{ty:.2f}" width="{T:.2f}" height="{T:.2f}" fill="#fff" stroke="#000" stroke-width="0.5"/>')
    c.raw(f'<rect x="{tx - 1.6:.2f}" y="{ty - 1.6:.2f}" width="1.6" height="{T + 1.6:.2f}" fill="#808080"/>')
    c.raw(f'<rect x="{tx - 1.6:.2f}" y="{ty - 1.6:.2f}" width="{T + 1.6:.2f}" height="1.6" fill="#808080"/>')
    cx, cy = tx + 50 * s2, ty + 50 * s2
    for d in (RG["od"], RG["bore"]):
        c.raw(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{d / 2 * s2:.2f}" fill="none" stroke="#000" stroke-width="0.25"/>')
    for ang in F["alex_feet_optional"]["screw_angles_deg"]:
        for rr, fill in ((RG["screw_circle_radius"], "#000"), (F["alex_feet_optional"]["screw_circle_radius"], "#fff")):
            hx, hy = cx + rr * s2 * math.cos(math.radians(ang)), cy + rr * s2 * math.sin(math.radians(ang))
            c.raw(f'<circle cx="{hx:.2f}" cy="{hy:.2f}" r="0.9" fill="{fill}" stroke="#000" stroke-width="0.4"/>')
    c.raw(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="0.5" fill="#000"/>')
    pline(c, (cx, cy), (cx, ty - 2)); pline(c, (cx, cy), (tx - 2, cy))
    dim(c, (cx, ty - 2), (tx, ty - 2), "5 cm", 3)
    dim(c, (tx - 2, ty), (tx - 2, cy), "50", 3) if False else dim(c, (tx - 2, cy), (tx - 2, ty), "5 cm", -3)
    X = tx + 60
    ptext(c, X, ty + 4, "fences against", size=3.2, anchor="start"); ptext(c, X, ty + 8.5, "both edges", size=3.2, anchor="start")
    h45 = (cx + RG["screw_circle_radius"] * s2 * 0.7071, cy + RG["screw_circle_radius"] * s2 * 0.7071)
    pline(c, (h45[0] + 0.8, h45[1] + 0.8), (X - 1, ty + 22))
    for i, t in enumerate(("● ring screws:", "5/64 in bit,", "r 33 mm")):
        ptext(c, X, ty + 22 + 4.2 * i, t, size=3.2, anchor="start")
    for i, t in enumerate(("○ inner holes:", "r 14.5 mm, for", "optional ALEX", "feet (bottom)")):
        ptext(c, X, ty + 37 + 4.2 * i, t, size=3.2, anchor="start")
    ptext(c, tx + 28, ty + 64, "ALEX corner template on a corner", size=3.2, weight="bold")
    save(c, "07-alex-rings.svg")


# ---------------- rails screwed to the tops ----------------
def fig_rails_plan():
    s = 0.6
    c, T = layout_top("A", "", s, (10, 16), (178, 68), rail_line=False)
    ra = D["railA"]
    q0, q1 = T(ra["x0"], ra["y0"]), T(ra["x1"], ra["y1"])
    c.rect(min(q0[0], q1[0]), q0[1], abs(q1[0] - q0[0]), q1[1] - q0[1], fill="#bfbfbf", lw="outline")
    for i, h in enumerate(ra["holes"]):
        end = i in (0, len(ra["holes"]) - 1)
        c.circle(T(ra["x0"] + h, ra["y0"] + D["holeOffset"]), 1.0 if end else 0.6, fill="#000" if end else "#fff", lw="thin")
    for x, anc in ((ra["x0"] + 11, "end"), ((ra["x0"] + ra["x1"]) / 2, "end"), (ra["x1"] - 9, "start")):
        dim(c, T(x, ra["y1"]), T(x, A["y1"]), "", 0, ext=False)
        q = c.P(*T(x, (ra["y1"] + A["y1"]) / 2)); ptext(c, q[0] + (1.2 if anc == "start" else -1.2), q[1], "12 cm", size=3.2, anchor=anc)
    ptext(c, *c.P(A["x1"] / 2, -9.5 / s), "top A face down, back edge away from you, x grows to the left", size=3.2, weight="bold")
    ptext(c, *c.P(A["x1"] / 2, A["y1"] + 4.5 / s), "front edge (rounded)", size=3.2)
    ptext(c, *c.P(A["x1"] + 4.5 / s, A["y1"] / 2), "side-wall end · x = 0", size=3.2, rotate=90)
    q = c.P(*T(4, A["y1"])); leader(c, T(ra["x0"] + 0.3, ra["y1"] - 0.5), (q[0], q[1] + 4.5), "wall end at x = 1 cm", anchor="end")
    leader(c, T(ra["x1"] - 40, ra["y0"] + D["holeOffset"]), c.P(*T(150, 30)), "● end screws first", anchor="start")
    save(c, "07-rails-plan.svg")


def fig_rails_detail():
    c = Canvas(178, 76)
    # (a) section across rail A, the top face down (mm); horizontal = y, vertical = height above the blanket
    k = 0.34
    Y0 = 420
    def S(y, z): return (6 + (y - Y0) * k, 58 - z * k)
    t = F["tops"]["thickness"]; L = F["steel"]["leg"]; th = F["steel"]["thickness"]
    yf, yv = D["railA"]["y0"] * 10, D["railA"]["y1"] * 10
    def poly(pts, fill, lw=0.5):
        c.raw('<polygon points="' + " ".join(f"{x:.2f},{y:.2f}" for x, y in (S(*p) for p in pts)) + f'" fill="{fill}" stroke="#000" stroke-width="{lw}"/>')
    slab = [(Y0, 0), (650, 0), (650, t), (Y0, t)]
    poly(slab, "#fff"); c.hatch([S(*p) for p in slab], spacing=1.6)
    pline(c, S(Y0, 0), S(650, 0), lw=0.8)
    poly([(yf, t), (yv, t), (yv, t + L), (yv - th, t + L), (yv - th, t + th), (yf, t + th)], "#bfbfbf")
    ys = yf + F["steel"]["screw_line_from_free_edge"]
    # puck on the flat leg, bit 20 mm into the wood
    pw, ph = 18, 20
    poly([(ys - pw / 2, t + th), (ys + pw / 2, t + th), (ys + pw / 2, t + th + ph), (ys - pw / 2, t + th + ph)], "#e6e6e6")
    poly([(ys - 0.8, t - 20), (ys + 0.8, t - 20), (ys + 0.8, t + th + ph), (ys - 0.8, t + th + ph)], "#808080", lw=0.25)
    poly([(ys - 6, t + th + ph), (ys + 6, t + th + ph), (ys + 6, t + th + ph + 16), (ys - 6, t + th + ph + 16)], "#bfbfbf")
    q = S(ys - pw / 2, t + th + ph / 2); pline(c, (q[0], q[1]), (q[0] - 3, q[1])); ptext(c, q[0] - 3.5, q[1], "25 RAIL puck", size=3.2, anchor="end")
    # 12 cm to the front edge
    a, b = S(yv, t + L + 8), S(650, t + L + 8)
    pline(c, S(yv, t + L + 1), S(yv, t + L + 10)); pline(c, S(650, t + 1), S(650, t + L + 10))
    pline(c, a, b); c._head(a[0], a[1], b[0], b[1], 1.5); c._head(b[0], b[1], a[0], a[1], 1.5)
    ptext(c, (a[0] + b[0]) / 2, a[1] - 2.4, "12 cm to the outer face", size=3.2)
    q = S(560, 0); ptext(c, q[0], q[1] + 3.5, "top, laminate down on the blanket", size=3.2)
    ptext(c, S(yv, 0)[0] + 2, S(0, t + 32)[1], "vertical leg", size=3.2, anchor="start")
    pline(c, S(yv, t + 30), (S(yv, 0)[0] + 1.6, S(0, t + 32)[1]))
    ptext(c, 6, 72, "(a) rail A in section: pilot 1/8 in, 20 mm into the wood", size=3.2, anchor="start", weight="bold")
    # (b) rail B at the joint end, face down (x grows to the left), plan
    s2 = 0.62
    def P(x, y): return (126 + (65 - x) * s2, 8 + (y - 50) * s2)
    def rect(x0, x1, y0, y1, fill="none", lw=0.5, dash=None):
        p, q = P(x0, y0), P(x1, y1)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        c.raw(f'<rect x="{min(p[0], q[0]):.2f}" y="{min(p[1], q[1]):.2f}" width="{abs(q[0] - p[0]):.2f}" height="{abs(q[1] - p[1]):.2f}" fill="{fill}" stroke="#000" stroke-width="{lw}"{d}/>')
    rect(0, 65, 65, 130, fill="#f2f2f2")
    pline(c, P(65, 65), P(0, 65), lw=0.5); pline(c, P(0, 65), P(0, 130), lw=1.2)
    rb = D["railB"]
    rect(rb["x0"], rb["x1"], rb["y0"], 130, fill="#bfbfbf")
    for i, h in enumerate(rb["holes"][:4]):
        y = rb["y0"] + h
        p = P(rb["x0"] + D["holeOffset"], y)
        c.raw(f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="0.8" fill="{"#fff" if i < 2 else "#000"}" stroke="#000" stroke-width="0.3"/>')
    a, b = P(rb["x1"] + 3, rb["y0"]), P(rb["x1"] + 3, 65)
    pline(c, P(rb["x1"], rb["y0"]), P(rb["x1"] + 5, rb["y0"]))
    pline(c, a, b); c._head(a[0], a[1], b[0], b[1], 1.4); c._head(b[0], b[1], a[0], a[1], 1.4)
    ptext(c, a[0] - 1.5, (a[1] + b[1]) / 2, "12 cm", size=3.2, anchor="end")
    ptext(c, 146, 62, "○ holes 1, 2: chapter H", size=3.2); ptext(c, 146, 66.5, "● holes 3–10: screw now", size=3.2)
    ptext(c, *P(32, 69), "joint end", size=3.2)
    ptext(c, P(0, 100)[0] + 4, P(0, 100)[1], "side-wall edge", size=3.2, rotate=90)
    ptext(c, 146, 72, "(b) rail B at top B's joint end", size=3.2, weight="bold")
    save(c, "07-rails-detail.svg")


# ---------------- G-11 ALEX placement by the walls ----------------
STAGE = 5    # cm: ALEX 2 stands 5 cm short of its final place until chapter G (build manual step 5)


def fig_alex_place():
    s = 0.34
    g = D["gap"]
    c = Canvas(120, 127, scale=s, origin=(-g - 16 / s, -g - 12 / s))
    wall_hatch(c, (-g, -g), (A["x1"] + 6, -g), (0, -1))
    wall_hatch(c, (-g, -g), (-g, B["y1"] + 26), (-1, 0))
    ptext(c, *c.P(120, -g - 13), "back wall", size=3.2, weight="bold")
    ptext(c, *c.P(-g - 13, 150), "side wall", size=3.2, weight="bold", rotate=-90)
    c.poly([(0, 0), (A["x1"], 0), (A["x1"], A["y1"]), (B["x1"], A["y1"]), (B["x1"], B["y1"]), (0, B["y1"])], lw="thin", dash="4 1 0.8 1 0.8 1")
    ptext(c, *c.P(32, 190), "tops come later (outline)", size=3.2, rotate=-90)
    a1, a2 = D["alex1"], D["alex2"]
    y2 = a2["y0"] + STAGE
    c.rect(a1["x0"], a1["y0"], a1["w"], a1["d"], fill="#e6e6e6")
    c.rect(a2["x0"], a2["y0"], a2["w"], a2["d"], lw="thin", dash="1.5 1")      # final place, chapter G
    c.rect(a2["x0"], y2, a2["w"], a2["d"], fill="#e6e6e6")
    c.line((a1["x0"], a1["y0"] + a1["d"]), (a1["x0"] + a1["w"], a1["y0"] + a1["d"]), lw="heavy")
    c.line((a2["x0"] + a2["w"], y2), (a2["x0"] + a2["w"], y2 + a2["d"]), lw="heavy")
    ptext(c, *c.P(a1["x0"] + 18, 32.5), "1", size=4.5, weight="bold")
    ptext(c, *c.P(32.5, y2 + 18), "2", size=4.5, weight="bold")
    c.arrow((a1["x0"] + 18, 70), (a1["x0"] + 18, 88)); ptext(c, *c.P(a1["x0"] + 4, 96), "drawers", size=3.2)
    ptext(c, *c.P(a1["x0"] + 4, 96 + 4.2 / s), "toward you", size=3.2)
    c.arrow((70, y2 + 18), (90, y2 + 18)); ptext(c, *c.P(96, y2 + 12), "door toward you", size=3.2, anchor="start")
    ptext(c, *c.P(96, y2 + 32), "staged 5 cm out;", size=3.2, anchor="start")
    ptext(c, c.P(96, 0)[0], c.P(0, y2 + 32)[1] + 4.2, "dashed: its final place", size=3.2, anchor="start")
    L = LAY["alex_by_walls"]
    leader(c, (240, a1["y0"] / 2 - g / 2), c.P(250, 12), cm(L["alex1_back_off_back_wall"]) + " cm", anchor="start")
    dim(c, (-g, 110), (a1["x0"], 110), cm(L["alex1_near_side_from_side_wall"]) + " cm", 3)
    xg = a2["x0"] / 2 - g / 2
    pline(c, c.P(xg, y2 + 10), c.P(xg, y2 + a2["d"] + 6)); c.raw('<circle cx="%.2f" cy="%.2f" r="0.6"/>' % c.P(xg, y2 + 10))
    q = c.P(xg, y2 + a2["d"] + 10); ptext(c, q[0] + 1, q[1], cm(L["alex2_side_off_side_wall"]) + " cm", size=3.2, anchor="start")
    dim(c, (110, -g), (110, y2), cm(L["alex2_near_end_from_back_wall"] + STAGE) + " cm (staged)", -3)
    save(c, "07-alex-place.svg")


def fig_wall_gauge():
    s = 0.42
    c = Canvas(44, 44, scale=s, origin=(-8 / s, -6 / s))
    pline(c, c.P(0, -10), c.P(0, 80), lw=0.8)
    for k in range(0, 90, 5):
        pline(c, c.P(0, k - 10), c.P(-2.4 / s, k - 10 + 2.4 / s), lw=0.2)
    c.poly([(0, 0), (65, 0), (65, 14), (14, 14), (14, 30), (0, 30)], fill="#bfbfbf")
    c.rect(65, -6, 10, 46, fill="#e6e6e6")
    ptext(c, *c.P(70, 17), "ALEX", size=3.2, rotate=-90)
    ptext(c, *c.P(40, 7), "6.5 cm leg", size=3.2, weight="bold")
    ptext(c, *c.P(4, 52), "6.5 cm: ALEX to wall", size=3.2, anchor="start")
    ptext(c, *c.P(4, 52 + 4.4 / s), "3 cm: top to wall", size=3.2, anchor="start")
    ptext(c, *c.P(4, 52 + 8.8 / s), "(raw edge)", size=3.2, anchor="start")
    save(c, "07-wall-gauge.svg")


# ---------------- G-12 cross-section: top, feet plate, foot, pad in ring, ALEX top ----------------
def fig_section():
    s = 0.72
    c = Canvas(178, 156, scale=s, origin=(-104, -48), flip_y=True)
    top_t = F["tops"]["thickness"]; fh = F["heights_mm"]["foot_height"]
    fo, od, bo, sr, ft, rh = RG["flange_od"], RG["od"], RG["bore"], RG["screw_circle_radius"], RG["flange_t"], RG["ring_h"]
    pad = FE["body_and_pad_diameter"]; P = FE["plate"]; hs = FE["plate_hole_spacing"] / 2
    alex_t = 15.9   # ALEX top panel, 5/8 in, VERIFIED 23 Oct 2026 (facts.rings.confidence)
    # ALEX top panel (cut, hatched)
    pts = [(-70, -alex_t), (52, -alex_t), (52, 0), (-70, 0)]
    c.poly(pts, fill="#fff"); c.hatch(pts, spacing=1.8)
    # top (cut, hatched)
    pts = [(-70, fh), (52, fh), (52, fh + top_t), (-70, fh + top_t)]
    c.poly(pts, fill="#fff"); c.hatch(pts, spacing=1.8, angle=135)
    for y in (fh + top_t,):
        c.line((-70, y), (52, y), lw="heavy")
    # ring halves (cut)
    for sg in (-1, 1):
        rp = [(sg * bo / 2, 0), (sg * fo / 2, 0), (sg * fo / 2, ft), (sg * od / 2, ft), (sg * od / 2, ft + rh), (sg * bo / 2, ft + rh)]
        c.poly(rp, fill="#bfbfbf")
    # ring screw on the right, #6 flat head, 13 into the ALEX
    c.poly([(sr - 3.5, ft), (sr + 3.5, ft), (sr + 1.9, 0), (sr - 1.9, 0)], fill="#000", lw="thin")
    c.rect(sr - 1.6, -13.4, 3.2, 13.4, fill="#808080", lw="thin")
    c.rect(sr - 1.0, -12, 2.0, 12, lw="thin", dash="0.8 0.6")
    # foot: pad, stem, body (not to the maker's drawing; only the 102 and the 50 are known)
    c.rect(-pad / 2, 0, pad, 9, fill="#808080")
    c.rect(-6, 9, 12, 22, fill="#fff")
    for k in range(10, 31, 3):
        c.line((-6, k), (6, k + 1.5), lw="thin")
    c.rect(-pad / 2, 31, pad, fh - 2 - 31, fill="#e6e6e6")
    # feet plate and its #8 screws, 14 into the top
    c.rect(-P / 2, fh - 2, P, 2, fill="#808080")
    for sx in (-hs, hs):
        c.rect(sx - 3.8, fh - 5, 7.6, 3, fill="#000", lw="thin")
        c.rect(sx - 1.6, fh, 3.2, 14, fill="#808080", lw="thin")
        c.rect(sx - 1.1, fh, 2.2, 15, lw="thin", dash="0.8 0.6")
    # 21 mm limit line
    c.line((-70, fh + F["tops"]["max_fastener_depth"]), (52, fh + F["tops"]["max_fastener_depth"]), lw="thin", dash="2 1")
    # dimensions (object = mm)
    def vdim(x, z0, z1, lab, side=-1, bold=True):
        a, b = c.P(x, z0), c.P(x, z1)
        pline(c, a, b); c._head(b[0], b[1], a[0], a[1], 1.5); c._head(a[0], a[1], b[0], b[1], 1.5)
        ptext(c, a[0] + side * 2.6, (a[1] + b[1]) / 2, lab, size=3.2, weight="bold" if bold else "normal", rotate=-90)
    def ext(x0, x1, z):
        pline(c, c.P(x0, z), c.P(x1, z))
    ext(-71, -92, 0); ext(-71, -92, fh); ext(-71, -92, fh + top_t)
    vdim(-88, 0, fh, "102 mm (gauge)"); vdim(-88, fh, fh + top_t, "28 mm")
    def hdim(z, x0, x1, lab, below=True):
        a, b = c.P(x0, z), c.P(x1, z)
        pline(c, a, b); c._head(b[0], b[1], a[0], a[1], 1.5); c._head(a[0], a[1], b[0], b[1], 1.5)
        ptext(c, (a[0] + b[0]) / 2, a[1] + (2.6 if below else -2.6), lab, size=3.2, weight="bold")
    for x in (-fo / 2, fo / 2): pline(c, c.P(x, -1), c.P(x, -alex_t - 22))
    for x in (-od / 2, od / 2): pline(c, c.P(x, -1), c.P(x, -alex_t - 14))
    for x in (-bo / 2, bo / 2): pline(c, c.P(x, -1), c.P(x, -alex_t - 6))
    hdim(-alex_t - 4, -bo / 2, bo / 2, f"⌀{bo:g} bore")
    hdim(-alex_t - 12, -od / 2, od / 2, f"⌀{od:g} ring")
    hdim(-alex_t - 20, -fo / 2, fo / 2, "⌀75 flange")
    hdim(fh + top_t + 6, -P / 2, P / 2, "59.5 plate", below=False)
    for x in (-P / 2, P / 2): pline(c, c.P(x, fh), c.P(x, fh + top_t + 8))
    # right-hand labels, two lines each
    def lab(target, tz, l1, l2):
        leader(c, target, c.P(60, tz), l1, anchor="start")
        q = c.P(60, tz); ptext(c, q[0] + 1.2, q[1] + 4.2, l2, size=3.2, anchor="start")
    lab((hs + 1.6, fh + 8), 152, "#8 × 5/8 pan head (H02):", "14 mm into the top, pilot 15 mm")
    lab((50, fh + F["tops"]["max_fastener_depth"]), 131, "21 mm: deepest any screw", "may go into the top")
    lab((P / 2 - 2, fh - 1), 110, "feet plate (P09), screwed", "to the top's underside")
    lab((pad / 2 - 1, 70), 89, "foot, wound out to 102 mm", "with the gauge")
    lab((od / 2, ft + rh - 2), 47, "printed ring (P10): 10 mm", "tall on a 2.5 mm flange")
    lab((pad / 2 - 4, 6), 68, "pad ⌀50: bears on the", "ALEX top inside the ring")
    lab((sr + 1.6, -7), 22, "#6 × 5/8 flat head (H06): 13.4 mm", "into the ALEX top, pilot 12 mm")
    lab((48, -alex_t / 2), 0, "ALEX top panel 15.9 mm (5/8 in):", "2.5 mm stays under the screw")
    save(c, "07-section.svg")


# ---------------- G-13 load path ----------------
def fig_loadpath():
    c = Canvas(178, 104)
    def box(x, y, w, h, lines, fill="#fff", dash=None, lw=0.5):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        c.raw(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#000" stroke-width="{lw}" rx="1"{d}/>')
        n = len(lines)
        for i, t in enumerate(lines):
            ptext(c, x + w / 2, y + h / 2 + (i - (n - 1) / 2) * 4.0, t, size=3.2, weight="bold" if i == 0 else "normal")
    arr = lambda p, q: c.arrow(p, q, lw="outline", head=2.0)
    box(44, 2, 90, 11, ["Tops A and B", "you, monitors, PC, everything on the desk"], fill="#e6e6e6")
    box(2, 24, 46, 14, ["6 OLOV legs", "wall edges, M4 screws"])
    box(56, 24, 62, 14, ["Rails A and B", "front edges, #10 screws"])
    box(126, 24, 50, 14, ["8 feet plates F1–F8", "#8 screws, 14 mm in"])
    arr((60, 13), (25, 24)); arr((89, 13), (87, 24)); arr((118, 13), (151, 24))
    box(56, 46, 62, 14, ["Corner: rail B hangs", "from rail A on 2 fittings"])
    arr((87, 38), (87, 46))
    box(56, 67, 62, 16, ["Rail ends load the top", "A ends 0.5 cm from F1/F3", "B ends 13.5 cm from F5/F6"])
    arr((87, 60), (87, 67))
    box(126, 46, 50, 14, ["Feet, wound to 102 mm", "pads bear on the ALEX top"])
    arr((151, 38), (151, 46))
    pline(c, (118, 75), (122, 75), lw=0.5); pline(c, (122, 75), (122, 53), lw=0.5); c.arrow((122, 53), (126, 53), head=2.0)
    box(126, 68, 50, 14, ["Rings on the ALEX tops", "hold the pads sideways"])
    arr((151, 60), (151, 68))
    box(126, 88, 50, 12, ["ALEX 1 and ALEX 2", "then the floor"])
    arr((151, 82), (151, 88))
    box(2, 88, 46, 12, ["Floor"])
    arr((25, 38), (25, 88))
    box(56, 88, 62, 12, ["NEVER: a rail on a cabinet", "rail 75.1 cm up, ALEX top 70 cm"], dash="2 1", lw=0.8)
    save(c, "07-loadpath.svg")


def fig_rail_ends():
    c = Canvas(178, 63)
    s = 1.45
    def rect(P, x0, x1, y0, y1, fill="none", lw=0.5, dash=None):
        a, b = P(x0, y0), P(x1, y1)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        c.raw(f'<rect x="{min(a[0], b[0]):.2f}" y="{min(a[1], b[1]):.2f}" width="{abs(b[0] - a[0]):.2f}" height="{abs(b[1] - a[1]):.2f}" fill="{fill}" stroke="#000" stroke-width="{lw}"{d}/>')
    h = FE["plate"] / 20
    # (a) rail A's far end over ALEX 1, plan: x 196..249, y 40..65
    Pa = lambda x, y: (6 + (x - 196) * s, 9 + (y - 40) * s)
    a1, ra = D["alex1"], D["railA"]
    rect(Pa, 196, 249, 40, 65, fill="#f2f2f2")
    rect(Pa, a1["x0"], a1["x0"] + a1["w"], 40, a1["y0"] + a1["d"], dash="2 1")
    rect(Pa, 196, ra["x1"], ra["y0"], ra["y1"], fill="#bfbfbf")
    for n, x, y, t in D["feet"]:
        if n in ("F3", "F4"):
            rect(Pa, x - h, x + h, y - h, y + h, fill="#fff")
            p = Pa(x, y); ptext(c, p[0], p[1], n, size=3.2, weight="bold")
    p = Pa(ra["x1"], ra["y0"]); pline(c, p, (p[0], 5.5)); ptext(c, p[0], 3.2, "rail end", size=3.2)
    ptext(c, *Pa(203, 50.5), "rail A", size=3.2, weight="bold")
    ptext(c, *Pa(232, 45), "ALEX 1 below", size=3.2)
    ptext(c, 44, 50, "(a) rail A's far end, plan", size=3.2, weight="bold")
    ptext(c, 44, 55, "rail end x 214 cm", size=3.2); ptext(c, 44, 59.5, "F1/F3 centres x 214.5 cm", size=3.2)
    # (b) rail B's end before ALEX 2, plan; y 256..290 runs to the right
    Pb = lambda x, y: (98 + (y - 256) * s * 1.55, 9 + (65 - x) * s)   # seen from above: x up, y right (a quarter turn, not a mirror)
    rb, a2 = D["railB"], D["alex2"]
    rect(Pb, 40, 65, 256, 290, fill="#f2f2f2")
    rect(Pb, 40, a2["x0"] + a2["w"], a2["y0"], 290, dash="2 1")
    rect(Pb, rb["x0"], rb["x1"], 256, rb["y1"], fill="#bfbfbf")
    f6 = [f for f in D["feet"] if f[0] == "F6"][0]
    rect(Pb, f6[1] - h, f6[1] + h, f6[2] - h, f6[2] + h, fill="#fff")
    p = Pb(f6[1], f6[2]); ptext(c, p[0], p[1], "F6", size=3.2, weight="bold")
    e = Pb(rb["x0"], rb["y1"]); pline(c, e, (e[0], 2)); pline(c, (p[0], p[1] - 4.5), (p[0], 2))
    a, b = (e[0], 3.5), (p[0], 3.5)
    pline(c, a, b); c._head(b[0], b[1], a[0], a[1], 1.5); c._head(a[0], a[1], b[0], b[1], 1.5)
    ptext(c, (a[0] + b[0]) / 2, 6.3, "13.5 cm", size=3.2, weight="bold")
    ptext(c, *Pb(50.4, 262), "rail B", size=3.2, weight="bold")
    ptext(c, *Pb(44.5, 283), "ALEX 2", size=3.2)
    ptext(c, *Pb(63, 285), "front edge", size=3.2)
    ptext(c, 136, 50, "(b) rail B's end, plan (front edge at the top)", size=3.2, weight="bold")
    ptext(c, 136, 55, "rail end y 266 cm · ALEX 2 face y 274.5 cm", size=3.2); ptext(c, 136, 59.5, "F5/F6 centres y 279.5 cm", size=3.2)
    save(c, "07-rail-ends.svg")


def fig_rail_elev():
    s = 1.3
    c = Canvas(178, 42)
    E = lambda x, z: (12 + (x - 186) * s, 5 + (84 - z) * s)
    def Re(x0, x1, z0, z1, fill="none", lw=0.5):
        a, b = E(x0, z0), E(x1, z1)
        c.raw(f'<rect x="{min(a[0], b[0]):.2f}" y="{min(a[1], b[1]):.2f}" width="{abs(b[0] - a[0]):.2f}" height="{abs(b[1] - a[1]):.2f}" fill="{fill}" stroke="#000" stroke-width="{lw}"/>')
    a1 = D["alex1"]
    Re(a1["x0"], a1["x0"] + a1["w"], 59, ALEX_H, fill="#e6e6e6")
    for x in (214.5, 240.5):
        Re(x - 2.5, x + 2.5, ALEX_H, Z0 - 0.2, fill="#fff", lw=0.25)
        Re(x - 2.975, x + 2.975, Z0 - 0.2, Z0, fill="#808080", lw=0.25)
        Re(x - 3.75, x + 3.75, ALEX_H, ALEX_H + 0.25, fill="#bfbfbf", lw=0.25)
    Re(186, 249, Z0, Z1, fill="#f2f2f2")
    Re(186, D["railA"]["x1"], RAIL_LOW, Z0, fill="#bfbfbf")
    for z, t in ((Z1, "83.0 cm surface"), (Z0, "80.2 cm underside"), (RAIL_LOW, "75.1 cm rail lower edge"), (ALEX_H, "70.0 cm ALEX top (ASSUMPTION)")):
        p = E(249, z); pline(c, (p[0] + 1, p[1]), (p[0] + 9, p[1]))
        ptext(c, p[0] + 10, p[1] + (1.2 if z == Z0 else (-1.2 if z == Z1 else 0)), t, size=3.2, anchor="start")
    a, b = E(195, ALEX_H), E(195, RAIL_LOW)
    pline(c, E(192, ALEX_H), E(a1["x0"], ALEX_H), lw=0.25, dash="1 0.6")
    pline(c, a, b); c._head(a[0], a[1], b[0], b[1], 1.4); c._head(b[0], b[1], a[0], a[1], 1.4)
    ptext(c, a[0] + 1.5, (a[1] + b[1]) / 2 + 0.3, "air", size=3.2, anchor="start", weight="bold")
    p = E(199, (RAIL_LOW + Z0) / 2); ptext(c, p[0], p[1], "rail A", size=3.2, weight="bold")
    p = E(227.5, 75.2); ptext(c, p[0], p[1], "feet", size=3.2)
    p = E(a1["x0"] + 18, 64); ptext(c, p[0], p[1], "ALEX 1", size=3.2, weight="bold")
    save(c, "07-rail-elev.svg")


# ---------------- G-14 complete underside, assembled (x-ray plan from above) ----------------
def fig_underside():
    s = 0.58
    g = D["gap"]
    c = Canvas(178, 200, scale=s, origin=(-g - 12 / s, -g - 8 / s))
    c.rect(0, 0, A["x1"], A["y1"], fill="#fff", lw="thin")
    c.rect(0, B["y0"], B["x1"], B["y1"] - B["y0"], fill="#fff", lw="thin")
    c.line((0, 0), (A["x1"], 0), lw="heavy"); c.line((0, 0), (0, B["y1"]), lw="heavy")
    plan_items(c, lambda x, y: (x, y), hidden=False)
    # rail screws
    for h in D["railA"]["holes"]:
        c.circle((D["railA"]["x0"] + h, D["railA"]["y0"] + D["holeOffset"]), 0.6, fill="#000", lw="thin")
    for h in D["railB"]["holes"]:
        c.circle((D["railB"]["x0"] + D["holeOffset"], D["railB"]["y0"] + h), 0.6, fill="#000", lw="thin")
    # joining plates
    for n, x in D["plates"]:
        c.rect(x - D["plateW"] / 2, D["plateY"] - D["plateL"] / 2, D["plateW"], D["plateL"], fill="#808080", lw="thin")
    # corner fittings (two L brackets at rail B's end)
    fl = D["fitting"]["legs"]
    c.poly([(53, 53), (53 + fl, 53), (53 + fl, 53.6), (53.6, 53.6), (53.6, 53 + fl), (53, 53 + fl)], fill="#000", lw="thin")
    c.poly([(52.5, 53), (52.5 - fl, 53), (52.5 - fl, 53.6), (51.9, 53.6), (51.9, 53 + fl), (52.5, 53 + fl)], fill="#000", lw="thin")
    # rings on the ALEX tops
    for n, x, y, t in D["feet"]:
        c.circle((x, y), RG["flange_od"] / 20, lw="thin", dash="1 0.6")
    ptext(c, *c.P(227.5, 32.5), "ALEX 1", size=3.2, weight="bold")
    ptext(c, *c.P(32, 292.5), "ALEX 2", size=3.2, weight="bold")
    for n, x, y, *_ in D["legs"]:
        ptext(c, *c.P(x + 7.5, y + 0.6), n, size=3.2, weight="bold", anchor="start")
    q = c.P(0, 0); c.raw(f'<circle cx="{q[0]:.2f}" cy="{q[1]:.2f}" r="1.3" fill="#000"/>'); ptext(c, q[0] - 2, q[1] + 3.5, "datum", size=3.2, anchor="end")
    bl = [((140, 10), (150, 22), "P05"), ((150, 50.5), (150, 80), "P06"), ((50.5, 200), (90, 200), "P07"),
          ((53.3, 57), (95, 100), "P08"), ((214.5, 56.5), (205, 95), "P09"), ((56.5, 305.5), (90, 300), "P10"),
          ((35, 72), (95, 140), "P11"), ((30, 4), (75, 30), "P11"), ((240.5, 50), (240, 90), "P03"),
          ((50, 274.5), (90, 270), "P04"), ((80, 49.8), (80, 85), "H03"), ((49.8, 263.5), (90, 240), "H03")]
    for t, p, n in bl:
        pballoon(c, t, c.P(*p), n)
    ptext(c, *c.P(130, 140), "Seen from above, through the tops", size=3.2, anchor="start", weight="bold")
    ptext(c, *c.P(130, 148), "(not a face-down view: nothing is mirrored)", size=3.2, anchor="start")
    save(c, "07-underside.svg")


if __name__ == "__main__":
    os.makedirs(FIG, exist_ok=True)
    fig_orient(); fig_layout_a(); fig_layout_b(); fig_leg_jig(); fig_leg_steps(); fig_feet_plate(); fig_feet_jigs(); fig_foot_gauge()
    fig_ring(); fig_alex_rings(); fig_rails_plan(); fig_rails_detail(); fig_alex_place(); fig_wall_gauge(); fig_section(); fig_loadpath(); fig_rail_ends(); fig_rail_elev(); fig_underside()
    print("figures_07: done")
