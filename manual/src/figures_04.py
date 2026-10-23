#!/usr/bin/env python3
"""Chapter D figures: datum, face-down marking diagrams for tops A and B, rail orientation, hole types and depths.

Face-down convention used on every drawing here (same as guide.html sections 3 and 4): the top lies face down on
the blanket and you stand at its front, with the taped reference edge (top A: back edge; top B: joint end) AWAY
from you. The page top is the far side, you are at the page bottom. Seen this way the underside is the plan
mirrored left-right, so desk x grows to the LEFT and the datum corner side (x = 0) is on your RIGHT. Both tops use
the same mapping (page u = -x, page v = +y): top B is top A's plan rotated, never mirrored differently.
All numbers come from manual/data.json, manual/facts.json and docs/build-manual.md (cm there, mm here).
"""
import json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.dirname(HERE)
sys.path.insert(0, MAN)
from lib.draw import Canvas, GREY, LW, FONT, _f  # noqa: E402

D = json.load(open(os.path.join(MAN, "data.json")))
F = json.load(open(os.path.join(MAN, "facts.json")))
FIG = os.path.join(MAN, "figures")
mm = lambda cm: round(cm * 10, 1)
fmt = lambda v: ("%.1f" % v).rstrip("0").rstrip(".")

_uid = [0]


_PFX = os.path.splitext(os.path.basename(sys.argv[0] or "f"))[0].replace("figures_", "f")


def uid(p):
    """Clip ids unique across every SVG inlined into one HTML page (prefix = the running figure script)."""
    _uid[0] += 1
    return f"{_PFX}{p}{_uid[0]}"


def hatch_rect(c, u0, v0, u1, v1, spacing=1.6, sw=0.2, color="#000"):
    """45-degree hatching in a page-space rectangle, unique clip id."""
    i = uid("h")
    x0, x1 = min(u0, u1), max(u0, u1); y0, y1 = min(v0, v1), max(v0, v1)
    L = (x1 - x0) + (y1 - y0)
    ls = []
    t = -L
    while t < L:
        ls.append(f'<line x1="{_f(x0 + t)}" y1="{_f(y1)}" x2="{_f(x0 + t + (y1 - y0))}" y2="{_f(y0)}" stroke="{color}" stroke-width="{sw}"/>')
        t += spacing
    c.raw(f'<clipPath id="{i}"><rect x="{_f(x0)}" y="{_f(y0)}" width="{_f(x1 - x0)}" height="{_f(y1 - y0)}"/></clipPath><g clip-path="url(#{i})">{"".join(ls)}</g>')


class FD:
    """Face-down mapping: desk mm -> page mm. region = (x0, x1, y0, y1) desk mm; s = page mm per desk mm."""

    def __init__(self, c, region, s, mL, mT):
        self.c, self.s, self.mL, self.mT = c, s, mL, mT
        self.x0, self.x1, self.y0, self.y1 = region

    def p(self, x, y):
        return (self.mL + (self.x1 - x) * self.s, self.mT + (y - self.y0) * self.s)

    def u(self, x):
        return self.p(x, 0)[0]

    def v(self, y):
        return self.p(0, y)[1]

    def clip_begin(self):
        i = uid("c")
        u0, v0 = self.p(self.x1, self.y0); u1, v1 = self.p(self.x0, self.y1)
        self.c.raw(f'<clipPath id="{i}"><rect x="{_f(u0)}" y="{_f(v0)}" width="{_f(u1 - u0)}" height="{_f(v1 - v0)}"/></clipPath><g clip-path="url(#{i})">')

    def clip_end(self):
        self.c.raw("</g>")

    def rect(self, x0, x1, y0, y1, **kw):
        self.c.poly([self.p(x0, y0), self.p(x1, y0), self.p(x1, y1), self.p(x0, y1)], **kw)

    def circle(self, x, y, r_mm, **kw):
        self.c.circle(self.p(x, y), r_mm * self.s, **kw)

    def hole(self, x, y, d_mm, cross=True):
        cu, cv = self.p(x, y)
        r = max(d_mm * self.s / 2, 0.35)
        self.c.circle((cu, cv), r, fill="#fff", lw="thin")
        if cross:
            m = r + 0.9
            self.c.line((cu - m, cv), (cu + m, cv), lw=0.15)
            self.c.line((cu, cv - m), (cu, cv + m), lw=0.15)

    def cmark(self, x, y, size=2.2):
        cu, cv = self.p(x, y)
        self.c.line((cu - size, cv), (cu + size, cv), lw="thin")
        self.c.line((cu, cv - size), (cu, cv + size), lw="thin")


# ---------------------------------------------------------------- geometry from the data files (desk mm)
LEGS = {l[0]: (mm(l[1]), mm(l[2]), l[3]) for l in D["legs"]}
FEET = {f[0]: (mm(f[1]), mm(f[2]), f[3]) for f in D["feet"]}
LEG_R = F["olov"]["plate_diameter"] / 2          # 52.5
LEG_HOLE_R = F["olov"]["hole_circle_radius"]     # 42.5
LEG_HOLE_D = F["olov"]["hole_diameter"]          # 5.5
FOOT_PLATE = F["feet"]["plate"]                  # 59.5
FOOT_SP = F["feet"]["plate_hole_spacing"]        # 46.8
FOOT_HOLE_D = F["feet"]["plate_hole_diameter"]   # 5.2
FOOT_PAD = F["feet"]["body_and_pad_diameter"]    # 50
RA, RB = D["railA"], D["railB"]
HOLE_OFF = mm(D["holeOffset"])                   # 19 from the free edge
CL = F["layout_cm"]["clamps"]
PADS = [[mm(v) for v in p] for p in D["pads"]]
PLATE_L, PLATE_W, PLATE_Y = mm(D["plateL"]), mm(D["plateW"]), mm(D["plateY"])
PLATE_HOLES = [mm(h) for h in D["plateHoles"]]
PLATES = [(p[0], mm(p[1])) for p in D["plates"]]
A1, A2 = D["alex1"], D["alex2"]


def leg_holes(name):
    """Five OLOV pilot positions from the leg jig: 100 pattern (L2-L6) has one hole pointing at the wall edge it
    hooks over; the 150 pattern (L1, hooked over the side-wall end) has one hole pointing away from that edge."""
    x, y, top = LEGS[name]
    if name == "L1":            # edge x = 0, away = +x, pattern rot 0
        base, ax = 0.0, "x"
    elif top == "A":            # edge y = 0, one hole toward it (-y)
        base, ax = -90.0, "y"
    else:                       # top B, edge x = 0, one hole toward it (-x)
        base, ax = 180.0, "x"
    out = []
    for i in range(5):
        a = math.radians(base + i * 72)
        out.append((x + LEG_HOLE_R * math.cos(a), y + LEG_HOLE_R * math.sin(a)))
    return out


