#!/usr/bin/env python3
"""Chapter B figures: safety pictograms, floor area, workshop tools, printed-tool icons (drawn by figures_03)."""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.dirname(HERE)
sys.path.insert(0, MAN); sys.path.insert(0, HERE)
from lib.draw import Canvas, GREY, _f  # noqa: E402
from figures_04 import hatch_rect, dim2, lead  # noqa: E402
from figures_03 import TOOL_ICONS, tool_icon_svg  # noqa: E402

F = json.load(open(os.path.join(MAN, "facts.json")))
FIG = os.path.join(MAN, "figures")


def person(c, x, y, s=1.0, arms_up=True):
    """Stick figure standing at (x, y) = feet, height about 22*s."""
    c.circle((x, y - 20 * s), 2.2 * s, fill="#fff", lw="outline")
    c.line((x, y - 17.8 * s), (x, y - 8 * s), lw=0.8)
    c.line((x, y - 8 * s), (x - 3 * s, y), lw=0.8); c.line((x, y - 8 * s), (x + 3 * s, y), lw=0.8)
    if arms_up:
        c.line((x, y - 15 * s), (x - 3.5 * s, y - 19.5 * s), lw=0.8); c.line((x, y - 15 * s), (x + 3.5 * s, y - 19.5 * s), lw=0.8)


def no_sign(c, x, y, r):
    c.circle((x, y), r, lw=1.0)
    c.line((x - r * 0.7, y - r * 0.7), (x + r * 0.7, y + r * 0.7), lw=1.0)


def fig_safety():
    W, H = 178, 44
    c = Canvas(W, H)
    pw = 35.6
    caps = [("21 mm deep at most", "into the 28 mm top"), ("tops face down", "on a blanket"), ("never drag steel", "across the laminate"),
            ("two people to stand", "a top up"), ("eye protection: steel;", "gloves: deburring")]
    for i, (a, b) in enumerate(caps):
        x0 = i * pw
        c.rect(x0 + 0.5, 0.5, pw - 1, H - 1, lw="thin")
        c.text((x0 + pw / 2, H - 7.2), a, size=3.0, weight="bold")
        c.text((x0 + pw / 2, H - 3.4), b, size=3.0)
    # 1 depth rule
    x0 = 0
    c.rect(x0 + 5, 8, 26, 14, fill=GREY["wood"], lw="outline"); c.rect(x0 + 5, 21.2, 26, 0.8, fill="#000", lw="thin")
    c.line((x0 + 3, 8 + 10.5), (x0 + 33, 8 + 10.5), lw=0.5, dash="1.5 0.7")
    c.poly([(x0 + 17, 6), (x0 + 19, 6), (x0 + 19, 16.5), (x0 + 18, 18.3), (x0 + 17, 16.5)], fill="#fff", lw="outline")
    c.rect(x0 + 15, 5, 6, 1.2, fill="#000", lw="thin")
    c.text((x0 + 26, 15.6), "21", size=3.0, weight="bold")
    c.text((x0 + 9, 15.6), "28", size=3.0)
    # 2 face down on a blanket
    x0 = pw
    c.raw(f'<path d="M {_f(x0 + 3)} 24 q 4 -2 8 0 t 8 0 t 8 0 t 8 0" fill="none" stroke="#000" stroke-width="0.5"/>')
    c.rect(x0 + 4, 18, 28, 4, fill=GREY["wood"], lw="outline"); c.rect(x0 + 4, 21.3, 28, 0.7, fill="#000", lw="thin")
    c.text((x0 + 18, 13), "laminate down", size=3.0)
    c.arrow((x0 + 18, 15), (x0 + 18, 20.5), lw="thin", head=1.3)
    # 3 no dragging steel
    x0 = 2 * pw
    c.rect(x0 + 3, 20, 30, 3, fill=GREY["wood"], lw="outline")
    c.poly([(x0 + 8, 16), (x0 + 22, 16), (x0 + 22, 17.2), (x0 + 9.2, 17.2), (x0 + 9.2, 20), (x0 + 8, 20)], fill=GREY["dark"], lw="outline")
    c.arrow((x0 + 12, 13), (x0 + 28, 13), lw="outline", head=1.6)
    no_sign(c, x0 + 18, 15, 9)
    # 4 two people
    x0 = 3 * pw
    person(c, x0 + 7, 28, 0.95); person(c, x0 + 29, 28, 0.95)
    c.rect(x0 + 3, 7, 30, 2.2, fill=GREY["wood"], lw="outline")
    # 5 goggles and glove
    x0 = 4 * pw
    c.raw(f'<path d="M {_f(x0 + 4)} 12 h 12 q 2 0 2 3 v 2 q 0 3 -3 3 h -2 q -2 0 -3 -2 q -1 2 -3 2 h -2 q -3 0 -3 -3 v -2 q 0 -3 2 -3 z" fill="#fff" stroke="#000" stroke-width="0.6"/>')
    c.line((x0 + 2, 15), (x0 + 4, 14), lw=0.6); c.line((x0 + 18, 14), (x0 + 20, 15), lw=0.6)
    c.raw(f'<path d="M {_f(x0 + 23)} 26 v -9 q 0 -2 1.5 -2 q 1.5 0 1.5 2 v -4 q 0 -2 1.5 -2 q 1.5 0 1.5 2 v 1 q 0 -2 1.5 -2 q 1.5 0 1.5 2 v 6 l 2 -2 q 1.5 -1 2 1 l -3 6 q -1 2 -3 2 h -5 q -2 0 -2 -2 z" fill="{GREY["light"]}" stroke="#000" stroke-width="0.5"/>')
    return c.save(os.path.join(FIG, "02-safety.svg"))


