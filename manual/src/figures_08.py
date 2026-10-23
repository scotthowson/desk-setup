#!/usr/bin/env python3
"""Chapter H figures: standing the tops, the joint, the checks and the wall-gap trim.
Writes manual/figures/08-*.svg. Every number comes from manual/data.json, manual/facts.json,
docs/build-manual.md or (trim profile only) parts/accessories/wall-gap-common.scad."""
import json, math, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from lib.draw import Canvas, GREY  # noqa: E402

D = json.load(open(os.path.join(ROOT, "data.json")))
F = json.load(open(os.path.join(ROOT, "facts.json")))
OUT = os.path.join(ROOT, "figures")
os.makedirs(OUT, exist_ok=True)

H = F["heights_mm"]
UNDER, SURF, FOOT, ALEXH = H["underside"], H["surface"], H["foot_height"], H["alex_height"]
T = F["tops"]["thickness"]
LEN, WID = F["tops"]["length"], F["tops"]["width"]
LEG = F["steel"]["leg"]; TH = F["steel"]["thickness"]
RAIL_LOW = UNDER - LEG
OLOV_R = F["olov"]["plate_diameter"] / 2
FP = F["feet"]["plate"] / 2; FB = F["feet"]["body_and_pad_diameter"] / 2
RG = F["rings"]
GAP = D["gap"] * 10
cm = lambda v: v * 10
legs = {n: (cm(x), cm(y)) for n, x, y, *_ in D["legs"]}
feet = {n: (cm(x), cm(y)) for n, x, y, _ in D["feet"]}
A1 = D["alex1"]; A2 = D["alex2"]
RA = D["railA"]; RB = D["railB"]


def R(x0, x1, z0, z1):
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


def rot(theta_deg, piv, lift=0.0, shift=(0.0, 0.0)):
    a = math.radians(theta_deg); c, s = math.cos(a), math.sin(a)

    def tf(p):
        dx, dz = p[0] - piv[0], p[1] - piv[1]
        return (piv[0] + dx * c - dz * s + shift[0], piv[1] + dx * s + dz * c + lift + shift[1])
    return tf


ident = lambda p: p
_uid = [0]


def dm(c, p1, p2, label, offset=4.0, side=1, size=3.0, gap=1.9):
    """Dimension with its text beside the line (lib's dim() centres the text on the line)."""
    c.dim(p1, p2, "", offset=offset, side=side, size=size)
    x1, y1 = c.P(*p1); x2, y2 = c.P(*p2)
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * side, dx / L * side
    k = offset + (gap if offset >= 0 else -gap)
    tx, ty = (x1 + x2) / 2 + nx * k, (y1 + y2) / 2 + ny * k
    ang = math.degrees(math.atan2(dy, dx))
    if ang > 90 or ang <= -90:
        ang += 180
    c.raw(f'<text x="{tx:.2f}" y="{ty:.2f}" font-family="Helvetica, Arial, sans-serif" font-size="{size}" text-anchor="middle" '
          f'dominant-baseline="middle" transform="rotate({ang:.1f} {tx:.2f} {ty:.2f})">{label}</text>')


def ldr(c, target, ptext, label, size=3.0, anchor=None):
    """Leader whose text runs away from the target, so the line never crosses its own text."""
    if anchor is None:
        anchor = "start" if c.P(*target)[0] < c.P(*ptext)[0] else "end"
    c.leader(target, ptext, label, size=size, anchor=anchor)


def place(dst, src, dx, dy):
    """Composite a sub-canvas, giving its clipPath ids a unique prefix (many SVGs share one HTML page)."""
    _uid[0] += 1
    s = "\n".join(src.parts)
    s = re.sub(r'id="(h[\w-]+)"', rf'id="s{_uid[0]}\1"', s).replace("url(#h", f"url(#s{_uid[0]}h")
    dst.raw(f'<g transform="translate({dx} {dy})">{s}</g>')


def save(c, name):
    svg = c.svg()
    svg = re.sub(r'id="((?:s\d+)?h[\w-]+)"', rf'id="f08{name.replace("-", "")}\1"', svg)
    svg = re.sub(r'url\(#((?:s\d+)?h[\w-]+)\)', rf'url(#f08{name.replace("-", "")}\1)', svg)
    open(os.path.join(OUT, f"08-{name}.svg"), "w").write(svg)


def shapes_draw(c, shapes, tf=ident):
    for pts, fill, lw, dash in shapes:
        c.poly([tf(p) for p in pts], fill=fill, lw=lw, dash=dash)


def person(c, x, y, s=1.0):
    """Tiny pictogram (page mm, not on the desk)."""
    c.raw(f'<circle cx="{x}" cy="{y}" r="{1.4*s}" fill="#000"/>'
          f'<path d="M{x-2.2*s},{y+7*s} L{x-2.2*s},{y+3.2*s} Q{x},{y+1.6*s} {x+2.2*s},{y+3.2*s} L{x+2.2*s},{y+7*s} Z" fill="#000"/>')


