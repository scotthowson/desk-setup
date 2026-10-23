#!/usr/bin/env python3
"""Chapter F figures: steel corner assembly. Writes manual/figures/06-*.svg.

Desk coordinates in mm (datum: top A's back-left corner; x along the back wall, y along the side wall,
z up from the tops' underside). Rail A's outer face is y = 530, rail B's outer face x = 530, both from
data.json. Fitting hole positions are drawn at data.json's assumed 25/65 mm from the heel and never
dimensioned. Bolt, washer and nut proportions are drawing sizes only; no size of theirs is printed.
"""
import math, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figures_05 import (Canvas, GREY, FACTS, DATA, S, LEG, T, SCREW, BOLT, HEEL_OUT, HEEL_IN, FIT_T, FIT_W, FIT_L,  # noqa: E402
                        FIT_H, RAILA_X0, TOP_T, SC_LBL, BO_LBL, SLOT_LBL, SLOT_L, SLOT_W, PILOT_LBL, SC_IN, BO_IN, SC_D, BO_D,
                        T_, L_, R_, P_, cm, head, dimh, dimv, leader, arrow, hole, hatch_rect, zig, save, num, _f)

OUT = DATA["railA"]["y1"] * 10           # 530: rail A's outer face (y) and rail B's outer face (x)
INB = OUT - T                            # 525.24: rail B's inner face (x)
ZC = -BOLT                               # fittings centred 29 below the top
CJ = FACTS["corner_joint"]

# ---------------------------------------------------------------- tiny isometric engine (view from above, from the knee space)
C30 = math.cos(math.radians(30))
VIEW = (1, 1, 1)                         # toward the viewer: +x, +y, +z (you, sitting in the knee space, tops lifted off)


def proj(p):
    x, y, z = p
    return ((y - x) * C30, z - (x + y) / 2)


def depth(p):
    return p[0] + p[1] + p[2]


def hull2(pts):
    pts = sorted(set(pts))
    if len(pts) < 3:
        return pts
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


class Scene:
    def __init__(self):
        self.faces = []                  # [depth, pts3, fill, lw, dash, decor, kind]

    def face(self, pts, fill, lw="outline", dash=None, decor=None, bias=0.0, kind="poly"):
        cx = sum(p[0] for p in pts) / len(pts); cy = sum(p[1] for p in pts) / len(pts); cz = sum(p[2] for p in pts) / len(pts)
        self.faces.append([depth((cx, cy, cz)) + bias, pts, fill, lw, dash, decor or [], kind])
        return self.faces[-1]

    def prism(self, base, axis, length, fills=("#fff", GREY["light"], GREY["mid"]), lw="outline", bias=0.0, decor=None):
        """Convex prism from a 3D base polygon extruded by axis*length; only faces turned to the viewer are kept.
        decor: {face_normal_axis: [fn, ...]} drawn right after that face, e.g. holes."""
        ax = [a * length for a in axis]
        top = [(p[0] + ax[0], p[1] + ax[1], p[2] + ax[2]) for p in base]
        n = len(base)
        polys = [list(base), top] + [[base[i], base[(i + 1) % n], top[(i + 1) % n], top[i]] for i in range(n)]
        cen = [sum(p[k] for p in base + top) / (2 * n) for k in range(3)]
        out = []
        for poly in polys:
            nx, ny, nz = normal(poly)
            fc = [sum(p[k] for p in poly) / len(poly) for k in range(3)]
            if nx * (fc[0] - cen[0]) + ny * (fc[1] - cen[1]) + nz * (fc[2] - cen[2]) < 0:
                nx, ny, nz = -nx, -ny, -nz
            if nx * VIEW[0] + ny * VIEW[1] + nz * VIEW[2] <= 1e-9:
                continue
            shade = fills[0] if nz > 0.5 else fills[1] if abs(nx) > abs(ny) else fills[2]
            key = "x" if abs(nx) > 0.9 else "y" if abs(ny) > 0.9 else "z" if abs(nz) > 0.9 else None
            out.append(self.face(poly, shade, lw=lw, bias=bias, decor=(decor or {}).get(key)))
        return out

    def box(self, x0, x1, y0, y1, z0, z1, **kw):
        return self.prism([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], (0, 0, 1), z1 - z0, **kw)

    def cylinder(self, c0, axis, length, r, fill=GREY["light"], cap_fill="#fff", lw="thin", bias=0.0, cap_decor=None):
        """Cylinder as a filled silhouette plus the end cap facing the viewer."""
        a = ngon(c0, axis, r, 32)
        b = [tuple(p[k] + axis[k] * length for k in range(3)) for p in a]
        f = self.face(a + b, fill, lw=lw, bias=bias, kind="hull")
        near = b if sum(axis[k] * VIEW[k] for k in range(3)) > 0 else a
        if abs(sum(axis[k] * VIEW[k] for k in range(3))) > 1e-9:
            f[5] = [lambda c, P, near=near: P_(c, [P(p) for p in near], fill=cap_fill, lw=lw)] + (cap_decor or [])
        return f

    def render(self, c, P):
        for d, pts, fill, lw, dash, decor, kind in sorted(self.faces, key=lambda f: f[0]):
            pp = [P(p) for p in pts]
            if kind == "hull":
                pp = hull2([(round(x, 3), round(y, 3)) for x, y in pp])
            if fill != "skip":
                P_(c, pp, fill=fill, lw=lw, dash=dash)
            for fn in decor:
                fn(c, P)