def draw_leg(fd, name, label=True, holes=True, lab_dx=0, lab_dy=0):
    x, y, _ = LEGS[name]
    fd.circle(x, y, LEG_R, fill=GREY["light"], lw="outline")
    if holes:
        for hx, hy in leg_holes(name):
            fd.hole(hx, hy, LEG_HOLE_D, cross=fd.s > 0.12)
    fd.cmark(x, y)
    if label:
        u, v = fd.p(x, y)
        fd.c.text((u + lab_dx, v - LEG_R * fd.s - 1.8 + lab_dy), name, size=3.4, weight="bold")


def draw_foot(fd, name, label=True, lab_dy=None):
    x, y, _ = FEET[name]
    h = FOOT_PLATE / 2
    fd.rect(x - h, x + h, y - h, y + h, fill=GREY["mid"], lw="outline")
    fd.circle(x, y, FOOT_PAD / 2, lw="thin", dash="1 0.6")
    for sx in (-1, 1):
        for sy in (-1, 1):
            fd.hole(x + sx * FOOT_SP / 2, y + sy * FOOT_SP / 2, FOOT_HOLE_D, cross=fd.s > 0.12)
    fd.cmark(x, y)
    if label:
        u, v = fd.p(x, y)
        dy = lab_dy if lab_dy is not None else -(h * fd.s + 2.0)
        fd.c.text((u, v + dy), name, size=3.4, weight="bold")


def draw_rail_A(fd, screws=True, text=True):
    x0, x1 = mm(RA["x0"]), mm(RA["x1"]); y0, y1 = mm(RA["y0"]), mm(RA["y1"])
    fd.rect(x0, x1, y0, y1, fill=GREY["steel"], lw="thin")
    fd.c.line(fd.p(x0, y1), fd.p(x1, y1), lw="heavy")
    if screws:
        for st in RA["holes"]:
            fd.hole(x0 + mm(st), y0 + HOLE_OFF, 4.8, cross=False)
    return x0, x1, y0, y1


def draw_rail_B(fd, screws=True, y_min=None):
    x0, x1 = mm(RB["x0"]), mm(RB["x1"]); y0, y1 = mm(RB["y0"]), mm(RB["y1"])
    ys = y0 if y_min is None else max(y0, y_min)
    fd.rect(x0, x1, ys, y1, fill=GREY["steel"], lw="thin")
    fd.c.line(fd.p(x1, ys), fd.p(x1, y1), lw="heavy")
    if screws:
        for st in RB["holes"]:
            yy = y0 + mm(st)
            if yy >= ys:
                fd.hole(x0 + HOLE_OFF, yy, 4.8, cross=False)
    return x0, x1, y0, y1


def draw_plates(fd, y_lo, y_hi, label=True, side_label=False):
    for name, px in PLATES:
        ya, yb = PLATE_Y - PLATE_L / 2, PLATE_Y + PLATE_L / 2
        a, b = max(ya, y_lo), min(yb, y_hi)
        fd.rect(px - PLATE_W / 2, px + PLATE_W / 2, a, b, fill="#fff", lw="outline", dash="2 0.8")
        for h in PLATE_HOLES:
            hy = ya + h
            if y_lo <= hy <= y_hi:
                fd.hole(px, hy, 4.8, cross=fd.s > 0.12)
        if side_label:
            u, v = fd.p(px + PLATE_W / 2, (a + b) / 2)
            fd.c.text((u - 0.9, v), name, size=3.2, weight="bold", anchor="end")
        elif label:   # put the name where it hides no hole
            hs = [ya + h for h in PLATE_HOLES if a <= ya + h <= b]
            cands = [a + (b - a) * k / 20 for k in range(3, 18)]
            ly = max(cands, key=lambda yy: min([abs(yy - h) for h in hs] + [99]))
            u, v = fd.p(px, ly)
            fd.c.label_box((u, v), name, size=3.2, weight="bold", pad=0.5)


def draw_clamp_zones(fd, label=True):
    z = CL["zones"]
    zin = mm(D["zoneIn"])
    for nm, (x0, x1, y0, y1) in (("C1", (mm(z["c1_x"][0]), mm(z["c1_x"][1]), 0, zin)), ("C2", (0, zin, mm(z["c2_y"][0]), mm(z["c2_y"][1])))):
        u0, v0 = fd.p(x0, y0); u1, v1 = fd.p(x1, y1)
        hatch_rect(fd.c, u0, v0, u1, v1, spacing=1.0 if fd.s > 0.1 else 0.7)
        fd.rect(x0, x1, y0, y1, lw="outline")
        if label:
            fd.c.label_box(((u0 + u1) / 2, (v0 + v1) / 2), nm, size=3.2, weight="bold", pad=0.4)


def draw_pads(fd, label=True):
    for i, (x0, x1, y0, y1) in enumerate(PADS):
        fd.rect(x0, x1, y0, y1, lw="thin", dash="1.4 0.8")


def draw_board(fd, x0, x1, y0, y1):
    fd.rect(x0, x1, y0, y1, fill=GREY["wood"], lw="heavy")


def datum_marker(fd, x, y, text="DATUM (0, 0)", anchor="end", dx=-2, dy=-2.5, size=3.2):
    u, v = fd.p(x, y)
    fd.c.raw(f'<circle cx="{_f(u)}" cy="{_f(v)}" r="1.6" fill="#000"/><circle cx="{_f(u)}" cy="{_f(v)}" r="2.6" fill="none" stroke="#000" stroke-width="0.4"/>')
    fd.c.text((u + dx, v + dy), text, size=size, anchor=anchor, weight="bold")


def spread(vals, gap):
    """Label positions at least gap apart, each cluster centred on its members' targets (order kept)."""
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    cl = [[vals[i]] for i in order]               # clusters of target values
    pos = lambda c: sum(c) / len(c) - (len(c) - 1) * gap / 2
    merged = True
    while merged:
        merged = False
        for k in range(len(cl) - 1):
            if pos(cl[k]) + (len(cl[k]) - 1) * gap + gap > pos(cl[k + 1]) + 1e-9:
                cl[k] = cl[k] + cl[k + 1]; del cl[k + 1]; merged = True
                break
    flat = []
    for c in cl:
        p0 = pos(c)
        flat += [p0 + j * gap for j in range(len(c))]
    out = [0] * len(vals)
    for k, i in enumerate(order):
        out[i] = flat[k]
    return out


def to_cm(t):
    """'2145 F1 F3' -> '214.5 F1 F3': ordinate labels are written in mm in the code, printed in cm (tape units)."""
    m = re.match(r"^(-?\d+(?:\.\d+)?)(.*)$", t)
    return (fmt(float(m.group(1)) / 10) + m.group(2)) if m else t