def fig_floor():
    s = 1 / 40.0
    W, H = 96, 106
    c = Canvas(W, H)
    ox, oy = 16, 14
    P = lambda x, y: (ox + x * s, oy + y * s)
    g = F["layout_cm"]["wall_gap"] * 10
    # the floor needed: walls at x = -30, y = -30; desk to x 2490, y 3140 -> 2520 x 3170
    c.rect(P(-g, -g)[0], P(-g, -g)[1], 2520 * s, 650 * s + g * s, fill="none", lw="thin", dash="1.5 0.8")
    c.rect(P(-g, -g)[0], P(-g, -g)[1], 650 * s + g * s, 3170 * s, fill="none", lw="thin", dash="1.5 0.8")
    c.poly([P(0, 0), P(2490, 0), P(2490, 650), P(650, 650), P(650, 3140), P(0, 3140)], fill=GREY["wood"], lw="outline")
    wu, wv = P(-g, -g)
    c.line((wu, wv), (P(2490, 0)[0] + 4, wv), lw="heavy"); c.line((wu, wv), (wu, P(0, 3140)[1] + 4), lw="heavy")
    hatch_rect(c, wu, wv - 2, P(2490, 0)[0] + 4, wv, spacing=1.1); hatch_rect(c, wu - 2, wv, wu, P(0, 3140)[1] + 4, spacing=1.1)
    dim2(c, (wu, wv), (P(2490, 0)[0], wv), "252 cm", off=5)
    dim2(c, (wu, P(0, 3140)[1]), (wu, wv), "317 cm", off=5)
    c.text((P(1500, 330)[0], P(0, 330)[1]), "desk", size=3.0)
    c.text((P(1500, 0)[0], P(0, 0)[1] + 9), "", size=3.0)
    lead(c, P(-15, 1000), (P(900, 1000)[0], P(0, 1000)[1]), "3 cm wall gap", size=3.0)
    # bench for the steel, outside the footprint
    bx, by = P(1150, 2000)
    c.rect(bx, by, 26, 9, fill=GREY["light"], lw="outline")
    c.rect(bx + 1, by + 3.4, 24, 1.2, fill=GREY["dark"], lw="thin")
    c.text((bx + 13, by + 14), "bench for the steel", size=3.0)
    c.text((bx + 13, by + 18), "(rails 213 cm long)", size=3.0)
    c.text((W / 2, H - 1.5), "Plan, 1:40. Both walls MEASURE.", size=3.0)
    return c.save(os.path.join(FIG, "02-floor.svg"))


# workshop tool icons --------------------------------------------------------------------------------
def i_drill(c, x, y):
    c.rect(x + 2, y + 4, 12, 6, fill=GREY["light"], lw="outline"); c.rect(x + 14, y + 5.5, 3, 3, fill=GREY["mid"], lw="thin")
    c.line((x + 17, y + 7), (x + 21, y + 7), lw=0.6); c.poly([(x + 5, y + 10), (x + 9, y + 10), (x + 8, y + 18), (x + 4, y + 18)], fill=GREY["light"], lw="outline")


