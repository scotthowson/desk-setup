#!/usr/bin/env python3
"""Chapter C figures: one line-art silhouette per part P01-P21, hardware H01-H11 at 1:1 where stated, and the
printed-tool icons (also used by chapter B). Sizes come from manual/facts.json and manual/data.json."""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.dirname(HERE)
sys.path.insert(0, MAN); sys.path.insert(0, HERE)
from lib.draw import Canvas, GREY, _f  # noqa: E402
from figures_04 import hatch_rect, dim2  # noqa: E402

F = json.load(open(os.path.join(MAN, "facts.json")))
D = json.load(open(os.path.join(MAN, "data.json")))
FIG = os.path.join(MAN, "figures")
IN = 25.4
W, H = 52, 30          # part card drawing size, page mm


def save(c, name):
    return c.save(os.path.join(FIG, name))


def iso_pt(ox, oy, s):
    """Iso projection to page: x right-down, y right-up, z up."""
    c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))
    return lambda x, y, z: (ox + (x - y) * c30 * s, oy - ((x + y) * s30 + z) * s)


def iso_fit(boxes, x0, y0, x1, y1):
    """Projection that fits all boxes (x, y, z, dx, dy, dz) into the page rectangle x0..x1, y0..y1."""
    c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))
    pts = []
    for (x, y, z, dx, dy, dz) in boxes:
        for a in (x, x + dx):
            for b in (y, y + dy):
                for h in (z, z + dz):
                    pts.append(((a - b) * c30, (a + b) * s30 + h))
    us = [p[0] for p in pts]; vs = [p[1] for p in pts]
    s = min((x1 - x0) / (max(us) - min(us)), (y1 - y0) / (max(vs) - min(vs)))
    ox = x0 + ((x1 - x0) - (max(us) - min(us)) * s) / 2 - min(us) * s
    oy = y1 - ((y1 - y0) - (max(vs) - min(vs)) * s) / 2 + min(vs) * s
    return lambda x, y, z: (ox + (x - y) * c30 * s, oy - ((x + y) * s30 + z) * s)


def iso_box(c, P, x, y, z, dx, dy, dz, fills=("#fff", GREY["light"], GREY["mid"]), lw="outline"):
    top = [P(x, y, z + dz), P(x + dx, y, z + dz), P(x + dx, y + dy, z + dz), P(x, y + dy, z + dz)]
    front = [P(x, y, z), P(x + dx, y, z), P(x + dx, y, z + dz), P(x, y, z + dz)]       # face toward -y (left-front)
    side = [P(x, y, z), P(x, y + dy, z), P(x, y + dy, z + dz), P(x, y, z + dz)]          # face toward -x (right-front)
    c.poly(top, fill=fills[0], lw=lw); c.poly(front, fill=fills[1], lw=lw); c.poly(side, fill=fills[2], lw=lw)


# ------------------------------------------------------------------ parts
def p_top(label):
    c = Canvas(W, H)
    P = iso_fit([(0, 0, 0, 2490, 650, 112)], 2, 6, W - 2, H - 2)
    iso_box(c, P, 0, 0, 0, 2490, 650, 28 * 4, fills=(GREY["wood"], GREY["light"], GREY["mid"]))  # thickness x4 for legibility
    c.text(P(1245, 325, 112), label, size=3.4, weight="bold")
    c.text((1, 3), "thickness drawn ×4", size=3.0, anchor="start")
    return c


def p_alex(door):
    c = Canvas(W, H)
    P = iso_fit([(0, 0, 0, 360, 580, 700)], 2, 2, 34, H - 2)
    iso_box(c, P, 0, 0, 0, 360, 580, 700)
    if door:   # one door on the narrow front face (x = 360 side faces the viewer's right)
        f = [P(25, 0, 25), P(335, 0, 25), P(335, 0, 675), P(25, 0, 675)]
        c.poly(f, fill="none", lw="thin")
        c.circle(P(300, 0, 360), 0.5, fill="#000", lw="thin")
    else:
        for k in range(1, 5):
            z = 700 * k / 5
            c.line(P(0, 0, z), P(360, 0, z), lw="thin")
        for k in range(5):
            z = 700 * (k + 0.5) / 5
            c.line(P(140, 0, z), P(220, 0, z), lw="outline")
    c.text((43, 15), "front", size=3.0)
    return c


