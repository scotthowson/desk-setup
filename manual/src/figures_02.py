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
    dim2(c, (wu, wv), (P(2490, 0)[0], wv), "2520", off=5)
    dim2(c, (wu, P(0, 3140)[1]), (wu, wv), "3170", off=5)
    c.text((P(1500, 330)[0], P(0, 330)[1]), "desk", size=3.0)
    c.text((P(1500, 0)[0], P(0, 0)[1] + 9), "", size=3.0)
    lead(c, P(-15, 1000), (P(900, 1000)[0], P(0, 1000)[1]), "30 wall gap", size=3.0)
    # bench for the steel, outside the footprint
    bx, by = P(1150, 2000)
    c.rect(bx, by, 26, 9, fill=GREY["light"], lw="outline")
    c.rect(bx + 1, by + 3.4, 24, 1.2, fill=GREY["dark"], lw="thin")
    c.text((bx + 13, by + 14), "bench for the steel", size=3.0)
    c.text((bx + 13, by + 18), "(rails 2130 long)", size=3.0)
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


if __name__ == "__main__":
    os.makedirs(FIG, exist_ok=True)
    for fn in (fig_safety, fig_floor, fig_workshop):
        print(fn())
    for name, fn, w, h in TOOL_ICONS:
        print(tool_icon_svg(name, fn, w, h))