def i_bits(c, x, y):
    for k, l in enumerate((10, 13, 15, 17)):
        u = x + 3 + k * 4.5
        c.line((u, y + 2), (u, y + 2 + l), lw=0.4 + k * 0.25)


def i_punch(c, x, y):
    c.poly([(x + 9, y + 1), (x + 13, y + 1), (x + 13, y + 13), (x + 11, y + 18), (x + 9, y + 13)], fill=GREY["light"], lw="outline")


def i_oil(c, x, y):
    c.rect(x + 5, y + 8, 10, 10, fill=GREY["light"], lw="outline"); c.poly([(x + 9, y + 8), (x + 11, y + 8), (x + 17, y + 2), (x + 16, y + 1.5)], fill=GREY["mid"], lw="thin")


def i_file(c, x, y):
    c.rect(x + 2, y + 8, 14, 3, fill=GREY["light"], lw="outline"); c.rect(x + 16, y + 8.7, 5, 1.6, fill=GREY["dark"], lw="thin")
    for k in range(6):
        c.line((x + 3 + k * 2.2, y + 8), (x + 4.2 + k * 2.2, y + 11), lw=0.2)


def i_paper(c, x, y):
    c.rect(x + 4, y + 4, 13, 12, fill=GREY["light"], lw="outline"); c.text((x + 10.5, y + 10), "120", size=3.0)


def i_can(c, x, y, t):
    c.rect(x + 5, y + 4, 11, 14, fill=GREY["light"], lw="outline"); c.rect(x + 7, y + 2, 7, 2, fill=GREY["mid"], lw="thin")
    c.text((x + 10.5, y + 11.5), t, size=3.0, weight="bold")


def i_robertson(c, x, y):
    c.rect(x + 2, y + 8, 14, 3, fill=GREY["light"], lw="outline"); c.rect(x + 16, y + 8.6, 4, 1.8, fill=GREY["dark"], lw="thin")
    c.rect(x + 21, y + 7.5, 2, 4, fill="#000", lw="thin")


def i_wrench(c, x, y):
    for d in (0, 6):
        c.line((x + 3, y + 15 - d), (x + 16, y + 4 - d + 2), lw=1.6)
        c.circle((x + 17, y + 5 - d + 1), 2.2, fill="#fff", lw="outline")


def i_clamp(c, x, y):
    c.poly([(x + 3, y + 2), (x + 17, y + 2), (x + 17, y + 4), (x + 5, y + 4), (x + 5, y + 16), (x + 3, y + 16)], fill=GREY["mid"], lw="outline")
    c.rect(x + 5, y + 13, 10, 2, fill=GREY["mid"], lw="outline"); c.line((x + 12, y + 4), (x + 12, y + 13), lw=0.8)


def i_tape(c, x, y):
    c.rect(x + 3, y + 4, 12, 12, fill=GREY["light"], lw="outline", rx=2); c.rect(x + 15, y + 13, 6, 2, fill=GREY["mid"], lw="thin")


def i_square(c, x, y):
    c.rect(x + 3, y + 6, 6, 4, fill=GREY["mid"], lw="outline"); c.rect(x + 9, y + 7, 12, 2, fill=GREY["light"], lw="outline")


def i_level(c, x, y):
    c.rect(x + 1, y + 8, 21, 4, fill=GREY["light"], lw="outline"); c.rect(x + 9, y + 8.8, 5, 2.4, fill="#fff", lw="thin")


def i_calipers(c, x, y):
    c.rect(x + 2, y + 7, 19, 2.4, fill=GREY["light"], lw="outline")
    c.poly([(x + 3, y + 9.4), (x + 5, y + 9.4), (x + 5, y + 17), (x + 3, y + 15)], fill=GREY["mid"], lw="thin")
    c.poly([(x + 10, y + 9.4), (x + 12, y + 9.4), (x + 12, y + 15), (x + 10, y + 17)], fill=GREY["mid"], lw="thin")


def i_goggles(c, x, y):
    c.raw(f'<path d="M {_f(x + 4)} {_f(y + 7)} h 14 q 2 0 2 3 v 2 q 0 3 -3 3 h -3 q -2 0 -3 -2 q -1 2 -3 2 h -3 q -3 0 -3 -3 v -2 q 0 -3 2 -3 z" fill="#fff" stroke="#000" stroke-width="0.6"/>')


