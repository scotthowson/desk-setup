#!/usr/bin/env python3
"""Chapter I figures (monitor mount and accessories) -> manual/figures/09-*.svg.
Every number comes from manual/data.json, manual/facts.json or docs/build-manual.md step 8."""
import json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.dirname(HERE)
sys.path.insert(0, MAN)
from lib.draw import Canvas, GREY, FONT, _f  # noqa: E402

D = json.load(open(os.path.join(MAN, "data.json")))
F = json.load(open(os.path.join(MAN, "facts.json")))
OUT = os.path.join(MAN, "figures")
V = F["vivo"]


def save(c, name):
    """Save, then make the hatch clip-path ids unique to this figure: lib.draw numbers them h<N> per canvas,
    and the builder inlines every SVG into one HTML page, where repeated ids clip the wrong figure."""
    path = c.save(os.path.join(OUT, name))
    tag = "f" + re.sub(r"[^a-z0-9]", "", name[:-4].lower())
    svg = open(path).read()
    svg = re.sub(r'id="h([0-9_]+)"', rf'id="{tag}h\1"', svg).replace("url(#h", f"url(#{tag}h")
    open(path, "w").write(svg)
    return path


def txt(c, p, s, size=3.2, anchor="middle", weight="normal", rotate=0, page=False):
    """Text; p in object coords, or page coords when page=True."""
    px, py = p if page else c.P(*p)
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    rot = f' transform="rotate({_f(rotate)} {_f(px)} {_f(py)})"' if rotate else ""
    c.raw(f'<text x="{_f(px)}" y="{_f(py)}" font-family="{FONT}" font-size="{size}" text-anchor="{anchor}" dominant-baseline="middle" font-weight="{weight}"{rot}>{s}</text>')


def lines(c, p, rows, size=3.2, anchor="start", lead=1.25, weight="normal"):
    px, py = c.P(*p)
    for i, s in enumerate(rows):
        txt(c, (px, py + i * size * lead), s, size, anchor, weight if i == 0 else "normal", page=True)


def dim(c, p1, p2, label, off, side=1, size=3.2, shift=0.0, gap=2.2):
    """Linear dimension (lib.draw.dim) with the label set beside the dimension line, outside it."""
    c.dim(p1, p2, "", offset=off, side=side, size=size)
    x1, y1 = c.P(*p1); x2, y2 = c.P(*p2)
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * side, dx / L * side
    mx, my = (x1 + x2) / 2 + nx * off, (y1 + y2) / 2 + ny * off
    tx, ty = mx + nx * gap + dx / L * shift, my + ny * gap + dy / L * shift
    ang = math.degrees(math.atan2(dy, dx))
    if ang > 90 or ang <= -90:
        ang += 180
    txt(c, (tx, ty), label, size, rotate=ang, page=True)


def pill(c, p, s, size=3.0, page=False):
    """Small boxed tag, e.g. MEASURE or ASSUMPTION, next to a dimension."""
    px, py = p if page else c.P(*p)
    w = len(s) * size * 0.62 + 2
    c.raw(f'<rect x="{_f(px - w / 2)}" y="{_f(py - size * 0.75)}" width="{_f(w)}" height="{_f(size * 1.5)}" rx="0.8" fill="#e6e6e6" stroke="#000" stroke-width="0.3"/>')
    txt(c, (px, py + 0.1), s, size, weight="bold", page=True)


def zig_h(c, x0, x1, y, n=2, a=12):
    """Break line drawn horizontally (object coords)."""
    pts, w = [(x0, y)], (x1 - x0)
    m = (x0 + x1) / 2
    pts += [(m - w * 0.06, y), (m - w * 0.02, y - a), (m + w * 0.02, y + a), (m + w * 0.06, y), (x1, y)]
    c.poly(pts, close=False, lw="thin")


def zig_v(c, x, y0, y1, a=12):
    h = y1 - y0; m = (y0 + y1) / 2
    c.poly([(x, y0), (x, m - h * 0.06), (x - a, m - h * 0.02), (x + a, m + h * 0.02), (x, m + h * 0.06), (x, y1)], close=False, lw="thin")


def datum(c, size=3.0):
    """Datum symbol at top A's back-left corner."""
    px, py = c.P(0, 0)
    c.raw(f'<circle cx="{_f(px)}" cy="{_f(py)}" r="1.1" fill="#000"/>')