def ord_x(fd, items, edge_y, base_v, up=True, gap=3.7, size=3.1, jog=3.0, cm=True):
    """Ordinate dimensions for desk-x stations: extension from the board edge (desk y = edge_y) to a baseline at page
    v = base_v; labels rotated, reading bottom-to-top. items: [(x_mm, text)]."""
    c = fd.c
    if cm:
        items = [(x, to_cm(t)) for x, t in items]
    us = [fd.u(x) for x, _ in items]
    pos = spread(us, gap)
    ev = fd.v(edge_y)
    sgn = -1 if up else 1
    for (x, t), u, pu in zip(items, us, pos):
        c.line((u, ev + sgn * 0.8), (u, base_v - sgn * jog), lw="dim")
        c.line((u, base_v - sgn * jog), (pu, base_v - sgn * 0.8), lw="dim")
        c.line((pu, base_v - sgn * 0.8), (pu, base_v), lw="dim")
        c.text((pu, base_v + sgn * 0.6), t, size=size, anchor="start" if up else "end", rotate=-90, baseline="middle")


def ord_y(fd, items, edge_x, base_u, right=True, gap=3.7, size=3.1, jog=3.0, cm=True):
    """Ordinate dimensions for desk-y stations, labels horizontal beside a vertical baseline at page u = base_u."""
    c = fd.c
    if cm:
        items = [(y, to_cm(t)) for y, t in items]
    vs = [fd.v(y) for y, _ in items]
    pos = spread(vs, gap)
    eu = fd.u(edge_x)
    sgn = 1 if right else -1
    for (y, t), v, pv in zip(items, vs, pos):
        c.line((eu + sgn * 0.8, v), (base_u - sgn * jog, v), lw="dim")
        c.line((base_u - sgn * jog, v), (base_u - sgn * 0.8, pv), lw="dim")
        c.line((base_u - sgn * 0.8, pv), (base_u, pv), lw="dim")
        c.text((base_u + sgn * 0.8, pv), t, size=size, anchor="start" if right else "end")


def dim2(c, p1, p2, label, off=0.0, size=3.0, ext=True):
    """Linear dimension between page points p1, p2, offset `off` page mm along the normal (left of p1->p2 in page
    coordinates), label upright beside the line on the offset side. (lib.draw.dim puts its text on the line.)"""
    (x1, y1), (x2, y2) = p1, p2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    nx, ny = dy / L, -dx / L
    a1 = (x1 + nx * off, y1 + ny * off); a2 = (x2 + nx * off, y2 + ny * off)
    sg = 1 if off >= 0 else -1
    if ext and off:
        c.line((x1 + nx * sg * 0.6, y1 + ny * sg * 0.6), (a1[0] + nx * sg * 1.2, a1[1] + ny * sg * 1.2), lw="dim")
        c.line((x2 + nx * sg * 0.6, y2 + ny * sg * 0.6), (a2[0] + nx * sg * 1.2, a2[1] + ny * sg * 1.2), lw="dim")
    c.line(a1, a2, lw="dim")
    c._head(a2[0], a2[1], a1[0], a1[1], 1.5); c._head(a1[0], a1[1], a2[0], a2[1], 1.5)
    ang = math.degrees(math.atan2(dy, dx))
    if ang >= 90:
        ang -= 180
    elif ang < -90:
        ang += 180
    tx, ty = (a1[0] + a2[0]) / 2 + nx * sg * 2.0, (a1[1] + a2[1]) / 2 + ny * sg * 2.0
    c.text((tx, ty), label, size=size, rotate=ang if abs(ang) > 0.01 else 0)


def lead(c, target, tp, label, size=3.0, weight="normal"):
    """Leader: dot on the target, thin line to tp, text beside tp on the far side (never crossed by the line)."""
    c.line(target, tp, lw="thin")
    c.raw(f'<circle cx="{_f(target[0])}" cy="{_f(target[1])}" r="0.6" fill="#000"/>')
    right = tp[0] >= target[0]
    c.text((tp[0] + (1.0 if right else -1.0), tp[1]), label, size=size, anchor="start" if right else "end", weight=weight)


def you_marker(c, u, v, text="YOU"):
    c.arrow((u, v + 5.5), (u, v), lw="outline", head=2.2)
    c.text((u, v + 8.6), text, size=3.2, weight="bold")


def datum_dot(c, u, v):
    c.raw(f'<circle cx="{_f(u)}" cy="{_f(v)}" r="1.5" fill="#000"/><circle cx="{_f(u)}" cy="{_f(v)}" r="2.6" fill="none" stroke="#000" stroke-width="0.4"/>')


def foot_labels(fd, names, below=(), left=(), right=()):
    for n in names:
        x, y, _ = FEET[n]
        u, v = fd.p(x, y)
        h = FOOT_PLATE / 2 * fd.s
        if n in left:
            fd.c.text((u - h - 1.0, v), n, size=3.3, weight="bold", anchor="end")
        elif n in right:
            fd.c.text((u + h + 1.0, v), n, size=3.3, weight="bold", anchor="start")
        else:
            fd.c.text((u, v + (h + 2.4 if n in below else -(h + 2.0))), n, size=3.3, weight="bold")


def leg_label(fd, n, where="above"):
    x, y, _ = LEGS[n]
    u, v = fd.p(x, y)
    r = LEG_R * fd.s
    if where == "above":
        fd.c.text((u, v - r - 1.8), n, size=3.3, weight="bold")
    elif where == "below":
        fd.c.text((u, v + r + 2.6), n, size=3.3, weight="bold")
    elif where == "left":
        fd.c.text((u - r - 1.2, v), n, size=3.3, weight="bold", anchor="end")
    else:
        fd.c.text((u + r + 1.2, v), n, size=3.3, weight="bold", anchor="start")