def p_olov():
    c = Canvas(W, H)
    s = 0.03
    cx, top = 14, 3
    # elevation: plate, tube, foot
    c.rect(cx - 52.5 * s, top, 105 * s, 1.0, fill=GREY["dark"], lw="thin")
    L = 802 * s
    c.poly([(cx - 0.9, top + 1), (cx + 0.9, top + 1), (cx + 0.7, top + L - 2), (cx - 0.7, top + L - 2)], fill=GREY["light"], lw="outline")
    c.rect(cx - 1.4, top + L - 2, 2.8, 2, fill=GREY["dark"], lw="thin")
    # plan of the plate, 1:2 inset
    k = 0.2
    pc = (38, 14)
    c.circle(pc, 52.5 * k, fill=GREY["light"], lw="outline")
    for i in range(5):
        a = math.radians(-90 + i * 72)
        c.circle((pc[0] + 42.5 * k * math.cos(a), pc[1] + 42.5 * k * math.sin(a)), 0.55, fill="#fff", lw="thin")
    c.text((pc[0], 28.5), "plate ⌀105 mm", size=3.0)
    return c


def p_rail(label):
    c = Canvas(W, H)
    # long bar in elevation + end section 1:2
    c.rect(2, 10, 26, 2.5, fill=GREY["steel"], lw="outline")
    c.line((2, 12.5), (28, 12.5), lw="heavy")
    c.text((15, 6), "RAIL " + label, size=3.2, weight="bold")
    c.text((15, 17), "213 cm long", size=3.0)
    s = 0.36
    ox, oy = 31, 3
    a, t = 50.8 * s, 4.76 * s
    c.poly([(ox, oy), (ox + a, oy), (ox + a, oy + t), (ox + t, oy + t), (ox + t, oy + a), (ox, oy + a)], fill=GREY["dark"], lw="outline")
    c.text((ox + a / 2 + 2, oy + a + 3.6), "end, 1:2.8", size=3.0)
    return c


def p_fitting():
    """One leg in plan (heel on the left) with its two slots dimensioned, plus the L-and-gusset profile."""
    c = Canvas(W, H)
    cj = F["corner_joint"]
    L, w, t = 100.5, 41, 5                       # from cj["fittings"] (measured 23 Oct 2026)
    sl, sw, s1, s2 = 21, 12, 29.15, 78.45
    s = 0.36
    x0, y0 = 1.5, 11.2
    c.rect(x0, y0, L * s, w * s, fill=GREY["light"], lw="outline")
    c.line((x0, y0), (x0, y0 + w * s), lw="heavy")
    for sc in (s1, s2):
        cx = x0 + sc * s
        c.rect(cx - sl / 2 * s, y0 + (w - sw) / 2 * s, sl * s, sw * s, fill="#fff", lw="outline", rx=sw / 2)
        c.line((cx, y0 + w * s / 2 - 3), (cx, y0 + w * s / 2 + 3), lw="thin")
    dim2(c, (x0, y0), (x0 + s1 * s, y0), "", off=2.8)
    c.text((x0 + s1 * s + 1.0, y0 - 2.8), "29.15", size=3.0, anchor="start")
    dim2(c, (x0, y0 - 0.01), (x0 + s2 * s, y0 - 0.01), "78.45", off=6.6)
    c.text((x0 + 1.2, y0 + w * s + 2.6), "heel", size=3.0, anchor="start")
    c.text((x0 + L * s / 2 + 6, y0 + w * s + 2.6), "100.5 × 41 mm leg", size=3.0)
    # profile: L with gusset, 1:5
    k, px, py = 0.09, 44.5, 27
    c.poly([(px, py), (px + L * k, py), (px + L * k, py - t * k * 2), (px + t * k * 2, py - t * k * 2), (px + t * k * 2, py - L * k), (px, py - L * k)], fill=GREY["dark"], lw="thin")
    c.poly([(px + 0.9, py - 0.9), (px + 5, py - 0.9), (px + 0.9, py - 5)], fill=GREY["mid"], lw="thin")
    return c