# --------------------------------------------------------------------------------------------
def fig_clamp_plan():
    """I-1: plan of the corner from above: clamps, zones, pad plates (under the top, dashed), poles, crossbar."""
    s = 0.155
    x0, y0, x1, y1 = -215, -215, 850, 740
    c = Canvas((x1 - x0) * s, (y1 - y0) * s, scale=s, origin=(x0, y0))
    E, EY = 820, 720  # break lines in x and in y
    # walls
    for pts in ([(-55, -55), (E + 30, -55), (E + 30, -30), (-55, -30)], [(-55, -55), (-30, -55), (-30, EY + 20), (-55, EY + 20)]):
        c.poly(pts, fill="#fff", lw="thin"); c.hatch(pts, spacing=1.2)
    c.line((-30, -30), (E + 30, -30)); c.line((-30, -30), (-30, EY + 20))
    # tops (L, broken)
    c.poly([(0, EY), (0, 0), (E, 0)], close=False)
    c.poly([(E, 650), (650, 650), (650, EY)], close=False)
    zig_v(c, E, 0, 650, a=10); zig_h(c, 0, 650, EY, a=10)
    c.line((0, 650), (650, 650), lw="thin")
    # rails (hidden)
    rA, rB = F["layout_cm"]["rails"]["A"], F["layout_cm"]["rails"]["B"]
    c.rect(rA["x"][0] * 10, rA["y"][0] * 10, E - rA["x"][0] * 10, (rA["y"][1] - rA["y"][0]) * 10, lw="thin", dash="2 1")
    c.rect(rB["x"][0] * 10, rB["y"][0] * 10, (rB["x"][1] - rB["x"][0]) * 10, EY - rB["y"][0] * 10, lw="thin", dash="2 1")
    # legs (hidden plates)
    for n, x, y, *_ in D["legs"]:
        if x * 10 < E and y * 10 < E:
            c.circle((x * 10, y * 10), D["legPlate"] * 5, lw="thin", dash="2 1")
            c.centre_mark((x * 10, y * 10), 1.5)
            txt(c, (x * 10 + 62, y * 10 + 40), n, 3.2, anchor="start", weight="bold")
    # pad plates (hidden, under the top)
    for x0_, x1_, y0_, y1_ in D["pads"]:
        c.rect(x0_ * 10, y0_ * 10, (x1_ - x0_) * 10, (y1_ - y0_) * 10, fill=GREY["light"], lw="thin", dash="2 1")
    # clamp zones and clamp backs (in the wall gap), poles, crossbar
    zi = D["zoneIn"] * 10
    c.rect(360, 0, 80, zi, lw="outline", dash="0.8 0.8")
    c.rect(0, 360, zi, 80, lw="outline", dash="0.8 0.8")
    bk = V["clamp_back_behind_edge"]
    c.rect(360, -bk, 80, bk, fill=GREY["dark"], lw="thin")
    c.rect(-bk, 360, bk, 80, fill=GREY["dark"], lw="thin")
    pi = V["pole_centre_from_desk_edge"]; pr = V["pole_diameter"] / 2
    p1, p2 = (400, pi), (pi, 400)
    c.line(p1, p2, lw=1.6, color="#808080")
    for p in (p1, p2):
        c.circle(p, pr, fill="#fff"); c.centre_mark(p, 1.2)
    # dimensions
    dim(c, (0, -55), (400, -55), "40.0 cm  clamp 1 centre", 14, side=-1)
    dim(c, (360, -55), (440, -55), "8 cm", 6, side=-1, shift=10)
    dim(c, (-55, 0), (-55, 400), "40.0 cm  clamp 2 centre", 14, side=1)
    dim(c, (-55, 360), (-55, 440), "8 cm", 6, side=1, shift=-10)
    dim(c, (560, -30), (560, 0), "", 0)
    txt(c, (600, -15), "wall gap 3 cm", 3.0, anchor="start")
    # crossbar dimension along the diagonal, offset toward you
    dim(c, p1, p2, "crossbar 50.2 cm c–c", 8, side=-1)
    # labels (ordered top to bottom like their targets so leaders do not cross)
    datum(c)
    txt(c, (25, 30), "datum (0, 0)", 3.0, anchor="start")
    for ty, tgt, rows in ((175, (430, -8), ["clamp back, in the gap: 80 mm", "long, 17.5 mm behind the edge"]),
                          (255, (418, 52), ["pole ⌀35 mm, centre 43.7 mm", "in from the edge"]),
                          (335, (440, 85), ["clamp zone x 36–44 cm,", "dotted: keep clear"]),
                          (415, (448, 40), ["pad plate P11, under the top:", "x 20.0–45.4 cm, y 0.5–8.1 cm"])):
        c.leader(tgt, (478, ty), "", 3)
        lines(c, (482, ty), rows, 3.0)
    lines(c, (95, 562), ["pad plate P11:", "y 20.0–45.4 cm, x 0.5–8.1 cm"], 3.0)
    c.leader((40, 440), (92, 566), "", 3)
    txt(c, (790, 505), "rail A", 3.0, anchor="end")
    txt(c, (505, 700), "rail B", 3.0, rotate=-90)
    txt(c, (25, 682), "joint y = 65 cm", 3.0, anchor="start")
    txt(c, (690, 600), "TOP A  P01", 3.2, weight="bold")
    txt(c, (330, 688), "TOP B  P02", 3.2, weight="bold")
    return save(c, "09-clamp-plan.svg")