def normal(poly):
    a, b, cc = poly[0], poly[1], poly[2]
    u = [b[i] - a[i] for i in range(3)]; v = [cc[i] - a[i] for i in range(3)]
    n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    L = math.sqrt(sum(k * k for k in n)) or 1
    return tuple(k / L for k in n)


def ngon(centre, axis, r, n, rot=0.0):
    """Regular n-gon of circumradius r round centre, in the plane normal to a unit x, y or z axis."""
    ax = [abs(a) for a in axis]
    e1, e2 = ((0, 1, 0), (0, 0, 1)) if ax[0] else ((0, 0, 1), (1, 0, 0)) if ax[1] else ((1, 0, 0), (0, 1, 0))
    return [tuple(centre[k] + r * (math.cos(rot + 2 * math.pi * i / n) * e1[k] + math.sin(rot + 2 * math.pi * i / n) * e2[k]) for k in range(3))
            for i in range(n)]


def hole_decor(centre, axis, d, fill="#fff"):
    def fn(c, P):
        P_(c, [P(p) for p in ngon(centre, axis, d / 2, 28)], fill=fill, lw="thin")
    return fn


def slot_decor(centre, along, normal_axis, L, W, fill="#fff"):
    """Stadium slot on a face: long axis `along` (unit x or y), face normal `normal_axis`."""
    nrm = [abs(a) for a in normal_axis]
    side = tuple(1 if (i == 2) else 0 for i in range(3))     # slots are 'long' horizontally, short vertically (z)
    def fn(c, P):
        r, a = W / 2, (L - W) / 2
        pts = []
        for i in range(13):
            t = -math.pi / 2 + math.pi * i / 12
            pts.append(tuple(centre[k] + along[k] * (a + r * math.cos(t)) + side[k] * r * math.sin(t) for k in range(3)))
        for i in range(13):
            t = math.pi / 2 + math.pi * i / 12
            pts.append(tuple(centre[k] + along[k] * (-a + r * math.cos(t)) + side[k] * r * math.sin(t) for k in range(3)))
        P_(c, [P(p) for p in pts], fill=fill, lw="thin")
    return fn


def add(p, v):
    return tuple(p[k] + v[k] for k in range(3))


def bolt(sc, face, axis, L=38.1):
    """Hex bolt: `face` is the bearing face of the head, `axis` points from the head toward the thread (drawing sizes only)."""
    back = tuple(-a for a in axis)
    sc.cylinder(face, axis, L, 4.76, fill=GREY["light"])
    sc.prism(ngon(add(face, tuple(b * 6.4 for b in back)), axis, 8.25, 6, rot=math.radians(30)), axis, 6.4,
             fills=("#fff", GREY["light"], GREY["mid"]), lw="thin")


def washer(sc, c0, axis):
    ctr = add(c0, tuple(a * 2.0 for a in axis)) if sum(axis[k] * VIEW[k] for k in range(3)) > 0 else c0
    sc.cylinder(c0, axis, 2.0, 10.0, fill=GREY["light"], cap_decor=[hole_decor(ctr, axis, 10.3)])


