#!/usr/bin/env python3
"""Drilling and placement templates (T0-T6): figures, page fragments and a geometry self-check.

    python3 manual/src/figures_T.py && python3 manual/build.py templates --render --dpi=60

Writes manual/figures/T-*.svg and manual/src/templates/NN-*.html (generated: edit this file, not them).
Every SVG is a scale=1 Canvas in true page millimetres and is placed with style="width:<W>mm", so the
printed sheet is 1:1. After drawing, check() re-reads each saved SVG, measures every hole against the
sheet's datum lines and asserts it matches the position recomputed from facts.json / data.json and the
parts' .scad sources. The table is printed on stdout.
"""
import json, math, os, re, sys, textwrap

HERE = os.path.dirname(os.path.abspath(__file__)); MAN = os.path.dirname(HERE); REPO = os.path.dirname(MAN)
sys.path.insert(0, MAN)
from lib.draw import Canvas, badge, warning_panel, FONT, _f

F = json.load(open(os.path.join(MAN, "facts.json")))
D = json.load(open(os.path.join(MAN, "data.json")))
FIG = os.path.join(MAN, "figures"); TPL = os.path.join(HERE, "templates")
REV = "2026-10-23"
SRC = F["source_commit"]


def scad(rel, name):
    """A numeric assignment from a parts/.scad file (provenance check)."""
    m = re.search(rf"^\s*(?:.*;\s*)?{name}\s*=\s*([-\d.]+)\s*;", open(os.path.join(REPO, "parts", rel)).read(), re.M)
    return float(m.group(1))


# ---------- source numbers, cross-checked against the parts' own geometry files ----------
RING = F["rings"]
ring_r = scad("structure/foot-ring.scad", "screw_r")
assert ring_r == scad("tools/alex-corner-template.scad", "screw_r")   # paper sheet, printed template and ring drill the same circle
assert ring_r == RING["screw_circle_radius"] and RING["od"] == scad("structure/foot-ring.scad", "pad_d") + scad("structure/foot-ring.scad", "clearance") + 2 * scad("structure/foot-ring.scad", "wall")
assert RING["flange_od"] == scad("structure/foot-ring.scad", "flange_od")
assert scad("tools/alex-corner-template.scad", "inset") == RING["centre_from_alex_corner"]
AF = F["alex_feet_optional"]
_tpl = open(os.path.join(REPO, "parts", "tools", "alex-corner-template.scad")).read()
assert len(set(re.findall(r"i \* 360 / n_screws \+ ([\d.]+)", _tpl))) == 1   # ring and foot holes share one offset
_o = float(re.search(r"i \* 360 / n_screws \+ ([\d.]+)", _tpl).group(1))
RING_ANGLES = [int(i * 120 + _o) for i in range(3)]   # as the printed ALEX corner template drills them: 45/165/285
assert RING_ANGLES == AF["screw_angles_deg"]
assert scad("accessories/alex-foot.scad", "screw_r") == AF["screw_circle_radius"] == scad("tools/alex-corner-template.scad", "foot_r")
FEET = F["feet"]
assert scad("tools/feet-corner-jig.scad", "hole_sp") == FEET["plate_hole_spacing"] and scad("tools/feet-corner-jig.scad", "plate") == FEET["plate"]
assert abs(FEET["between_holes_inside_jaws"] + FEET["plate_hole_diameter"] - FEET["plate_hole_spacing"]) < 1e-9
assert abs(FEET["across_holes_outside_jaws"] - FEET["plate_hole_diameter"] - FEET["plate_hole_spacing"]) < 1e-9
FOOT_IN = scad("tools/feet-corner-jig.scad", "inset")
assert FOOT_IN == round((D["feet"][1][2]) * 10, 6) == 85   # F2 y 8.5 cm
OLOV = F["olov"]
assert scad("tools/leg-jig.scad", "r") == OLOV["hole_circle_radius"] and scad("tools/leg-jig.scad", "n") == OLOV["holes"]
assert D["legs"][1][2] * 10 == 100 and D["legs"][0][1] * 10 == 150   # L2 y 10 cm, L1 x 15 cm
ST = F["steel"]
RAILS = {"A": [round(v * 10, 1) for v in D["railA"]["holes"]], "B": [round(v * 10, 1) for v in D["railB"]["holes"]]}
assert RAILS["A"] == [round(v * 10, 1) for v in ST["railA"]["holes_from_wall_end_cm"]] and RAILS["B"] == [round(v * 10, 1) for v in ST["railB"]["holes_from_corner_end_cm"]]
SCREW_LINE = ST["screw_line_from_free_edge"]; assert SCREW_LINE == D["holeOffset"] * 10
BOUGHT = float(re.search(r"= ([\d.]+) mm", ST["purchased_as"]).group(1))
BITS = {"5/64": (2.0, "5/64 in"), "1/8": (3.2, "1/8 in"), "7/32": (5.56, "7/32 in")}

HOLES = []      # recorded while drawing: (svg, id, kind, expected (u, v), expected d, source)
CHECKS = []     # filled by check()


# ---------- drawing helpers (page mm, y down) ----------
# Every text and every mark (hole crosshair, ruler, edge line) registers a box on the canvas; save() refuses a
# sheet where text overlaps text or a mark, or anything leaves the canvas. Text width is estimated at 0.58 em.
EM = 0.58


def reg(c, kind, x0, y0, x1, y1, grp=None, what=""):
    if not hasattr(c, "boxes"):
        c.boxes = []
    c.boxes.append((kind, min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1), grp, what))


def ring(c, ctr, r, **kw):
    """Dashed reference circle, registered so no text may cross its outline."""
    c.circle(ctr, r, lw="thin", dash="0.8 0.6", **kw); reg(c, "circle", ctr[0], ctr[1], ctr[0], ctr[1], None, f"circle r{r}"); c.boxes[-1] = ("circle", ctr[0], ctr[1], r, None, None, f"circle r{r}")


def T(c, p, s, size=3.0, anchor="start", weight="normal", rotate=0, grp=None):
    assert size >= 3.0, s
    c.text(p, s, size=size, anchor=anchor, weight=weight, rotate=rotate)
    w = len(s) * size * EM * (1.06 if weight == "bold" else 1); h = size * 0.85
    a0 = {"start": 0, "middle": -w / 2, "end": -w}[anchor]
    if rotate in (90, -90):   # text runs along y
        s0 = a0 if rotate == 90 else -a0 - w
        reg(c, "text", p[0] - h / 2, p[1] + s0, p[0] + h / 2, p[1] + s0 + w, grp, s)
    else:
        reg(c, "text", p[0] + a0, p[1] - h / 2, p[0] + a0 + w, p[1] + h / 2, grp, s)


def para(c, x, y, s, width, size=3.0, lead=1.38, weight="normal", grp=None):
    """Wrapped text block; returns the y below it."""
    n = max(8, int(width / (size * EM * (1.06 if weight == "bold" else 1))))
    for raw in s.split("\n"):
        for line in textwrap.wrap(raw, n) or [""]:
            T(c, (x, y), line, size=size, weight=weight, grp=grp); y += size * lead
    return y


def boxed(c, x, y, w, head, body, size=3.0):
    """Heavy-bordered panel with a bold heading (the SVG twin of warning_panel)."""
    start = len(c.parts); g = f"panel{start}"
    y2 = para(c, x + 2, y + 3.6, head, w - 4, size=size, weight="bold", grp=g)
    y2 = para(c, x + 2, y2 + 0.4, body, w - 4, size=size, grp=g)
    c.parts.insert(start, f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(y2 - y)}" fill="#fff" stroke="#000" stroke-width="0.6"/>')
    reg(c, "mark", x, y, x + w, y2, g, "panel")
    return y2