def fig_clamp_section():
    """I-2: section through clamp 1 at x = 400, looking along the back wall. Only measured values are dimensioned;
    the clamp body is a schematic C (dashed, grey) because its shape is not measured."""
    s = 0.58
    y0, z0, y1, z1 = -80, -78, 214, 122
    c = Canvas((y1 - y0) * s, (z1 - z0) * s, scale=s, origin=(y0, z0), flip_y=True)
    T = F["tops"]["thickness"]; pl = 3.0
    bk = V["clamp_back_behind_edge"]
    reach = 89; arm = 8; low = -pl - 4 - arm
    pi = V["pole_centre_from_desk_edge"]; pr = V["pole_diameter"] / 2
    # wall (broken top and bottom)
    w = [(-62, -22), (-30, -22), (-30, 100), (-62, 100)]
    c.poly(w, fill="#fff", lw="thin"); c.hatch(w, spacing=1.4); c.line((-30, -22), (-30, 100))
    txt(c, (-46, 108), "wall", 3.0)
    # clamp body: schematic C (phantom), drawn first so the top sits over it
    c.poly([(-bk, low), (-bk, T + arm), (reach, T + arm), (reach, T), (0, T), (0, -pl - 4), (70, -pl - 4), (70, low)],
           fill="#f2f2f2", lw="outline", dash="3 1.2")
    # lower pad (oval 90 x 50 seen edge-on): 13.5-63.5 from the edge
    c.rect(13.5, -pl - 4, 50, 4, fill=GREY["mid"], lw="thin")
    # top (section) and pad plate
    t = [(0, 0), (102, 0), (102, T), (0, T)]
    c.poly(t, fill="#fff"); c.hatch(t, spacing=1.6)
    zig_v(c, 102, -2, T + 2, a=3)
    c.rect(5, -pl, 76, pl, fill="#000", lw="thin")
    # pole, broken
    c.rect(pi - pr, T + arm, 2 * pr, 80 - T - arm, fill="#fff")
    c.raw(f'<rect x="{_f(c.P(pi - pr - 2, 86)[0])}" y="{_f(c.P(0, 86)[1])}" width="{_f((2 * pr + 4) * s)}" height="{_f(12 * s)}" fill="#fff"/>')
    zig_h(c, pi - pr - 3, pi + pr + 3, 80, a=3)
    c.centreline((pi, -29), (pi, 92))
    c.label_box((70, T / 2), "top A  P01", 3.0)
    # ---- measured dimensions ----
    dim(c, (102, 0), (102, T), "28", 4, side=1)
    dim(c, (-bk, 50), (0, 50), "17.5", 0, side=-1, gap=3.0)
    c.line((-bk, T + arm), (-bk, 53), lw="thin", dash="1 0.8")
    dim(c, (-30, 66), (0, 66), "3 cm", 0, side=-1, gap=3.0)
    txt(c, (-15, 80), "wall gap", 3.0)
    # each extension line stops at its own dimension level, so no label is crossed
    for x, ztop, zbot in ((0, -pl, -66), (5, -pl, -58), (13.5, -pl - 4, -42), (63.5, -pl - 4, -42), (81, -pl, -66)):
        c.line((x, ztop), (x, zbot), lw="thin", dash="1 0.8")
    dim(c, (0, -27), (pi, -27), "43.7", 0, side=1, gap=-3.0)
    dim(c, (13.5, -40), (63.5, -40), "pad 13.5–63.5", 0, side=1, gap=-3.0)
    dim(c, (0, -64), (81, -64), "plate 0.5–8.1 cm", 0, side=1, gap=-3.0)
    dim(c, (0, -56), (5, -56), "", 0)
    txt(c, (-3, -56), "0.5 cm", 3.0, anchor="end")
    # unverified: reach and opening
    c.line((0, T + arm), (0, 101), lw="thin", dash="1 0.8"); c.line((reach, T + arm), (reach, 101), lw="thin", dash="1 0.8")
    dim(c, (0, 98), (reach, 98), "reach about 89 mm", 0, side=-1, gap=3.0)
    pill(c, (44.5, 114), "ASSUMPTION · MEASURE")
    c.line((81, -pl), (136, -pl), lw="thin", dash="1 0.8"); c.line((102, T), (136, T), lw="thin", dash="1 0.8")
    dim(c, (134, -pl), (134, T), "31", 0, side=1, gap=-3.0)
    # labels
    lines(c, (92, 72), ["pole P12, ⌀35", "centre 43.7 from the edge"], 3.0)
    c.leader((pi + pr, 65), (90, 72), "", 3)
    lines(c, (-78, -32), ["clamp back", "behind the edge"], 3.0)
    c.leader((-bk + 3, -6), (-60, -30), "", 3)
    lines(c, (142, -12), ["plate P11, 3 mm (0.12 in)", "loose, no screws"], 3.0)
    c.leader((76, -1.5), (140, -11), "", 3)
    lines(c, (142, -30), ["lower pad, oval 90 × 50", "(seen edge-on)"], 3.0)
    c.leader((63.5, -5), (140, -29), "", 3)
    lines(c, (100, 50), ["clamp body: schematic", "(grey, dashed), not measured"], 3.0)
    pill(c, (170, -52), "MEASURE: opening ≥ 31 mm")
    return save(c, "09-clamp-section.svg")