def nut(sc, c0, axis):
    out = sc.prism(ngon(c0, axis, 8.25, 6, rot=math.radians(30)), axis, 11.0, fills=("#fff", GREY["light"], GREY["mid"]), lw="thin")
    ctr = add(c0, tuple(a * 11.0 for a in axis)) if sum(axis[k] * VIEW[k] for k in range(3)) > 0 else c0
    key = "x" if abs(axis[0]) else "y" if abs(axis[1]) else "z"
    for f in out:
        n = normal(f[1])
        if abs(abs(n["xyz".index(key)]) - 1) < 1e-6:
            f[5] = [hole_decor(ctr, axis, 9.5)]


def fitting(sc, heel, dx, z_c, gusset_up, off=(0, 0, 0)):
    """Gusseted 90-degree fitting, heel (outside of the bend) at heel=(x, y); A-leg against rail A's outer face (y = heel y) running
    toward dx (+1 far end, -1 wall end); B-leg against a face of rail B (x = heel x) running toward +y."""
    hx, hy = heel[0] + off[0], heel[1] + off[1]
    z0, z1 = z_c - FIT_W / 2 + off[2], z_c + FIT_W / 2 + off[2]
    zc = z_c + off[2]
    fl = (GREY["light"], GREY["light"], GREY["light"])
    ax_holes = [slot_decor((hx + dx * h, hy + FIT_T + 0.05, zc), (1, 0, 0), (0, 1, 0), SLOT_L, SLOT_W) for h in FIT_H]
    if dx > 0:
        sc.box(hx, hx + FIT_L, hy, hy + FIT_T, z0, z1, fills=fl, decor={"y": ax_holes})
        bx_face = hx + FIT_T
        sc.box(hx, hx + FIT_T, hy + FIT_T, hy + FIT_L, z0, z1, fills=fl,
               decor={"x": [slot_decor((bx_face + 0.05, hy + h, zc), (0, 1, 0), (1, 0, 0), SLOT_L, SLOT_W) for h in FIT_H]})
        ix = hx + FIT_T
    else:
        sc.box(hx - FIT_L, hx, hy, hy + FIT_T, z0, z1, fills=fl, decor={"y": ax_holes})
        sc.box(hx - FIT_T, hx, hy + FIT_T, hy + FIT_L, z0, z1, fills=fl,
               decor={"x": [slot_decor((hx + 0.05, hy + h, zc), (0, 1, 0), (1, 0, 0), SLOT_L, SLOT_W) for h in FIT_H]})
        ix = hx - FIT_T
    iy = hy + FIT_T
    g = 26
    gz0 = z1 - FIT_T if gusset_up else z0
    sc.prism([(ix, iy, gz0), (ix + dx * g, iy, gz0), (ix, iy + g, gz0)], (0, 0, 1), FIT_T, fills=(GREY["mid"], GREY["mid"], GREY["mid"]), bias=(80.0 if gusset_up else 0.0))  # the outside gusset sits in the open corner, in front of its legs
    return (hx, hy, z1), (hx, hy, z0)


RAILA_Y0 = DATA["railA"]["y0"] * 10      # 479
RAILB_X0 = DATA["railB"]["x0"] * 10      # 479


def fit_view(sc, W, H, margin):
    pts = [proj(p) for f in sc.faces for p in f[1]]
    u0, u1 = min(p[0] for p in pts), max(p[0] for p in pts)
    v0, v1 = min(p[1] for p in pts), max(p[1] for p in pts)
    l, t, r, b = margin
    k = min((W - l - r) / (u1 - u0), (H - t - b) / (v1 - v0))
    return k, (lambda p: (l + (proj(p)[0] - u0) * k, t + (v1 - proj(p)[1]) * k))


def rails(sc, xa0, xa1, yb1, holes=True):
    st = (GREY["steel"], GREY["mid"], GREY["steel"])
    a_holes = [hole_decor((HEEL_OUT + RAILA_X0 + h - RAILA_X0, OUT + 0.05, ZC), (0, 1, 0), BO_D) for h in FIT_H] + \
              [hole_decor((INB - h, OUT + 0.05, ZC), (0, 1, 0), BO_D) for h in FIT_H] if holes else []
    sc.box(xa0, xa1, RAILA_Y0, OUT, -T, 0, fills=st)
    sc.box(xa0, xa1, INB, OUT, -LEG, -T, fills=st, decor={"y": a_holes})
    b_holes = [hole_decor((OUT + 0.05, OUT + h, ZC), (1, 0, 0), BO_D) for h in FIT_H] if holes else []
    sc.box(RAILB_X0, OUT, OUT, yb1, -T, 0, fills=st)
    sc.box(INB, OUT, OUT, yb1, -LEG, -T, fills=st, decor={"x": b_holes})