# ============================================================== Fig D-1: datum and the two tops (plan, from above)
def fig_datum():
    s = 1 / 34.0
    W, H = 178, 118
    c = Canvas(W, H)
    ox, oy = 44, 15
    P = lambda x, y: (ox + x * s, oy + y * s)
    gap = F["layout_cm"]["wall_gap"] * 10
    wu, wv = P(-gap, -gap)
    c.line((wu, wv), (P(2490 + 150, 0)[0], wv), lw="heavy")
    c.line((wu, wv), (wu, P(0, 3140 + 60)[1]), lw="heavy")
    hatch_rect(c, wu, wv - 2.2, P(2490 + 150, 0)[0], wv, spacing=1.2)
    hatch_rect(c, wu - 2.2, wv, wu, P(0, 3140 + 60)[1], spacing=1.2)
    c.text((P(2490, 0)[0] + 3, wv - 4.4), "BACK WALL", size=3.0, weight="bold", anchor="start")
    c.text((wu - 4.5, P(0, 2350)[1]), "SIDE WALL", size=3.0, weight="bold", rotate=-90)
    c.poly([P(0, 0), P(2490, 0), P(2490, 650), P(0, 650)], fill=GREY["wood"], lw="heavy")
    c.poly([P(0, 650), P(650, 650), P(650, 3140), P(0, 3140)], fill=GREY["wood"], lw="heavy")
    c.line(P(0, 650), P(650, 650), lw="thin", dash="1.5 1")
    c.text(P(1450, 380), "TOP A (P01): along the back wall", size=3.4, weight="bold")
    c.text(P(380, 1950), "TOP B (P02): along the side wall", size=3.4, weight="bold", rotate=-90)
    c.text((P(1650, 0)[0], P(0, 0)[1] + 3.2), "back edge, unfinished: y = 0", size=3.0)
    c.text((P(1100, 0)[0], P(0, 650)[1] + 3.6), "front edge (rounded, laminated): y = 65 cm", size=3.0, anchor="start")
    c.text((P(0, 0)[0] + 2.7, P(0, 1950)[1]), "side-wall edge, unfinished: x = 0", size=3.0, rotate=-90)
    c.text((P(650, 0)[0] + 2.8, P(0, 1950)[1]), "front edge (rounded, laminated): x = 65 cm", size=3.0, rotate=-90)
    c.text((P(325, 3140)[0], P(0, 3140)[1] + 3.4), "far end", size=3.0)
    c.text((P(2490, 0)[0] + 2.6, P(0, 325)[1]), "far end", size=3.0, rotate=-90)
    lead(c, P(420, 650), (P(900, 920)[0], P(0, 920)[1]), "joint: B's end butts against A's front edge (y = 65 cm)")
    # axes
    c.arrow(P(0, 0), P(520, 0), lw="outline", head=2.0)
    c.arrow(P(0, 0), P(0, 520), lw="outline", head=2.0)
    c.text((P(520, 0)[0], P(0, 0)[1] + 3.4), "x", size=3.6, weight="bold")
    c.text((P(0, 0)[0] + 3.4, P(0, 520)[1]), "y", size=3.6, weight="bold")
    datum_dot(c, ox, oy)
    c.line((ox - 1.8, oy + 1.8), (ox - 9, oy + 9), lw="thin")
    for k, t in enumerate(("DATUM (0, 0):", "top A's", "back-left", "corner")):
        c.text((ox - 9.5, oy + 10.5 + k * 3.7), t, size=3.0, anchor="end", weight="bold" if k == 0 else "normal")
    # seat
    su, sv = P(1150, 1400)
    c.circle((su, sv), 3.5, fill="#fff", lw="outline")
    c.arrow((su - 2.6, sv - 2.6), (su - 9, sv - 9), lw="outline", head=1.8)
    c.text((su + 5, sv + 0.5), "your seat, facing the inside corner", size=3.0, anchor="start")
    # dimensions
    dim2(c, (P(0, 0)[0], oy), (P(2490, 0)[0], oy), "249 cm", off=8.5)
    dim2(c, P(2490, 0), P(2490, 650), "65 cm", off=9)
    dim2(c, P(0, 3140), P(650, 3140), "65 cm", off=-6.5)
    dim2(c, P(0, 0), P(0, 3140), "314 cm", off=-38)
    c.text((W - 1, H - 6), "Both tops: 249 × 65 cm, 28 mm thick, identical. Both stand 3 cm off their walls.", size=3.0, anchor="end")
    c.text((W - 1, H - 1.8), "Plan from above, face up, as installed. Scale 1:34.", size=3.0, anchor="end")
    return c.save(os.path.join(FIG, "04-datum-plan.svg"))


# ============================================================== Fig D-2: face up vs face down (top A)
def fig_flip():
    W, H = 178, 58
    c = Canvas(W, H)
    s = 1 / 36.0
    w, h = 2490 * s, 650 * s
    top = 17
    for k, ox in enumerate((14, 101)):
        c.text((ox + w / 2, 4), ("FACE UP: installed, seen from above", "FACE DOWN: on the blanket, as you mark it")[k], size=3.2, weight="bold")
        c.rect(ox, top, w, h, fill=GREY["wood"] if k == 0 else GREY["light"], lw="heavy")
        du = ox if k == 0 else ox + w
        datum_dot(c, du, top)
        c.text((du + (2 if k == 0 else -2), top - 6.2), "datum, x = 0", size=3.0, anchor="start" if k == 0 else "end", weight="bold")
        c.text((ox + w / 2, top - 2.2), "back edge (taped), y = 0", size=3.0)
        c.text((ox + w / 2, top + h + 3.6), "front edge (rounded)", size=3.0)
        if k == 0:
            c.arrow((ox + 2, top + h / 2 + 3.4), (ox + 16, top + h / 2 + 3.4), lw="outline", head=1.6)
            c.text((ox + 18, top + h / 2 + 3.4), "x grows to the right", size=3.0, anchor="start")
            c.text((ox + w / 2, top + h / 2 - 2.6), "laminate up", size=3.0)
            you_marker(c, ox + w / 2, top + h + 7, "your side when seated")
        else:
            c.arrow((ox + w - 2, top + h / 2 + 3.4), (ox + w - 16, top + h / 2 + 3.4), lw="outline", head=1.6)
            c.text((ox + w - 18, top + h / 2 + 3.4), "x grows to the LEFT", size=3.0, anchor="end", weight="bold")
            c.text((ox + w / 2, top + h / 2 - 2.6), "underside up", size=3.0)
            you_marker(c, ox + w / 2, top + h + 7, "YOU STAND HERE")
    c.arrow((85, top + h / 2), (98, top + h / 2), lw="heavy", head=2.4)
    c.text((91.5, top + h / 2 - 4), "turn", size=3.0)
    c.text((91.5, top + h / 2 + 5), "over", size=3.0)
    return c.save(os.path.join(FIG, "04-flip.svg"))


# ============================================================== top A face-down
def topA_content(fd):
    draw_board(fd, 0, 2490, 0, 650)
    fd.rect(mm(A1["x0"]), mm(A1["x0"] + A1["w"]), mm(A1["y0"]), mm(A1["y0"] + A1["d"]), lw="thin", dash="3 1.5")
    draw_rail_A(fd)
    xb0, xb1 = mm(RB["x0"]), mm(RB["x1"])
    fd.rect(xb0, xb1, mm(RB["y0"]), 650, lw="thin", dash="1.4 0.8")
    for st in RB["holes"][:2]:
        fd.hole(xb0 + HOLE_OFF, mm(RB["y0"]) + mm(st), 4.8, cross=False)
    draw_clamp_zones(fd)
    draw_pads(fd)
    draw_plates(fd, 0, 650, label=True, side_label=fd.s < 0.1)
    for n in ("L1", "L2", "L3"):
        draw_leg(fd, n, label=False)
    for n in ("F1", "F2", "F3", "F4"):
        draw_foot(fd, n, label=False)