# ------------------------------------------------------------------ H-1: top A onto its legs
def topA_front_shapes():
    """Front elevation of top A with its legs, feet and rail A (x right, z up), as built."""
    sh = []
    for n in ("L1", "L2", "L3"):
        x = legs[n][0]
        sh.append((R(x - 18, x + 18, 25, UNDER - 5), "#fff", "outline", None))      # tube (graphic width)
        sh.append((R(x - 26, x + 26, 0, 25), GREY["mid"], "outline", None))          # foot
        sh.append((R(x - OLOV_R, x + OLOV_R, UNDER - 5, UNDER), GREY["dark"], "thin", None))
    for n in ("F1", "F2"):
        x = feet[n][0]
        sh.append((R(x - FB, x + FB, ALEXH, UNDER - 5), GREY["steel"], "outline", None))
        sh.append((R(x - FP, x + FP, UNDER - 5, UNDER), GREY["dark"], "thin", None))
    sh.append((R(cm(RA["x0"]), cm(RA["x1"]), RAIL_LOW, UNDER), GREY["steel"], "outline", None))
    sh.append((R(0, LEN, UNDER, SURF), GREY["wood"], "outline", None))
    return sh


def alex1_front(c, rings=True):
    x0 = cm(A1["x0"]); x1 = x0 + cm(A1["w"])
    c.poly(R(x0, x1, 0, ALEXH), fill="#fff")
    for k in range(3):
        z = ALEXH * (k + 1) / 4
        c.line((x0 + 15, z), (x1 - 15, z), lw="thin")
    if rings:
        for n in ("F1", "F2"):
            x = feet[n][0]
            c.poly(R(x - RG["flange_od"] / 2, x + RG["flange_od"] / 2, ALEXH, ALEXH + RG["flange_t"]), fill=GREY["mid"], lw="thin")
            c.poly(R(x - RG["od"] / 2, x + RG["od"] / 2, ALEXH + RG["flange_t"], ALEXH + RG["flange_t"] + RG["ring_h"]), fill=GREY["mid"], lw="thin")


def floor(c, x0, x1):
    c.line((x0, 0), (x1, 0), lw="heavy")