# ---------------------------------------------------------------- Fig F-1: exploded isometric of the corner
def fig_exploded():
    sc = Scene()
    xa0, xa1, yb1 = 400, 740, 800
    rails(sc, xa0, xa1, yb1)
    OO = (75, 75, -95)            # outside fitting group, pulled into the knee space and down
    IO = (-30, 95, -205)           # inside fitting group, pulled out from under rail B's flat leg and down
    top_o, _ = fitting(sc, (OUT, OUT), +1, ZC, gusset_up=True, off=OO)
    top_i, bot_i = fitting(sc, (INB, OUT), -1, ZC, gusset_up=False, off=IO)
    c = Canvas(172, 132)
    k, P = fit_view(sc, 172, 132, (2, 4, 46, 2))
    sc.render(c, P)
    # the inside fitting's gusset is hidden behind its own legs: show it dashed
    ix, iy, gz = INB - FIT_T + IO[0], OUT + FIT_T + IO[1], ZC - FIT_W / 2 + IO[2]
    P_(c, [P((ix, iy, gz)), P((ix - 26, iy, gz)), P((ix, iy + 26, gz))], lw="thin", dash="1.2 0.8")
    c.balloon(P((640, OUT, -25)), (14, 30), "P06")
    c.balloon(P((505, 740, 0)), (120, 14), "P07")
    c.balloon(P((OUT + OO[0] + 60, OUT + OO[1] + FIT_T, ZC + OO[2])), (14, 104), "P08")
    c.balloon(P((INB + IO[0] + FIT_T, OUT + IO[1] + 60, ZC + IO[2])), (146, 98), "P08")
    for i, (t, w) in enumerate([("OUTSIDE FITTING", "bold"), ("heel in the outside corner;", ""), ("legs on rail A (toward the", ""),
                                ("far end) and on rail B's", ""), ("outer face; gusset up,", ""), ("facing the knee space", "")]):
        T_(c, 3, 110 + i * 4.1, t, size=3.2, weight=w or "normal")
    for i, (t, w) in enumerate([("INSIDE FITTING", "bold"), ("heel in the inside corner", ""), ("legs on rail A (toward", ""),
                                ("the wall end) and on rail", ""), ("B's inner face, under its", ""), ("flat leg; gusset DOWN,", ""),
                                ("at the floor (dashed)", "")]):
        T_(c, 128, 60 + i * 4.1, t, size=3.2, weight=w or "normal")
    for tgt, frm in (((OUT, OUT, ZC + FIT_W / 2), top_o), ((INB, OUT, ZC + FIT_W / 2), top_i)):
        a, b = P(frm), P(tgt)
        L_(c, a[0], a[1], b[0], b[1], lw="thin", dash="2 1")
        head(c, a[0], a[1], b[0], b[1], 2.0)
    return c, P, k