def i_gloves(c, x, y):
    c.raw(f'<path d="M {_f(x + 6)} {_f(y + 18)} v -9 q 0 -2 1.5 -2 q 1.5 0 1.5 2 v -4 q 0 -2 1.5 -2 q 1.5 0 1.5 2 v 1 q 0 -2 1.5 -2 q 1.5 0 1.5 2 v 6 l 2 -2 q 1.5 -1 2 1 l -3 6 q -1 2 -3 2 h -5 q -2 0 -2 -2 z" fill="{GREY["light"]}" stroke="#000" stroke-width="0.5"/>')


WORKSHOP = [
    ("drill, clutch", i_drill), ("bits 5/64 1/8 7/32 7/16", i_bits), ("centre punch", i_punch), ("cutting oil", i_oil), ("flat + round file", i_file),
    ("120 grit", i_paper), ("acetone", lambda c, x, y: i_can(c, x, y, "AC")), ("flat black enamel", lambda c, x, y: i_can(c, x, y, "BK")),
    ("Robertson #2 + 3 in ext.", i_robertson), ("two wrenches", i_wrench), ("two clamps", i_clamp), ("tape measure", i_tape),
    ("combination square", i_square), ("spirit level", i_level), ("calipers", i_calipers), ("eye protection", i_goggles), ("gloves", i_gloves),
]


def fig_workshop():
    cols, cw, ch = 6, 178 / 6, 31
    rows = math.ceil(len(WORKSHOP) / cols)
    c = Canvas(178, rows * ch)
    for i, (lab, fn) in enumerate(WORKSHOP):
        r, k = divmod(i, cols)
        x, y = k * cw, r * ch
        c.rect(x + 0.4, y + 0.4, cw - 0.8, ch - 0.8, lw="thin")
        fn(c, x + (cw - 23) / 2, y + 2)
        parts = lab.split(" ", 2) if len(lab) > 16 else [lab]
        if len(parts) == 3:
            parts = [" ".join(parts[:2]), parts[2]]
        for j, t in enumerate(parts):
            c.text((x + cw / 2, y + 23.4 + j * 3.6), t, size=3.0)
    return c.save(os.path.join(FIG, "02-workshop.svg"))


# ---------------------------------------------------------------- printed tools in use (Figs B-4 to B-13)
UW = 86


def wood(c, x, y, w, h):
    c.rect(x, y, w, h, fill=GREY["wood"], lw="outline")


def hole(c, p, r, fill="#fff", lw="thin", ring=False):
    c.circle(p, r, fill=fill, lw=lw)
    if ring:
        c.circle(p, r + 0.9, lw=0.2)


def drill_arrow(c, p, length=7):
    c.arrow((p[0] + length * 0.6, p[1] - length), p, lw="outline", head=1.6)


def use_tsquare():
    c = Canvas(UW, 76)
    k = 0.34
    ey = 12                                    # the top's edge (face down), top region below
    wood(c, 2, ey, 82, 62)
    c.line((2, ey), (84, ey), lw="heavy")
    hx = 20                                    # head 110 along the edge
    c.rect(hx, ey - 3, 110 * k, 3, fill=GREY["mid"], lw="outline")      # lip over the edge
    bx = hx + 110 * k / 2
    bw = 60 * k
    c.rect(bx - bw / 2, ey, bw, 162 * k, fill=GREY["light"], lw="outline")
    for d in (50, 85, 100, 150):
        hole(c, (bx, ey + d * k), 0.7, fill="#000" if d == 100 else "#fff")
    for sx in (-1, 1):
        for sy in (-1, 1):
            hole(c, (bx + sx * 23.4 * k, ey + (85 + sy * 23.4) * k), 0.8)
    for d, t in ((50, "50"), (85, "85"), (100, "100"), (150, "150")):
        c.text((bx + bw / 2 + 1.2, ey + d * k), t, size=3.0, anchor="start")
    c.line((bx, ey - 6), (bx, ey + 1.5), lw="thin", dash="1.5 0.6")
    c.text((bx, ey - 7.8), "station (tape)", size=3.0)
    dim2(c, (bx - bw / 2 - 3, ey), (bx - bw / 2 - 3, ey + 100 * k), "10 cm", off=-0.01)
    lead(c, (bx + 23.4 * k, ey + (85 - 23.4) * k), (bx + bw / 2 + 9, ey + 22), "85 pad: four 1/8 in", size=3.0)
    c.text((bx + bw / 2 + 10, ey + 25.6), "feet-plate holes", size=3.0, anchor="start")
    lead(c, (bx, ey + 100 * k), (bx - bw / 2 - 9, ey + 48), "scriber", size=3.0)
    c.text((4, 71.5), "face-down top", size=3.0, anchor="start")
    c.text((hx + 110 * k + 1.5, ey - 1.5), "lip", size=3.0, anchor="start")
    return c.save(os.path.join(FIG, "02-use-tsquare.svg"))


