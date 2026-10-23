#!/usr/bin/env python3
"""Figures for the cover and chapter A (finished assembly). Also holds the plan / isometric helpers
that figures_07.py imports. Every number comes from manual/data.json or manual/facts.json (cm in the
data, mm on the page labels)."""
import json, math, os, sys

MAN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MAN)
from lib.draw import Canvas, FONT, LW  # noqa: E402

D = json.load(open(os.path.join(MAN, "data.json")))
F = json.load(open(os.path.join(MAN, "facts.json")))
LAY = F["layout_cm"]
FIG = os.path.join(MAN, "figures")
Z0, Z1 = D["Y0"], D["Y1"]          # underside 80.2, surface 83.0 (cm)
ALEX_H = F["heights_mm"]["alex_height"] / 10   # 70 (ASSUMPTION)
RAIL_LOW = F["heights_mm"]["rail_lower_edge"] / 10


def mm(v_cm):
    """cm value from the data files -> mm label."""
    return ("%.1f" % (v_cm * 10)).rstrip("0").rstrip(".")


def cm(v_cm):
    """tape-measure label in cm, as the build manual writes it."""
    return ("%.1f" % v_cm).rstrip("0").rstrip(".")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


# ---------------- page-space annotation (the library's dim() puts its label on the line) ----------------
def ptext(c, x, y, s, size=3.2, anchor="middle", weight="normal", rotate=0, color="#000"):
    rot = f' transform="rotate({rotate:.2f} {x:.2f} {y:.2f})"' if rotate else ""
    c.raw(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{FONT}" font-size="{size}" text-anchor="{anchor}" '
          f'dominant-baseline="middle" font-weight="{weight}" fill="{color}"{rot}>{esc(s)}</text>')