# ---------------------------------------------------------------- Fig F-2: section at the bolt line, which bolt goes where
def fig_plan():
    k = 0.64
    c = Canvas(172, 128)
    X = lambda x: 6 + (x - 412) * k
    Y = lambda y: 8 + (y - 468) * k
    xa0, xa1, yb1 = 412, 660, 650
    # flat legs (above the cut): dashed outlines
    P_(c, [(X(xa0), Y(RAILA_Y0)), (X(xa1), Y(RAILA_Y0)), (X(xa1), Y(INB)), (X(xa0), Y(INB))], lw="thin", dash="2 1")
    P_(c, [(X(RAILB_X0), Y(OUT)), (X(INB), Y(OUT)), (X(INB), Y(yb1)), (X(RAILB_X0), Y(yb1))], lw="thin", dash="2 1")
    # vertical legs in section
    def sect(x0, x1, y0, y1, fill=GREY["steel"]):
        pts = [(X(x0), Y(y0)), (X(x1), Y(y0)), (X(x1), Y(y1)), (X(x0), Y(y1))]
        P_(c, pts, fill=fill); c.hatch(pts, spacing=0.9)
    sect(xa0, xa1, INB, OUT)
    sect(INB, OUT, OUT, yb1)
    for xx in (X(xa0), X(xa1)):
        c.raw(f'<rect x="{_f(xx - 1.2)}" y="{_f(Y(RAILA_Y0) - 1)}" width="2.4" height="{_f((OUT - RAILA_Y0) * k + 2)}" fill="#fff"/>')
        zig(c, xx, Y(RAILA_Y0) - 0.5, Y(OUT) + 0.5, amp=0.9, n=2)
    c.raw(f'<rect x="{_f(X(RAILB_X0) - 1)}" y="{_f(Y(yb1) - 1.2)}" width="{_f((OUT - RAILB_X0) * k + 2)}" height="2.4" fill="#fff"/>')
    # fittings in section (L shapes) and gusset outlines (below the cut: hidden for the inside one)
    def L_fit(hx, hy, dx):
        ix = hx + dx * FIT_T
        pts = [(X(hx), Y(hy)), (X(hx + dx * FIT_L), Y(hy)), (X(hx + dx * FIT_L), Y(hy + FIT_T)), (X(ix), Y(hy + FIT_T)), (X(ix), Y(hy + FIT_L)), (X(hx), Y(hy + FIT_L))]
        P_(c, pts, fill=GREY["light"]); c.hatch(pts, spacing=1.6, angle=135)
        return ix, hy + FIT_T
    ox_, oy_ = L_fit(OUT, OUT, +1)
    ix_, iy_ = L_fit(INB, OUT, -1)
    for h in FIT_H:   # the cut runs along each slot: 21 gaps in the fitting legs
        for x in (OUT + h, INB - h):
            R_(c, X(x - SLOT_L / 2), Y(OUT) + 0.15, SLOT_L * k, FIT_T * k - 0.3, fill="#fff", lw="thin")
        for x0 in (OUT, INB - FIT_T):
            R_(c, X(x0) + 0.15, Y(OUT + h - SLOT_L / 2), FIT_T * k - 0.3, SLOT_L * k, fill="#fff", lw="thin")
    P_(c, [(X(ox_), Y(oy_)), (X(ox_ + 26), Y(oy_)), (X(ox_), Y(oy_ + 26))], lw="thin")
    P_(c, [(X(ix_), Y(iy_)), (X(ix_ - 26), Y(iy_)), (X(ix_), Y(iy_ + 26))], lw="thin", dash="1.2 0.8")

    def bolt_plan(axis_pt, d, head_at, nut_at):
        """Bolt along a horizontal page axis: d = (dx, dy) unit from head to thread; head_at / nut_at are the bearing planes."""
        (ax, ay) = axis_pt
        def seg(a0, a1, half, fill, lw="thin"):
            if d[0]:
                xs = sorted([a0, a1]); P_(c, [(X(xs[0]), Y(ay - half)), (X(xs[1]), Y(ay - half)), (X(xs[1]), Y(ay + half)), (X(xs[0]), Y(ay + half))], fill=fill, lw=lw)
            else:
                ys = sorted([a0, a1]); P_(c, [(X(ax - half), Y(ys[0])), (X(ax + half), Y(ys[0])), (X(ax + half), Y(ys[1])), (X(ax - half), Y(ys[1]))], fill=fill, lw=lw)
        s = d[0] or d[1]                                                # positions along the axis: head_at + s*t toward the thread
        seg(head_at, head_at + s * 38.1, 4.76, "#fff")                 # shank, 1-1/2 in
        seg(head_at, head_at - s * 2.0, 10, GREY["light"])             # washer under the head
        seg(head_at - s * 2.0, head_at - s * 8.4, 7.15, GREY["mid"])    # head
        seg(nut_at, nut_at + s * 2.0, 10, GREY["light"])               # washer under the nut
        seg(nut_at + s * 2.0, nut_at + s * 13.0, 7.15, GREY["mid"])     # nylon-insert nut
        return s
    labels = []
    for h in FIT_H:
        x = OUT + h
        bolt_plan((x, None), (0, -1), OUT + FIT_T, INB)
        labels.append(("O", x))
        x = INB - h
        bolt_plan((x, None), (0, -1), OUT + FIT_T, INB)
        labels.append(("I", x))
        y = OUT + h
        bolt_plan((None, y), (-1, 0), OUT + FIT_T, INB - FIT_T)
    # insertion arrows on the head side; names at the thread end
    for h, n in zip(FIT_H, (1, 2)):
        for x, nm in ((OUT + h, "O"), (INB - h, "I")):
            arrow(c, X(x), Y(OUT + FIT_T + 18), X(x), Y(OUT + FIT_T + 10), lw="thin", h=1.5)
            T_(c, X(x), Y(INB - 38) - 1.5, f"{nm}{n}", size=3.2, anchor="middle", weight="bold")
        y = OUT + h
        arrow(c, X(OUT + FIT_T + 30), Y(y), X(OUT + FIT_T + 10), Y(y), lw="thin", h=1.5)
        T_(c, X(OUT + FIT_T + 30) + 1.2, Y(y), f"C{n}", size=3.2, weight="bold")
    # labels
    T_(c, X(xa1) - 1, Y(RAILA_Y0) - 2.5, "rail A (P06)", size=3.2, anchor="end", weight="bold")
    T_(c, X(OUT) + 3, Y(yb1) - 5, "rail B (P07)", size=3.2, weight="bold")
    T_(c, X(xa0) + 1, Y(RAILA_Y0) - 2.5, "← wall end", size=3.2)
    leader(c, X(600), Y(625), X(OUT + FIT_T / 2), Y(OUT + 96), "outside fitting:", lines=[f"heel on rail A's", f"{cm(HEEL_OUT, True)} cm mark"])
    leader(c, X(414), Y(625), X(INB - FIT_T / 2), Y(OUT + 96), "inside fitting:", anchor="start", lines=[f"heel on rail A's", f"{cm(HEEL_IN, True)} cm mark"])
    T_(c, 6, 4, f"Section at the bolt line, {BOLT} mm below the top, seen from above. Dashed: flat legs above the cut.", size=3.2)
    return save(c, "06-plan.svg")