def fig_heights():
    """I-3: heights above the top surface, viewed from the seat with the three screens unfolded flat.
    Heights to scale (guide.html tHeights, build manual step 8); widths schematic."""
    s = 0.133
    x0, z0, x1, z1 = -170, -110, 1110, 740
    c = Canvas((x1 - x0) * s, (z1 - z0) * s, scale=s, origin=(x0, z0), flip_y=True)
    tp = [(0, -28), (1000, -28), (1000, 0), (0, 0)]
    c.poly(tp, fill="#fff"); c.hatch(tp, spacing=1.2)
    c.rect(0, 400, 1000, 30, fill="none", lw="thin", dash="2 1")          # crossbar, behind
    acL, acR = (20, 260), (740, 980)
    for a, b in (acL, acR):
        c.rect(a, 260, b - a, 410, fill=GREY["light"])
        c.centreline((a - 10, 465), (b + 10, 465))
    c.rect(20, 0, 120, 234, fill=GREY["mid"]); c.rect(860, 0, 120, 234, fill=GREY["mid"])   # Edifiers, outer halves
    c.rect(380, 230, 240, 439, fill="#fff", lw="heavy")                  # G5
    c.rect(420, 0, 160, 100, fill=GREY["mid"])                            # ELLOVEN
    c.line((360, 673), (640, 673), lw="thin", dash="3 1")
    c.line((380, 120), (620, 120), lw="thin", dash="1 1")
    dim(c, (20, 0), (20, 234), "23.4", 4, side=-1)
    dim(c, (20, 0), (20, 260), "26", 12, side=-1)
    dim(c, (620, 0), (620, 230), "23", 4, side=1)
    dim(c, (620, 0), (620, 669), "66.9", 11, side=1)
    dim(c, (420, 0), (420, 100), "10", 4, side=-1)
    dim(c, (980, 0), (980, 465), "46.5", 5, side=1)
    txt(c, (140, 600), "Acer left P14", 3.0, weight="bold"); txt(c, (140, 300), "bottom 26 (109.0)", 3.0)
    txt(c, (860, 600), "Acer right P14", 3.0, weight="bold"); txt(c, (860, 300), "bottom 26 (109.0)", 3.0)
    txt(c, (500, 550), "G5 P13", 3.2, weight="bold")
    txt(c, (500, 630), "top 66.9 (149.9)", 3.0); txt(c, (500, 265), "bottom 23 (106.0)", 3.0)
    txt(c, (500, 50), "ELLOVEN P16", 3.0); txt(c, (500, 150), "lowest G5 bottom 12", 3.0)
    txt(c, (500, 705), "mount limit 67.3 (26.5 in)", 3.0)
    for x in (80, 920):
        txt(c, (x, 135), "Edifier", 3.0); txt(c, (x, 105), "P15", 3.0)
    txt(c, (500, 370), "crossbar 40–43", 3.0); txt(c, (500, 340), "(behind)", 3.0)
    txt(c, (500, -70), "top surface = 0 (83.0 from the floor)", 3.0)
    txt(c, (-155, 330), "cm above the top surface (cm from the floor)", 3.0, rotate=-90)
    return save(c, "09-heights.svg")