def leg_pattern(c, cx, cy, k, rot, dashed):
    c.circle((cx, cy), 52.5 * k, lw="outline" if not dashed else 0.4, dash="1.4 0.8" if dashed else None)
    c.circle((cx, cy), 0.5, fill="#000", lw="thin")
    for i in range(5):
        a = math.radians(rot + i * 72)
        hole(c, (cx + 42.5 * k * math.cos(a), cy + 42.5 * k * math.sin(a)), 0.8, ring=dashed)


def use_legjig():
    c = Canvas(UW, 62)
    k = 0.3
    ex = 12
    wood(c, ex, 4, 72, 46)
    hatch_rect(c, 2, 4, 6, 50, spacing=1.2); c.line((6, 4), (6, 50), lw="heavy")
    c.text((4, 54.5), "wall", size=3.0)
    c.line((ex, 4), (ex, 50), lw="heavy")
    jy = 27 - 110 * k / 2
    c.rect(ex - 2, jy, 2, 110 * k, fill=GREY["mid"], lw="outline")      # lip on the wall edge
    c.rect(ex, jy, 205 * k, 110 * k, fill=GREY["light"], lw="outline")
    c.line((ex - 5, 27), (ex + 3, 27), lw=0.4, dash="1.2 0.6")
    leg_pattern(c, ex + 100 * k, 27, k, 180, False)
    leg_pattern(c, ex + 150 * k, 27, k, 0, True)
    c.text((ex + 100 * k, 54.5), "100: L2-L6", size=3.0)
    c.text((ex + 150 * k + 12, 54.5), "150: L1", size=3.0)
    c.text((ex + 1, 58.5), "unfinished (wall) edge; dashed tick: station", size=3.0, anchor="start")
    c.line((ex + 100 * k, 50), (ex + 100 * k, 52), lw="thin"); c.line((ex + 150 * k, 50), (ex + 150 * k + 6, 52), lw="thin")
    return c.save(os.path.join(FIG, "02-use-legjig.svg"))


def use_cornerjig():
    c = Canvas(UW, 64)
    k = 0.36
    # a far corner of a face-down top: edges along the top and the right of the drawing
    rx, ty = 70, 12
    wood(c, 4, ty, rx - 4, 54)
    c.line((4, ty), (rx, ty), lw="heavy"); c.line((rx, ty), (rx, 62), lw="heavy")
    js = 130 * k
    c.rect(rx - js, ty, js, js, fill=GREY["light"], lw="outline")
    c.rect(rx - js, ty - 2, js + 2, 2, fill=GREY["mid"], lw="outline"); c.rect(rx, ty - 2, 2, js + 2, fill=GREY["mid"], lw="outline")
    fx, fy = rx - 85 * k, ty + 85 * k
    c.rect(fx - 29.75 * k, fy - 29.75 * k, 59.5 * k, 59.5 * k, lw=0.25, dash="1.2 0.7")
    c.circle((fx, fy), 0.5, fill="#000", lw="thin")
    for sx in (-1, 1):
        for sy in (-1, 1):
            hole(c, (fx + sx * 23.4 * k, fy + sy * 23.4 * k), 0.8)
    dim2(c, (fx, ty), (rx, ty), "8.5 cm", off=5.5)
    dim2(c, (rx, ty), (rx, fy), "8.5 cm", off=-6)
    c.text((fx, fy + 14), "plate outline", size=3.0)
    return c.save(os.path.join(FIG, "02-use-cornerjig.svg"))