def fig_topA_overview():
    s = 1 / 16.0
    W, H = 178, 86
    mL, mT = 8, 33
    c = Canvas(W, H)
    fd = FD(c, (0, 2490, 0, 650), s, mL, mT)
    topA_content(fd)
    xs = [(0, "0"), (mm(RA["x0"]), "10"), (150, "150 L1"), (650, "650 L2"), (1400, "1400 L3"),
          (2145, "2145 F1 F3"), (mm(RA["x1"]), "2140 rail A end"), (2405, "2405 F2 F4"), (2490, "2490")]
    ord_x(fd, xs, 0, mT - 5, up=True, gap=3.8, jog=1.6)
    datum_dot(c, fd.u(0), fd.v(0))
    c.text((fd.u(0) - 3.2, fd.v(0) - 2.6), "DATUM", size=3.0, anchor="end", weight="bold")
    c.text((fd.u(1245), 3), "← x grows to the LEFT · all cm · tape hooked on the side-wall end", size=3.1, weight="bold")
    for n, w in (("L1", "above"), ("L2", "below"), ("L3", "below")):
        leg_label(fd, n, w)
    foot_labels(fd, ("F1", "F2", "F3", "F4"), below=("F2",), right=("F1", "F3"))
    dim2(c, fd.p(1400, 0), fd.p(1400, 100), "10", off=-5.5)
    c.text((fd.u(1100), fd.v(440)), "RAIL A: vertical leg's outer face on y = 53 cm", size=3.0)
    c.text((fd.u(2275), fd.v(325)), "ALEX 1", size=3.0)
    c.text((fd.u(2275), fd.v(325) + 3.6), "below", size=3.0)
    c.text((fd.u(1245), fd.v(650) + 4.2), "FRONT EDGE · rounded, laminated · y = 65 cm · you stand here", size=3.1, weight="bold")
    c.text((fd.u(0) + 3.0, fd.v(325)), "side-wall end, x = 0", size=3.0, rotate=-90)
    c.text((fd.u(2490) - 3.0, fd.v(325)), "far end", size=3.0, rotate=-90)
    c.text((W - 1, H - 1.5), "Scale 1:16. y: tape hooked on the back edge. Details: Figs D-4, D-5.", size=3.0, anchor="end")
    return c.save(os.path.join(FIG, "04-topA-overview.svg"))


def fig_topA_corner():
    s = 1 / 5.0
    W, H = 178, 184
    mL, mT = 4, 40
    c = Canvas(W, H)
    fd = FD(c, (0, 720, 0, 650), s, mL, mT)
    fd.clip_begin(); topA_content(fd); fd.clip_end()
    u = fd.u(720)
    c.line((u, fd.v(0) - 1), (u, fd.v(650) + 1), lw="thin", dash="3 1 0.6 1")
    p1, p2 = CL["pad_plates"]["p1"], CL["pad_plates"]["p2"]
    xs = [(0, "0"), (mm(RA["x0"]), "10 rail A wall end"), (150, "150 L1, P1"), (mm(p1["x"][0]), "200"), (350, "350 P2"),
          (mm(CL["zones"]["c1_x"][0]), "360"), (400, "400 clamp 1"), (mm(CL["zones"]["c1_x"][1]), "440"), (mm(p1["x"][1]), "454"),
          (mm(RB["x0"]), "479"), (mm(RB["x1"]), "530 rail B line"), (650, "650 L2")]
    ord_x(fd, xs, 0, mT - 4, up=True, gap=4.0, jog=1.6)
    ys = [(0, "0"), (mm(p1["y"][0]), "5"), (mm(p1["y"][1]), "81"), (mm(D["zoneIn"]), "90"), (100, "100 L2"),
          (mm(p2["y"][0]), "200"), (mm(CL["zones"]["c2_y"][0]), "360"), (400, "400 clamp 2"), (420, "420 L1"),
          (mm(CL["zones"]["c2_y"][1]), "440"), (mm(p2["y"][1]), "454"), (mm(RA["y0"]), "479"), (mm(RA["y1"]), "530 rail A"),
          (PLATE_Y - PLATE_L / 2, "533 P1 P2"), (650, "650")]
    ord_y(fd, ys, 0, fd.u(0) + 8, right=True, gap=3.75, jog=2.4)
    datum_dot(c, fd.u(0), fd.v(0))
    c.text((fd.u(0) - 3.4, fd.v(0) + 4.2), "DATUM", size=3.0, anchor="end", weight="bold")
    leg_label(fd, "L1", "above"); leg_label(fd, "L2", "below")
    # labels inside outlines
    pu, pv = fd.p((mm(p1["x"][0]) + mm(p1["x"][1])) / 2, (mm(p1["y"][0]) + mm(p1["y"][1])) / 2)
    pu, pv = fd.p(280, 43)
    c.text((pu, pv - 1.8), "pad plate 1", size=3.0); c.text((pu, pv + 1.9), "(outline only)", size=3.0)
    pu, pv = fd.p((mm(p2["x"][0]) + mm(p2["x"][1])) / 2, (mm(p2["y"][0]) + mm(p2["y"][1])) / 2)
    pu, pv = fd.p(43, 280)
    c.text((pu - 1.8, pv), "pad plate 2", size=3.0, rotate=-90); c.text((pu + 1.9, pv), "(outline only)", size=3.0, rotate=-90)
    lead(c, fd.p(530, 600), fd.p(590, 600), "rail B end, later")
    c.label_box(fd.p(170, 505), "RAIL A", size=3.2, weight="bold", pad=0.6)
    lead(c, fd.p(150, 420 + LEG_R), fd.p(330, 440), "6.5 mm clear of rail A")
    c.text((fd.u(360), fd.v(650) + 4.2), "FRONT EDGE · rounded · y = 65 · top B butts here · you stand here", size=3.1, weight="bold")
    c.text((2, 3), "BACK EDGE · y = 0 · away from you · all cm", size=3.1, weight="bold", anchor="start")
    c.text((fd.u(360), fd.v(650) + 9.4), "x: tape hooked on the side-wall end · y: tape hooked on the back edge · Scale 1:5", size=3.0)
    return c.save(os.path.join(FIG, "04-topA-corner.svg"))


def fig_topA_far():
    s = 1 / 4.5
    W, H = 124, 190
    mL, mT = 22, 33
    c = Canvas(W, H)
    fd = FD(c, (2040, 2490, 0, 650), s, mL, mT)
    fd.clip_begin(); topA_content(fd); fd.clip_end()
    u = fd.u(2040)
    c.line((u, fd.v(0) - 1), (u, fd.v(650) + 1), lw="thin", dash="3 1 0.6 1")
    xs = [(2490, "2490 far end"), (2455, "2455"), (2405, "2405 F2 F4"), (2145, "2145 F1 F3"), (mm(RA["x1"]), "2140 rail A end"), (mm(A1["x0"]), "2095")]
    ord_x(fd, xs, 0, mT - 4, up=True, gap=4.0, jog=1.6)
    ys = [(0, "0"), (mm(A1["y0"]), "35"), (85, "85 F1 F2"), (mm(RA["y0"]), "479"), (mm(RA["y1"]), "530 rail"), (565, "565 F3 F4"), (mm(A1["y0"] + A1["d"]), "615"), (650, "650")]
    ord_y(fd, ys, 2490, fd.u(2490) - 2.5, right=False, gap=3.75, jog=1.4)
    foot_labels(fd, ("F1", "F2", "F3", "F4"), below=("F1", "F2", "F3", "F4"))
    cu = fd.u(2275)
    for k, t in enumerate(("ALEX 1 outline below,", "x 209.5–245.5, y 3.5–61.5 cm", "(reference only)")):
        c.text((cu, fd.v(250) + k * 4), t, size=3.0)
    x, y, _ = FEET["F2"]
    lead(c, fd.p(x - FOOT_SP / 2, y + FOOT_SP / 2), fd.p(2380, 170), "4 × ⌀5.2 mm on a 46.8 mm square", size=3.0)
    c.text((fd.u(2265), fd.v(650) + 4.2), "FRONT EDGE · y = 65", size=3.1, weight="bold")
    c.text((fd.u(2265), fd.v(650) + 9.2), "All cm. x: tape on the side-wall end. y: tape on the back edge. 1:4.5", size=3.0)
    c.text((fd.u(2265), 3), "BACK EDGE · y = 0", size=3.1, weight="bold")
    return c.save(os.path.join(FIG, "04-topA-far.svg"))