def p_foot():
    c = Canvas(W, H)
    s = 0.24
    cx, top = 26, 2
    pw = 59.5 * s
    c.rect(cx - pw / 2, top, pw, 0.8, fill=GREY["dark"], lw="thin")
    c.rect(cx - 0.9, top + 0.8, 1.8, 30 * s, fill="#fff", lw="thin")
    for k in range(1, 7):
        y = top + 0.8 + k * 30 * s / 7
        c.line((cx - 0.9, y), (cx + 0.9, y + 0.4), lw=0.15)
    by = top + 0.8 + 30 * s
    c.rect(cx - 25 * s, by, 50 * s, 56 * s, fill=GREY["steel"], lw="outline")
    c.rect(cx - 25 * s, by + 56 * s, 50 * s, 102 * s - 0.8 - 86 * s, fill=GREY["dark"], lw="outline")
    dim2(c, (cx + pw / 2 + 4, top), (cx + pw / 2 + 4, top + 102 * s), "102 mm", off=-0.1)
    c.text((cx - pw / 2 - 1, top + 1), "plate", size=3.0, anchor="end")
    c.text((cx - 25 * s - 1, by + 7), "body", size=3.0, anchor="end")
    c.text((cx - 25 * s - 1, top + 102 * s - 1), "pad", size=3.0, anchor="end")
    return c


def p_ring():
    c = Canvas(W, H)
    s = 0.4
    cx, base = 16, 22
    fo, ro, bo = F["rings"]["flange_od"] * s / 2, F["rings"]["od"] * s / 2, F["rings"]["bore"] * s / 2
    ft, rh = 2.5 * s, 10 * s
    c.rect(cx - fo, base - ft, 2 * fo, ft, fill="#fff", lw="outline")
    c.rect(cx - ro, base - ft - rh, 2 * ro, rh, fill="#fff", lw="outline")
    hatch_rect(c, cx + bo, base - ft - rh, cx + ro, base, spacing=0.5)
    hatch_rect(c, cx + ro, base - ft, cx + fo, base, spacing=0.5)
    c.line((cx + bo, base - ft - rh), (cx + bo, base), lw="outline")
    c.line((cx, base - ft - rh - 1.5), (cx, base + 1.5), lw="thin", dash="2 0.6 0.5 0.6")
    c.text((cx, 8), "half section", size=3.0)
    c.text((cx, 27.5), "flange 75, bore 52 mm", size=3.0)
    pc, k = (43, 13), 0.2
    c.circle(pc, F["rings"]["flange_od"] * k / 2, fill="#fff", lw="outline"); c.circle(pc, F["rings"]["od"] * k / 2, lw="thin"); c.circle(pc, F["rings"]["bore"] * k / 2, fill=GREY["light"], lw="outline")
    for a in (90, 210, 330):
        r = math.radians(a)
        c.circle((pc[0] + 33 * k * math.cos(r), pc[1] - 33 * k * math.sin(r)), 0.45, fill="#fff", lw="thin")
    c.text((pc[0], 27.5), "plan", size=3.0)
    return c


def p_plate():
    c = Canvas(W, H)
    s = 0.19
    x0, y0 = 2, 8
    c.rect(x0, y0, 254 * s, 76 * s, fill=GREY["steel"], lw="outline")
    for h in D["plateHoles"]:
        c.circle((x0 + h * 10 * s, y0 + 38 * s), 0.9, fill="#fff", lw="thin")
    c.text((x0 + 127 * s, y0 + 76 * s + 4), "254 × 76 × 3 mm (10 × 3 × 0.12 in)", size=3.0)
    c.text((x0 + 127 * s, 4), "4 holes along the centreline", size=3.0)
    return c


def p_vivo():
    c = Canvas(W, H)
    s = 0.034
    base = 27
    for u in (12, 40):
        c.rect(u - 3, base - 1.5, 6, 1.5, fill=GREY["dark"], lw="thin")       # clamp
        c.rect(u - 35 * s / 2 - 0.3, base - 610 * s, 35 * s + 0.6, 610 * s - 1.5, fill=GREY["light"], lw="outline")
    c.rect(12, base - 430 * s, 28, 1.2, fill=GREY["dark"], lw="thin")
    for u, d in ((12, -1), (40, 1)):
        c.line((u, base - 500 * s), (u + d * 10, base - 520 * s), lw="outline")
        c.line((u + d * 10, base - 520 * s), (u + d * 11, base - 540 * s), lw="outline")
    c.text((26, base - 430 * s - 3), "50.2 cm c/c", size=3.0)
    return c