# ---------------------------------------------------------------- Fig F-3: bolt stack-ups
def fig_stackup():
    k = 1.4
    PH = 12                                     # half-height of the plates drawn in section (cut off; drawing only)
    c = Canvas(172, 134)
    m = re.search(r"leave ([\d.]+ mm) of play across and ([\d.]+ mm) along.* ([\d.]+ mm)$", CJ["why_tight"])
    play_x, play_l, play_rail = m.group(1), m.group(2), m.group(3)

    def row(ax, layers, title, balloons, side="the fitting"):
        T_(c, 3, ax - 31, title, size=3.4, weight="bold")
        x = 34
        P_(c, [(x - 6.4 * k, ax - 8.25 * k), (x, ax - 8.25 * k), (x, ax + 8.25 * k), (x - 6.4 * k, ax + 8.25 * k)], fill=GREY["mid"])
        L_(c, x - 6.4 * k, ax - 4.1 * k, x, ax - 4.1 * k, lw="thin"); L_(c, x - 6.4 * k, ax + 4.1 * k, x, ax + 4.1 * k, lw="thin")
        P_(c, [(x, ax - 4.76 * k), (x + 38.1 * k, ax - 4.76 * k), (x + 38.1 * k, ax + 4.76 * k), (x, ax + 4.76 * k)], fill="#fff")
        xx, pos, tops = x, {"head": (x - 6.4 * k, x)}, {"head": ax - 8.25 * k}
        for name, t, kind in layers:
            w = t * k
            inner, outer, fill, sp, ang = {"washer": (5.15, 10, GREY["light"], 0.8, 45), "nut": (4.76, 8.25, GREY["mid"], 0.8, 45),
                                          "fitting": (SLOT_W / 2, PH, GREY["light"], 1.2, 135), "steel": (BO_D / 2, PH, GREY["steel"], 0.8, 45)}[kind]
            for sg in (-1, 1):
                pts = [(xx, ax + sg * inner * k), (xx + w, ax + sg * inner * k), (xx + w, ax + sg * outer * k), (xx, ax + sg * outer * k)]
                P_(c, pts, fill=fill); c.hatch(pts, spacing=sp, angle=ang)
            if kind == "nut":
                L_(c, xx + w * 0.72, ax - outer * k, xx + w * 0.72, ax + outer * k, lw="thin")
            pos[name], tops[name] = (xx, xx + w), ax - outer * k
            xx += w
        L_(c, x - 10 * k, ax, x + 41 * k, ax, lw="thin", dash="4 1 0.8 1")
        arrow(c, 3, ax, x - 6.4 * k - 1.5, ax, h=2.0)
        T_(c, 3, ax + 4, "in from", size=3.2); T_(c, 3, ax + 8.2, side, size=3.2); T_(c, 3, ax + 12.4, "fitting" if side == "the outside" else "side", size=3.2)
        for name, label, bx in balloons:
            a0, a1 = pos[name]
            c.balloon(((a0 + a1) / 2, tops[name] + 0.8), (bx, ax - 23), label)
        return pos, ax

    def dims(pos, ax, names):
        yb = ax + PH * k + 4
        for i, nme in enumerate(names):
            a0, a1 = pos[nme]
            L_(c, a0, ax + PH * k + 0.6, a0, yb + 1.2, lw="dim"); L_(c, a1, ax + PH * k + 0.6, a1, yb + 1.2, lw="dim")
            head(c, a0 - 3, yb, a0, yb, 1.3); head(c, a1 + 3, yb, a1, yb, 1.3)
            L_(c, a0 - 3.5, yb, a1 + 3.5, yb, lw="dim")
            t = f"{FIT_T}" if nme.startswith("fit") else f"{T}"
            T_(c, (a0 + a1) / 2, yb + 3.6 + (i % 2) * 3.6, t, size=3.2, anchor="middle")

    A = [("w1", 2.0, "washer"), ("fitA", FIT_T, "fitting"), ("railA", T, "steel"), ("w2", 2.0, "washer"), ("nut", 11.0, "nut")]
    pos, ax = row(36, A, "Rail A: 4 bolts, one fitting each (O1, O2, I1, I2)",
                  [("head", "H08", 24), ("w1", "H09", 34), ("fitA", "P08", 43), ("railA", "P06", 52), ("w2", "H09", 61), ("nut", "H10", 72)])
    dims(pos, ax, ["fitA", "railA"])
    lines = [(f"fitting {SLOT_LBL} (cut across):", ""), (f"{play_x} play across, {play_l} along", ""), (f"rail hole {BO_LBL}:", ""),
             (f"{play_rail} of play", ""), ("so the joint holds by friction:", "bold"), ("tighten fully, 25 N·m", "bold")]
    for i, (t, w) in enumerate(lines):
        T_(c, 104, 22 + i * 4.3, t, size=3.2, weight=w or "normal")
    B = [("w1", 2.0, "washer"), ("fitO", FIT_T, "fitting"), ("railB", T, "steel"), ("fitI", FIT_T, "fitting"), ("w2", 2.0, "washer"), ("nut", 11.0, "nut")]
    pos, ax = row(102, B, "Rail B: 2 bolts through outside fitting, rail B and inside fitting (C1, C2)",
                  [("head", "H08", 24), ("w1", "H09", 33), ("fitO", "P08", 42), ("railB", "P07", 51), ("fitI", "P08", 60), ("w2", "H09", 69), ("nut", "H10", 80)], side="the outside")
    dims(pos, ax, ["fitO", "railB", "fitI"])
    for i, t in enumerate(["head and washer on the", "outside fitting (knee side);", "washer and nut on the", "inside fitting, in the pocket", "under rail B's flat leg"]):
        T_(c, 104, 90 + i * 4.3, t, size=3.2)
    return save(c, "06-stackup.svg")