def pline(c, a, b, lw=0.25, dash=None, color="#000"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    c.raw(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="{color}" stroke-width="{lw}"{d} stroke-linecap="round"/>')


def dim(c, p1, p2, label, off, size=3.2, ext=True, tside=None):
    """Dimension between object points p1, p2 drawn `off` page-mm to the left of p1->p2 (negative: right).
    The label sits outside the dimension line."""
    x1, y1 = c.P(*p1); x2, y2 = c.P(*p2)
    L = math.hypot(x2 - x1, y2 - y1) or 1
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = uy, -ux                      # left normal in page space (y down)
    a1 = (x1 + nx * off, y1 + ny * off); a2 = (x2 + nx * off, y2 + ny * off)
    sg = 1 if off >= 0 else -1
    if ext and off:
        pline(c, (x1 + nx * sg * 0.8, y1 + ny * sg * 0.8), (a1[0] + nx * sg * 1.5, a1[1] + ny * sg * 1.5))
        pline(c, (x2 + nx * sg * 0.8, y2 + ny * sg * 0.8), (a2[0] + nx * sg * 1.5, a2[1] + ny * sg * 1.5))
    pline(c, a1, a2)
    if L > 7:
        c._head(a2[0], a2[1], a1[0], a1[1], 1.5); c._head(a1[0], a1[1], a2[0], a2[1], 1.5)
    else:  # short: arrows outside
        c._head(a1[0] - ux * 3, a1[1] - uy * 3, a1[0], a1[1], 1.5); c._head(a2[0] + ux * 3, a2[1] + uy * 3, a2[0], a2[1], 1.5)
        pline(c, (a1[0] - ux * 3, a1[1] - uy * 3), (a2[0] + ux * 3, a2[1] + uy * 3))
    ts = sg if tside is None else tside
    tx, ty = (a1[0] + a2[0]) / 2 + nx * ts * 2.2, (a1[1] + a2[1]) / 2 + ny * ts * 2.2
    ang = math.degrees(math.atan2(uy, ux))
    if ang > 90.01 or ang < -89.99:
        ang += 180
    ptext(c, tx, ty, label, size=size, rotate=ang)


def leader(c, target, textpos, label, size=3.2, anchor="start"):
    """Leader from page-mm text position to object target point."""
    tx, ty = c.P(*target)
    px, py = textpos
    pline(c, (px, py), (tx, ty))
    c.raw(f'<circle cx="{tx:.2f}" cy="{ty:.2f}" r="0.6" fill="#000"/>')
    ptext(c, px + (1.2 if anchor == "start" else -1.2), py, label, size=size, anchor=anchor)


def pballoon(c, target, pos, num, r=3.6):
    """Balloon at page position `pos` with leader to object point `target`."""
    tx, ty = c.P(*target)
    pline(c, pos, (tx, ty))
    c.raw(f'<circle cx="{tx:.2f}" cy="{ty:.2f}" r="0.7" fill="#000"/>')
    c.raw(f'<circle cx="{pos[0]:.2f}" cy="{pos[1]:.2f}" r="{r}" fill="#fff" stroke="#000" stroke-width="0.5"/>')
    ptext(c, pos[0], pos[1] + 0.1, str(num), size=3.0, weight="bold")


# ---------------- isometric ----------------
class Iso(Canvas):
    """Canvas whose iso() matches iso_box()'s face order for desk coordinates: x along the back wall,
    y toward the room, z up; seen from the room, above. (The library's own iso() shows the hidden x face;
    see the report.) Rotation only, so nothing is mirrored."""
    @staticmethod
    def iso(x, y, z, angle=30):
        a = math.radians(angle); X, Y = x, -y
        return ((X + Y) * math.cos(a), (Y - X) * math.sin(a) + z)


def ibox(c, x0, x1, y0, y1, z0, z1, fill=("#fff", "#e6e6e6", "#cccccc"), lw="outline"):
    c.iso_box(x0, y1, z0, x1 - x0, -(y1 - y0), z1 - z0, fill=fill, lw=lw)


def ipoly(c, pts, fill="none", lw="outline", dash=None, close=True):
    c.poly([c.iso(*p) for p in pts], fill=fill, lw=lw, dash=dash, close=close)


def _hull(pts):
    pts = sorted(set((round(a, 4), round(b, 4)) for a, b in pts))
    def cr(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def icyl(c, cx, cy, r, z0, z1, fill="#e6e6e6", top="#fff", lw="outline", n=28):
    ring = lambda z: [c.iso(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n), z) for i in range(n)]
    c.poly(_hull(ring(z0) + ring(z1)), fill=fill, lw=lw)
    c.poly(ring(z1), fill=top, lw=lw)


def iellipse(c, cx, cy, r, z, fill="none", lw="outline", dash=None, n=36):
    c.poly([c.iso(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n), z) for i in range(n)], fill=fill, lw=lw, dash=dash)


def panel(c, cx, cy, nx, ny, W, H, zb, R, depth=2.5, n=10):
    """Curved monitor panel (radius R cm), centre (cx, cy), facing (nx, ny), bottom at zb."""
    tx, ty = -ny, nx
    def edge(z, back=0.0):
        out = []
        for i in range(n + 1):
            s = -W / 2 + W * i / n
            sag = R - math.sqrt(R * R - s * s)
            out.append((cx + s * tx + (sag - back) * nx, cy + s * ty + (sag - back) * ny, z))
        return out
    ipoly(c, edge(zb, depth) + edge(zb + H, depth)[::-1], fill="#808080", lw="thin")
    ipoly(c, edge(zb) + edge(zb + H)[::-1], fill="#fff")
    inset = 1.2
    def edge2(z):
        out = []
        for i in range(n + 1):
            s = -W / 2 + inset + (W - 2 * inset) * i / n
            sag = R - math.sqrt(R * R - s * s)
            out.append((cx + s * tx + sag * nx, cy + s * ty + sag * ny, z))
        return out
    ipoly(c, edge2(zb + inset) + edge2(zb + H - inset)[::-1], fill="#d9d9d9", lw="thin")


def idim(c, p1, p2, offv, label, size=3.2):
    """Isometric dimension: p1, p2 3D points, offv the 3D offset of the dimension line."""
    q1 = tuple(p1[i] + offv[i] for i in range(3)); q2 = tuple(p2[i] + offv[i] for i in range(3))
    e = 0.12
    q1e = tuple(p1[i] + offv[i] * (1 + e) for i in range(3)); q2e = tuple(p2[i] + offv[i] * (1 + e) for i in range(3))
    s1 = tuple(p1[i] + offv[i] * 0.1 for i in range(3)); s2 = tuple(p2[i] + offv[i] * 0.1 for i in range(3))
    c.line(c.iso(*s1), c.iso(*q1e), lw="thin"); c.line(c.iso(*s2), c.iso(*q2e), lw="thin")
    a = c.P(*c.iso(*q1)); b = c.P(*c.iso(*q2))
    pline(c, a, b)
    c._head(b[0], b[1], a[0], a[1], 1.6); c._head(a[0], a[1], b[0], b[1], 1.6)
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    if ang > 90.01 or ang < -89.99:
        ang += 180
    o = c.P(*c.iso(*tuple(p1[i] + offv[i] * 1.6 for i in range(3))))
    # label on the outer side of the dimension line
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    Ll = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
    nx, ny = -(b[1] - a[1]) / Ll, (b[0] - a[0]) / Ll          # page normal of the dimension line
    if nx * (o[0] - a[0]) + ny * (o[1] - a[1]) < 0 or (abs(o[0] - a[0]) < 0.2 and nx < 0):
        nx, ny = -nx, -ny                                     # label on the outer side (right, for a vertical line)
    ptext(c, mx + nx * 2.4, my + ny * 2.4, label, size=size, rotate=ang, weight="bold")


def itext(c, p3, s, size=3.2, anchor="middle", weight="normal", rotate=0):
    x, y = c.P(*c.iso(*p3))
    ptext(c, x, y, s, size=size, anchor=anchor, weight=weight, rotate=rotate)


def iso_canvas(width_mm, ext_pts, margin=(6, 6, 6, 6)):
    """Canvas sized so the projected ext_pts fill width_mm (minus margins l, r, t, b in page mm)."""
    uv = [Iso.iso(*p) for p in ext_pts]
    u0, u1 = min(p[0] for p in uv), max(p[0] for p in uv)
    v0, v1 = min(p[1] for p in uv), max(p[1] for p in uv)
    l, r, t, b = margin
    s = (width_mm - l - r) / (u1 - u0)
    h = (v1 - v0) * s + t + b
    c = Iso(width_mm, h, scale=s, origin=(u0 - l / s, v0 - b / s), flip_y=True)
    return c


def desk_iso(c, walls=False, detail=True, mid=None):
    """The finished desk, back to front (painter's order)."""
    A, B = D["A"], D["B"]
    if walls:
        g = -D["gap"]; WH = 165
        ipoly(c, [(g, g, 0), (A["x1"] + 12, g, 0), (A["x1"] + 12, g, WH), (g, g, WH)], fill="#f2f2f2", lw="thin")
        ipoly(c, [(g, g, 0), (g, B["y1"] + 14, 0), (g, B["y1"] + 14, WH), (g, g, WH)], fill="#f2f2f2", lw="thin")
    # legs (back first)
    for n, x, y, *_ in sorted(D["legs"], key=lambda l: l[1] + l[2]):
        icyl(c, x, y, 2.4, 0, Z0, fill="#d9d9d9")
    # ALEX units, with drawer / door lines, rings and feet
    a1 = D["alex1"]; a2 = D["alex2"]
    for a, kind in ((a1, "drawers"), (a2, "door")):
        x0, y0 = a["x0"], a["y0"]; x1, y1 = x0 + a["w"], y0 + a["d"]
        ibox(c, x0, x1, y0, y1, 0, ALEX_H)
        if kind == "drawers":   # front face y1
            for k in range(1, 5):
                z = ALEX_H * k / 5
                c.line(c.iso(x0 + 1, y1, z), c.iso(x1 - 1, y1, z), lw="thin")
        else:                   # door on the x1 face
            ipoly(c, [(x1, y0 + 1.5, 2), (x1, y1 - 1.5, 2), (x1, y1 - 1.5, ALEX_H - 2), (x1, y0 + 1.5, ALEX_H - 2)], lw="thin")
        feet = [f for f in D["feet"] if x0 <= f[1] <= x1 and y0 <= f[2] <= y1]
        for f in sorted(feet, key=lambda f: f[1] + f[2]):
            iellipse(c, f[1], f[2], D["ringOD"] / 2 + 0.9, ALEX_H, fill="#cccccc", lw="thin")
            icyl(c, f[1], f[2], D["footPad"] / 2, ALEX_H, Z0, fill="#e6e6e6", lw="thin")
    # tops
    ibox(c, A["x0"], A["x1"], A["y0"], A["y1"], Z0, Z1, fill=("#f2f2f2", "#cccccc", "#bfbfbf"))
    ibox(c, B["x0"], B["x1"], B["y0"], B["y1"], Z0, Z1, fill=("#f2f2f2", "#cccccc", "#bfbfbf"))
    # rails, hidden under the front edges: dashed
    for r in (D["railA"], D["railB"]):
        x0, x1, y0, y1 = r["x0"], r["x1"], r["y0"], r["y1"]
        zl = RAIL_LOW
        if r is D["railA"]:   # outer face y1
            ipoly(c, [(x0, y1, zl), (x1, y1, zl), (x1, y1, Z0)], lw="thin", dash="1.6 0.9", close=False)
        else:                 # outer face x1
            ipoly(c, [(x1, y0, zl), (x1, y1, zl), (x1, y1, Z0)], lw="thin", dash="1.6 0.9", close=False)
    if mid:
        mid(c)   # dimensions etc. that the monitors should hide
    if not detail:
        return
    # VIVO poles, crossbar, monitors, Y60 (on the tops, back to front)
    inset = F["vivo"]["pole_centre_from_desk_edge"] / 10
    p1 = (D["clamp"], inset); p2 = (inset, D["clamp"])
    top_z = Z1 + 61
    Y = LAY["surface_items"]["Y60"]
    ibox(c, Y["x"][0], Y["x"][1], Y["y"][0], Y["y"][1], Z1, Z1 + 48)
    ipoly(c, [(Y["x"][0] + 3, Y["y"][1], Z1 + 6), (Y["x"][1] - 3, Y["y"][1], Z1 + 6), (Y["x"][1] - 3, Y["y"][1], Z1 + 45), (Y["x"][0] + 3, Y["y"][1], Z1 + 45)], fill="#d9d9d9", lw="thin")
    for p in (p1, p2):
        ibox(c, p[0] - 4, p[0] + 4, -1.75, 2, Z1 - 3, Z1 + 3) if p is p1 else ibox(c, -1.75, 2, p[1] - 4, p[1] + 4, Z1 - 3, Z1 + 3)
    for p in (p1, p2):
        icyl(c, p[0], p[1], 1.8, Z1, top_z, fill="#bfbfbf")
    zc = Z1 + 41.5
    ipoly(c, [(p1[0], p1[1], zc - 1.5), (p2[0], p2[1], zc - 1.5), (p2[0], p2[1], zc + 1.5), (p1[0], p1[1], zc + 1.5)], fill="#808080", lw="thin")
    s15, c15 = math.sin(math.radians(15)), math.cos(math.radians(15))
    ar, al = LAY["surface_items"]["acer_right"], LAY["surface_items"]["acer_left"]
    panel(c, ar[0], ar[1], -s15, c15, 70, 39.5, Z1 + 26, 150)
    panel(c, al[0], al[1], c15, -s15, 70, 39.5, Z1 + 26, 150)
    g5 = LAY["surface_items"]["G5"]
    panel(c, g5[0], g5[1], 1 / math.sqrt(2), 1 / math.sqrt(2), 71, 44, Z1 + LAY["surface_items"]["G5_bottom_above_top_cm"], 100)


ISO_EXT = [(0, 0, 0), (249, 0, 0), (249, 65, 0), (65, 314, 0), (0, 314, 0), (0, 0, 150), (249, 0, 131), (0, 314, 83)]


def fig_cover():
    c = iso_canvas(170, ISO_EXT + [(-25, 0, 83), (0, -30, 83)], margin=(4, 4, 4, 4))
    A, B = D["A"], D["B"]
    def dims(c):
        idim(c, (0, 0, Z1), (A["x1"], 0, Z1), (0, -26, 0), cm(A["x1"]) + " cm")
        idim(c, (0, 0, Z1), (0, B["y1"], Z1), (-24, 0, 0), cm(B["y1"]) + " cm")
        idim(c, (B["x1"], A["y1"], 0), (B["x1"], A["y1"], Z1), (14, 10, 0), "%.1f cm" % Z1)
    desk_iso(c, mid=dims)
    for lab, (x, y) in (("A", (150, 32)), ("B", (32, 200))):
        px, py = c.P(*c.iso(x, y, Z1))
        c.raw(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="5.5" fill="#fff" stroke="#000" stroke-width="0.8"/>')
        ptext(c, px, py + 0.2, lab, size=7, weight="bold")
    c.save(os.path.join(FIG, "01-cover-iso.svg"))


def fig_iso_a():
    c = iso_canvas(178, ISO_EXT + [(-3, -3, 165), (262, -3, 165), (-3, 330, 165), (262, -3, 0), (-3, 330, 0), (150, 150, 0)], margin=(2, 2, 4, 15))
    desk_iso(c, walls=True)
    # orientation words
    itext(c, (220, -3, 150), "BACK WALL", size=4, weight="bold", rotate=30)
    itext(c, (-3, 230, 140), "SIDE WALL", size=4, weight="bold", rotate=-30)
    # seat: on the floor at the inside corner, facing the diagonal
    s0 = (150, 150, 0); s1 = (92, 92, 0)
    a = c.P(*c.iso(*s0)); b = c.P(*c.iso(*s1))
    c.raw(f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="#000" stroke-width="0.8"/>')
    c._head(a[0], a[1], b[0], b[1], 3.0)
    iellipse(c, 150, 150, 14, 0, lw="outline", dash="1.5 1")
    ptext(c, a[0], a[1] + 12.5, "SEAT: inside corner,", size=3.4, weight="bold")
    ptext(c, a[0], a[1] + 16.5, "facing the diagonal", size=3.4, weight="bold")
    # front / left / right as seen from the seat
    itext(c, (225, 92, 0), "front edge A (you)", size=3.2, rotate=30)
    itext(c, (92, 260, 0), "front edge B (you)", size=3.2, rotate=-30)
    # balloons (part numbers from facts.json)
    bl = [  # target 3D, page offset from target, number
        ((150, 32, Z1), (-14, 14), "P01"), ((32, 200, Z1), (-20, 6), "P02"),
        ((227, 61.5, 40), (16, 16), "P03"), ((61.5, 292, 35), (-6, 22), "P04"),
        ((140, 10, 30), (6, 26), "P05"), ((150, 53, RAIL_LOW), (8, 22), "P06"), ((53, 180, RAIL_LOW), (14, 20), "P07"),
        ((240.5, 56.5, 72), (14, 2), "P09"), ((40, 4.4, Z1 + 55), (12, -16), "P12"),
        ((36.5, 36.5, Z1 + 45), (-18, -14), "P13"), ((99, 19, Z1 + 50), (16, -14), "P14"), ((222, 35.5, Z1 + 30), (-16, -12), "P17"),
    ]
    for t, d, n in bl:
        x, y = c.P(*c.iso(*t))
        pballoon(c, c.iso(*t), (x + d[0], y + d[1]), n)
    c.save(os.path.join(FIG, "01-iso-a.svg"))


# ---------------- plan view (true top view: x right, y down = toward the room) ----------------
def plan_items(c, T, which=("legs", "feet", "alex", "rails", "clamps"), hidden=True, labels=True, tops=("A", "B")):
    """Draw desk parts into canvas c through the mapping T(x, y) -> object coords."""
    def R(x0, x1, y0, y1, **kw):
        pts = [T(x0, y0), T(x1, y0), T(x1, y1), T(x0, y1)]
        c.poly(pts, **kw)
    dsh = "1.6 0.9" if hidden else None
    if "alex" in which:
        for a, n in ((D["alex1"], "ALEX 1"), (D["alex2"], "ALEX 2")):
            R(a["x0"], a["x0"] + a["w"], a["y0"], a["y0"] + a["d"], lw="outline", dash="3 1.5")
    if "rails" in which:
        ra, rb = D["railA"], D["railB"]
        R(ra["x0"], ra["x1"], ra["y0"], ra["y1"], fill="#d9d9d9", lw="thin")
        R(rb["x0"], rb["x1"], rb["y0"], rb["y1"], fill="#d9d9d9", lw="thin")
    if "clamps" in which:
        for p in D["pads"]:
            R(p[0], p[1], p[2], p[3], lw="thin", dash="1 0.8")
        z = D["zoneIn"]; k = D["clamp"]
        R(k - 4, k + 4, 0, z, fill="#bfbfbf", lw="thin")
        R(0, z, k - 4, k + 4, fill="#bfbfbf", lw="thin")
    if "legs" in which:
        for n, x, y, *_ in D["legs"]:
            c.circle(T(x, y), D["legPlate"] / 2, fill="#fff", lw="outline", dash=dsh)
            c.circle(T(x, y), 2.4, fill="#808080", lw="thin")
    if "feet" in which:
        for n, x, y, _ in D["feet"]:
            h = F["feet"]["plate"] / 20
            R(x - h, x + h, y - h, y + h, fill="#fff", lw="thin", dash=dsh)
            c.circle(T(x, y), D["footPad"] / 2, lw="thin")


def wall_hatch(c, p0, p1, side, n_step=2.4):
    """Short hatch ticks behind a wall line (page space), side = unit page vector into the wall."""
    a = c.P(*p0); b = c.P(*p1)
    pline(c, a, b, lw=0.8)
    L = math.hypot(b[0] - a[0], b[1] - a[1]); ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    t = 0
    while t < L:
        x, y = a[0] + ux * t, a[1] + uy * t
        pline(c, (x, y), (x + side[0] * 2 + ux * 1.5, y + side[1] * 2 + uy * 1.5), lw=0.2)
        t += n_step


def fig_plan():
    s = 0.58
    W, H = 178, 215
    ox, oy = -3 - 20 / s, -3 - 22 / s
    c = Canvas(W, H, scale=s, origin=(ox, oy))
    A, B, g = D["A"], D["B"], D["gap"]
    I = lambda x, y: (x, y)
    # walls
    wall_hatch(c, (-g, -g), (A["x1"] + 8, -g), (0, -1))
    wall_hatch(c, (-g, -g), (-g, B["y1"] + 8), (-1, 0))
    ptext(c, *c.P(195, -g - 5.5), "BACK WALL", size=3.4, weight="bold")
    ptext(c, *c.P(-g - 5.5, 196), "SIDE WALL", size=3.4, weight="bold", rotate=-90)
    # tops
    c.rect(0, 0, A["x1"], A["y1"], fill="#f2f2f2")
    c.rect(0, B["y0"], B["x1"], B["y1"] - B["y0"], fill="#f2f2f2")
    # unfinished edges against the walls (heavy)
    c.line((0, 0), (A["x1"], 0), lw="heavy"); c.line((0, B["y0"]), (0, B["y1"]), lw="heavy"); c.line((0, 0), (0, B["y0"]), lw="heavy")
    # knee zone
    for k in D["knee"]:
        c.rect(k[0], k[2], k[1] - k[0], k[3] - k[2], lw="thin", dash="0.6 1.2")
    plan_items(c, I)
    # labels
    for n, x, y, *_ in D["legs"]:
        ptext(c, *c.P(x + 7, y + 0.5), n, size=3.2, weight="bold", anchor="start")
    for n, x, y, _ in D["feet"]:
        a = D["alex1"] if x > 100 else D["alex2"]
        cx, cy = a["x0"] + a["w"] / 2, a["y0"] + a["d"] / 2
        ptext(c, *c.P(x + math.copysign(7, cx - x), y + math.copysign(7, cy - y)), n, size=3.2, weight="bold")
    a1, a2 = D["alex1"], D["alex2"]
    ptext(c, *c.P(a1["x0"] + a1["w"] / 2, 32.5), "ALEX 1", size=3.2, weight="bold")
    ptext(c, *c.P(32, a2["y0"] + a2["d"] / 2), "ALEX 2", size=3.2, weight="bold")
    ptext(c, *c.P(120, 50.4), "rail A", size=3.2, weight="bold")
    ptext(c, *c.P(50.4, 210), "rail B", size=3.2, weight="bold", rotate=-90)
    ptext(c, *c.P(178, 38), "A", size=7, weight="bold"); ptext(c, *c.P(32, 160), "B", size=9, weight="bold")
    leader(c, (D["clamp"], 4.5), c.P(74, 26), "VIVO clamp 1 (x 40)", anchor="start")
    leader(c, (4.5, D["clamp"]), c.P(21, 24), "clamp 2 (y 40)", anchor="start")
    leader(c, (0, 0), c.P(4, 14), "datum 0,0", anchor="start")
    # seat
    a = c.P(97, 97); b = c.P(74, 74)
    pline(c, a, b, lw=0.8); c._head(a[0], a[1], b[0], b[1], 2.6)
    c.circle((101, 101), 9, lw="outline", dash="1.5 1")
    ptext(c, *c.P(101, 116), "seat, facing", size=3.2, weight="bold"); ptext(c, c.P(101, 116)[0], c.P(101, 116)[1] + 3.8, "the diagonal", size=3.2, weight="bold")
    # dimensions (mm)
    dim(c, (-g, -g), (A["x1"], -g), cm(A["x1"] + g), 12)        # 2520 floor incl. gap
    dim(c, (0, 0), (A["x1"], 0), cm(A["x1"]), 6.5)              # 2490
    dim(c, (-g, B["y1"]), (-g, -g), cm(B["y1"] + g), 13.5)      # 3170
    dim(c, (0, B["y1"]), (0, 0), cm(B["y1"]), 8)                # 3140
    dim(c, (A["x1"], 0), (A["x1"], A["y1"]), cm(A["y1"]), 6)    # 650 A
    dim(c, (B["x1"], B["y1"]), (0, B["y1"]), cm(B["x1"]), 6)    # 650 B
    dim(c, (B["x1"], B["y0"]), (B["x1"], B["y1"]), cm(B["y1"] - B["y0"]), 5)  # 2490 B
    dim(c, (180, D["railA"]["y1"]), (180, A["y1"]), "12", -4)            # rail A back from front edge
    dim(c, (D["railB"]["x1"], 150), (B["x1"], 150), "12", 4)              # rail B
    # wall gap callouts
    leader(c, (160, -g / 2), c.P(150, 27), "3 cm gap to the wall", anchor="start")
    leader(c, (-g / 2, 118), c.P(16, 128), "3 cm gap", anchor="start")
    # ALEX inset callout
    leader(c, (247.2, 40), c.P(256, 78), "3.5 cm all round", anchor="end")
    # datum
    dx, dy = c.P(0, 0)
    c.raw(f'<circle cx="{dx:.2f}" cy="{dy:.2f}" r="1.3" fill="#000"/>')
    # coordinate table in the open quadrant
    tx, ty = c.P(86, 150)
    rows = [("Leg", "x", "y")] + [(l[0], cm(l[1]), cm(l[2])) for l in D["legs"]]
    rows += [("Foot", "x", "y")] + [(f[0], cm(f[1]), cm(f[2])) for f in D["feet"]]
    col = [0, 20, 40]
    y = ty
    for i, r in enumerate(rows):
        bold = r[0] in ("Leg", "Foot")
        for j, v in enumerate(r):
            ptext(c, tx + (0, 27, 41)[j], y, v, size=3.2, anchor="start" if j == 0 else "end", weight="bold" if bold else "normal")
        y += 4.4
    t2 = tx + 50
    y2 = ty
    other = [("ALEX 1", f"x {cm(a1['x0'])}–{cm(a1['x0'] + a1['w'])}", f"y {cm(a1['y0'])}–{cm(a1['y0'] + a1['d'])}"),
             ("ALEX 2", f"x {cm(a2['x0'])}–{cm(a2['x0'] + a2['w'])}", f"y {cm(a2['y0'])}–{cm(a2['y0'] + a2['d'])}"),
             ("Rail A", f"x {cm(D['railA']['x0'])}–{cm(D['railA']['x1'])}", f"y {cm(D['railA']['y0'])}–{cm(D['railA']['y1'])}"),
             ("Rail B", f"x {cm(D['railB']['x0'])}–{cm(D['railB']['x1'])}", f"y {cm(D['railB']['y0'])}–{cm(D['railB']['y1'])}"),
             ("Clamp 1", f"x {cm(D['clamp'])}", "on A's back edge"),
             ("Clamp 2", f"y {cm(D['clamp'])}", "on A's left end")]
    for r in other:
        ptext(c, t2, y2, r[0], size=3.2, anchor="start", weight="bold"); y2 += 4.0
        ptext(c, t2 + 2, y2, r[1], size=3.2, anchor="start"); y2 += 4.0
        ptext(c, t2 + 2, y2, r[2], size=3.2, anchor="start"); y2 += 5.4
    ptext(c, tx, ty - 7, "Centres and extents, cm from the datum", size=3.2, anchor="start", weight="bold")
    # legend
    lx = tx
    ly = max(y, y2) + 1
    items = [("heavy", "unfinished edge, against the wall"), ("dash", "hidden: ALEX, leg plates, feet plates"), ("grey", "rail (steel angle)"), ("dark", "clamp zone C1 / C2, keep clear"), ("dot", "knee zone, keep clear")]
    for kind, txt in items:
        if kind == "heavy": pline(c, (lx, ly), (lx + 8, ly), lw=0.8)
        elif kind == "dash": pline(c, (lx, ly), (lx + 8, ly), lw=0.5, dash="1.6 0.9")
        elif kind == "grey": c.raw(f'<rect x="{lx:.2f}" y="{ly - 1.2:.2f}" width="8" height="2.4" fill="#d9d9d9" stroke="#000" stroke-width="0.25"/>')
        elif kind == "dark": c.raw(f'<rect x="{lx:.2f}" y="{ly - 1.2:.2f}" width="8" height="2.4" fill="#bfbfbf" stroke="#000" stroke-width="0.25"/>')
        else: pline(c, (lx, ly), (lx + 8, ly), lw=0.25, dash="0.6 1.2")
        ptext(c, lx + 10, ly, txt, size=3.2, anchor="start")
        ly += 4.6
    c.save(os.path.join(FIG, "01-plan.svg"))
    return c


if __name__ == "__main__":
    os.makedirs(FIG, exist_ok=True)
    fig_cover(); fig_iso_a(); fig_plan()
    print("figures_01: 3 figures")