def ruler(c, x, y, label=True):
    """100 mm calibration ruler: baseline at y, ticks up (0 and 100 tallest, for the pixel check), numbers below."""
    c.raw(f'<line id="ruler-base" x1="{_f(x)}" y1="{_f(y)}" x2="{_f(x + 100)}" y2="{_f(y)}" stroke="#000" stroke-width="0.25"/>')
    for i in range(101):
        h = 7 if i in (0, 100) else 4 if i % 10 == 0 else 2.4 if i % 5 == 0 else 1.3
        c.line((x + i, y), (x + i, y - h), lw="thin")
        if i % 10 == 0:
            T(c, (x + i, y + 2.8), str(i), anchor="middle", grp="ruler")
    reg(c, "mark", x - 0.5, y - 7, x + 100.5, y + 0.3, "ruler", "ruler")
    if label:
        T(c, (x + 50, y - 9.6), "CALIBRATION 0-100 mm: must measure 100.0 (+/- 0.5)", anchor="middle", weight="bold")


def crosscheck(c, x, y):
    """50 mm cross-check bar perpendicular to the ruler (vertical), so both print axes are checked; label on its right."""
    c.line((x, y), (x, y + 50), lw="outline")
    for yy in (y, y + 50):
        c.line((x - 2.5, yy), (x + 2.5, yy), lw="outline")
    for i in range(1, 5):
        c.line((x - 1.2, y + 10 * i), (x + 1.2, y + 10 * i), lw="thin")
    reg(c, "mark", x - 2.6, y - 0.4, x + 2.6, y + 50.4, None, "50 bar")
    T(c, (x + 4.2, y + 25), "50 mm CROSS-CHECK", anchor="middle", rotate=90, weight="bold")


def dim2(c, p1, p2, label):
    """Dimension with its label in a white box on the line (turned with a vertical line)."""
    c.dim(p1, p2, "", offset=0)
    g = f"dim{len(c.parts)}"; reg(c, "mark", p1[0] - 0.3, p1[1] - 0.3, p2[0] + 0.3, p2[1] + 0.3, g, "dimension line")
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    w = len(label) * 3.0 * EM + 1.6; h = 3.0 + 1.0
    if abs(p1[0] - p2[0]) < 1e-9:
        c.raw(f'<rect x="{_f(mx - h / 2)}" y="{_f(my - w / 2)}" width="{_f(h)}" height="{_f(w)}" fill="#fff"/>')
        c.raw(f'<text x="{_f(mx)}" y="{_f(my)}" font-family="{FONT}" font-size="3" text-anchor="middle" dominant-baseline="middle" transform="rotate(-90 {_f(mx)} {_f(my)})">{label}</text>')
        reg(c, "text", mx - h / 2, my - w / 2, mx + h / 2, my + w / 2, g, label)
    else:
        c.raw(f'<rect x="{_f(mx - w / 2)}" y="{_f(my - h / 2)}" width="{_f(w)}" height="{_f(h)}" fill="#fff"/>')
        c.raw(f'<text x="{_f(mx)}" y="{_f(my)}" font-family="{FONT}" font-size="3" text-anchor="middle" dominant-baseline="middle">{label}</text>')
        reg(c, "text", mx - w / 2, my - h / 2, mx + w / 2, my + h / 2, g, label)


def leader2(c, target, p, s):
    """Text at p (start anchor) with a leader from the nearest point of its box to the target."""
    T(c, p, s); b = c.boxes[-1]
    q = (min(max(target[0], b[1] - 1), b[3] + 1), min(max(target[1], b[2] - 1), b[4] + 1))
    if b[1] - 1 < q[0] < b[3] + 1:   # target above or below: leave from the box's top or bottom edge
        q = (min(max(target[0], b[1] + 2), b[3] - 2), b[2] - 1 if target[1] < b[2] else b[4] + 1)
    c.arrow(q, target, lw="thin", head=1.4)


def label_box(c, p, s):
    c.label_box(p, s, size=3.0, pad=0.8)
    w = len(s) * 3.0 * EM + 1.6
    reg(c, "text", p[0] - w / 2, p[1] - 2, p[0] + w / 2, p[1] + 2, None, s)


def drill(c, svg, hid, p, bit, uv, src, ref_d=None, optional=False, label=None, lpos=None, anchor=None):
    """DRILL symbol: circle at the bit diameter, crosshair, centre dot. Recorded for the check."""
    d, _ = BITS[bit]
    if ref_d:   # the part's own hole, for orientation
        c.circle(p, ref_d / 2, lw="thin", dash="0.8 0.6")
    dash = ' stroke-dasharray="0.7 0.5"' if optional else ""
    c.raw(f'<circle id="{hid}" class="drill" cx="{_f(p[0])}" cy="{_f(p[1])}" r="{_f(d / 2)}" fill="none" stroke="#000" stroke-width="0.35"{dash}/>')
    m = 4.2
    c.line((p[0] - m, p[1]), (p[0] + m, p[1]), lw="thin"); c.line((p[0], p[1] - m), (p[0], p[1] + m), lw="thin")
    c.raw(f'<circle cx="{_f(p[0])}" cy="{_f(p[1])}" r="0.22" fill="#000"/>')
    reg(c, "mark", p[0] - m, p[1] - m, p[0] + m, p[1] + m, None, hid)
    if label:
        lp = lpos or (p[0] + 3.5, p[1] - 3.5)
        T(c, lp, label, anchor=anchor or ("start" if lp[0] >= p[0] else "end"))
    HOLES.append((svg, hid, "OPTIONAL DRILL" if optional else "DRILL", uv, d, src))


def refhole(c, svg, hid, p, uv, src, d):
    """A part's own hole shown for checking: dashed circle at its size plus a POSITION mark. Never drilled from this sheet."""
    c.raw(f'<circle id="{hid}" cx="{_f(p[0])}" cy="{_f(p[1])}" r="0" fill="none" stroke="none"/>')   # anchor for the check only
    posmark(c, p, size=4.2)
    HOLES.append((svg, hid, "POSITION", uv, d, src))


def posmark(c, p, size=5, hid=None):
    """POSITIONING reference: thin cross in an open diamond. Centre mark only, never drilled."""
    c.line((p[0] - size, p[1]), (p[0] + size, p[1]), lw="thin"); c.line((p[0], p[1] - size), (p[0], p[1] + size), lw="thin")
    s = 1.8
    idattr = f' id="{hid}"' if hid else ""
    c.raw(f'<polygon{idattr} points="{_f(p[0])},{_f(p[1] - s)} {_f(p[0] + s)},{_f(p[1])} {_f(p[0])},{_f(p[1] + s)} {_f(p[0] - s)},{_f(p[1])}" fill="none" stroke="#000" stroke-width="0.25"/>')
    reg(c, "mark", p[0] - size, p[1] - size, p[0] + size, p[1] + size, None, "posmark")


def drill_symbol(c, p, optional=False):
    c.circle(p, 1.6, lw=0.35, dash="0.7 0.5" if optional else None)
    c.line((p[0] - 4, p[1]), (p[0] + 4, p[1]), lw="thin"); c.line((p[0], p[1] - 4), (p[0], p[1] + 4), lw="thin")
    reg(c, "mark", p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4, None, "legend symbol")


def legend(c, x, y, drill_txt, optional_txt=None, w=60):
    T(c, (x, y), "LEGEND", weight="bold"); y += 5
    if drill_txt:
        drill_symbol(c, (x + 4, y + 1.5))
        y = max(para(c, x + 10, y, drill_txt, w - 10), y + 6) + 1.5
    if optional_txt:
        drill_symbol(c, (x + 4, y + 1.5), optional=True)
        y = max(para(c, x + 10, y, optional_txt, w - 10), y + 6) + 1.5
    posmark(c, (x + 4, y + 1.5), size=3.5)
    y = max(para(c, x + 10, y, "POSITION: centre mark only. Do NOT drill.", w - 10), y + 6) + 1.5
    c.line((x, y + 0.5), (x + 8, y + 0.5), lw="thin", dash="0.8 0.6")
    y = para(c, x + 10, y + 0.5, "Outline of the part, reference only.", w - 10) + 1.5
    c.line((x, y + 0.5), (x + 8, y + 0.5), lw="heavy")
    y = para(c, x + 10, y + 0.5, "Datum edge line: trim the paper on it, butt it to the edge.", w - 10)
    return y