def _n(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


def num_circle(c, p, s, size=3.6):
    x, y = c.P(*p)
    c.raw(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.2" fill="#fff" stroke="#000" stroke-width="0.5"/>')
    c.text(p, s, size=size, weight="bold")


# ------------------------------------------------------------------ H-1: top A onto its legs
def fig_standA():
    s = 1 / 26.0
    W = 172
    out = Canvas(W, 104)
    # frame a: tilted, ALEX end low, pads just over their rings
    a = Canvas(W, 60, scale=s, origin=(-300, -100), flip_y=True)
    floor(a, -300, 4100)
    alex1_front(a, rings=False)
    piv = (feet["F2"][0], ALEXH)
    tf = rot(-7.5, piv, lift=25)
    shapes_draw(a, topA_front_shapes(), tf)
    pr = tf((LEN - 60, SURF)); pl = tf((60, SURF))
    a.arrow((pr[0] + 40, pr[1] + 330), (pr[0] + 40, pr[1] + 50), lw="heavy", head=2.6)
    num_circle(a, (pr[0] + 260, pr[1] + 240), "1")
    a.text((pr[0] + 420, pr[1] + 240), "ALEX end first:", anchor="start")
    a.text((pr[0] + 420, pr[1] + 90), "pads on the bare top", anchor="start")
    a.arrow((-170, pl[1] + 20), (-170, pl[1] - 330), lw="heavy", head=2.6)
    num_circle(a, (250, 1290), "2")
    a.text((380, 1290), "then the leg end", anchor="start")
    a.text((-280, 1290), "a", size=4.2, weight="bold", anchor="start")
    for i in range(2):
        person(a, 150 + i * 6, 3)
    a.raw('<text x="160" y="6" font-family="Helvetica, Arial, sans-serif" font-size="3.2" dominant-baseline="middle" font-weight="bold">×2</text>')
    a.balloon(tf((1100, SURF - 6)), (1500, 1190), "P01")
    a.balloon(tf((1750, RAIL_LOW + 20)), (1700, 380), "P06")
    a.balloon(tf((legs["L3"][0], 400)), (1050, 200), "P05")
    a.balloon((cm(A1["x0"]) + 360, 350), (2900, 350), "P03")
    place(out, a, 0, 0)
    # frame b: standing, level
    b = Canvas(W, 43, scale=s, origin=(-300, -100), flip_y=True)
    floor(b, -300, 4100)
    alex1_front(b)
    shapes_draw(b, topA_front_shapes())
    b.text((-260, 950), "b", size=4.2, weight="bold", anchor="start")
    b.balloon((feet["F2"][0] + FB - 3, ALEXH + 50), (3250, 650), "P09")
    b.balloon((feet["F2"][0] + RG["flange_od"] / 2 - 4, ALEXH + 4), (3250, 330), "P10")
    dm(b, (0, 0), (0, SURF), "83.0 cm", offset=4.5, side=-1)
    dm(b, (LEN, 0), (LEN, SURF), "83.0 cm", offset=-4.5, side=-1)
    b.text((1245, 930), "level along x and y; all four pads bear, no rock", size=3.2)
    place(out, b, 0, 61)
    save(out, "standA")


# ------------------------------------------------------------------ H-2: pad into its ring (section)
def fig_pad_ring():
    out = Canvas(172, 56)
    b, o, fo, ft, rh = RG["bore"] / 2, RG["od"] / 2, RG["flange_od"] / 2, RG["flange_t"], RG["ring_h"]
    # a: plan, the ring set on its pencil circle
    sp = 0.5
    p = Canvas(92, 56, scale=sp, origin=(-42, -56), flip_y=True)
    p.circle((0, 0), fo, fill=GREY["light"]); p.circle((0, 0), o, fill=GREY["mid"]); p.circle((0, 0), b, fill="#fff")
    p.circle((0, 0), FB, lw="thin", dash="0.9 0.5")
    p.centre_mark((0, 0), size=2)
    for ang in RG["screw_angles_deg"]:
        a_ = math.radians(ang)
        p.circle((RG["screw_circle_radius"] * math.cos(a_), RG["screw_circle_radius"] * math.sin(a_)), RG["screw_hole"] / 2, fill="#fff")
    p.text((-40, 50), "a", size=4.2, weight="bold", anchor="start")
    ldr(p, (FB * 0.72, FB * 0.69), (46, 28), "pencil line (pad outline)", anchor="start")
    p.text((49, 18), "shows all round inside", size=3.0, anchor="start")
    p.text((49, 8), f"the ⌀{_n(RG['bore'])} mm bore", size=3.0, anchor="start")
    a3 = math.radians(330)
    ldr(p, (RG["screw_circle_radius"] * math.cos(a3) + 2.5, RG["screw_circle_radius"] * math.sin(a3)), (46, -16), "3 holes: start 5/64 in", anchor="start")
    p.text((49, -26), "pilots through, 3–4 mm", size=3.0, anchor="start")
    place(out, p, 0, 0)
    # b: section, the pad drops in
    s_ = 0.42
    c = Canvas(80, 56, scale=s_, origin=(-80, 671), flip_y=True)
    c.text((-76, 794), "b", size=4.2, weight="bold", anchor="start")
    c.poly(R(-80, 60, 684, ALEXH), fill=GREY["light"], lw="thin")
    c.hatch(R(-80, 60, 684, ALEXH), spacing=1.6)
    c.label_box((-50, 692), "ALEX top", size=3.0, pad=0.6)
    for sg in (-1, 1):
        pts = [(sg * b, ALEXH), (sg * fo, ALEXH), (sg * fo, ALEXH + ft), (sg * o, ALEXH + ft), (sg * o, ALEXH + ft + rh), (sg * b, ALEXH + ft + rh)]
        c.poly(pts, fill=GREY["mid"])
    lift = 30
    zb = ALEXH + lift
    c.poly(R(-FB, FB, zb, zb + 52), fill=GREY["steel"])
    c.line((-FB, zb + 52), (-FB, zb + 58), lw="outline"); c.line((FB, zb + 52), (FB, zb + 58), lw="outline")
    c.arrow((-FB - 14, zb + 50), (-FB - 14, zb + 2), lw="heavy", head=2.4)
    c.dim((-b, ALEXH + ft + rh + 5), (b, ALEXH + ft + rh + 5), "", offset=0)
    c.text((fo + 2, ALEXH + ft + rh + 5), f"⌀{_n(RG['bore'])} mm bore", size=3.0, anchor="start")
    c.dim((-FB, zb + 12), (FB, zb + 12), "", offset=0)
    c.text((FB + 4, zb + 12), f"⌀{_n(FB * 2)} mm pad", size=3.0, anchor="start")
    c.balloon((FB - 2, zb + 45), (FB + 30, zb + 40), "P09")
    c.balloon((fo - 6, ALEXH + 1.2), (fo + 18, ALEXH - 2), "P10")
    place(out, c, 92, 0)
    save(out, "pad-ring")


# ------------------------------------------------------------------ H-3: top B slides in under A's front edge
def topB_side_shapes():
    """Top B seen from the knee space (+x), y right, z up; rail B's outer face toward you."""
    sh = []
    for n in ("L4", "L5", "L6"):
        y = legs[n][1]
        sh.append((R(y - 18, y + 18, 25, UNDER - 5), "#fff", "outline", None))
        sh.append((R(y - 26, y + 26, 0, 25), GREY["mid"], "outline", None))
        sh.append((R(y - OLOV_R, y + OLOV_R, UNDER - 5, UNDER), GREY["dark"], "thin", None))
    for n in ("F5", "F7"):
        y = feet[n][1]
        sh.append((R(y - FB, y + FB, ALEXH, UNDER - 5), GREY["steel"], "outline", None))
        sh.append((R(y - FP, y + FP, UNDER - 5, UNDER), GREY["dark"], "thin", None))
    sh.append((R(cm(RB["y0"]), cm(RB["y1"]), RAIL_LOW, UNDER), GREY["steel"], "outline", None))
    sh.append((R(cm(D["B"]["y0"]), cm(D["B"]["y1"]), UNDER, SURF), GREY["wood"], "outline", None))
    return sh


def alex2_side(c, dy=0.0):
    y0 = cm(A2["y0"]) + dy; y1 = y0 + cm(A2["d"])
    c.poly(R(y0, y1, 0, ALEXH), fill="#fff")
    c.line((y0 + 20, ALEXH - 60), (y1 - 20, ALEXH - 60), lw="thin")
    for n in ("F5", "F7"):
        y = feet[n][1] + dy
        c.poly(R(y - RG["flange_od"] / 2, y + RG["flange_od"] / 2, ALEXH, ALEXH + RG["flange_t"] + RG["ring_h"]), fill=GREY["mid"], lw="thin")


def topA_cut(c):
    """Top A cut beyond top B's inside edge: section hatched, rail A's angle in section, L1 and L2 behind."""
    for n in ("L1", "L2"):
        y = legs[n][1]
        c.poly(R(y - 18, y + 18, 25, UNDER - 5), fill="#fff")
        c.poly(R(y - 26, y + 26, 0, 25), fill=GREY["mid"])
        c.poly(R(y - OLOV_R, y + OLOV_R, UNDER - 5, UNDER), fill=GREY["dark"], lw="thin")
    sec = R(0, WID, UNDER, SURF)
    c.poly(sec, fill="#fff"); c.hatch(sec, spacing=1.2)
    c.poly(rail_section(), fill="#000", lw="thin")


def rail_section():
    yo = cm(RA["y1"])
    return [(yo - LEG, UNDER), (yo, UNDER), (yo, RAIL_LOW), (yo - TH, RAIL_LOW), (yo - TH, UNDER - TH), (yo - LEG, UNDER - TH)]


def wall(c, y, z0, z1, side=-1, w=30):
    c.line((y, z0), (y, z1), lw="heavy")
    c.hatch(R(y + side * w, y, z0, z1) if side < 0 else R(y, y + w, z0, z1), spacing=1.4)




def fig_slideB():
    s = 1 / 24.0
    W = 172
    out = Canvas(W, 100)
    sh = 160  # graphic offset of the approach position (not a dimension)
    for k, (dy, lab, oy) in enumerate([(sh, "a", 0), (0, "b", 51)]):
        c = Canvas(W, 49, scale=s, origin=(-150, -110), flip_y=True)
        floor(c, -60, 3400)
        wall(c, -GAP, 0, 1000, side=-1, w=60)
        topA_cut(c)
        alex2_side(c, dy)
        shapes_draw(c, topB_side_shapes(), rot(0, (0, 0), shift=(dy, 0)))
        c.text((20, 1020), lab, size=4.2, weight="bold", anchor="start")
        if k == 0:
            yend = cm(D["B"]["y1"]) + dy
            c.arrow((yend + 30, 960), (yend - 470, 960), lw="heavy", head=2.6)
            c.text((yend - 220, 1020), "push", size=3.2)
            ldr(c, (legs["L5"][1] + dy - 18, 330), (1690, 330), "legs wound", size=3.2, anchor="end")
            c.text((1655, 190), "2–3 mm short", size=3.2, anchor="end")
            c.balloon((1900 + dy, UNDER - 25), (2150 + dy, 420), "P07")
            c.balloon((1000 + dy, SURF - 6), (950, 960), "P02")
            c.balloon((cm(A2["y0"]) + dy + 40, 300), (2700, 300), "P04")
            c.balloon((300, SURF - 6), (300, 960), "P01")
        else:
            for y in (legs["L4"][1], legs["L6"][1]):
                c.arrow((y + 80, 250), (y + 80, 560), lw="heavy", head=2.2)
            c.text((1450, 1010), "rail B's end on rail A, B's end at A's front edge: wind B's legs up to flush", size=3.2)
        place(out, c, 0, oy)
    save(out, "slideB")


# ------------------------------------------------------------------ H-4: the joint in section (detail)
def fig_joint_section():
    s = 0.45
    c = Canvas(172, 66, scale=s, origin=(418, 713), flip_y=True)
    y0, y1 = 430, 790
    secA = R(y0, WID, UNDER, SURF)
    c.poly(secA, fill="#fff"); c.hatch(secA, spacing=1.4)
    c.poly(rail_section(), fill=GREY["dark"], lw="outline")
    yb = cm(RB["y0"])
    c.poly(R(WID, y1, UNDER, SURF), fill=GREY["wood"])
    c.poly(R(yb, y1, RAIL_LOW, UNDER), fill=GREY["steel"])
    c.line((yb, UNDER - TH), (y1, UNDER - TH), lw="hidden", dash="1.2 0.8")
    dz, dy = -3, 45   # approach position: 3 mm low (the manual's 2-3), offset along y for clarity
    c.poly(R(WID + dy, y1, UNDER + dz, SURF + dz), lw="thin", dash="1.5 1")
    c.poly(R(yb + dy, y1, RAIL_LOW + dz, UNDER + dz), lw="thin", dash="1.5 1")
    c.arrow((yb + dy - 4, 775), (yb + 4, 775), lw="outline", head=1.8)
    for y in (y0, y1):
        c.line((y, UNDER - 4), (y, SURF + 4), lw="thin")
    dm(c, (yb, RAIL_LOW), (WID, RAIL_LOW), "12 cm under top A", offset=4, side=-1)
    ldr(c, (yb, 768), (548, 722), "rail B's end touches rail A's vertical leg (y = 53 cm)")
    ldr(c, (WID, SURF), (625, 852), "B's end meets A's front edge (y = 65 cm)")
    ldr(c, (712, SURF), (725, 852), "flush, 83.0 cm", anchor="start")
    c.text((785, 737), "dashed: on its way in, 2–3 mm low", size=3.0, anchor="end")
    c.label_box((520, 816), "top A (cut)", size=3.0, pad=0.6)
    c.text((470, 776), "rail A", size=3.0)
    save(c, "joint-section")


# ------------------------------------------------------------------ H-5: joint plan (from above, through the tops)
def fig_joint_plan():
    s = 0.195
    c = Canvas(172, 120, scale=s, origin=(-80, 345))
    yA = cm(RA["y1"]); xB = cm(RB["x1"])
    X1, Y1 = 790, 950
    c.line((-GAP, 345), (-GAP, Y1), lw="heavy"); c.hatch(R(-GAP - 15, -GAP, 345, Y1), spacing=1.4)
    c.poly([(0, 345), (X1, 345), (X1, WID), (WID, WID), (WID, Y1), (0, Y1)], fill=GREY["wood"], lw="thin", close=False)
    c.line((0, 345), (0, Y1), lw="outline")
    c.line((WID, WID), (X1, WID), lw="outline")
    c.line((WID, WID), (WID, Y1), lw="outline")
    c.line((0, WID), (WID, WID), lw="heavy")
    for n in ("L1", "L4"):
        c.circle(legs[n], OLOV_R, dash="1.2 0.8", lw="thin"); c.text(legs[n], n, size=3.0)
    c.poly(R(cm(RA["x0"]), X1, cm(RA["y0"]), yA), fill=GREY["steel"])
    c.line((cm(RA["x0"]), yA - TH), (X1, yA - TH), lw="thin")
    c.poly(R(cm(RB["x0"]), xB, yA, Y1), fill=GREY["steel"])
    c.line((xB - TH, yA), (xB - TH, Y1), lw="thin")
    off = cm(D["holeOffset"])
    for h in RA["holes"][:3]:
        c.hole((cm(RA["x0"]) + cm(h), cm(RA["y0"]) + off), 5.56)
    for h in RB["holes"][:3]:
        c.hole((cm(RB["x0"]) + off, yA + cm(h)), 5.56)
    for i in (0, 1):
        c.arrow((668, 760), (cm(RB["x0"]) + off + 5, yA + cm(RB["holes"][i]) + 3), lw="thin", head=1.4)
    for k, t in enumerate(("rail B", "holes 1, 2", "(step 7)")):
        c.text((672, 765 + 18 * k), t, size=3.0, anchor="start")
    fl, ft = cm(D["fitting"]["legs"]), 5
    c.poly([(xB, yA), (xB + fl, yA), (xB + fl, yA + ft), (xB + ft, yA + ft), (xB + ft, yA + fl), (xB, yA + fl)], dash="1.2 0.8", lw="outline")
    xi = xB - TH
    c.poly([(xi, yA), (xi - fl, yA), (xi - fl, yA + ft), (xi - ft, yA + ft), (xi - ft, yA + fl), (xi, yA + fl)], dash="1.2 0.8", lw="outline")
    c.balloon((xB + fl - 8, yA + 3), (690, 590), "P08")
    c.text((665, 680), "fittings:", size=3.0, anchor="start"); c.text((665, 698), "chapter F", size=3.0, anchor="start")
    pw, pl = cm(D["plateW"]), cm(D["plateL"])
    py0 = cm(F["layout_cm"]["joining_plates"]["y_span"][0])
    for name, xc in D["plates"]:
        x = cm(xc)
        c.poly(R(x - pw / 2, x + pw / 2, py0, py0 + pl), fill=GREY["mid"])
        for h in D["plateHoles"]:
            c.hole((x, py0 + cm(h)), 4.8)
        c.balloon((x + pw / 2 - 3, py0 + pl - 12), (x + 80, py0 + pl + 40), "P11")
        c.text((x + 18, py0 + pl / 2 - 26), name, size=3.4, weight="bold", rotate=-90)
    x2 = cm(D["plates"][1][1]) + pw / 2
    c.line((x2 + 6, py0), (x2 + 38, py0), lw="thin")
    for h in D["plateHoles"]:
        c.line((x2 + 6, py0 + cm(h)), (x2 + 38, py0 + cm(h)), lw="thin")
        c.text((x2 + 42, py0 + cm(h)), _n(cm(h)), size=3.0, anchor="start")
    c.line((x2 + 30, py0), (x2 + 30, py0 + cm(D["plateHoles"][-1])), lw="thin")
    x1p = cm(D["plates"][0][1]) - pw / 2
    c.dim((x1p, py0), (x1p, py0 + pl), "", offset=3.5, side=1)
    c.text((x1p - 5.4 / s, 590), _n(pl), size=3.0, rotate=-90)
    x2l = cm(D["plates"][1][1]) - pw / 2
    c.dim((x2l, py0 + pl), (x2l + pw, py0 + pl), "", offset=3, side=1)
    c.text((x2l + pw * 0.27, py0 + pl + 4.9 / s), _n(pw), size=3.0)
    for k, (name, xc) in enumerate(D["plates"]):
        dm(c, (0, 922 + 24 * k), (cm(xc), 922 + 24 * k), f"{_n(xc)} cm", offset=0, side=-1, gap=1.6)
        c.line((cm(xc), py0 + pl), (cm(xc), 927 + 24 * k), lw="thin", dash="4 1 0.8 1")
    ldr(c, (cm(D["plates"][0][1]) + 25, py0), (250, 395), "3 mm clear of rail A")
    c.text((250, WID - 8), "joint, y = 65 cm", size=3.0, baseline="auto")
    c.text((420, 375), "top A", size=3.2, weight="bold"); c.text((570, 900), "top B", size=3.2, weight="bold")
    c.text((-GAP - 25, 650), "side wall", size=3.0, rotate=-90, baseline="auto")
    c.label_box((680, 505), "rail A", size=3.0, pad=0.4)
    save(c, "joint-plan")


# ------------------------------------------------------------------ H-6: final checks, plan
def fig_checks():
    s = 1 / 28.0
    c = Canvas(112, 134, scale=s, origin=(-280, -260))
    yB1 = cm(D["B"]["y1"])
    L = [(0, 0), (LEN, 0), (LEN, WID), (WID, WID), (WID, yB1), (0, yB1)]
    c.line((-GAP, -250), (-GAP, 3300), lw="heavy"); c.line((-270, -GAP), (2700, -GAP), lw="heavy")
    c.text((1245, -GAP - 30), "back wall", size=3.0, baseline="auto")
    c.text((-GAP - 30, 1700), "side wall", size=3.0, rotate=-90, baseline="auto")
    c.poly(L, fill=GREY["wood"])
    c.line((0, WID), (WID, WID), lw="heavy")
    for x0, y0, w, d in ((A1["x0"], A1["y0"], A1["w"], A1["d"]), (A2["x0"], A2["y0"], A2["w"], A2["d"])):
        c.rect(cm(x0), cm(y0), cm(w), cm(d), dash="1.2 0.8", lw="thin")
    for n, (x, y) in feet.items():
        c.circle((x, y), FB, fill="#fff", lw="thin")
    c.text((cm(A1["x0"]) + cm(A1["w"]) / 2, 330), "F1–F4", size=3.0)
    c.text((330, cm(A2["y0"]) + cm(A2["d"]) / 2), "F5–F8", size=3.0)
    offs = [(-140, -140), (140, -140), (160, 130), (-170, 150), (160, 130), (-140, 140)]
    for i, (p, o) in enumerate(zip(L, offs)):
        c.circle(p, 25, fill="#000", lw="thin")
        c.balloon(p, (p[0] + o[0], p[1] + o[1]), str(i + 1), r=3.0)
    a, b = (WID + 600, WID), (WID, WID + 800)
    c.line(a, b, lw="outline", dash="2 1")
    for p in (a, b):
        c.circle(p, 20, fill="#000", lw="thin")
    c.text(((WID + a[0]) / 2, WID + 70), "60 cm", size=3.0)
    c.text((WID - 30, (WID + b[1]) / 2), "80 cm", size=3.0, anchor="end")
    c.text(((a[0] + b[0]) / 2 + 60, (a[1] + b[1]) / 2 + 40), "100 cm (field check)", size=3.0, anchor="start")
    c.rect(300, 450, 60, 400, fill="#fff"); c.circle((330, 560), 18, lw="thin")
    c.rect(120, 620, 400, 60, fill="#fff"); c.circle((230, 650), 18, lw="thin")
    ldr(c, (360, 470), (900, 190), "levels across")
    c.text((936, 300), "and along the joint", size=3.0, anchor="start")
    ldr(c, (600, WID - 4), (900, 480), "butt joint closed,")
    c.text((936, 590), "full width", size=3.0, anchor="start")
    save(c, "checks")


# ------------------------------------------------------------------ H-7: desk pulled 40 cm off both walls
def fig_pulled():
    s = 1 / 40.0
    c = Canvas(172, 98, scale=s, origin=(-200, -200))
    pull = 400
    yB1 = cm(D["B"]["y1"])
    L = [(0, 0), (LEN, 0), (LEN, WID), (WID, WID), (WID, yB1), (0, yB1)]
    c.line((-GAP, -200), (-GAP, 3700), lw="heavy"); c.line((-200, -GAP), (3500, -GAP), lw="heavy")
    c.hatch(R(-GAP - 60, -GAP, -200, 3700), spacing=1.4); c.hatch(R(-200, 3500, -GAP - 60, -GAP), spacing=1.4)
    c.label_box((1600, -GAP - 32), "back wall", size=3.0, pad=0.5)
    c.poly(L, dash="1.5 1", lw="thin")
    M = [(x + pull, y + pull) for x, y in L]
    c.poly(M, fill=GREY["wood"])
    for x0, y0, w, d, n in ((A1["x0"], A1["y0"], A1["w"], A1["d"], "1"), (A2["x0"], A2["y0"], A2["w"], A2["d"], "2")):
        c.rect(cm(x0) + pull, cm(y0) + pull, cm(w), cm(d), dash="1.2 0.8", lw="outline")
        c.rect(cm(x0), cm(y0), cm(w), cm(d), dash="0.6 0.8", lw="thin")
        cx, cy = cm(x0) + cm(w) / 2 + pull, cm(y0) + cm(d) / 2 + pull
        c.arrow((cx - pull, cy - pull), (cx - 30, cy - 30), lw="heavy", head=2.4)
        px, py = (cx + 330, cy - 160) if n == "1" else (cx + 420, cy - 60)
        person(c, *c.P(px, py), s=0.9)
        c.text((px + 110, py + 40), f"ALEX {n}", size=3.0, anchor="start")
    c.dim((-GAP, 1700), (pull, 1700), "", offset=0)
    c.text((pull + 30, 1700), "40 cm", size=3.0, anchor="start")
    c.dim((1700, -GAP), (1700, pull), "", offset=0)
    c.text((1740, 200), "40 cm", size=3.0, anchor="start")
    c.text((1500, 1700), "Pads stay in their rings;", size=3.2, anchor="start")
    c.text((1500, 1840), "the ALEX units slide on", size=3.2, anchor="start")
    c.text((1500, 1980), "their feet. Nothing comes apart.", size=3.2, anchor="start")
    save(c, "pulled")


# ------------------------------------------------------------------ H-8: chain order along both walls
def fig_chain():
    s = 1 / 20.0
    c = Canvas(172, 64, scale=s, origin=(-60, 0))
    runs = [("back wall", LEN, 8, (3, 8), [0, 200, 520, 1000, 1240, 2200, 2440]),
            ("side wall", cm(D["B"]["y1"]), 10, (3,), [0, 200, 520, 1000, 1240, 2920, 3140])]
    for r, (name, end, nseg, slots, ticks) in enumerate(runs):
        y = 90 + r * 560
        h = 150
        c.text((-55, y - 30), name, size=3.2, anchor="start", weight="bold", baseline="auto")
        pieces = [(-GAP, 200, "C", GREY["dark"]), (200, 280, "F", GREY["light"]), (280, 520, "K", GREY["mid"])]
        x = 520
        for k in range(nseg):
            pieces.append((x, x + 240, str(k + 1), GREY["light"] if (k + 1) in slots else "#fff")); x += 240
        pieces.append((x, end, "", "#fff"))
        for x0, x1, lab, fill in pieces:
            c.rect(x0, y, x1 - x0, h, fill=fill, lw="outline")
            if lab == "K":
                c.rect(360, y + 20, 80, 70, fill="#fff", lw="thin")
                c.text((470, y + h - 35), "K", size=3.0, weight="bold", anchor="start")
            elif lab:
                c.text(((x0 + x1) / 2, y + 55), lab, size=3.0, weight="bold", color="#fff" if fill == GREY["dark"] else "#000")
        for k in slots:
            xs = 520 + (k - 1) * 240 + 90
            c.rect(xs, y + 95, 60, 35, fill="#fff", lw="thin")
        for x0, *_ in pieces[1:]:
            c.rect(x0 - 20, y + h + 8, 40, 45, fill="#000", lw="thin")
        if end - x >= 150:
            c.text(((x + end) / 2, y + 55), _n(end - x), size=3.0)
        else:
            c.text((end + 30, y + h / 2), f"{_n(end - x)} mm", size=3.0, anchor="start")
        for t in ticks:
            c.line((t, y + h + 60), (t, y + h + 110), lw="thin")
            c.text((t, y + h + 125), _n(t / 10), size=3.0, baseline="hanging")
    c.text((-55, 1110), "Desk positions in cm. C corner · F 80 mm filler · K clamp piece (white: notch round the clamp back)", size=3.0, anchor="start")
    c.text((-55, 1190), "1, 2 … 240 mm segments, grey with a slot = slotted · ■ connector tile under every joint", size=3.0, anchor="start")
    save(c, "chain")


# ------------------------------------------------------------------ H-9: trim profile on the edge (section)
TRIM = {"gap": 29, "ontop": 12, "lip": 20, "hole_z": 14}  # parts/accessories/wall-gap-common.scad


def fig_profile():
    s = 1.8
    c = Canvas(172, 90, scale=s, origin=(-14, -12))
    g, on, lip, hz = TRIM["gap"], TRIM["ontop"], TRIM["lip"], TRIM["hole_z"]
    th, lt = 3, 3   # graphic only (plate and lip thickness, not printed)
    zf = lambda z: -z
    c.line((-1, zf(10)), (-1, zf(-31)), lw="heavy"); c.hatch(R(-5, -1, zf(10), zf(-31)), spacing=1.4)
    desk = [(g, zf(0)), (70, zf(0)), (70, zf(-T)), (g, zf(-T))]
    c.poly(desk, fill=GREY["wood"])
    c.line((70, zf(2)), (70, zf(-T - 2)), lw="thin")
    prof = [(0, zf(0)), (g - lt, zf(0)), (g - lt, zf(-lip)), (g, zf(-lip)), (g, zf(0)), (g + on, zf(0)), (g + on, zf(th - 1.5)),
            (g + on - 1.5, zf(th)), (1.5, zf(th)), (0, zf(th - 1.5))]
    c.poly(prof, fill=GREY["mid"], lw="outline")
    pc = (g - lt) / 2
    c.rect(pc - 6, zf(1.2), 12, 1.2, dash="0.8 0.6", lw="thin")
    yz = zf(-hz)
    c.poly([(g - lt, yz - 2.6), (g - lt + 2.2, yz - 1.1), (g - lt + 2.2, yz + 1.1), (g - lt, yz + 2.6)], fill="#000", lw="thin")
    c.rect(g - lt + 2.2, yz - 0.75, 12.7 - 2.2, 1.5, fill="#000", lw="thin")
    c.line((g, yz - 1.1), (g + 10, yz - 1.1), lw="thin", dash="0.8 0.5")
    c.line((g, yz + 1.1), (g + 10, yz + 1.1), lw="thin", dash="0.8 0.5")
    c.line((g + 10, yz - 1.1), (g + 10, yz + 1.1), lw="thin", dash="0.8 0.5")
    dm(c, (0, zf(th)), (g, zf(th)), "29 reach", offset=4.5, side=-1)
    dm(c, (g, zf(th)), (g + on, zf(th)), "12 on top", offset=4.5, side=-1)
    c.text((-13, zf(-6)), "1 to", size=3.0, anchor="start")
    c.text((-13, zf(-8.2)), "the wall", size=3.0, anchor="start")
    c.arrow((-6.5, zf(-4.6)), (-0.6, zf(1.0)), lw="thin", head=1.2)
    dm(c, (g - lt, zf(0)), (g - lt, zf(-lip)), "20 lip", offset=5, side=1)
    dm(c, (76, zf(0)), (76, zf(-hz)), "14", offset=0, side=-1)
    c.line((70, zf(0)), (78, zf(0)), lw="thin"); c.line((g + 12, yz), (78, yz), lw="thin", dash="4 1 0.8 1")
    c.text((g + 16, zf(-T - 3.5)), "pilot ⌀2.0 (5/64 in) × 10 mm deep,", size=3.0, anchor="start", baseline="hanging")
    c.text((g + 16, zf(-T - 5.6)), "puck 10 EDGE, bit horizontal", size=3.0, anchor="start", baseline="hanging")
    c.line((g + 12, yz + 1.2), (g + 17, zf(-T - 3)), lw="thin")
    c.text((-13, zf(-T - 3.5)), "#4 × 1/2 in flat head (H07)", size=3.0, anchor="start", baseline="hanging")
    c.line((g - lt + 1, yz + 2.6), (6, zf(-T - 3)), lw="thin")
    c.label_box((53, zf(-7)), "desk top, raw back edge", size=3.0, pad=0.5)
    c.text((g + on + 2, zf(2.0)), "desk surface", size=3.0, anchor="start", baseline="auto")
    c.text((pc, zf(-7)), "gap", size=3.0)
    c.text((pc, zf(-10)), "(wall side)", size=3.0)
    save(c, "trim-profile")


# ------------------------------------------------------------------ H-10: connector tile
def fig_tile():
    s = 1.8
    c = Canvas(82, 72, scale=s, origin=(-2, -7))
    tl, tw, pd, pin, pp = 39, 11.6, 1.2, 2.4, 20   # wall-gap-connector.scad and parts/README.md
    c.rect(0, 0, tl, tw, fill=GREY["light"])
    for x in (tl / 2 - pp / 2, tl / 2 + pp / 2):
        c.circle((x, tw / 2), pin / 2, fill="#000", lw="thin")
    dm(c, (0, tw), (tl, tw), "39", offset=3, side=1)
    dm(c, (tl, 0), (tl, tw), "11.6", offset=3, side=-1)
    dm(c, (tl / 2 - pp / 2, 0), (tl / 2 + pp / 2, 0), "20", offset=3, side=-1)
    c.text((tl / 2 + pp / 2 + 2, tw / 2), "pins ⌀2.4", size=3.0, anchor="start")
    y = tw + 12
    c.rect(0, y, tl, pd, fill=GREY["light"])
    for x in (tl / 2 - pp / 2, tl / 2 + pp / 2):
        c.rect(x - pin / 2, y - 0.9, pin, 0.9, fill="#000", lw="thin")
    c.text((0, y + 4.5), "side view, 1.2 thick", size=3.0, anchor="start", baseline="hanging")
    c.arrow((tl - 4, y + 10), (tl - 4, y + 2.2), lw="outline", head=1.6)
    c.text((tl - 6, y + 4.5), "push up", size=3.0, anchor="end", baseline="hanging")
    save(c, "tile")


# ------------------------------------------------------------------ H-11: wall gauge at an ALEX
def fig_gauge():
    s = 0.3
    c = Canvas(80, 84, scale=s, origin=(-60, 588), flip_y=True)
    c.line((0, 600), (0, 860), lw="heavy"); c.hatch(R(-22, 0, 600, 860), spacing=1.4)
    c.poly(R(GAP, 190, UNDER, SURF), fill=GREY["wood"])
    c.poly([(1, SURF), (GAP + 12, SURF), (GAP + 12, SURF + 3), (1, SURF + 3)], fill=GREY["mid"], lw="thin")
    c.poly(R(GAP - 3, GAP, SURF - 20, SURF), fill=GREY["mid"], lw="thin")
    ab = cm(A1["y0"]) + GAP
    c.poly(R(ab, 190, 600, ALEXH), fill="#fff")
    yf = feet["F1"][1] + GAP
    c.poly(R(yf - FB, yf + FB, ALEXH + RG["flange_t"], UNDER - 5), fill=GREY["steel"])
    c.poly(R(yf - FP, yf + FP, UNDER - 5, UNDER), fill=GREY["dark"], lw="thin")
    c.poly(R(yf - RG["flange_od"] / 2, yf + RG["flange_od"] / 2, ALEXH, ALEXH + RG["flange_t"]), fill=GREY["mid"], lw="thin")
    c.poly(R(yf - RG["od"] / 2, yf - RG["bore"] / 2, ALEXH + RG["flange_t"], ALEXH + RG["flange_t"] + RG["ring_h"]), fill=GREY["mid"], lw="thin")
    c.poly(R(yf + RG["bore"] / 2, yf + RG["od"] / 2, ALEXH + RG["flange_t"], ALEXH + RG["flange_t"] + RG["ring_h"]), fill=GREY["mid"], lw="thin")
    c.poly(R(0, 65, 640, 654), fill="#000", lw="thin")
    c.text((32.5, 630), "ALEX 65", size=3.0, baseline="hanging"); c.text((32.5, 616), "leg", size=3.0, baseline="hanging")
    dm(c, (0, 670), (65, 670), "6.5 cm", offset=0, side=-1)
    dm(c, (0, SURF + 14), (GAP, SURF + 14), "3 cm", offset=0, side=-1)
    c.text((100, 655), "ALEX 1", size=3.0, anchor="start")
    c.text((105, SURF + 16), "top A", size=3.0, anchor="start")
    c.text((-30, 730), "back wall", size=3.0, rotate=-90)
    save(c, "gauge")


if __name__ == "__main__":
    fig_standA(); fig_pad_ring(); fig_slideB(); fig_joint_section(); fig_joint_plan(); fig_checks()
    fig_pulled(); fig_chain(); fig_profile(); fig_tile(); fig_gauge()
    print("chapter H figures:", sorted(f for f in os.listdir(OUT) if f.startswith("08-")))