def use_alexcorner():
    c = Canvas(UW, 66)
    k = 0.45
    rx, ty = 54, 12
    c.rect(4, ty, rx - 4, 52, fill=GREY["light"], lw="outline")
    c.line((4, ty), (rx, ty), lw="heavy"); c.line((rx, ty), (rx, 64), lw="heavy")
    c.text((6, 61.5), "ALEX top", size=3.0, anchor="start")
    js = 100 * k
    c.rect(rx - js, ty, js, js, fill="#fff", lw="outline")
    c.rect(rx - js, ty - 2, js + 2, 2, fill=GREY["mid"], lw="outline"); c.rect(rx, ty - 2, 2, js + 2, fill=GREY["mid"], lw="outline")
    cx, cy = rx - 50 * k, ty + 50 * k
    c.circle((cx, cy), 75 * k / 2, lw=0.25, dash="1.2 0.7")
    c.circle((cx, cy), 0.5, fill="#000", lw="thin")
    for a in (90, 210, 330):
        r = math.radians(a)
        hole(c, (cx + 33 * k * math.cos(r), cy - 33 * k * math.sin(r)), 1.0, fill="#000")
    for a in (45, 165, 285):
        r = math.radians(a)
        hole(c, (cx + 14.5 * k * math.cos(r), cy - 14.5 * k * math.sin(r)), 0.9)
    dim2(c, (cx, ty), (rx, ty), "5 cm", off=5.5)
    dim2(c, (rx, ty), (rx, cy), "5 cm", off=-6)
    lead(c, (cx + 33 * k * math.cos(math.radians(330)), cy - 33 * k * math.sin(math.radians(330))), (rx + 6, 40), "outer 3:", size=3.0)
    c.text((rx + 7, 43.7), "drill, 5/64", size=3.0, anchor="start")
    lead(c, (cx + 14.5 * k * math.cos(math.radians(285)), cy - 14.5 * k * math.sin(math.radians(285))), (rx + 6, 52), "inner 3:", size=3.0)
    c.text((rx + 7, 55.7), "ALEX feet only", size=3.0, anchor="start")
    return c.save(os.path.join(FIG, "02-use-alexcorner.svg"))


def use_railgauge():
    c = Canvas(UW, 66)
    k = 0.85
    hx, hy = 22, 16                                   # heel (outer corner) of the angle, section
    a, t = 50.8 * k, 4.76 * k
    c.poly([(hx, hy), (hx + a, hy), (hx + a, hy + t), (hx + t, hy + t), (hx + t, hy + a), (hx, hy + a)], fill=GREY["dark"], lw="outline")
    # gauge 1 on the flat leg, lip over its free edge (right)
    gy = hy - 3
    c.rect(hx + a - 34, gy, 34, 3, fill=GREY["light"], lw="outline")
    c.rect(hx + a, gy, 2.4, 3 + t + 1.5, fill=GREY["light"], lw="outline")
    px = hx + a - 19 * k
    c.poly([(px - 1, gy - 4), (px + 1, gy - 4), (px, gy)], fill="#000", lw="thin")
    dim2(c, (px, gy - 5), (hx + a, gy - 5), "19 mm", off=1.2)
    c.text((hx + a + 4, gy + 6), "free edge", size=3.0, anchor="start")
    # gauge 2 on the vertical leg's outer face (left), lip over the heel edge (top)
    gx = hx - 3
    c.rect(gx, hy, 3, 40, fill=GREY["light"], lw="outline")
    c.rect(gx, hy - 2.4, 3, 2.4, fill=GREY["light"], lw="outline")
    py = hy + 29 * k
    c.poly([(gx - 4, py - 1), (gx - 4, py + 1), (gx, py)], fill="#000", lw="thin")
    dim2(c, (gx - 5, hy), (gx - 5, py), "29 mm", off=-0.01)
    c.text((hx + 8, hy + 30), "screw line: 19 mm in", size=3.0, anchor="start")
    c.text((hx + 8, hy + 33.8), "from the flat leg's free edge", size=3.0, anchor="start")
    c.text((hx + 8, hy + 40), "bolt line: 29 mm down", size=3.0, anchor="start")
    c.text((hx + 8, hy + 43.8), "from the heel edge", size=3.0, anchor="start")
    c.text((hx, 64.5), "angle end-on; gauges grey, pencil black", size=3.0, anchor="start")
    return c.save(os.path.join(FIG, "02-use-railgauge.svg"))