def p_monitor(curve, label):
    c = Canvas(W, H)
    w = 40
    x0 = (W - w) / 2
    c.rect(x0, 2, w, 17, fill=GREY["light"], lw="outline")
    c.rect(x0 + 1, 3, w - 2, 15, fill="#fff", lw="thin")
    R = 32 if curve == 1000 else 48          # plan curve, drawn deeper for the tighter 1000R
    top = 22
    a = math.asin((w / 2) / R)
    sag = R - R * math.cos(a)
    p0 = (W / 2 - w / 2, top + sag); p1 = (W / 2 + w / 2, top + sag)
    c.raw(f'<path d="M {_f(p0[0])} {_f(p0[1])} A {R} {R} 0 0 1 {_f(p1[0])} {_f(p1[1])}" fill="none" stroke="#000" stroke-width="0.8"/>')
    c.text((W / 2, H - 1.0), f"plan: {label}", size=3.0)
    return c


def p_speaker():
    c = Canvas(W, H)
    for u in (8, 30):
        c.rect(u, 3, 14, 24, fill=GREY["light"], lw="outline")
        c.circle((u + 7, 9), 2.4, lw="thin"); c.circle((u + 7, 19), 4.6, lw="thin"); c.circle((u + 7, 19), 1.4, fill=GREY["mid"], lw="thin")
    return c


def p_elloven():
    c = Canvas(W, H)
    c.rect(4, 12, 44, 12, fill=GREY["light"], lw="outline")
    c.rect(10, 15, 32, 7, fill="#fff", lw="thin")
    c.line((22, 18.5), (30, 18.5), lw="outline")
    c.text((26, 7), "monitor stand with drawer", size=3.0)
    return c


def p_y60():
    c = Canvas(W, H)
    P = iso_fit([(0, 0, 0, 490, 310, 480)], 2, 6, 40, H - 1)
    iso_box(c, P, 0, 0, 0, 490, 310, 60, fills=(GREY["mid"], GREY["dark"], GREY["dark"]))
    iso_box(c, P, 0, 0, 60, 490, 310, 420, fills=(GREY["light"], "#fff", GREY["light"]))
    c.text((46, 26), "pedestal", size=3.0)
    return c


def p_tools():
    """P18 card: a strip of tool icons."""
    c = Canvas(W, H)
    icon_tsquare(c, 1, 2, 0.4); icon_legjig(c, 20, 2, 0.4); icon_guide(c, 37, 2, 0.32)
    icon_gauge(c, 1, 18, 0.4); icon_plug(c, 22, 18, 0.4); icon_corner(c, 33, 16, 0.4); icon_height(c, 46, 16, 0.22)
    return c


def p_trim():
    c = Canvas(W, H)
    c.poly([(4, 14), (36, 14), (36, 17), (10, 17), (10, 24), (7, 24), (7, 17), (4, 17)], fill=GREY["light"], lw="outline")
    c.text((22, 9), "strip on the edge, lip in the gap", size=3.0)
    c.line((40, 12), (40, 26), lw="heavy"); hatch_rect(c, 40, 12, 43, 26, spacing=0.8)
    c.text((46, 21), "wall", size=3.0)
    return c


def p_alexfoot():
    c = Canvas(W, H)
    s = 0.3
    for u, h in ((10, 20), (26, 40), (42, 60)):
        c.rect(u - 28 * s, 27 - h * s, 56 * s, h * s, fill=GREY["light"], lw="outline")
        c.rect(u - 26 * s, 27 - 0.9, 52 * s, 0.9, fill=GREY["dark"], lw="thin")
        c.text((u, 27 - h * s - 2.2), f"{h // 10} cm", size=3.0)
    return c


def p_cables():
    c = Canvas(W, H)
    c.raw('<path d="M 6 6 L 6 18 Q 6 24 12 24 Q 18 24 18 18 L 18 15" fill="none" stroke="#000" stroke-width="1.2"/>')
    c.text((12, 28.5), "hook", size=3.0)
    c.raw('<path d="M 23 20 L 23 12 Q 29 6 35 12 L 35 20" fill="none" stroke="#000" stroke-width="1.0"/>')
    c.line((21, 20), (37, 20), lw="outline")
    c.text((29, 28.5), "clip", size=3.0)
    c.poly([(40, 10), (50, 10), (50, 22), (40, 22)], fill=GREY["light"], lw="outline")
    c.text((45, 28.5), "tray", size=3.0)
    return c