# ============================================================== top B face-down
def topB_content(fd):
    draw_board(fd, 0, 650, 650, 3140)
    fd.rect(mm(A2["x0"]), mm(A2["x0"] + A2["w"]), mm(A2["y0"]), mm(A2["y0"] + A2["d"]), lw="thin", dash="3 1.5")
    x0, x1 = mm(RB["x0"]), mm(RB["x1"])
    fd.rect(x0, x1, mm(RB["y0"]), 650, lw="thin", dash="1.4 0.8")
    draw_rail_B(fd, y_min=650)
    for st in RB["holes"][:2]:
        fd.hole(x0 + HOLE_OFF, mm(RB["y0"]) + mm(st), 4.8, cross=False)
    draw_plates(fd, 650, 3140, label=True, side_label=fd.s < 0.1)
    for n in ("L4", "L5", "L6"):
        draw_leg(fd, n, label=False)
    for n in ("F5", "F6", "F7", "F8"):
        draw_foot(fd, n, label=False)


def fig_topB_overview():
    s = 1 / 14.0
    W, H = 80, 232
    mL, mT = 7, 30
    c = Canvas(W, H)
    fd = FD(c, (0, 650, 520, 3140), s, mL, mT)
    topB_content(fd)
    ys = [(650, "0"), (850, "20"), (1600, "95"), (2350, "170"),
          (mm(RB["y1"]), "201"), (2795, "214.5"), (3055, "240.5"), (3140, "249")]
    ord_y(fd, ys, 0, fd.u(0) + 3.5, right=True, gap=3.7, jog=1.2, size=3.0, cm=False)
    xs = [(0, "0"), (85, "85"), (100, "100"), (mm(RB["x0"]), "479"), (mm(RB["x1"]), "530"), (565, "565"), (650, "650")]
    ord_x(fd, xs, 650, mT - 13, up=True, gap=3.4, jog=1.2, size=3.0)
    for n in ("L4", "L5", "L6"):
        leg_label(fd, n, "left")
    foot_labels(fd, ("F5", "F6", "F7", "F8"), below=("F5", "F6"))
    c.text((1, 3), "JOINT END away from you", size=3.0, weight="bold", anchor="start")
    c.text((1, 6.8), "← x grows to the LEFT", size=3.0, weight="bold", anchor="start")
    c.text((fd.u(325), fd.v(3140) + 4.0), "far end", size=3.0)
    c.text((fd.u(650) - 2.6, fd.v(1250)), "front edge, rounded, x = 65", size=3.0, rotate=-90)
    c.text((fd.u(0) + 2.6, fd.v(1250)), "side-wall edge, x = 0", size=3.0, rotate=90)
    c.text((fd.u(505), fd.v(1250)), "RAIL B", size=3.0, rotate=-90, weight="bold")
    c.text((fd.u(325), fd.v(2925)), "ALEX 2", size=3.0)
    c.text((1, H - 5.4), "All cm. Right: tape hooked on the joint end.", size=3.0, anchor="start")
    c.text((1, H - 1.6), "Top: tape on the side-wall edge. 1:14", size=3.0, anchor="start")
    return c.save(os.path.join(FIG, "04-topB-overview.svg"))


def fig_topB_joint():
    s = 1 / 5.0
    W, H = 178, 138
    mL, mT = 4, 36
    c = Canvas(W, H)
    fd = FD(c, (0, 650, 500, 950), s, mL, mT)
    fd.clip_begin()
    u0, v0 = fd.p(650, 500); u1, v1 = fd.p(0, 650)
    hatch_rect(c, u0, v0, u1, v1, spacing=2.5, sw=0.15)
    topB_content(fd)
    fd.clip_end()
    v = fd.v(950)
    c.line((fd.u(650) - 1, v), (fd.u(0) + 1, v), lw="thin", dash="3 1 0.6 1")
    xs = [(0, "0"), (100, "100 L4"), (150, "150 P1"), (350, "350 P2"), (mm(RB["x0"]), "479"), (mm(RB["x1"]), "530 rail B line"), (650, "650")]
    ord_x(fd, xs, 500, mT - 4, up=True, gap=4.0, jog=1.6)
    ys = [(mm(RB["y0"]), "rail B end, 12 past"), (650, "0 joint end"), (PLATE_Y - PLATE_L / 2 + PLATE_HOLES[2], "6.7"),
          (PLATE_Y - PLATE_L / 2 + PLATE_HOLES[3], "11.7"), (PLATE_Y + PLATE_L / 2, "13.7 P1 P2 end"), (850, "20 L4")]
    ord_y(fd, ys, 0, fd.u(0) + 5, right=True, gap=3.8, jog=2.0, cm=False)
    leg_label(fd, "L4", "left")
    c.label_box(fd.p(250, 545), "top A goes here (not this top)", size=3.0, pad=0.8)
    lead(c, fd.p(505, 580), fd.p(420, 615), "")
    c.label_box((fd.u(420) + 35.8, fd.v(615)), "rail B sticks out 12 cm past the joint end", size=3.0, pad=0.8)
    c.text((fd.u(325), H - 5.6), "All cm. Top: tape hooked on the side-wall edge. Right: tape hooked on the joint end.", size=3.0)
    c.text((fd.u(325), H - 1.6), "Joint end away from you, x grows to the left. Scale 1:5", size=3.0)
    return c.save(os.path.join(FIG, "04-topB-joint.svg"))