# ---------------------------------------------------------------- Fig F-4: rail screw into the top
def fig_screw():
    k = 1.4
    c = Canvas(172, 104)
    pen = float(S["rail_screws"].split("; ")[1].split(" mm")[0])     # 20.6 into the top
    for p in (0, 1):
        ox = 38 + p * 94                     # screw axis (page x)
        uz = 48                              # top's underside (page y)
        Y = lambda z: uz - z * k             # z up from the underside
        T_(c, ox - 36, 4.5, ["a  pilot through the rail hole", "b  screw driven"][p], size=3.4, weight="bold")
        # top slab, 28, laminate both faces
        xa, xb = ox - 30, ox + 30
        P_(c, [(xa, Y(TOP_T)), (xb, Y(TOP_T)), (xb, Y(0)), (xa, Y(0))], fill=GREY["wood"])
        hatch_rect(c, xa, Y(TOP_T), xb - xa, TOP_T * k, spacing=2.4)
        for z in (TOP_T - 1, 1):
            L_(c, xa, Y(z), xb, Y(z), lw="thin")
        # flat leg under it, with the clearance hole
        P_(c, [(xa, Y(0)), (xb, Y(0)), (xb, Y(-T)), (xa, Y(-T))], fill=GREY["steel"], lw="heavy")
        c.hatch([(xa, Y(0)), (xb, Y(0)), (xb, Y(-T)), (xa, Y(-T))], spacing=0.9)
        R_(c, ox - SC_D / 2 * k, Y(0) - 0.1, SC_D * k, T * k + 0.2, fill="#fff", lw="thin")
        # pilot hole 20 into the wood
        R_(c, ox - 1.6 * k, Y(20), 3.2 * k, 20 * k, fill="#fff", lw="thin")
        if p == 0:
            # puck 25 RAIL against the leg's exposed face, bit up through it, chuck nose on the puck
            ph = 20
            R_(c, ox - 9 * k, Y(-T), 18 * k, ph * k, fill=GREY["light"])
            R_(c, ox - 1.75 * k, Y(-T), 3.5 * k, ph * k, fill="#fff", lw="thin")
            R_(c, ox - 1.6 * k, Y(20), 3.2 * k, (20 + T + ph) * k, fill="#fff")
            R_(c, ox - 8 * k, Y(-T - ph), 16 * k, 6, fill=GREY["mid"])
            T_(c, ox + 9 * k + 2, Y(-T - ph / 2) - 2, "puck 25 RAIL (P18)", size=3.2)
            T_(c, ox + 9 * k + 2, Y(-T - ph / 2) + 2.2, "on the leg's face", size=3.2)
            T_(c, ox + 8 * k + 2, Y(-T - ph) + 3, "chuck nose stops here", size=3.2)
            dimv(c, Y(-T), Y(20), xa - 4, "25 mm from the leg", x_from=ox - 1.6 * k)
            dimv(c, Y(0), Y(20), ox + 12, "20", x_from=ox + 1.6 * k, left=False, box=True)
            T_(c, xb + 2, Y(16), "pilot", size=3.2)
            T_(c, xb + 2, Y(16) + 4.2, PILOT_LBL, size=3.2)
        else:
            # pan head below the leg, shank up 20.6 into the top
            hw, hh = 4.8, 3.6
            P_(c, [(ox - hw * k, Y(-T)), (ox + hw * k, Y(-T)), (ox + hw * k * 0.85, Y(-T - hh)), (ox - hw * k * 0.85, Y(-T - hh))], fill=GREY["mid"])
            P_(c, [(ox - 2.4 * k, Y(-T)), (ox + 2.4 * k, Y(-T)), (ox + 2.4 * k, Y(pen - 2)), (ox, Y(pen)), (ox - 2.4 * k, Y(pen - 2))], fill=GREY["dark"])
            for z in range(1, int(pen) - 1, 2):
                L_(c, ox - 2.4 * k, Y(z), ox + 2.4 * k, Y(z + 1), lw="thin", color="#fff")
            dimv(c, Y(0), Y(pen), xa - 4, f"{pen:g} in wood", x_from=ox - 2.4 * k)
            dimv(c, Y(pen), Y(TOP_T), xa - 4, f"{TOP_T - pen:.1f} left", x_from=ox, rot=False)
            dimv(c, Y(0), Y(-T), xa - 4, f"{T}", x_from=xa, rot=False)
            dimv(c, Y(0), Y(TOP_T), xb + 4, f"{TOP_T} top", x_from=xb, left=False)
            T_(c, ox, Y(-T - hh) + 4.5, "#10 × 1 in pan head (H03)", size=3.2, anchor="middle")
            T_(c, ox, Y(-T - hh) + 8.7, f"through the {SC_LBL} hole", size=3.2, anchor="middle")
    T_(c, 4, 100, f"Never more than {FACTS['tops']['max_fastener_depth']} mm into the {TOP_T} mm top. Drawn upright, as for rail B's holes 1 and 2.", size=3.2)
    return save(c, "06-screw.svg")


if __name__ == "__main__":
    c, P, k = fig_exploded()
    print(save(c, "06-exploded.svg"))
    print(fig_plan())
    print(fig_stackup())
    print(fig_screw())