def line_id(c, hid, p1, p2, heavy=True, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    c.raw(f'<line id="{hid}" x1="{_f(p1[0])}" y1="{_f(p1[1])}" x2="{_f(p2[0])}" y2="{_f(p2[1])}" stroke="#000" stroke-width="{0.8 if heavy else 0.25}"{d}/>')
    reg(c, "mark", p1[0] - 0.4, p1[1] - 0.4, p2[0] + 0.4, p2[1] + 0.4, None, hid)


def edge(c, hid, p1, p2):
    line_id(c, hid, p1, p2)


def waste(c, x, y, w, h):
    c.hatch([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], spacing=1.6)


def ident(c, x, y, tid, part, anchor="start"):
    T(c, (x, y), f"{tid} · {part} · rev {REV}", anchor=anchor, weight="bold")


def lint(c, name):
    bad = []
    B = c.boxes
    for i, a in enumerate(B):
        if a[0] == "circle":
            continue
        if a[1] < 0 or a[2] < 0 or a[3] > c.w or a[4] > c.h:
            bad.append(f"outside canvas: {a[6]!r} {[round(v, 1) for v in a[1:5]]}")
        if a[0] != "text":
            continue
        for j, b in enumerate(B):
            if j == i or (b[0] == "text" and j < i) or (a[5] is not None and a[5] == b[5]):
                continue
            if b[0] == "circle":
                cx, cy, r = b[1], b[2], b[3]
                near = math.hypot(max(a[1] - cx, 0, cx - a[3]), max(a[2] - cy, 0, cy - a[4]))
                far = max(math.hypot(x - cx, y - cy) for x in (a[1], a[3]) for y in (a[2], a[4]))
                if near < r + 0.3 and far > r - 0.3:
                    bad.append(f"{a[6]!r} crosses {b[6]}")
                continue
            if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                bad.append(f"{a[6]!r} overlaps {b[0]} {b[6]!r}")
    assert not bad, f"{name}:\n  " + "\n  ".join(bad)


def save(c, name):
    lint(c, name)
    path = os.path.join(FIG, name); c.save(path); return name


# ---------- T0 index ----------
def t0():
    name = "T-0-index.svg"; W, H = 178, 76
    c = Canvas(W, H)
    ruler(c, 8, 14); crosscheck(c, 150, 4)
    legend(c, 8, 26, "DRILL ⌀ (bit): circle at the bit size, crosshair and centre dot. Punch the centre through the paper, lift the sheet, drill.", "OPTIONAL DRILL: dashed circle; only where the sheet says so.", w=128)
    return save(c, name), W


# ---------- T1 locating ring (P10) + optional ALEX foot (P20) ----------
def t1():
    name = "T-1-ring.svg"; W, H = 178, 196
    c = Canvas(W, H)
    C = (8, 188)                         # ALEX corner (datum); u along the bottom edge, v up into the cabinet
    U = lambda u, v: (C[0] + u, C[1] - v)
    waste(c, 2, C[1] - 150, C[0] - 2, 150 + 6); waste(c, C[0], C[1], 150, 6)
    edge(c, "T-1-edge-v", U(0, 150), C); edge(c, "T-1-edge-h", C, U(150, 0))
    T(c, U(3.5, 112), "ALEX EDGE: trim, butt to the cabinet edge", rotate=-90, anchor="middle")
    T(c, U(127, 3.2), "ALEX EDGE: trim, butt to it", anchor="middle")
    label_box(c, (C[0] + 20, C[1] + 3.4), "DATUM: ALEX corner")
    c.arrow(U(104, 7), U(114, 17)); T(c, U(116, 12), "into the cabinet")
    k = RING["centre_from_alex_corner"]; R = U(k, k)
    ring(c, R, RING["flange_od"] / 2); ring(c, R, RING["bore"] / 2)
    posmark(c, R, size=6, hid="T-1-centre")
    dim2(c, U(0, 10), U(k, 10), "50 (5.0 cm)"); dim2(c, U(k + 42, 0), U(k + 42, k), "50 (5.0 cm)")
    c.line(U(k + 6, k), U(k + 44, k), lw="thin", dash="2 1"); T(c, U(k + 45.5, k), "0°")
    r = RING["screw_circle_radius"]
    for a in RING_ANGLES:
        t = math.radians(a); uv = (k + r * math.cos(t), k + r * math.sin(t))
        lp, an = {45: ((88, 106), "start"), 165: ((9.5, 116), "start"), 285: ((72, 178), "start")}[a]
        refhole(c, name, f"T-1-R{a}", U(*uv), uv, f"facts rings r {r} (foot-ring.scad) at {a}° as alex-corner-template.scad", 0)
        T(c, lp, f"RING {a}°", anchor=an)
    rf = AF["screw_circle_radius"]
    for a in AF["screw_angles_deg"]:
        t = math.radians(a); uv = (k + rf * math.cos(t), k + rf * math.sin(t))
        drill(c, name, f"T-1-F{a}", U(*uv), "5/64", uv, f"facts alex_feet_optional r {rf} at {a}° (alex-foot.scad)", optional=True)
    T(c, (16, 93), "inner 3 = DRILL, ALEX feet only (bottom)")
    c.arrow((40, 95), (43.6, 129.6), lw="thin", head=1.4)
    # calibration, id, use; legend and notes in the right column
    ruler(c, 20, 17); crosscheck(c, 20, 23)
    ident(c, 28, 27, "T1", "P10 locating ring + P20 ALEX foot (opt.)")
    y = para(c, 28, 33, "CHECK, before drilling any ring (chapter G, step 2a): top lifted off, lay the sheet face up on the bare ALEX corner, edge lines on the two edges. The pencil trace of the pad must lie inside the ⌀52 circle all round; if not, move the cabinet and re-trace.", 92)
    para(c, 28, y + 1, "DRILL, ALEX BOTTOM, only if fitting ALEX feet (unit on its back): punch the 3 inner centres, lift, pilot 5/64 in, 12 mm deep (puck 12 ALEX).", 92)
    yl = legend(c, 124, 35, None, "DRILL ⌀2.0 (5/64 in), dashed: ALEX feet only, ALEX BOTTOM.", w=52)
    para(c, 124, yl + 3, "Dashed circles: ring bore ⌀52 (the check), ring flange ⌀75. RING marks: position only, never drilled; the ring is fitted turned, its own holes at any angle. ALEX foot: 3 holes on r 14.5 at 45 / 165 / 285°, counter-clockwise from the bottom edge, sheet face up. Turn the sheet for each corner, never flip it.", 52)
    return save(c, name), W


# ---------- T2 feet plates (P09) ----------
def plate_pattern(c, name, tag, O, uv0, rot_uv, src):
    s = FEET["plate_hole_spacing"] / 2; P = FEET["plate"] / 2
    c.rect(O[0] - P, O[1] - P, 2 * P, 2 * P, lw="thin", dash="0.8 0.6")
    for (a, b) in (((-P, -P), (P, -P)), ((-P, P), (P, P)), ((-P, -P), (-P, P)), ((P, -P), (P, P))):
        reg(c, "mark", O[0] + a[0] - 0.3, O[1] + a[1] - 0.3, O[0] + b[0] + 0.3, O[1] + b[1] + 0.3, None, "plate outline")
    posmark(c, O, size=6, hid=f"T-2-{tag}-centre")
    i = 0
    for sx in (-1, 1):
        for sy in (-1, 1):
            i += 1; uv = rot_uv(uv0[0] + sx * s, uv0[1] + sy * s)
            drill(c, name, f"T-2-{tag}{i}", (O[0] + sx * s, O[1] - sy * s), "1/8", uv, src, ref_d=FEET["plate_hole_diameter"])


def t2():
    name = "T-2-feet.svg"; W, H = 178, 226
    c = Canvas(W, H)
    k = FOOT_IN; src = "facts feet spacing 46.8 at 85/85 (feet-corner-jig.scad)"
    ruler(c, 20, 17); crosscheck(c, 168, 26)
    ident(c, 20, 23.5, "T2", "P09 feet plate · piece B")
    # piece B (top): one edge line (vertical, x = 8) + station line through the centre
    EX, Ey = 8, 62
    waste(c, 2, 28, EX - 2, 70); edge(c, "T-2-B-edge", (EX, 28), (EX, 98))
    OB = (EX + k, Ey)
    line_id(c, "T-2-B-station", (EX, Ey), (EX + k + 40, Ey), heavy=False, dash="4 1 0.8 1")
    plate_pattern(c, name, "B", OB, (0, 0), lambda a, b: (b, a + k), src)      # u = along the edge from the station, v = from the edge
    dim2(c, (EX, 95), (EX + k, 95), "85 (8.5 cm)")
    T(c, (12, 32), "PIECE B · F1 F3 F5 F6", weight="bold")
    para(c, 12, 37, "Hook the tape on the FAR end; set the station line on your mark at 34.5 cm, along this edge.", 46)
    T(c, (12, 54), "← TOP EDGE: trim, butt to it")
    T(c, (EX + k + 33, Ey - 2.6), "STATION LINE")
    # cut line
    c.line((0, 100), (W, 100), lw="thin", dash="3 1.5"); T(c, (104, 98.2), "✂ CUT: two templates")
    # piece A (bottom): L corner 85/85
    C = (8, 219); U = lambda u, v: (C[0] + u, C[1] - v)
    waste(c, 2, 104, C[0] - 2, C[1] - 104 + 6); waste(c, C[0], C[1], 150, 6)
    edge(c, "T-2-A-edge-v", (C[0], 104), C); edge(c, "T-2-A-edge-h", C, U(150, 0))
    T(c, (12, 110), "← TOP EDGE: trim, butt to it"); T(c, U(105, 3.2), "TOP END: trim, butt to the end", anchor="middle")
    label_box(c, (C[0] + 26, C[1] + 3.4), "DATUM: far corner of the top")
    plate_pattern(c, name, "A", U(k, k), (k, k), lambda a, b: (a, b), src)
    dim2(c, U(0, 10), U(k, 10), "85 (8.5 cm)"); dim2(c, U(10, 0), U(10, k), "85 (8.5 cm)")
    T(c, (127, 108), "PIECE A · F2 F4 F7 F8", weight="bold")
    T(c, (127, 113), f"T2-A · rev {REV}", weight="bold")
    yl = legend(c, 127, 120, "DRILL ⌀3.2 (1/8 in), 15 mm deep (puck 15 LEG). Plate holes ⌀5.2 dashed.", w=49)
    para(c, 127, yl + 3, "Top FACE DOWN. Plate 59.5 square, holes 46.8 apart, square to the edges; symmetric, either way round. #8 × 5/8 in pan head.", 49)
    return save(c, name), W


# ---------- T3 OLOV plates (P05) ----------
def t3(inset, name, tid):
    W, H = 178, 214
    c = Canvas(W, H)
    EY = H - 10; SX = 66                       # edge line (horizontal), station line (vertical through the centre)
    waste(c, 2, EY, 174, 6); edge(c, f"{tid}-edge", (2, EY), (176, EY))
    label_box(c, (120, EY + 3.4), "TOP EDGE: trim on this line, butt to the edge")
    label_box(c, (32, EY + 3.4), "DATUM: edge × station line")
    O = (SX, EY - inset)
    line_id(c, f"{tid}-station", (SX, max(2, O[1] - 56)), (SX, EY), heavy=False, dash="4 1 0.8 1")
    ring(c, O, OLOV["plate_diameter"] / 2); posmark(c, O, size=6, hid=f"{tid}-centre")
    toward = inset == 100                      # L2-L6: one hole toward the edge; L1: turned 36°, one hole away
    r = OLOV["hole_circle_radius"]
    for i in range(OLOV["holes"]):
        a = math.radians((-90 if toward else 90) + 72 * i)   # angle in (u along the edge, v from the edge) frame
        uv = (r * math.cos(a), inset + r * math.sin(a))
        drill(c, name, f"{tid}-H{i + 1}", (O[0] + uv[0], EY - uv[1]), "1/8", uv, f"facts olov r {r}, 5 × 72°, {'one toward' if toward else 'one away from'} the edge (leg-jig.scad)", ref_d=OLOV["hole_diameter"])
    dim2(c, (8, EY), (8, EY - inset), f"{inset} ({inset / 10:g} cm)")
    c.arrow((60, EY - 38), (60, EY - 2)); T(c, (58, EY - 20), "toward the edge", anchor="end")
    tag = tid.replace("T-", "T")
    legtxt = "DRILL ⌀3.2 (1/8 in), 15 mm deep (puck 15 LEG). OLOV holes ⌀5.5 dashed."
    if toward:
        T(c, (SX + 2, O[1] - 56), "STATION LINE"); T(c, (94, 53), "plate ⌀105")
        ruler(c, 20, 17); crosscheck(c, 20, 23)
        T(c, (28, 27), f"{tag} · P05 OLOV plate · 100", weight="bold")
        y = para(c, 128, 6, f"{tag} · rev {REV}", 48, weight="bold")
        y = para(c, 128, y + 1, "The sheet sets 10 cm from the edge. Top A, edge = back edge, tape from the side-wall end: L2 65 cm, L3 140 cm. Top B, edge = side-wall edge, tape from the joint end: L4 20 cm, L5 95 cm, L6 170 cm. One hole points AT the edge.", 48)
        legend(c, 128, y + 4, legtxt, w=48)
    else:
        T(c, (SX + 2, 112), "STATION LINE"); T(c, (100, 100), "plate ⌀105")
        ruler(c, 74, 132); crosscheck(c, 74, 137)
        y = para(c, 124, 6, f"{tag} · P05 OLOV plate · 150 · L1 · rev {REV}", 52, weight="bold")
        para(c, 124, y + 1, "L1 on top A: the sheet sets 15 cm from the side-wall end; tape the station along that end: 42 cm from the back edge. Turned 36°: one hole points AWAY from the edge.", 52)
        para(c, 12, 118, "Only for L1. L2-L6 use sheet T3a.", 48, weight="bold")
        legend(c, 84, 142, legtxt, w=92)
    return save(c, name), W


# ---------- T4 rail station strips (P06 / P07), landscape ----------
OVER, STEP, SPAN = 20, 250, 270


def free_spot(c, cands, box):
    """First candidate whose box clears everything registered so far."""
    for v in cands:
        bx = box(v)
        if not any(x0 < b[3] and b[1] < x1 and y0 < b[4] and b[2] < y1 for x0, y0, x1, y1 in (bx if isinstance(bx, list) else [bx]) for b in c.boxes):
            return v
    raise AssertionError("no free spot")


def t4(rail):
    names = []
    stations = RAILS[rail]
    end_name = "WALL END" if rail == "A" else "CORNER END"
    n_sheets = math.ceil((BOUGHT - SPAN) / STEP) + 1
    for n in range(1, n_sheets + 1):
        s0 = STEP * (n - 1); W, H = 273, 128
        name = f"T-4{rail}-{n}.svg"; c = Canvas(W, H); c.boxes = []
        XL = 1.5; X = lambda s: XL + (s - s0)
        YF = 66; YS = YF + SCREW_LINE; YB = YF + 40
        s_end = s0 + SPAN
        # band
        edge(c, f"T-4{rail}-{n}-free", (X(s0), YF), (X(s_end), YF))
        c.line((X(s0), YB), (X(s_end), YB), lw="thin")
        line_id(c, f"T-4{rail}-{n}-screw", (X(s0), YS), (X(s_end), YS), heavy=False, dash="4 1 0.8 1")
        waste(c, X(s0), YF - 5, SPAN, 5)
        T(c, (X(s0) + 135, YF - 7.5), "FREE EDGE of the flat leg: trim on the heavy line, set it flush with the leg's free edge", anchor="middle")
        for s in range(s0, s_end + 1):
            h = 5 if s % 50 == 0 else 3.5 if s % 10 == 0 else 2.2 if s % 5 == 0 else 1.1
            c.line((X(s), YF), (X(s), YF + h), lw="thin")
            if s % 50 == 0 and s != s0:
                T(c, (X(s), YF + 8.2), str(s), anchor="middle")
        reg(c, "mark", X(s0), YF, X(s_end), YF + 5, None, "ticks")
        # holes
        for i, s in enumerate(stations, 1):
            if s0 <= s <= s_end:
                drill(c, name, f"T-4{rail}-{n}-{rail}{i}", (X(s), YS), "7/32", (s, SCREW_LINE), f"data.json rail{rail}.holes[{i - 1}] = {s / 10:g} cm; facts screw line {SCREW_LINE:g}")
                c.circle((X(s), YS), BITS["1/8"][0] / 2, lw="thin", dash="0.5 0.4")
                T(c, (X(s), YS + 7.5), f"{rail}{i} · {s:g} mm ({s / 10:g} cm)", anchor="middle", weight="bold")
        # start: reference end or join
        if n == 1:
            line_id(c, f"T-4{rail}-{n}-ref", (X(0), YF - 5), (X(0), YB + 4))
            T(c, (X(0) + 2, YB + 3.5), f"0 = REFERENCE END ({end_name}): trim, butt flush with the rail's cut end")
        else:
            j = s0 + OVER // 2
            waste(c, X(s0), YF, j - s0, YB - YF)
            line_id(c, f"T-4{rail}-{n}-ref", (X(j), YF - 5), (X(j), YB + 4), dash="2.5 1")
            T(c, (X(j) + 2, YB + 3.5), f"J{n - 1}: TRIM HERE, lay this edge on sheet {n - 1}'s J{n - 1} line")
        if n < n_sheets:
            j = s0 + STEP + OVER // 2
            c.raw(f'<rect x="{_f(X(j))}" y="{_f(YF + 5)}" width="{_f(X(s_end) - X(j))}" height="{_f(YB - YF - 5)}" fill="#e6e6e6" stroke="none"/>')
            line_id(c, f"T-4{rail}-{n}-join", (X(j), YF - 5), (X(j), YB + 4), dash="2.5 1")
            for yy in (YF + 14, YB - 4):
                c.arrow((X(j) - 6, yy), (X(j) - 0.4, yy), head=1.6)
            T(c, (X(j) - 1.5, YB + 3.5), f"J{n}: sheet {n + 1} butts here (tab under it)", anchor="end")
        else:
            for s in (ST["design_length"], BOUGHT):
                c.line((X(s), YF - 5), (X(s), YB + 4), lw="outline", dash="1.5 0.8")
            T(c, (X(BOUGHT) + 2, YB + 3.5), "design end 213.0 cm | 213.4 cm = 84 in as bought")
            para(c, X(BOUGHT) + 4, YS + 6, "FAR END: your rail ends near here. It carries any extra length; no station depends on it.", 66)
        # ident inside the band, screw-line label and 19 dimension where they clear the holes
        tag = f"T4-{rail} · sheet {n}/{n_sheets} · rev {REV}"
        off = free_spot(c, [14, 60, 120, 180], lambda o: (X(s0) + o, YB - 4.5, X(s0) + o + len(tag) * 3.2 * EM + 2, YB - 1.5))
        T(c, (X(s0) + off, YB - 3), tag, weight="bold")
        lab = f"screw line {SCREW_LINE:g} mm from the free edge"
        off = free_spot(c, range(14, 240, 4), lambda o: [(X(s0) + o + 1.5, YF + 5.2, X(s0) + o + 6.5, YS - 0.5), (X(s0) + o + 7.5, YS - 4.5, X(s0) + o + 9 + len(lab) * 3 * EM, YS - 0.5)])
        T(c, (X(s0) + off + 8, YS - 2.6), lab)
        dim2(c, (X(s0) + off + 4, YF), (X(s0) + off + 4, YS), f"{SCREW_LINE:g}")
        # header zone: calibration, legend, panels
        ruler(c, 4, 19); crosscheck(c, 110, 2)
        drill_symbol(c, (124, 6.5)); c.circle((124, 6.5), BITS["1/8"][0] / 2, lw="thin", dash="0.5 0.4")
        para(c, 130, 5, "DRILL ⌀5.56 (7/32 in) through the steel; 1/8 in pilot first (dashed). Centre-punch through the paper, low speed, cutting oil.", 68)
        posmark(c, (124, 22.5), size=3.5); para(c, 130, 22, "Ticks and numbers: position only, never drilled.", 68)
        para(c, 118, 31, "Preferred method: the printed rail drill jig on the 19 line, with a tape from the reference end. This strip is the check. Tape it to either face of the flat leg. 19 is from the FREE edge (chapter E), not from the heel.", 80)
        boxed(c, 200, 1, 72, "MEASURE THE DELIVERED RAIL", f"Design 213.0 cm (2130 mm); bought as 84 in = 213.4 cm (2133.6 mm). Every station runs from the labelled {end_name.lower()}; the far end carries any extra. Tape-check each station from that end.")
        para(c, 4, YB + 9, f"Joins: trim each later sheet on its start J line and lay it on the previous sheet's J line so ticks, numbers and the screw line run on; tape. Rail {rail} holes, cm from the {end_name.lower()}: " + ", ".join(f"{rail}{i} {s / 10:g}" for i, s in enumerate(stations, 1)) + ".", 266)
        names.append((save(c, name), W, n, n_sheets, s0, s_end))
    return names


# ---------- T5 corner fitting placement (reference, 1:2, with a 1:1 detail of one leg) ----------
CJ = F["corner_joint"]
_fm = re.search(r"legs ([\d.]+) long x ([\d.]+) wide, two slots ([\d.]+) x ([\d.]+) mm per leg, slot centres ([\d.]+) and ([\d.]+) mm from the heel", CJ["fittings"])
FIT = dict(zip(("leg", "w", "sl", "sw", "c1", "c2"), map(float, _fm.groups()))); FIT["t"] = float(re.search(r"(\d+) mm gusseted", CJ["fittings"]).group(1))
RH = CJ["rail_hole_positions_mm"]
T5H = []   # (id, expected s, page x, page y, scale, x0, s_a, bolt-line y)


def slot(c, ctr, k, along_x=True):
    L, Wd = FIT["sl"] * k, FIT["sw"] * k
    w, h = (L, Wd) if along_x else (Wd, L)
    c.raw(f'<rect x="{_f(ctr[0] - w / 2)}" y="{_f(ctr[1] - h / 2)}" width="{_f(w)}" height="{_f(h)}" rx="{_f(Wd / 2)}" fill="#fff" stroke="#000" stroke-width="0.35"/>')


def t5():
    name = "T-5-fittings.svg"; W, H = 178, 230
    c = Canvas(W, H); k = 0.5
    below = ST["bolt_line_below_heel"]; ang = D["angle"] * 10; th = ST["thickness"]; legl, fw, t = FIT["leg"], FIT["w"], FIT["t"]
    heels = ST["railA"]["fitting_heels_from_wall_end_cm"]
    heel_out, heel_in = heels["outside_fitting_facing_far_end"] * 10, heels["inside_fitting_facing_wall_end"] * 10
    holesA = [(f"T-5-A{i}", s) for i, s in enumerate(RH["railA_inside_fitting_from_wall_end"][::-1] + RH["railA_outside_fitting_from_wall_end"], 1)]
    for s, ref in zip(RH["railA_outside_fitting_from_wall_end"], (heel_out + FIT["c1"], heel_out + FIT["c2"])):
        assert abs(s - ref) <= 0.051, (s, ref)       # rail holes = heel + slot centre, rounded to 0.1
    for s, ref in zip(RH["railA_inside_fitting_from_wall_end"], (heel_in - FIT["c1"], heel_in - FIT["c2"])):
        assert abs(s - ref) <= 0.051, (s, ref)
    for s, ref in zip(RH["railB_from_corner_end"], (FIT["c1"], FIT["c2"])):
        assert abs(s - ref) <= 0.051, (s, ref)
    exact = [heel_in - FIT["c2"], heel_in - FIT["c1"], heel_out + FIT["c1"], heel_out + FIT["c2"], FIT["c1"], FIT["c2"]]
    CM = {s: round(e / 10, 1) for (_, s), e in zip(holesA + [(0, v) for v in RH["railB_from_corner_end"]], exact)}   # cm from the unrounded heel + slot centre
    assert list(CM.values()) == [43.7, 48.6, 54.9, 59.8, 2.9, 7.8], CM
    ruler(c, 8, 17); crosscheck(c, 170, 2)
    T(c, (8, 26), f"T5 · P08 on P06 / P07 · REFERENCE 1:2, NOT FOR DRILLING · rev {REV}", weight="bold")

    def hole(hid, s, P, x0, s_a, yb):
        p = P(s, below)
        c.circle(p, 11.1 / 2 * k, lw=0.35); c.line((p[0] - 3.5, p[1]), (p[0] + 3.5, p[1]), lw="thin"); c.line((p[0], p[1] - 3.5), (p[0], p[1] + 3.5), lw="thin")
        c.raw(f'<circle id="{hid}" cx="{_f(p[0])}" cy="{_f(p[1])}" r="0.2" fill="#000"/>')
        T5H.append((hid, s, x0, s_a, yb))

    # view 1: rail A front face, s 400-650
    X0, Y0, s_a = 14, 52, 400
    P = lambda s, d: (X0 + (s - s_a) * k, Y0 + d * k)
    T(c, (4, 32), "VIEW 1 · rail A vertical leg, front face (from the knee side), 1:2", weight="bold")
    c.rect(*P(s_a, 0), 250 * k, ang * k, fill="#f2f2f2")
    line_id(c, "T-5-heel-in", (P(heel_in, 0)[0], 38.6), (P(heel_in, 0)[0], P(0, ang + 4)[1]), heavy=False)
    line_id(c, "T-5-heel-out", (P(heel_out, 0)[0], 44.6), (P(heel_out, 0)[0], P(0, ang + 4)[1]), heavy=False)
    T(c, (P(heel_in, 0)[0] - 1.5, 38), "INSIDE heel 51.5 cm: legs ← wall end", anchor="end")
    T(c, (P(heel_out, 0)[0] + 1.5, 44), "OUTSIDE heel 52.0 cm: legs → far end")
    for s0 in (heel_out, heel_in - legl):
        c.rect(*P(s0, below - fw / 2), legl * k, fw * k, fill="#bfbfbf")
    for hc in (heel_out + FIT["c1"], heel_out + FIT["c2"], heel_in - FIT["c1"], heel_in - FIT["c2"]):
        slot(c, P(hc, below), k)
    sec = [(heel_out - ang, 0), (heel_out, 0), (heel_out, ang), (heel_out - th, ang), (heel_out - th, th), (heel_out - ang, th)]
    c.poly([P(*p) for p in sec], fill="#fff"); c.hatch([P(*p) for p in sec], spacing=0.9)
    c.rect(*P(heel_out, below - fw / 2), t * k, fw * k, fill="#808080"); c.rect(*P(heel_out - th - t, below - fw / 2), t * k, fw * k, fill="#808080")
    c.centreline(P(s_a - 6, below), P(s_a + 256, below)); T(c, (P(s_a + 262, 0)[0], P(0, below)[1]), "bolt line")
    dim2(c, P(s_a + 254, 0), P(s_a + 254, below), f"{below:g}")
    for hid, s in holesA:
        hole(hid, s, P, X0, s_a, Y0 + below * k)
        T(c, (P(s, 0)[0], P(0, ang + 6)[1]), f"{s:g}", anchor="middle", weight="bold"); T(c, (P(s, 0)[0], P(0, ang + 6)[1] + 4.2), f"({CM[s]:g} cm)", anchor="middle")
    T(c, (14, 90), "rail A hole centres from the WALL END (40 cm off the drawing)")
    T(c, (P(heel_out, 0)[0] + 3, 95), "rail B end (section)")
    # view 2: rail B outer face near the corner end
    Y0 = 116
    Q = lambda s, d: (19 + s * k, Y0 + d * k)
    T(c, (4, 102), "VIEW 2 · rail B vertical leg, outer face, corner end, 1:2", weight="bold")
    c.rect(*Q(0, 0), 230 * k, ang * k, fill="#f2f2f2")
    line_id(c, "T-5-heel-B", (Q(0, 0)[0], 111), (Q(0, 0)[0], Q(0, ang + 4)[1]))
    c.rect(*Q(0, below - fw / 2), legl * k, fw * k, fill="#bfbfbf")
    for hc in (FIT["c1"], FIT["c2"]):
        slot(c, Q(hc, below), k)
    c.centreline(Q(-8, below), Q(236, below))
    for i, s in enumerate(RH["railB_from_corner_end"], 1):
        hole(f"T-5-B{i}", s, Q, 19, 0, Y0 + below * k)
        T(c, (Q(s, 0)[0], Q(0, ang + 6)[1]), f"{s:g}", anchor="middle", weight="bold"); T(c, (Q(s, 0)[0], Q(0, ang + 6)[1] + 4.2), f"({CM[s]:g} cm)", anchor="middle")
    T(c, (21, 109), "HEEL = corner end (0): fitting legs → far end")
    T(c, (66, Q(0, ang + 6)[1]), "from the CORNER END; bolts pass both fittings")
    # detail 1:1: one fitting leg with its slots
    T(c, (4, 160), f"DETAIL 1:1 · one leg, slots {FIT['sl']:g} × {FIT['sw']:g}", weight="bold")
    hx, ly = 14, 178
    c.rect(hx, ly, legl, fw, fill="#e6e6e6")
    c.line((hx, ly - 3), (hx, ly + fw + 3), lw="heavy"); T(c, (hx - 1.5, ly + fw / 2), "HEEL", rotate=-90, anchor="middle")
    for hc in (FIT["c1"], FIT["c2"]):
        slot(c, (hx + hc, ly + fw / 2), 1); c.centre_mark((hx + hc, ly + fw / 2), size=3)
    reg(c, "mark", hx, ly, hx + legl, ly + fw, None, "fitting leg")
    dim2(c, (hx, 167), (hx + FIT["c2"], 167), f"{FIT['c2']:g}"); dim2(c, (hx, 173), (hx + FIT["c1"], 173), f"{FIT['c1']:g}")
    dim2(c, (hx, ly + fw + 5), (hx + legl, ly + fw + 5), f"{legl:g}")
    dim2(c, (hx + legl + 4, ly), (hx + legl + 4, ly + fw), f"{fw:g}")
    boxed(c, 124, 152, 50, "RAIL HOLES · VERIFIED 23 Oct 2026", "Rail A, cm from the wall end: 54.9 / 59.8 (outside fitting, heel 52.0), 48.6 / 43.7 (inside, heel 51.5). Rail B, cm from the corner end: 2.9 / 7.8. All on the bolt line, 29 mm below the heel. Drill THROUGH THE FITTING: clamp on the heel mark, printed slot plug in each slot, pilot 1/8 in, open to 7/16 in (11.1 mm). Inside gusset DOWN, outside toward the knee space.")
    return save(c, name), W


# ---------- T6 clamp pad plates (reference, 1:4) ----------
def t6():
    name = "T-6-pads.svg"; W, H = 178, 212
    c = Canvas(W, H); k = 0.25
    X0, Y0 = 20, 50
    P = lambda x, y: (X0 + x * k, Y0 + y * k)
    pads = [[v * 10 for v in p] for p in D["pads"]]
    zone = [v * 10 for v in F["layout_cm"]["clamps"]["zones"]["c1_x"]]; zin = D["zoneIn"] * 10
    ruler(c, 8, 17); crosscheck(c, 170, 2)
    T(c, (8, 26), f"T6 · P11 pads for P12 · POSITIONING ONLY, NO DRILLING · 1:4 · rev {REV}", weight="bold")
    c.hatch([P(-30, -30), P(560, -30), P(560, -42), P(-42, -42), P(-42, 540), P(-30, 540)], spacing=1.2)
    c.poly([P(560, 0), P(0, 0), P(0, 540)], close=False, lw="heavy")
    T(c, (P(300, 0)[0], P(0, -48)[1]), "back wall", anchor="middle"); T(c, (P(-48, 0)[0], P(0, 300)[1]), "side wall", rotate=-90, anchor="middle")
    T(c, (25, 56), "DATUM (0, 0)")
    c.arrow(P(10, 10), P(100, 10)); T(c, (P(104, 0)[0], P(0, 10)[1]), "x")
    c.arrow(P(10, 10), P(10, 100)); T(c, (P(10, 0)[0], P(0, 112)[1]), "y", anchor="middle")
    c.rect(*P(10, 479), 550 * k, 51 * k, lw="thin", dash="1.5 1"); T(c, (P(300, 0)[0], P(0, 465)[1]), "rail A (y 47.9-53.0 cm)", anchor="middle")
    c.circle(P(150, 420), 52.5 * k, lw="thin", dash="1.5 1"); T(c, P(150, 420), "L1", anchor="middle")
    for i, (x0, x1, y0, y1) in enumerate(pads, 1):
        c.raw(f'<rect id="T-6-pad{i}" x="{_f(P(x0, y0)[0])}" y="{_f(P(x0, y0)[1])}" width="{_f((x1 - x0) * k)}" height="{_f((y1 - y0) * k)}" fill="#e6e6e6" stroke="#000" stroke-width="0.5"/>')
    c.rect(*P(zone[0], 0), (zone[1] - zone[0]) * k, zin * k, lw="thin", dash="0.8 0.6"); c.rect(*P(0, zone[0]), zin * k, (zone[1] - zone[0]) * k, lw="thin", dash="0.8 0.6")
    cx = (zone[0] + zone[1]) / 2; cy = (13.5 + 63.5) / 2
    for (ex, ey, rx, ry) in ((cx, cy, 45, 25), (cy, cx, 25, 45)):
        p = P(ex, ey); c.raw(f'<ellipse cx="{_f(p[0])}" cy="{_f(p[1])}" rx="{_f(rx * k)}" ry="{_f(ry * k)}" fill="none" stroke="#000" stroke-width="0.25" stroke-dasharray="0.6 0.5"/>')
    dim2(c, P(0, -10), P(200, -10), "200 (20.0 cm)"); dim2(c, P(0, -22), P(454, -22), "454 (45.4 cm)")
    dim2(c, P(-10, 0), P(-10, 200), "200 (20.0 cm)"); dim2(c, P(-22, 0), P(-22, 454), "454 (45.4 cm)")
    leader2(c, P(330, 70), (92, 88), "pad plate x 20.0-45.4 cm, y 0.5-8.1 cm")
    leader2(c, P(445, 45), (138, 76), "clamp zone 36-44 cm"); T(c, (138, 80.5), "jaw pad 90 × 50 mm")
    leader2(c, P(70, 300), (52, 116), "pad plate x 0.5-8.1 cm, y 20.0-45.4 cm")
    leader2(c, P(52, 430), (52, 123), "clamp zone 36-44 cm; oval")
    para(c, 8, 192, "Plan from above, datum top A's back-left corner (x along the back wall, y along the side wall). The plates lie LOOSE on the underside under the VIVO lower jaws (chapter I): with the top face down, draw the outlines measuring from the same two named edges. Jaw pad: oval 90 × 50 mm, 13.5-63.5 mm in from the edge (measured), drawn centred on each clamp.", 166)
    return save(c, name), W


# ---------- geometry check ----------
def expected(hid):
    """Hole position recomputed straight from facts.json / data.json, independent of the drawing code."""
    cs = lambda r, a: (r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))
    if hid.startswith("T-1-"):
        r, a = (F["rings"]["screw_circle_radius"], int(hid[5:])) if hid[4] == "R" else (F["alex_feet_optional"]["screw_circle_radius"], int(hid[5:]))
        assert a in (RING_ANGLES if hid[4] == "R" else F["alex_feet_optional"]["screw_angles_deg"]), hid
        x, y = cs(r, a); c0 = F["rings"]["centre_from_alex_corner"]; return (c0 + x, c0 + y)
    if hid.startswith("T-2-"):
        i = int(hid[-1]) - 1; sx, sy = (-1, 1)[i // 2], (-1, 1)[i % 2]; h = F["feet"]["plate_hole_spacing"] / 2; k = F["layout_cm"]["feet"]["F2"][1] * 10
        return (k + sx * h, k + sy * h) if hid[4] == "A" else (sy * h, k + sx * h)
    if hid.startswith("T-3"):
        inset = D["legs"][1][2] * 10 if hid[3] == "a" else D["legs"][0][1] * 10
        x, y = cs(F["olov"]["hole_circle_radius"], (-90 if hid[3] == "a" else 90) + 360 / F["olov"]["holes"] * (int(hid[-1]) - 1)); return (x, inset + y)
    rail, i = hid.split("-")[-1][0], int(hid.split("-")[-1][1:])
    return (D["rail" + rail]["holes"][i - 1] * 10, F["steel"]["screw_line_from_free_edge"])



def check():
    """Re-read each saved SVG and measure every recorded hole from its sheet's datum lines (true mm)."""
    def attrs(svg, el_id):
        m = re.search(rf'<(\w+) id="{re.escape(el_id)}"([^>]*)>', svg)
        assert m, el_id
        return {k: float(v) for k, v in re.findall(r'(?<![\w-])(\w+)="([-\d.]+)"', m.group(2))}
    rows = []
    for svgname, hid, kind, uv, d, src in HOLES:
        svg = open(os.path.join(FIG, svgname)).read()
        root = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)" width="([\d.]+)mm" height="([\d.]+)mm"', svg)
        assert root and root.group(1) == root.group(3) and root.group(2) == root.group(4), f"{svgname}: not 1:1"
        h = attrs(svg, hid); cx, cy, dd = h["cx"], h["cy"], 2 * h["r"]
        if svgname == "T-1-ring.svg":
            ev, eh = attrs(svg, "T-1-edge-v"), attrs(svg, "T-1-edge-h"); m = (cx - ev["x1"], eh["y1"] - cy)
        elif svgname == "T-2-feet.svg" and "-A" in hid:
            ev, eh = attrs(svg, "T-2-A-edge-v"), attrs(svg, "T-2-A-edge-h"); m = (cx - ev["x1"], eh["y1"] - cy)
        elif svgname == "T-2-feet.svg":
            e, st = attrs(svg, "T-2-B-edge"), attrs(svg, "T-2-B-station"); m = (st["y1"] - cy, cx - e["x1"])
        elif svgname.startswith("T-3"):
            tid = hid.rsplit("-", 1)[0]; e, st = attrs(svg, f"{tid}-edge"), attrs(svg, f"{tid}-station"); m = (cx - st["x1"], e["y1"] - cy)
        else:   # rail strips: u = s from the reference end, via the sheet's start line; v = from the free edge
            base = hid.rsplit("-", 1)[0]; n = int(base.split("-")[-1]); fe, ref = attrs(svg, f"{base}-free"), attrs(svg, f"{base}-ref")
            s_ref = 0 if n == 1 else STEP * (n - 1) + OVER // 2
            m = (cx - ref["x1"] + s_ref, cy - fe["y1"])
        e = expected(hid); assert abs(e[0] - uv[0]) < 1e-9 and abs(e[1] - uv[1]) < 1e-9, (hid, e, uv)
        du, dv = m[0] - e[0], m[1] - e[1]
        assert abs(du) < 0.002 and abs(dv) < 0.002 and abs(dd - d) < 0.002, (hid, uv, m, d, dd)
        rows.append((hid, kind, uv, m, d, src))
    # reference sheets: positions at scale
    s5 = open(os.path.join(FIG, "T-5-fittings.svg")).read()
    gap = (attrs(s5, "T-5-heel-out")["x1"] - attrs(s5, "T-5-heel-in")["x1"]) / 0.5
    assert abs(gap - 5.0) < 1e-6, gap
    t5rows = []
    for hid, s, x0, s_a, yb in T5H:
        h = attrs(s5, hid); got = (h["cx"] - x0) / 0.5 + s_a
        assert abs(got - s) < 1e-6 and abs(h["cy"] - yb) < 1e-6, (hid, got, s)
        t5rows.append(f"{hid} {s:g} (SVG {got:g}, bolt line {(h['cy'] - yb) / 0.5 + ST['bolt_line_below_heel']:g} below the heel)")
    s6 = open(os.path.join(FIG, "T-6-pads.svg")).read()
    for i, (x0, x1, y0, y1) in enumerate(D["pads"], 1):
        r = attrs(s6, f"T-6-pad{i}")
        got = ((r["x"] - 20) / 0.25, (r["x"] - 20 + r["width"]) / 0.25, (r["y"] - 50) / 0.25, (r["y"] - 50 + r["height"]) / 0.25)
        assert all(abs(a - b * 10) < 1e-6 for a, b in zip(got, (x0, x1, y0, y1))), (i, got)
    print(f"{'hole':<16}{'kind':<15}{'expected u, v (mm)':>22}{'SVG u, v (mm)':>22}{'bit':>7}  source")
    for hid, kind, uv, m, d, src in rows:
        print(f"{hid:<16}{kind:<15}{uv[0]:>10.3f}{uv[1]:>12.3f}{m[0]:>10.3f}{m[1]:>12.3f}{d:>7.2f}  {src}")
    print("T5 rail holes (facts corner_joint.rail_hole_positions_mm, 1:2): " + "; ".join(t5rows))
    print(f"{len(rows)} holes match to 0.002 mm; T5 heels 520/515, T5 rail holes and T6 pad plates match at scale.")