def fig_topB_far():
    s = 1 / 5.0
    W, H = 178, 152
    mL, mT = 4, 30
    c = Canvas(W, H)
    fd = FD(c, (0, 650, 2600, 3140), s, mL, mT)
    fd.clip_begin(); topB_content(fd); fd.clip_end()
    v = fd.v(2600)
    c.line((fd.u(650) - 1, v), (fd.u(0) + 1, v), lw="thin", dash="3 1 0.6 1")
    xs = [(0, "0"), (mm(A2["x0"]), "35"), (85, "85 F5 F7"), (mm(RB["x0"]), "479"), (mm(RB["x1"]), "530"), (565, "565 F6 F8"), (mm(A2["x0"] + A2["w"]), "615"), (650, "650")]
    ord_x(fd, xs, 2600, mT - 4, up=True, gap=4.0, jog=1.6)
    ys = [(mm(RB["y1"]), "201 rail end"), (mm(A2["y0"]), "209.5 ALEX 2"), (2795, "214.5 F5 F6"), (3055, "240.5 F7 F8"),
          (mm(A2["y0"] + A2["d"]), "245.5"), (3140, "249 far end")]
    ord_y(fd, ys, 0, fd.u(0) + 5, right=True, gap=3.8, jog=2.0, cm=False)
    foot_labels(fd, ("F5", "F6", "F7", "F8"), below=("F7", "F8"))
    c.text((fd.u(325), fd.v(2900)), "ALEX 2 outline below (reference only)", size=3.0)
    c.text((fd.u(325), fd.v(3140) + 4.2), "FAR END", size=3.1, weight="bold")
    c.text((fd.u(325), H - 1.6), "All cm. Top: tape on the side-wall edge. Right: tape hooked on the joint end. 1:5", size=3.0)
    return c.save(os.path.join(FIG, "04-topB-far.svg"))


# ============================================================== rails: labels and orientation
def fig_rail_orientation():
    W, H = 178, 68
    c = Canvas(W, H)
    s = 0.55
    ox, oy = 14, 26
    Yp = lambda y: ox + (y - 400) * s
    T, ang, wall = F["tops"]["thickness"], mm(D["angle"]), F["steel"]["thickness"]
    c.rect(Yp(400), oy - T * s, (650 - 400) * s - 2.5, T * s, fill=GREY["wood"], lw="outline")
    hatch_rect(c, Yp(400), oy - T * s, Yp(650) - 2.5, oy, spacing=1.6, sw=0.15)
    c.raw(f'<path d="M {_f(Yp(650) - 2.5)} {_f(oy - T * s)} q 2.5 0 2.5 {_f(T * s / 2)} q 0 {_f(T * s / 2)} -2.5 {_f(T * s / 2)}" fill="{GREY["wood"]}" stroke="#000" stroke-width="0.5"/>')
    c.line((Yp(400), oy - T * s), (Yp(400), oy), lw="thin", dash="2 1")
    y0, y1 = mm(RA["y0"]), mm(RA["y1"])
    pts = [(Yp(y0), oy), (Yp(y1), oy), (Yp(y1), oy + ang * s), (Yp(y1 - wall), oy + ang * s), (Yp(y1 - wall), oy + wall * s), (Yp(y0), oy + wall * s)]
    c.poly(pts, fill=GREY["dark"], lw="outline")
    sy = y0 + HOLE_OFF
    c.rect(Yp(sy) - 1.3, oy - 20.6 * s, 2.6, 20.6 * s, fill="#fff", lw="thin")
    c.raw(f'<path d="M {_f(Yp(sy) - 2.6)} {_f(oy + wall * s)} h 5.2 v 0.8 q -2.6 1.4 -5.2 0 z" fill="#000"/>')
    lead(c, (Yp(y0 + 8), oy + wall * s / 2), (Yp(y0 + 30), oy + 33), "flat leg UP, tight against the underside")
    lead(c, (Yp(y1), oy + ang * s * 0.75), (Yp(y1) + 24, oy + 21), "vertical leg DOWN, on the front-edge side")
    lead(c, (Yp(y1), oy + 4), (Yp(y1) + 24, oy + 12), "its outer face on the rail line (top A: y = 53 cm)")
    dim2(c, (Yp(y1), oy - T * s), (Yp(650), oy - T * s), "12 cm to the front edge", off=5)
    c.label_box((Yp(590), oy - T * s / 2), "TOP A, laminate up (as installed)", size=3.0, weight="bold", pad=0.8)
    c.text((Yp(650) + 3, oy - T * s / 2), "front edge", size=3.0, anchor="start")
    c.text((Yp(400) + 1, oy + 8), "← back wall side", size=3.0, anchor="start")
    c.text((W - 1, H - 1.5), "Section through top A and rail A, end-on, about 1:2. Rail B on top B: the same, outer face on x = 53 cm.", size=3.0, anchor="end")
    return c.save(os.path.join(FIG, "04-rail-orientation.svg"))


def fig_rail_labels():
    W, H = 178, 44
    c = Canvas(W, H)
    L, ox = 146, 30
    for i, (name, endname, holes) in enumerate((("RAIL A", "WALL END", RA["holes"]), ("RAIL B", "CORNER END", RB["holes"]))):
        y = 6 + i * 18
        c.rect(ox, y, L, 5, fill=GREY["steel"], lw="outline")
        c.line((ox, y + 5), (ox + L, y + 5), lw="heavy")
        for st in holes:
            c.circle((ox + st * 10 / 2130 * L, y + 2.0), 0.5, fill="#fff", lw="thin")
        hatch_rect(c, ox - 6, y - 0.5, ox, y + 5.5, spacing=0.9)
        c.rect(ox - 6, y - 0.5, 6, 6, lw="outline")
        c.text((ox - 7.5, y + 2.5), name, size=3.2, anchor="end", weight="bold")
        c.text((ox - 6, y + 9.6), f"tape flag on the end: “{name[-1]} · {endname}”  (stations measured from this end)", size=3.0, anchor="start")
        c.text((ox + L, y + 9.6), "far end", size=3.0, anchor="end")
    c.text((W - 1, H - 1.5), "Bench view, flat leg up. Holes shown for orientation; positions are in chapter E.", size=3.0, anchor="end")
    return c.save(os.path.join(FIG, "04-rail-labels.svg"))