# ------------------------------------------------------------------ printed-tool icons (page mm at scale k)
def icon_tsquare(c, x, y, k=1.0):
    c.poly([(x, y), (x + 6 * k, y), (x + 6 * k, y + 22 * k), (x, y + 22 * k)], fill=GREY["mid"], lw="outline")
    c.poly([(x + 6 * k, y + 7 * k), (x + 40 * k, y + 7 * k), (x + 40 * k, y + 15 * k), (x + 6 * k, y + 15 * k)], fill=GREY["light"], lw="outline")
    for d in (12, 20, 27, 35):
        c.circle((x + (6 + d) * k, y + 11 * k), 0.9 * k, fill="#fff", lw="thin")


def icon_legjig(c, x, y, k=1.0):
    c.poly([(x, y), (x + 34 * k, y), (x + 34 * k, y + 22 * k), (x, y + 22 * k)], fill=GREY["light"], lw="outline")
    c.rect(x - 2 * k, y, 2 * k, 22 * k, fill=GREY["mid"], lw="thin")
    for cx, ls in ((12, None), (24, "1 0.6")):
        c.circle((x + cx * k, y + 11 * k), 9 * k, lw="thin", dash=ls)
        for i in range(5):
            a = math.radians(i * 72 + (180 if ls is None else 0))
            c.circle((x + cx * k + 7.3 * k * math.cos(a), y + 11 * k + 7.3 * k * math.sin(a)), 0.7 * k, fill="#fff", lw="thin")


def icon_corner(c, x, y, k=1.0, holes=4):
    c.poly([(x, y), (x + 26 * k, y), (x + 26 * k, y + 26 * k), (x, y + 26 * k)], fill=GREY["light"], lw="outline")
    c.line((x, y), (x + 26 * k, y), lw="heavy"); c.line((x + 26 * k, y), (x + 26 * k, y + 26 * k), lw="heavy")
    cx, cy = x + 14 * k, y + 12 * k
    c.circle((cx, cy), 0.6 * k, fill="#000", lw="thin")
    if holes == 4:
        for sx in (-1, 1):
            for sy in (-1, 1):
                c.circle((cx + sx * 6 * k, cy + sy * 6 * k), 0.9 * k, fill="#fff", lw="thin")
    else:
        for a in (90, 210, 330):
            r = math.radians(a)
            c.circle((cx + 8 * k * math.cos(r), cy - 8 * k * math.sin(r)), 0.8 * k, fill="#fff", lw="thin")
        c.circle((cx, cy), 10 * k, lw="thin", dash="1 0.6")


def icon_gauge(c, x, y, k=1.0):
    c.poly([(x, y), (x + 40 * k, y), (x + 40 * k, y + 6 * k), (x, y + 6 * k)], fill=GREY["light"], lw="outline")
    c.rect(x, y + 6 * k, 3 * k, 3 * k, fill=GREY["mid"], lw="thin")
    for d in (19, 29):
        c.poly([(x + d * k - 1.2 * k, y), (x + d * k + 1.2 * k, y), (x + d * k, y + 2.2 * k)], fill="#fff", lw="thin")


def icon_drilljig(c, x, y, k=1.0):
    c.poly([(x, y), (x + 28 * k, y), (x + 28 * k, y + 24 * k), (x, y + 24 * k)], fill=GREY["light"], lw="outline")
    c.rect(x, y + 24 * k, 28 * k, 3 * k, fill=GREY["mid"], lw="thin")
    c.circle((x + 14 * k, y + 5 * k), 1.6 * k, fill="#fff", lw="outline")
    c.line((x + 14 * k, y + 9 * k), (x + 14 * k, y + 23 * k), lw="thin", dash="1 0.6")


def icon_plug(c, x, y, k=1.0):
    c.rect(x, y, 16 * k, 4 * k, fill=GREY["mid"], lw="outline")
    c.rect(x + 2.5 * k, y + 4 * k, 11 * k, 10 * k, fill=GREY["light"], lw="outline", rx=2 * k)
    c.line((x + 8 * k, y - 1.5 * k), (x + 8 * k, y + 15.5 * k), lw="thin", dash="1 0.6")


def icon_guide(c, x, y, k=1.0):
    c.rect(x, y + 2 * k, 8 * k, 22 * k, fill=GREY["mid"], lw="outline")
    for i, h in enumerate((10, 13, 9, 10, 20)):
        u = x + (10 + i * 5.5) * k
        c.rect(u, y + (24 - h) * k, 4.5 * k, h * k, fill=GREY["light"], lw="thin")