# ---------- pages ----------
HEAD_CSS = """<style>
@page land { size: A4 landscape; margin: 0; }
.page.land { page: land; width: 297mm; height: 210mm; padding: 12mm 12mm 13mm 12mm; }
.tph { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 0.5mm solid #000; padding-bottom: 1mm; margin-bottom: 1.5mm; }
.tph .tid { font-size: 17pt; font-weight: bold; margin-right: 2mm; }
.tph .tname { font-size: 11.5pt; font-weight: bold; }
.tph .trev { font-size: 7pt; text-align: right; max-width: 66mm; line-height: 1.25; }
.tplwarn .warn { margin: 1mm 0 1.5mm 0; padding: 1mm 2mm; font-size: 8.5pt; }
.tplwarn .warn-icon { width: 7mm; height: 7mm; font-size: 12pt; }
</style>"""


def head(tid, name, badges, extra=""):
    b = "".join(badge(x) for x in badges)
    w = warning_panel("DISABLE FIT TO PAGE / shrink to fit / scale to fit. Measure the ruler before use: 0 to 100 must read 100.0 mm and the cross-check bar 50.0 mm (±0.5). If either is off, do not use the sheet: reprint." + extra, kind="PRINT AT 100% / ACTUAL SIZE" + (" · A4 LANDSCAPE" if tid.startswith("T4") else ""))
    return (f'<div class="tph"><div><span class="tid">{tid}</span><span class="tname">{name}</span> {b}</div>'
            f'<div class="trev">Template {tid} · rev {REV}<br><b>units: mm; tape stations also in cm</b><br>numbers: manual/facts.json + data.json, source_commit: {SRC}</div></div><div class="tplwarn">{w}</div>')