# ============================================================== hole types and depths
def fig_depths():
    s = 2.0
    W, H = 178, 122
    c = Canvas(W, H)
    T = F["tops"]["thickness"]; lim = F["tops"]["max_fastener_depth"]
    x0, x1 = 12, 140
    yb = 32
    yt = yb + T * s
    c.rect(x0, yb, x1 - x0, T * s, fill=GREY["wood"], lw="outline")
    c.rect(x0, yt - 0.9, x1 - x0, 0.9, fill="#000", lw="thin")
    yl = yb + lim * s
    c.line((x0, yl), (x1 + 4, yl), lw=0.5, dash="2.5 1")
    c.text((x0 + 1.5, yl + 3.2), "21 mm LIMIT: no screw tip and no pilot past this line", size=3.0, anchor="start", weight="bold")
    c.text((x0 + 1.5, yt - 3.0), "7 mm of wood must remain above the laminate", size=3.0, anchor="start")
    c.text((x0 + 1.5, yt + 3.4), "laminate face (desk surface), down on the blanket", size=3.0, anchor="start")
    dim2(c, (x0, yt), (x0, yb), "28 mm", off=4)

    def screw(u, depth, part_t, pilot, l1, l2, puck, head="pan"):
        if part_t:
            c.rect(u - 6.5, yb - part_t * s, 13, part_t * s, fill=GREY["dark"], lw="thin")
        c.rect(u - 0.9, yb, 1.8, pilot * s, fill="#fff", lw=0.2, dash="0.8 0.5")
        top_v = yb - part_t * s
        c.poly([(u - 1.6, top_v), (u + 1.6, top_v), (u + 1.6, yb + depth * s - 2), (u, yb + depth * s), (u - 1.6, yb + depth * s - 2)], fill="#fff", lw="outline")
        k = 1
        while top_v + k * 1.6 < yb + depth * s - 2:
            yy = top_v + k * 1.6
            c.line((u - 1.6, yy), (u + 1.6, yy + 0.6), lw=0.15); k += 1
        c.raw(f'<path d="M {_f(u - 3.4)} {_f(top_v)} v -1.2 q 3.4 -2.2 6.8 0 v 1.2 z" fill="#000"/>')
        c.text((u, 4.2), l1, size=3.0, weight="bold")
        c.text((u, 8.0), l2, size=3.0)
        c.text((u + 2.4, yb + depth * s - 3.0), f"{fmt(depth)}", size=3.0, anchor="start", weight="bold")
        c.text((u, yt + 9.0), f"pilot {fmt(pilot)}", size=3.0, weight="bold")
        c.text((u, yt + 12.8), puck, size=3.0)

    screw(27, 13, 3, 15, "OLOV plate", "M4 × 16", "15 LEG")
    screw(55, 14, 1.8, 15, "foot plate", "#8 × 5/8", "15 LEG")
    screw(84, 20.6, F["steel"]["thickness"], 20, "rail flat leg", "#10 × 1", "25 RAIL")
    screw(113, 13, 3, 12, "joining plate", "#10 × 5/8", "12 PLATE")
    c.text((84, yt + 16.6), "(25 from the steel face)", size=3.0)
    # trim: sideways into the raw back edge (right end of the section), 14 below the surface
    tv = yt - 14 * s
    c.rect(x1 - 10 * s, tv - 0.9, 10 * s, 1.8, fill="#fff", lw=0.2, dash="0.8 0.5")
    c.arrow((x1 + 15, tv), (x1 + 1, tv), lw="outline", head=1.8)
    c.text((x1 + 2, tv - 6), "trim #4 × 1/2", size=3.0, anchor="start", weight="bold")
    c.text((x1 + 2, tv + 4.0), "pilot 10, 10 EDGE,", size=3.0, anchor="start")
    c.text((x1 + 2, tv + 7.8), "14 mm below the surface", size=3.0, anchor="start")
    c.text((x1 + 2, yb - 4), "raw back edge", size=3.0, anchor="start")
    c.text((x0 + 1.5, H - 5.4), "Section through a 28 mm top, face down as you drill it (underside up), 2:1. Grey: the part being screwed on.", size=3.0, anchor="start")
    c.text((x0 + 1.5, H - 1.6), "Dashed: the pilot hole. Bold numbers: how far the screw goes into the wood, mm.", size=3.0, anchor="start")
    return c.save(os.path.join(FIG, "04-depths.svg"))


def fig_ring_depth():
    """Ring screw into the ALEX top: the panel thickness is unknown (MEASURE)."""
    s = 2.0
    W, H = 60, 76
    c = Canvas(W, H)
    yb = 22
    # ALEX top panel: thickness unknown -> drawn with a break line, labelled
    c.rect(4, yb, 52, 34, fill=GREY["wood"], lw="outline")
    c.raw(f'<path d="M 4 {_f(yb + 34)} l 13 0 l 2 -2 l 2 4 l 2 -2 l 33 0" fill="none" stroke="#000" stroke-width="0.25"/>')
    c.rect(18, yb - 2.5 * s, 24, 2.5 * s, fill=GREY["dark"], lw="thin")
    u = 30
    c.rect(u - 0.8, yb, 1.6, 12 * s, fill="#fff", lw=0.2, dash="0.8 0.5")
    c.poly([(u - 3.2, yb - 2.5 * s), (u + 3.2, yb - 2.5 * s), (u + 1.4, yb - 2.5 * s + 1.8), (u + 1.4, yb + 13 * s - 2), (u, yb + 13 * s), (u - 1.4, yb + 13 * s - 2), (u - 1.4, yb - 2.5 * s + 1.8)], fill="#fff", lw="outline")
    c.text((u + 3, yb + 13 * s - 1), "13 mm", size=3.0, anchor="start", weight="bold")
    c.text((30, 4), "ring flange", size=3.0, weight="bold")
    c.text((30, 7.8), "#6 × 5/8 flat head", size=3.0)
    c.text((30, 11.6), "pilot 12, 12 ALEX", size=3.0)
    c.text((30, yb + 40), "ALEX top panel:", size=3.0, weight="bold")
    c.text((30, yb + 43.8), "thickness unknown,", size=3.0)
    c.text((30, yb + 47.6), "must be 16 mm or more", size=3.0)
    return c.save(os.path.join(FIG, "04-ring-depth.svg"))


def fig_hole_types():
    W, H = 178, 34
    c = Canvas(W, H)
    items = [
        (18, 1 / 8 * 25.4, "pilot ⌀3.2 (1/8 in)", "into the tops: legs, feet,", "rails, joining plates"),
        (52, 5 / 64 * 25.4, "pilot ⌀2.0 (5/64 in)", "into the ALEX tops", "and the trim edge"),
        (87, 5.56, "clearance ⌀5.56", "(7/32 in): rail flat", "legs, for #10 screws"),
        (121, 11.1, "through ⌀11.1 (7/16 in)", "rail vertical legs,", "6 holes, 3/8 bolts"),
    ]
    for u, d, t1, t2, t3 in items:
        c.circle((u, 10), d / 2, fill="#fff", lw="outline")
        m = d / 2 + 1.5
        c.line((u - m, 10), (u + m, 10), lw="thin"); c.line((u, 10 - m), (u, 10 + m), lw="thin")
        c.text((u, 21.5), t1, size=3.0, weight="bold"); c.text((u, 25.3), t2, size=3.0); c.text((u, 29.1), t3, size=3.0)
    u = 157   # the fittings' own slots (bought, not drilled), 21 x 12
    c.rect(u - 10.5, 4, 21, 12, fill="#fff", lw="outline", rx=6)
    c.line((u - 12, 10), (u + 12, 10), lw="thin"); c.line((u, 2.5), (u, 17.5), lw="thin")
    c.text((u, 21.5), "slot 21 × 12", size=3.0, weight="bold"); c.text((u, 25.3), "in each fitting leg,", size=3.0); c.text((u, 29.1), "bought, not drilled", size=3.0)
    c.text((W - 1, 2.5), "1:1", size=3.0, anchor="end")
    return c.save(os.path.join(FIG, "04-hole-types.svg"))


ALL = (fig_datum, fig_flip, fig_topA_overview, fig_topA_corner, fig_topA_far, fig_topB_overview, fig_topB_joint, fig_topB_far,
       fig_rail_orientation, fig_rail_labels, fig_depths, fig_ring_depth, fig_hole_types)

if __name__ == "__main__":
    os.makedirs(FIG, exist_ok=True)
    for fn in ALL:
        print(fn())