def icon_height(c, x, y, k=1.0):
    c.poly([(x, y), (x + 20 * k, y), (x + 20 * k, y + 4 * k), (x + 4 * k, y + 4 * k), (x + 4 * k, y + 22 * k), (x + 20 * k, y + 22 * k), (x + 20 * k, y + 26 * k), (x, y + 26 * k)], fill=GREY["light"], lw="outline")


def icon_wall(c, x, y, k=1.0):
    c.poly([(x, y), (x + 6 * k, y), (x + 6 * k, y + 20 * k), (x + 26 * k, y + 20 * k), (x + 26 * k, y + 26 * k), (x, y + 26 * k)], fill=GREY["light"], lw="outline")
    c.text((x + 9 * k, y + 11 * k), "65", size=3.0, anchor="start") if k >= 0.9 else None
    c.text((x + 18 * k, y + 16.5 * k), "30", size=3.0) if k >= 0.9 else None


def icon_alexcorner(c, x, y, k=1.0):
    icon_corner(c, x, y, k, holes=3)


TOOL_ICONS = [
    ("edge-t-square", icon_tsquare, 44, 24), ("leg-jig", icon_legjig, 38, 24), ("feet-corner-jig", icon_corner, 28, 28),
    ("alex-corner-template", icon_alexcorner, 28, 28), ("rail-marking-gauge", icon_gauge, 44, 12), ("rail-drill-jig", icon_drilljig, 30, 29),
    ("fitting-centring-plug", icon_plug, 20, 18), ("pilot-drill-guide", icon_guide, 40, 26), ("foot-height-gauge", icon_height, 22, 28),
    ("wall-gauge", icon_wall, 28, 28),
]


def tool_icon_svg(name, fn, w, h, k=0.62, prefix="02"):
    c = Canvas(w * k + 3, h * k + 3)
    fn(c, 1.5 + (2 * k if fn is icon_legjig else 0), 1.5 + (1.5 * k if fn is icon_plug else 0), k)
    return c.save(os.path.join(FIG, f"{prefix}-tool-{name}.svg"))


# ------------------------------------------------------------------ hardware, 1:1
HW_W, HW_H = 36, 52


def screw_1to1(length, dia, head, drive="cross", hex_head=False, note=""):
    """Vertical screw, head up, true length and nominal diameter at 1:1 (page mm = mm)."""
    c = Canvas(HW_W, HW_H)
    cx, top = 12, 7.5
    if hex_head:
        hw, hh = dia * 1.5, dia * 0.65
        c.rect(cx - hw / 2, top - hh, hw, hh, fill=GREY["mid"], lw="outline")
        c.line((cx - hw / 6, top - hh), (cx - hw / 6, top), lw="thin"); c.line((cx + hw / 6, top - hh), (cx + hw / 6, top), lw="thin")
        c.rect(cx - dia / 2, top, dia, length, fill="#fff", lw="outline")
        for k in range(1, int(length / 1.4)):
            yy = top + length * 0.35 + k * 1.4
            if yy < top + length - 0.4:
                c.line((cx - dia / 2, yy), (cx + dia / 2, yy + 0.5), lw=0.2)
    else:
        if head == "pan":
            hd = dia * 2.0
            c.raw(f'<path d="M {_f(cx - hd / 2)} {_f(top)} v -0.8 q {_f(hd / 2)} -2.2 {_f(hd)} 0 v 0.8 z" fill="{GREY["mid"]}" stroke="#000" stroke-width="0.5"/>')
            shank_top = top
        else:  # flat head: the length includes the head
            hd = dia * 2.0
            c.poly([(cx - hd / 2, top - 0.4), (cx + hd / 2, top - 0.4), (cx + dia / 2, top + (hd - dia) / 2 * 0.9), (cx - dia / 2, top + (hd - dia) / 2 * 0.9)], fill=GREY["mid"], lw="outline")
            shank_top = top + (hd - dia) / 2 * 0.9
            length = length - (shank_top - top)
        tip = 2.2 if head != "machine" else 0
        c.poly([(cx - dia / 2, shank_top), (cx + dia / 2, shank_top), (cx + dia / 2, shank_top + length - tip), (cx, shank_top + length), (cx - dia / 2, shank_top + length - tip)], fill="#fff", lw="outline")
        k = 1
        while shank_top + k * 1.3 < shank_top + length - tip:
            yy = shank_top + k * 1.3
            c.line((cx - dia / 2, yy), (cx + dia / 2, yy + 0.5), lw=0.2); k += 1
    # head seen from above
    hx, hy = 28, 8
    if hex_head:
        r = dia * 0.68
        c.poly([(hx + r * math.cos(math.radians(a)), hy + r * math.sin(math.radians(a))) for a in range(0, 360, 60)], fill=GREY["mid"], lw="outline")
    else:
        r = dia
        c.circle((hx, hy), r, fill=GREY["mid"], lw="outline")
        if drive == "square":
            q = r * 0.42
            c.rect(hx - q, hy - q, 2 * q, 2 * q, fill="#000", lw="thin")
        else:
            q = r * 0.55
            c.line((hx - q, hy), (hx + q, hy), lw=0.6); c.line((hx, hy - q), (hx, hy + q), lw=0.6)
    c.h = max(20, 7.5 + length + 2.5)   # scale note is printed in the HTML card
    return c