def page(tid, title, name, badges, fig, W, cls="", extra="", after="", pre=""):
    return (f'<section class="page{cls}" data-chapter="{tid}" data-title="{title}">\n{head(tid, name, badges, extra)}{pre}\n'
            f'<img class="fig" src="../../figures/{fig}" style="width:{_f(W)}mm">{after}\n</section>\n')


def write(fname, html):
    open(os.path.join(TPL, fname), "w").write("<!-- generated by manual/src/figures_T.py: edit that file, not this one -->\n" + html)


def main():
    os.makedirs(FIG, exist_ok=True); os.makedirs(TPL, exist_ok=True)
    f0, w0 = t0(); f1, w1 = t1(); f2, w2 = t2()
    f3a, w3 = t3(100, "T-3a-olov-100.svg", "T-3a"); f3b, _ = t3(150, "T-3b-olov-150.svg", "T-3b")
    rA, rB = t4("A"), t4("B"); f5, w5 = t5(); f6, w6 = t6()
    check()
    sheets = [("T1", "Locating ring P10 (+ optional ALEX foot P20)", "1:1 check; drilling only for the ALEX feet"), ("T2", "Feet plate P09, two pieces", "1:1 drilling"),
              ("T3a", "OLOV plate P05 at 100: L2-L6", "1:1 drilling"), ("T3b", "OLOV plate P05 at 150: L1", "1:1 drilling"),
              ("T4-A", f"Rail A P06 station strip, {len(rA)} landscape sheets", "1:1 marking check"), ("T4-B", f"Rail B P07 station strip, {len(rB)} landscape sheets", "1:1 marking check"),
              ("T5", "Corner fitting P08 placement", "reference 1:2, not for drilling"), ("T6", "Clamp pad plate P11 placement", "reference 1:4, positioning only")]
    rows = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in sheets)
    write("00-index.html", f"""<section class="page" data-chapter="T0" data-title="Print first">
{HEAD_CSS}
{head("T0", "Templates · print this page first", [])}
<p>Print every sheet from the PDF viewer at <b>100 % / Actual size</b>, on A4 (T4 sheets are A4 landscape). Then lay a steel rule on the ruler below. Use the sheets only if 0 to 100 reads 100.0 mm and the bar reads 50.0 mm. A sheet that is 1 % small puts a hole 0.5 mm off at 50 mm.</p>
<img class="fig" src="../../figures/{f0}" style="width:{_f(w0)}mm">
<table><tr><th>Sheet</th><th>What</th><th>Use</th></tr>{rows}</table>
<p class="small">Using a drilling sheet: trim on the heavy datum line(s), butt the trimmed edge to the named edge, tape, then punch each DRILL centre through the paper with an awl or automatic centre punch, lift the sheet and drill to the depth stated. The printed jigs (P18) are the primary tools; these sheets reproduce their patterns and serve as the check. Top marking is done face down (underside up); every pattern here is used without flipping the sheet.</p>
</section>
""")
    write("01-ring.html", page("T1", "Locating ring P10", "Locating ring (P10) · check template 1:1", ["VERIFIED"], f1, w1,
          pre='<div class="note"><b>CHECK SHEET (chapter G, step 2a).</b> With the top lifted off and before drilling any ring, lay this sheet on each bare ALEX corner: the pencil trace of the pad must lie inside the ⌀52 circle all round. If not, move the cabinet and re-trace. It is a drilling template only for the optional ALEX feet, on the bottom corners.</div>',
          after='<div class="note">The ring is fitted turned: its own holes may sit at any angle. ALEX top panel 15.9 mm (5/8 in), measured 23 Oct 2026: the #6 × 5/8 in screws go 13.4 mm in and leave 2.5 mm.</div>'))
    write("02-feet.html", page("T2", "Feet plate P09", "Feet plate (P09) · drilling template 1:1", ["VERIFIED"], f2, w2,
          extra=" Verified on the purchased plate 23 Oct 2026: 41.6 between holes (inside jaws), 52.0 across (outside jaws), so 46.8 centres."))
    write("03-olov.html", page("T3a", "OLOV plate P05, 100", "OLOV plate (P05) · 100 from the edge · 1:1", ["VERIFIED"], f3a, w3)
          + page("T3b", "OLOV plate P05, 150", "OLOV plate (P05) · 150 from the end · 1:1", ["VERIFIED"], f3b, w3))
    html = ""
    for rail, lst, part in (("A", rA, "P06"), ("B", rB, "P07")):
        for fig, W, n, N, s0, s1 in lst:
            html += page(f"T4-{rail}", f"Rail {rail} strip {n}/{N}", f"Rail {rail} ({part}) station strip {n}/{N}", ["SOURCE", "MEASURE"], fig, W, cls=" land")
    write("04-rails.html", html)
    write("05-fittings.html", page("T5", "Corner fittings P08", "Corner fitting (P08) placement · reference", ["SOURCE", "VERIFIED"], f5, w5))
    write("06-pads.html", page("T6", "Clamp pad plates P11", "Clamp pad plate (P11) placement · reference", ["SOURCE", "VERIFIED", "ASSUMPTION"], f6, w6,
          after='<p class="small">SOURCE-DEFINED: the pad plate outlines (marking table, chapter D). VERIFIED: the 90 × 50 mm lower-jaw pad, measured 21-23 Oct 2026 (facts.json vivo). ASSUMPTION / FIELD CHECK: the oval drawn centred on the clamp; the clamp back sets the final position (crossbar fitted as the spacing guide).</p>'))


if __name__ == "__main__":
    main()