def use_raildrill():
    c = Canvas(UW, 60)
    k = 0.85
    y0 = 6
    c.rect(2, y0, 82, 50.8 * k, fill=GREY["steel"], lw="outline")
    c.line((2, y0), (84, y0), lw="heavy")
    c.text((4, y0 + 3.5), "heel", size=3.0, anchor="start")
    fe = y0 + 50.8 * k
    c.text((58, fe + 4.2), "free edge", size=3.0, anchor="start")
    sx = 44
    c.line((sx, y0), (sx, fe + 4), lw=0.4, dash="2 0.8")
    c.text((sx + 1, y0 + 3.5), "station line", size=3.0, anchor="start")
    jw, jh = 28 * k, 24 * k
    c.rect(sx - jw / 2, fe - jh, jw, jh, fill=GREY["light"], lw="outline")
    c.rect(sx - jw / 2, fe, jw, 2.6, fill=GREY["mid"], lw="outline")
    c.line((sx, fe - jh - 1.5), (sx, fe - jh + 2), lw=0.6); c.line((sx, fe - 2), (sx, fe + 1), lw=0.6)
    bp = (sx, fe - 19 * k)
    hole(c, bp, 1.6)
    dim2(c, (sx + jw / 2 + 3, fe), (sx + jw / 2 + 3, fe - 19 * k), "19 mm", off=-0.01)
    lead(c, (sx, fe - jh - 0.8), (sx - 18, y0 + 12), "sight grooves", size=3.0)
    return c.save(os.path.join(FIG, "02-use-raildrill.svg"))


def use_slotplug():
    c = Canvas(UW, 54)
    k = 0.7
    x0, y0 = 6, 10
    c.rect(2, y0 - 6, 80, 6 + 41 * k + 8, fill=GREY["steel"], lw="thin")
    c.text((4, y0 + 41 * k + 5.5), "rail's vertical leg", size=3.0, anchor="start")
    c.rect(x0, y0, 100.5 * k, 41 * k, fill=GREY["light"], lw="outline")
    c.line((x0, y0), (x0, y0 + 41 * k), lw="heavy")
    c.line((x0, y0 - 5), (x0, y0), lw=0.5)
    c.text((x0 + 1, y0 - 2.5), "heel on the mark", size=3.0, anchor="start")
    for n, sc in enumerate((29.15, 78.45)):
        cx, cy = x0 + sc * k, y0 + 41 * k / 2
        c.rect(cx - 10.5 * k, cy - 6 * k, 21 * k, 12 * k, fill=GREY["mid"] if n == 0 else "#fff", lw="outline", rx=6 * k)
        if n == 0:
            hole(c, (cx, cy), 1.6)
    lead(c, (x0 + 29.15 * k, y0 + 41 * k / 2 + 1.6), (x0 + 40 * k, y0 + 41 * k + 12), "plug: 1/8 in bore on the slot centre", size=3.0)
    c.text((x0 + 78.45 * k, y0 + 41 * k / 2 - 6), "next", size=3.0)
    return c.save(os.path.join(FIG, "02-use-slotplug.svg"))


def use_guide():
    c = Canvas(UW, 74)
    k = 0.5
    # (a) SET tower: block with a blind hole 45 deep, bit tip-first inside, chuck nose on top
    tx, base = 6, 56
    th = 60 * k
    c.rect(tx, base - th, 16, th, fill=GREY["light"], lw="outline")
    c.rect(tx + 6.5, base - th, 3, 45 * k, fill="#fff", lw="thin")
    c.line((tx + 8, base - th - 12), (tx + 8, base - th + 45 * k), lw=0.8)
    c.rect(tx + 3, base - th - 12, 10, 12, fill=GREY["mid"], lw="outline")
    dim2(c, (tx + 18, base - th + 45 * k), (tx + 18, base - th), "45 mm", off=-0.01)
    c.text((tx + 8, base + 4), "(a) SET", size=3.0, weight="bold")
    c.text((tx + 8, base + 7.8), "1/8: 45, 5/64: 35", size=3.0)
    # (b) puck on the surface
    px = 36
    c.rect(px - 6, base, 26, 10, fill=GREY["wood"], lw="outline")
    ph = 20 * k
    c.rect(px, base - ph, 14, ph, fill=GREY["light"], lw="outline")
    c.rect(px + 5.5, base - ph, 3, ph, fill="#fff", lw="thin")
    c.rect(px + 2, base - ph - 12, 10, 12, fill=GREY["mid"], lw="outline")
    c.line((px + 7, base - ph), (px + 7, base + 6), lw=0.8)
    c.rect(px + 6.2, base, 1.6, 6, fill="#fff", lw=0.2, dash="0.6 0.4")
    lead(c, (px + 7.8, base + 6), (px + 24, base + 6), "depth of the puck", size=3.0)
    lead(c, (px + 12, base - ph - 1), (px + 18, base - ph - 8), "chuck nose stops", size=3.0)
    c.text((px + 7, 72.5), "(b) drill through the puck", size=3.0, weight="bold")
    return c.save(os.path.join(FIG, "02-use-guide.svg"))