def washer(od, idd, t, note="symbol, not to scale"):
    c = Canvas(HW_W, HW_H)
    cx, cy = 18, 16
    c.circle((cx, cy), od / 2, fill=GREY["light"], lw="outline"); c.circle((cx, cy), idd / 2, fill="#fff", lw="outline")
    c.rect(cx - od / 2, 32, od, t, fill=GREY["mid"], lw="outline")
    c.h = 36
    return c


def nut(note="symbol, not to scale"):
    c = Canvas(HW_W, HW_H)
    cx, cy, r = 18, 15, 10
    c.poly([(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(30, 390, 60)], fill=GREY["light"], lw="outline")
    c.circle((cx, cy), 6.2, lw="thin", dash="1 0.6")
    c.circle((cx, cy), 4.8, fill="#fff", lw="outline")
    c.rect(cx - r * 0.87, 30, r * 1.74, 6, fill=GREY["light"], lw="outline")
    c.rect(cx - r * 0.87, 30, r * 1.74, 1.8, fill=GREY["dark"], lw="thin")
    c.h = 38
    return c


def magnet():
    c = Canvas(HW_W, HW_H)
    c.circle((18, 14), 5, fill=GREY["dark"], lw="outline")
    c.rect(13, 28, 10, 3, fill=GREY["dark"], lw="outline")
    c.h = 33
    return c


def hardware():
    out = []
    lst = [
        ("H01", screw_1to1(16, 4, "pan", note="1:1 · head as supplied")),
        ("H02", screw_1to1(5 / 8 * IN, 4.2, "pan", note="1:1")),
        ("H03", screw_1to1(1 * IN, 4.8, "pan", drive="square", note="1:1 · Robertson")),
        ("H04", screw_1to1(5 / 8 * IN, 4.8, "pan", note="1:1")),
        ("H05", washer(12, 5.2, 1.0)),
        ("H06", screw_1to1(5 / 8 * IN, 3.5, "flat", note="1:1 · flat head")),
        ("H07", screw_1to1(0.5 * IN, 2.8, "flat", note="1:1 · flat head")),
        ("H08", screw_1to1(1.5 * IN, 3 / 8 * IN, "hex", hex_head=True, note="1:1 · hex head")),
        ("H09", washer(20, 10.5, 1.6)),
        ("H10", nut()),
        ("H11", magnet()),
    ]
    for hid, c in lst:
        out.append(save(c, f"03-{hid}.svg"))
    return out


if __name__ == "__main__":
    os.makedirs(FIG, exist_ok=True)
    parts = {
        "P01": p_top("A"), "P02": p_top("B"), "P03": p_alex(False), "P04": p_alex(True), "P05": p_olov(),
        "P06": p_rail("A"), "P07": p_rail("B"), "P08": p_fitting(), "P09": p_foot(), "P10": p_ring(), "P11": p_plate(),
        "P12": p_vivo(), "P13": p_monitor(1000, "1000R"), "P14": p_monitor(1500, "1500R"), "P15": p_speaker(), "P16": p_elloven(),
        "P17": p_y60(), "P18": p_tools(), "P19": p_trim(), "P20": p_alexfoot(), "P21": p_cables(),
    }
    for k, c in parts.items():
        print(save(c, f"03-{k}.svg"))
    for p in hardware():
        print(p)