def fig_placement():
    """I-4: plan of everything on the desk (centres from build manual step 8)."""
    s = 0.040
    x0, y0, x1, y1 = -120, -120, 2620, 3220
    c = Canvas((x1 - x0) * s, (y1 - y0) * s, scale=s, origin=(x0, y0))
    c.poly([(0, 0), (2490, 0), (2490, 650), (650, 650), (650, 3140), (0, 3140)])
    c.line((0, 650), (650, 650), lw="thin")
    c.line((-30, -30), (2560, -30), lw="heavy"); c.line((-30, -30), (-30, 3200), lw="heavy")
    for a in ("alex1", "alex2"):
        A = F["layout_cm"][a]
        c.rect(A["x"][0] * 10, A["y"][0] * 10, (A["x"][1] - A["x"][0]) * 10, (A["y"][1] - A["y"][0]) * 10, lw="thin", dash="3 1.5")
    txt(c, (2275, 480), "ALEX 1", 3.0); txt(c, (325, 2810), "ALEX 2", 3.0)
    S = F["layout_cm"]["surface_items"]
    # poles and crossbar
    pi = V["pole_centre_from_desk_edge"]
    c.line((400, pi), (pi, 400), lw=0.8, color="#808080")
    for p in ((400, pi), (pi, 400)):
        c.circle(p, 30, fill="#000")
    # Y60 rectangle and mat
    y60 = S["Y60"]; c.rect(y60["x"][0] * 10, y60["y"][0] * 10, (y60["x"][1] - y60["x"][0]) * 10, (y60["y"][1] - y60["y"][0]) * 10, fill=GREY["light"])
    cx, cy = 550, 550; a = math.radians(45)
    hw, hd = 400, 150  # mat 800 x 300, long side across the diagonal
    ux, uy = math.cos(a), -math.sin(a); vx, vy = math.sin(a), math.cos(a)
    c.poly([(cx + ux * hw * sx + vx * hd * sy, cy + uy * hw * sx + vy * hd * sy) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))], fill=GREY["light"], lw="thin")
    pts = {
        "G5": S["G5"], "ELLOVEN": S["ELLOVEN"], "keyboard": S["keyboard"], "mouse": S["mouse"], "lamp": S["lamp"],
        "headset": S["headset"], "plant": S["plant"], "acerR": S["acer_right"], "acerL": S["acer_left"], "edR": S["edifiers"][0], "edL": S["edifiers"][1],
    }
    for k, (x, y) in pts.items():
        c.circle((x * 10, y * 10), 22, fill="#000" if k in ("G5", "acerR", "acerL") else "#fff", lw="thin")
    # numbers beside the centres; the key sits in the open area right of top B
    num = {"G5": ("1 2", (330, 300), "end"), "keyboard": ("3", (640, 600), "start"), "mouse": ("4", (790, 450), "start"),
           "acerR": ("5", (990, 100), "middle"), "edR": ("7", (1130, 250), "start"), "acerL": ("6", (130, 990), "end"),
           "edL": ("8", (270, 1090), "start"), "lamp": ("9", (1880, 200), "start"), "headset": ("10", (330, 1400), "start"),
           "plant": ("11", (370, 2980), "start")}
    for k, (n, p, anc) in num.items():
        txt(c, p, n, 3.2, anchor=anc, weight="bold")
    key = ["all cm from the datum", "1  G5 P13 (36.5, 36.5)", "2  ELLOVEN P16 (36, 36)", "3  keyboard (58.5, 58.5)", "4  mouse (74, 45)",
           "5  Acer P14 (99, 19)", "6  Acer P14 (19, 99)", "7  Edifier P15 (108, 22)", "8  Edifier P15 (22, 108)",
           "9  lamp (183, 20)", "10  headset (28, 140)", "11  plant (32, 298)", "",
           "grey 45°: mat 80 × 30 at (55, 55)", "black: VIVO poles and crossbar P12", "datum (0, 0): top A back-left corner"]
    lines(c, (950, 1200), key, 3.0, lead=1.35)
    txt(c, (2200, 140), "Y60 P17", 3.0)
    c.arrow((920, 920), (710, 710), lw="outline", head=2.2)
    lines(c, (950, 960), ["seat: facing the corner"], 3.0)
    datum(c)
    return save(c, "09-placement.svg")


if __name__ == "__main__":
    for f in (fig_clamp_plan, fig_clamp_section, fig_heights, fig_placement):
        print(f())