def use_height():
    """Schematic: the C gauge round a foot, inner faces on the plate face and the pad's bottom."""
    c = Canvas(UW, 70)
    k = 0.5
    base = 60                                  # inner face of the lower jaw = bottom of the pad
    cx = 26
    top = base - 102 * k                       # inner face of the upper jaw = plate face
    c.rect(cx - 25 * k, base - 16 * k, 50 * k, 16 * k, fill=GREY["dark"], lw="outline")          # pad
    c.rect(cx - 25 * k, base - 70 * k, 50 * k, 54 * k, fill=GREY["steel"], lw="outline")         # body
    c.rect(cx - 0.9, top + 1.2, 1.8, base - 70 * k - top - 1.2, fill="#fff", lw="thin")          # stem
    c.rect(cx - 29.75 * k, top, 59.5 * k, 1.2, fill=GREY["mid"], lw="outline")                   # plate
    sx = cx + 29.75 * k + 6                    # spine of the C
    c.poly([(cx - 20, top - 3), (sx + 4, top - 3), (sx + 4, base + 3), (cx - 20, base + 3), (cx - 20, base), (sx, base), (sx, top), (cx - 20, top)], fill=GREY["light"], lw="outline")
    c.arrow((sx + 20, (top + base) / 2), (sx + 6, (top + base) / 2), lw="outline", head=1.6)
    c.text((sx + 7, (top + base) / 2 - 3.5), "slide on", size=3.0, anchor="start")
    dim2(c, (sx + 30, top), (sx + 30, base), "", off=-0.01)
    c.text((sx + 28, top + 8), "102 mm", size=3.0, anchor="end", weight="bold")
    c.text((sx + 28, top + 11.8), "inside", size=3.0, anchor="end")
    c.text((cx - 20, top - 5.5), "plate", size=3.0, anchor="start")
    c.text((cx - 20, base + 6.2), "pad", size=3.0, anchor="start")
    return c.save(os.path.join(FIG, "02-use-height.svg"))


def use_wall():
    c = Canvas(UW, 60)
    k = 0.42
    for i, (gap, what) in enumerate(((65, "ALEX back"), (30, "top's raw edge"))):
        x = 3 + i * 43
        hatch_rect(c, x, 4, x + 37, 8, spacing=1.2); c.line((x, 8), (x + 37, 8), lw="heavy")
        c.text((x + 19, 2.4), "wall", size=3.0)
        y = 8 + gap * k
        c.rect(x, y, 37, 12, fill=GREY["light"] if i == 0 else GREY["wood"], lw="outline")
        c.text((x + 19, y + 6), what, size=3.0)
        gx = x + 14
        c.rect(gx, 8, 3, gap * k, fill=GREY["mid"], lw="outline")
        dim2(c, (gx - 2, 8), (gx - 2, y), f"{gap / 10:g} cm", off=-0.01)
        c.text((x + 19, 58), f"{gap} leg", size=3.0, weight="bold")
    return c.save(os.path.join(FIG, "02-use-wall.svg"))


USE = (use_tsquare, use_legjig, use_cornerjig, use_alexcorner, use_railgauge, use_raildrill, use_slotplug, use_guide, use_height, use_wall)


if __name__ == "__main__":
    os.makedirs(FIG, exist_ok=True)
    for fn in (fig_safety, fig_floor, fig_workshop) + USE:
        print(fn())
    for name, fn, w, h in TOOL_ICONS:
        print(tool_icon_svg(name, fn, w, h))
