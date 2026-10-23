#!/usr/bin/env python3
"""Chapter E figures: steel rail fabrication and drilling. Writes manual/figures/05-*.svg.

Every printed number comes from manual/facts.json or manual/data.json (steel, corner_joint, rails).
The fitting's hole spacing is never dimensioned: it is drawn at data.json's assumed 25/65 mm only so the
picture has holes, and every drawing says the fitting itself is the template (MEASURE ON HARDWARE).
figures_06.py imports the helpers below.
"""
import json, math, os, re, sys

MANUAL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, MANUAL)
from lib.draw import Canvas, GREY, LW, FONT, _f  # noqa: E402

FACTS = json.load(open(os.path.join(MANUAL, "facts.json")))
DATA = json.load(open(os.path.join(MANUAL, "data.json")))
FIG = os.path.join(MANUAL, "figures")

S = FACTS["steel"]
LEG, T = S["leg"], S["thickness"]                     # 50.8, 4.76
LEN = S["design_length"]                              # 2130
SCREW, BOLT = S["screw_line_from_free_edge"], S["bolt_line_below_heel"]   # 19, 29
HOLES_A = [round(h * 10) for h in S["railA"]["holes_from_wall_end_cm"]]
HOLES_B = [round(h * 10) for h in S["railB"]["holes_from_corner_end_cm"]]
HEEL_OUT = round(S["railA"]["fitting_heels_from_wall_end_cm"]["outside_fitting_facing_far_end"] * 10)   # 520
HEEL_IN = round(S["railA"]["fitting_heels_from_wall_end_cm"]["inside_fitting_facing_wall_end"] * 10)    # 515
UNDER_A = round(S["railB"]["corner_overlap_under_topA_cm"] * 10)                                        # 120
FIT_T = 5                                             # "5 mm gusseted 90-degree strut fittings" (corner_joint.fittings)
FIT_W = round(DATA["fitting"]["w"] * 10, 2)            # 41 wide (measured 23 Oct 2026)
FIT_L = round(DATA["fitting"]["legs"] * 10, 2)         # 100.5 long legs (measured)
FIT_H = [round(h * 10, 2) for h in DATA["fitting"]["h"]]   # 29.15, 78.45: slot centres from the heel (measured)
SLOT_L, SLOT_W = [round(v * 10, 2) for v in DATA["fitting"]["slot"]]   # 21 x 12 slots, long axis along the leg
RH = FACTS["corner_joint"]["rail_hole_positions_mm"]
HOLES_AO, HOLES_AI, HOLES_BC = RH["railA_outside_fitting_from_wall_end"], RH["railA_inside_fitting_from_wall_end"], RH["railB_from_corner_end"]


def cm(mm, one_decimal=False):
    """Tape reading in cm as the build manual writes it: 35 -> '3.5', 280 -> '28', 520 -> '52.0' with one_decimal."""
    v = round(mm / 10 + 1e-9, 1)
    return f"{v:.1f}" if one_decimal else f"{v:g}"


# bolt-hole tape readings from the exact slot centres (heel +/- 29.15 / 78.45), as docs/build-manual.md step 1 prints them
BOLT_CM = {}
for _heel, _d, _mm in ((HEEL_OUT_MM := round(S["railA"]["fitting_heels_from_wall_end_cm"]["outside_fitting_facing_far_end"] * 10), +1, RH["railA_outside_fitting_from_wall_end"]),
                       (round(S["railA"]["fitting_heels_from_wall_end_cm"]["inside_fitting_facing_wall_end"] * 10), -1, RH["railA_inside_fitting_from_wall_end"]),
                       (0, +1, RH["railB_from_corner_end"])):
    for _h, _m in zip([round(h * 10, 2) for h in DATA["fitting"]["h"]], _mm):
        BOLT_CM[_m] = cm(_heel + _d * _h)
assert [BOLT_CM[m] for m in RH["railA_outside_fitting_from_wall_end"] + RH["railA_inside_fitting_from_wall_end"] + RH["railB_from_corner_end"]] == \
    ["54.9", "59.8", "48.6", "43.7", "2.9", "7.8"]   # docs/build-manual.md step 1
RAILA_Y = DATA["railA"]["y0"] * 10, DATA["railA"]["y1"] * 10   # 479, 530
RAILA_X0 = DATA["railA"]["x0"] * 10                   # 10: wall end on top A
TOP_T = FACTS["tops"]["thickness"]                    # 28
OUTF = DATA["railA"]["y1"] * 10                        # 530: vertical legs' outer faces (y on rail A, x on rail B)


def num(v):
    return f"{v:g}"


def frac_mm(s):
    """'7/32 in (5.56 mm)' -> ('7/32 in', 5.56)."""
    m = re.match(r"(.+ in) \(([\d.]+) mm\)", s)
    return m.group(1), float(m.group(2))


SC_IN, SC_D = frac_mm(S["screw_clearance_hole"])      # 7/32 in, 5.56
BO_IN, BO_D = frac_mm(S["bolt_hole"])                 # 7/16 in, 11.1
SC_LBL = f"⌀{SC_D:g} ({SC_IN})"
BO_LBL = f"⌀{BO_D:g} ({BO_IN})"
SLOT_LBL = f"{num(SLOT_L)} × {num(SLOT_W)} slot"
PILOT_LBL = "⌀3.2 (1/8 in)"                           # design-review hole table: 1/8 in (3.2 mm)


# ---------------------------------------------------------------- page-space helpers (Canvas at scale 1)
def text_box(x, y, s, size, anchor, weight, rotate):
    """Estimated page-mm box (x0, y0, x1, y1) of a text item; Helvetica ~0.55 em per character."""
    w = len(s) * size * (0.58 if weight == "bold" else 0.54)
    h = size * 0.95
    a0 = {"start": 0, "middle": -w / 2, "end": -w}[anchor]
    if rotate in (-90, 90, 270):
        sg = -1 if rotate == -90 else 1
        ys = sorted([y + sg * a0, y + sg * (a0 + w)])
        return (x - h / 2, ys[0], x + h / 2, ys[1])
    return (x + a0, y - h / 2, x + a0 + w, y + h / 2)


def T_(c, x, y, s, size=3.2, anchor="start", weight="normal", rotate=0, color="#000", italic=False, box=False):
    if size < 3.0:
        raise ValueError(f"text under 3 mm: {s!r}")
    if not hasattr(c, "tb"):
        c.tb = []
    c.tb.append((text_box(x, y, s, size, anchor, weight, rotate), s))
    if box:
        b = c.tb[-1][0]
        c.raw(f'<rect x="{_f(b[0] - 0.8)}" y="{_f(b[1] - 0.5)}" width="{_f(b[2] - b[0] + 1.6)}" height="{_f(b[3] - b[1] + 1.0)}" fill="#fff"/>')
    c.text((x, y), s, size=size, anchor=anchor, weight=weight, rotate=rotate, color=color)
    if italic:
        c.parts[-1] = c.parts[-1].replace("<text ", '<text font-style="italic" ', 1)


def L_(c, x1, y1, x2, y2, lw="outline", dash=None, color="#000"):
    c.line((x1, y1), (x2, y2), lw=lw, dash=dash, color=color)


def R_(c, x, y, w, h, fill="none", lw="outline", dash=None):
    c.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill=fill, lw=lw, dash=dash)


def P_(c, pts, fill="none", lw="outline", dash=None, close=True):
    c.poly(pts, fill=fill, lw=lw, dash=dash, close=close)


def head(c, x1, y1, x2, y2, h=1.6):
    c._head(x1, y1, x2, y2, h)


def dimh(c, x1, x2, y, label, y_from=None, size=3.2, above=True, ext=True, txt_dx=0):
    """Horizontal dimension at page y between x1 and x2; extension lines from y_from (a y or (y1, y2))."""
    if ext and y_from is not None:
        f1, f2 = (y_from, y_from) if not isinstance(y_from, tuple) else y_from
        for xx, ff in ((x1, f1), (x2, f2)):
            s = 1 if y > ff else -1
            L_(c, xx, ff + 0.8 * s, xx, y + 1.2 * s, lw="dim")
    L_(c, x1, y, x2, y, lw="dim")
    if abs(x2 - x1) >= 4.5:
        head(c, x2, y, x1, y); head(c, x1, y, x2, y)
        tx = (x1 + x2) / 2 + txt_dx
    else:  # arrows outside, text beside
        head(c, x1 - 3, y, x1, y); head(c, x2 + 3, y, x2, y)
        L_(c, x1 - 3.5, y, x2 + 3.5, y, lw="dim")
        tx = (x1 + x2) / 2 + txt_dx
    T_(c, tx, y - 1.7 if above else y + 1.9, label, size=size, anchor="middle")


def dimv(c, y1, y2, x, label, x_from=None, size=3.2, left=True, ext=True, txt_dy=0, rot=True, box=False):
    """Vertical dimension at page x between y1 and y2; text rotated, on the left (or right) of the line."""
    if ext and x_from is not None:
        f1, f2 = (x_from, x_from) if not isinstance(x_from, tuple) else x_from
        for yy, ff in ((y1, f1), (y2, f2)):
            s = 1 if x > ff else -1
            L_(c, ff + 0.8 * s, yy, x + 1.2 * s, yy, lw="dim")
    L_(c, x, y1, x, y2, lw="dim")
    if abs(y2 - y1) >= 4.5:
        head(c, x, y2, x, y1); head(c, x, y1, x, y2)
    else:
        lo, hi = min(y1, y2), max(y1, y2)
        head(c, x, lo - 3, x, lo); head(c, x, hi + 3, x, hi)
        L_(c, x, lo - 3.5, x, hi + 3.5, lw="dim")
    ty = (y1 + y2) / 2 + txt_dy
    if rot:
        tx = x - 1.7 if left else x + 1.9
        T_(c, tx, ty, label, size=size, anchor="middle", rotate=-90, box=box)
    else:
        T_(c, x - 1.2 if left else x + 1.2, ty, label, size=size, anchor="end" if left else "start")


def leader(c, tx, ty, px, py, label, size=3.2, anchor="start", dot=True, lines=None, box=False):
    """Text at (tx, ty), thin line to the target (px, py) ending in a dot. lines: extra text lines below."""
    off = 1.2 if anchor == "start" else -1.2 if anchor == "end" else 0
    b = text_box(tx + off, ty, label, size, anchor, "normal", 0)
    if px > b[2]:
        sx, sy = b[2] + 0.8, ty
    elif px < b[0]:
        sx, sy = b[0] - 0.8, ty
    else:  # target under or over the text: leave from the nearer long edge
        sx, sy = min(max(px, b[0] + 1), b[2] - 1), (b[3] + 0.4 if py > ty else b[1] - 0.4)
        if py > ty and lines:
            sy += len(lines) * size * 1.25
    L_(c, sx, sy, px, py, lw="thin")
    if dot:
        c.raw(f'<circle cx="{_f(px)}" cy="{_f(py)}" r="0.55" fill="#000"/>')
    T_(c, tx + off, ty, label, size=size, anchor=anchor, box=box)
    for i, s in enumerate(lines or []):
        T_(c, tx + off, ty + (i + 1) * size * 1.25, s, size=size, anchor=anchor, box=box)


def arrow(c, x1, y1, x2, y2, lw="outline", h=2.2):
    L_(c, x1, y1, x2, y2, lw=lw)
    head(c, x1, y1, x2, y2, h)


def hole(c, x, y, d, cross=1.0, fill="#fff", lw="outline", dash=None):
    """Hole symbol in page mm: circle of diameter d plus centre mark."""
    r = d / 2
    da = f' stroke-dasharray="{dash}"' if dash else ""
    c.raw(f'<circle cx="{_f(x)}" cy="{_f(y)}" r="{_f(r)}" fill="{fill}" stroke="#000" stroke-width="{LW.get(lw, lw)}"{da}/>')
    m = r + max(1.2, r * 0.45) * cross
    L_(c, x - m, y, x + m, y, lw="thin"); L_(c, x, y - m, x, y + m, lw="thin")


def slot(c, x, y, L, W, fill="#fff", lw="outline", dash=None, vertical=False):
    """Stadium slot in page mm, centre (x, y), length L along page x (or y if vertical), width W."""
    r = W / 2
    a = (L - W) / 2
    da = f' stroke-dasharray="{dash}"' if dash else ""
    if not vertical:
        d = f"M{_f(x - a)},{_f(y - r)} L{_f(x + a)},{_f(y - r)} A{_f(r)},{_f(r)} 0 0 1 {_f(x + a)},{_f(y + r)} L{_f(x - a)},{_f(y + r)} A{_f(r)},{_f(r)} 0 0 1 {_f(x - a)},{_f(y - r)} Z"
    else:
        d = f"M{_f(x + r)},{_f(y - a)} L{_f(x + r)},{_f(y + a)} A{_f(r)},{_f(r)} 0 0 1 {_f(x - r)},{_f(y + a)} L{_f(x - r)},{_f(y - a)} A{_f(r)},{_f(r)} 0 0 1 {_f(x + r)},{_f(y - a)} Z"
    c.raw(f'<path d="{d}" fill="{fill}" stroke="#000" stroke-width="{LW.get(lw, lw)}"{da}/>')


def balloon(c, bx, by, tx, ty, label, r=3.8):
    c.balloon((tx, ty), (bx, by), label, r=r)


def boxed(c, x, y, w, h, title=None, size=3.4):
    R_(c, x, y, w, h, lw="thin")
    if title:
        T_(c, x + 2, y + 3.6, title, size=size, weight="bold")


def hatch_rect(c, x, y, w, h, spacing=1.4):
    c.hatch([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], spacing=spacing)


def zig(c, x, y1, y2, amp=1.4, n=3):
    """Vertical break line (zigzag) at page x from y1 to y2."""
    pts = [(x, y1)]
    step = (y2 - y1) / (2 * n)
    for i in range(1, 2 * n):
        pts.append((x + (amp if i % 2 else -amp), y1 + i * step))
    pts.append((x, y2))
    P_(c, pts, close=False, lw="thin")


def check(c, name):
    """Report text boxes that leave the canvas or overlap each other (estimated extents)."""
    tb = getattr(c, "tb", [])
    bad = 0
    for (b, s) in tb:
        if b[0] < -0.2 or b[1] < -0.2 or b[2] > c.w + 0.2 or b[3] > c.h + 0.2:
            print(f"  [{name}] OUT OF CANVAS: {s!r} {tuple(round(v, 1) for v in b)}"); bad += 1
    for i in range(len(tb)):
        for j in range(i + 1, len(tb)):
            a, b = tb[i][0], tb[j][0]
            if a[0] < b[2] - 0.3 and b[0] < a[2] - 0.3 and a[1] < b[3] - 0.3 and b[1] < a[3] - 0.3:
                print(f"  [{name}] OVERLAP: {tb[i][1]!r} / {tb[j][1]!r}"); bad += 1
    return bad


def save(c, name, rotate=False):
    check(c, name)
    path = os.path.join(FIG, name)
    if not rotate:
        c.save(path)
        return path
    # landscape drawing turned to read with the page rotated clockwise (top of the drawing at the page's left edge)
    W, H = c.w, c.h
    body = "\n".join(c.parts)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_f(H)} {_f(W)}" width="{_f(H)}mm" height="{_f(W)}mm" class="fig">\n'
           f'<g transform="translate(0 {_f(W)}) rotate(-90)">\n{body}\n</g>\n</svg>')
    open(path, "w").write(svg)
    return path


def spread(xs, gap, lo=-1e9, hi=1e9):
    """Spread label positions so neighbours are at least `gap` apart, staying as close as possible to xs."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    pos = [xs[i] for i in order]
    for _ in range(50):
        moved = False
        for i in range(1, len(pos)):
            if pos[i] - pos[i - 1] < gap - 1e-6:
                d = (gap - (pos[i] - pos[i - 1])) / 2
                pos[i - 1] -= d; pos[i] += d; moved = True
        pos = [min(max(p, lo), hi) for p in pos]
        if not moved:
            break
    out = [0] * len(xs)
    for k, i in enumerate(order):
        out[i] = pos[k]
    return out


assert spread([0, 1, 10], 4)[1] - spread([0, 1, 10], 4)[0] >= 3.99   # self-check of the label spreader


# ---------------------------------------------------------------- Fig E-1: delivered length and the datum end
def fig_length():
    c = Canvas(172, 94)
    for r, (name, end) in enumerate([("RAIL A (P06)", "WALL END"), ("RAIL B (P07)", "CORNER END")]):
        y = 20 + r * 46
        T_(c, 4, y - 14, name, size=3.6, weight="bold")
        R_(c, 10, y - 9, 50, 6, fill="#fff")
        T_(c, 35, y - 6, f"TAPE LABEL: {end}", size=3.2, anchor="middle", weight="bold")
        L_(c, 12, y - 3, 11, y, lw="thin")
        R_(c, 10, y, 130, 6, fill=GREY["steel"])
        R_(c, 140, y, 7, 6, fill=GREY["light"], dash="1.2 0.8")
        L_(c, 10, y + 1.6, 147, y + 1.6, lw="thin")
        L_(c, 10, y - 2, 10, y + 8, lw="heavy")
        T_(c, 12, y + 3.8, "0", size=3.2, weight="bold")
        R_(c, 10, y + 8.5, 137, 2.2, fill=GREY["light"], lw="thin")
        P_(c, [(8.8, y + 7), (10, y + 7), (10, y + 10.7), (8.8, y + 10.7)], fill="#000", lw="thin")
        for k in range(0, 137, 6):
            L_(c, 10 + k, y + 8.5, 10 + k, y + 9.6, lw="thin")
        dimh(c, 10, 140, y + 17.5, f"design length {cm(LEN)} cm · last hole at {cm(max(HOLES_A))} cm", y_from=y + 6)
        dimh(c, 10, 147, y + 25.5, "delivered length: MEASURE ______ cm", y_from=y + 6)
        for i, s in enumerate(["far end:", "any extra", "stays here"]):
            T_(c, 150, y + 1 + i * 4.1, s, size=3.2)
    return save(c, "05-length.svg")


# ---------------------------------------------------------------- Fig E-2: cross-section and orientation
def fig_section():
    c = Canvas(172, 110)
    ox, oz = 66, 40
    X = lambda y: ox + (y - RAILA_Y[0])
    Z = lambda z: oz - z
    xa, xb = X(465), X(540)
    R_(c, xa, Z(TOP_T), xb - xa, TOP_T, fill=GREY["wood"])
    hatch_rect(c, xa, Z(TOP_T), xb - xa, TOP_T, spacing=2.2)
    for xx in (xa, xb):
        c.raw(f'<rect x="{_f(xx - 1.7)}" y="{_f(Z(TOP_T) - 1)}" width="3.4" height="{_f(TOP_T + 2)}" fill="#fff"/>')
        zig(c, xx, Z(TOP_T) - 1, Z(0) + 0.6)
    T_(c, (xa + xb) / 2, Z(TOP_T / 2), f"TOP (P01 / P02), {TOP_T} mm", size=3.2, anchor="middle", box=True)
    fl = [(X(479), Z(0)), (X(530), Z(0)), (X(530), Z(-LEG)), (X(530 - T), Z(-LEG)), (X(530 - T), Z(-T)), (X(479), Z(-T))]
    P_(c, fl, fill=GREY["steel"], lw="heavy"); c.hatch(fl, spacing=1.1)
    sy = 479 + SCREW
    R_(c, X(sy - SC_D / 2), Z(0) - 0.25, SC_D, T + 0.5, fill="#fff", lw="thin")
    L_(c, X(sy), Z(8), X(sy), Z(-T) + 3, lw="thin", dash="4 1 0.8 1")
    R_(c, X(530 - T) - 0.25, Z(-BOLT + BO_D / 2), T + 0.5, BO_D, fill="#fff", lw="thin")
    L_(c, X(530 - T) - 2, Z(-BOLT), X(530) + 3, Z(-BOLT), lw="thin", dash="4 1 0.8 1")
    # dimensions
    dimh(c, X(479), X(sy), Z(-T) + 7, f"{SCREW}", y_from=Z(-T))
    dimv(c, Z(0), Z(-T), X(479) - 4, f"{T}", x_from=X(479), rot=False)
    dimh(c, X(479), X(530), Z(-LEG) + 8, f"{LEG}", y_from=(Z(-T), Z(-LEG)))
    dimh(c, X(530 - T), X(530), Z(-LEG) + 15, f"{T}", y_from=Z(-LEG), txt_dx=8.5, above=False)
    dimv(c, Z(0), Z(-BOLT), X(530) + 7, f"{BOLT}", x_from=X(530), left=False)
    dimv(c, Z(0), Z(-LEG), X(530) + 16, f"{LEG}", x_from=X(530), left=False)
    # labels
    leader(c, X(479) - 3, Z(-T) + 6, X(479), Z(-T) + 0.2, "free edge", anchor="end")
    for i, s in enumerate(["screw hole", f"⌀{SC_D:g}", f"({SC_IN})"]):
        T_(c, X(sy) + 4.5, Z(-T) + 4 + i * 4, s, size=3.2)
    L_(c, X(sy) + 3.7, Z(-T) + 4, X(sy) + SC_D / 2, Z(-T) + 0.3, lw="thin")
    for i, s in enumerate(["bolt hole", f"⌀{BO_D:g}", f"({BO_IN})"]):
        T_(c, X(530 - T) - 7, Z(-BOLT) - 4.5 + i * 4, s, size=3.2, anchor="end")
    L_(c, X(530 - T) - 6.4, Z(-BOLT) - 0.5, X(530 - T), Z(-BOLT) - 1.5, lw="thin")
    T_(c, X(530 - T) - 2.2, Z(-41.5), "inner face", size=3.2, anchor="middle", rotate=-90)
    T_(c, X(530) + 2.4, Z(-41), "outer face", size=3.2, anchor="middle", rotate=-90)
    leader(c, X(530) + 22, Z(2.5), X(530), Z(0), "heel", lines=["(outside of", "the bend)"])
    block = [("FLAT LEG", "bold"), ("lies against the", ""), ("top's underside", ""), ("", ""), ("VERTICAL LEG", "bold"),
             ("hangs down, toward", ""), ("you; outer face at", ""), (f"y = {cm(OUTF)} cm (rail A)", ""), (f"x = {cm(OUTF)} cm (rail B)", "")]
    for i, (s, w) in enumerate(block):
        if s:
            T_(c, 3, Z(-12) + i * 4.2, s, size=3.2, weight=w or "normal")
    arrow(c, X(468), 6, X(452), 6)
    T_(c, X(468) + 1.5, 6, f"BACK: wall side ({FACTS['layout_cm']['wall_gap']:g} cm gap)", size=3.2)
    arrow(c, X(512), 6, X(540), 6)
    T_(c, X(540) + 1.5, 6, "FRONT: you", size=3.2)
    return save(c, "05-section.svg")


# ---------------------------------------------------------------- Fig E-3/E-4: opened-out fabrication drawings
def table(c, x, y, cols, rows, widths, size=3.2, rh=4.35):
    W = sum(widths)
    allr = [cols] + rows
    R_(c, x, y, W, rh, fill=GREY["light"], lw="thin")
    for r, row in enumerate(allr):
        xx = x
        for j, cell in enumerate(row):
            T_(c, xx + 1.2, y + r * rh + rh / 2 + 0.1, cell, size=size, weight="bold" if r == 0 else "normal")
            xx += widths[j]
    for r in range(len(allr) + 1):
        L_(c, x, y + r * rh, x + W, y + r * rh, lw="thin")
    xx = x
    for wd in [0] + widths:
        xx += wd
        L_(c, xx, y, xx, y + len(allr) * rh, lw="thin")
    return y + len(allr) * rh


def fab(part, name, holes, datum, heels, d_from, d_to, bolt_rows, block, fig="", note=""):
    """heels: [(station, +1 legs toward far end / -1 toward datum, label)]."""
    W, H = 250, 178
    c = Canvas(W, H)
    x0 = 27; x1 = x0 + LEN / 10
    kx, kw = 0.1, 0.4
    fe = 34; heel = fe + LEG * kw; vfe = heel + LEG * kw
    sl, bl = fe + SCREW * kw, heel + BOLT * kw
    X = lambda s: x0 + s * kx
    T_(c, 3, 5, f"{fig} · {part} {name} · OPENED-OUT FABRICATION DRAWING · ordinates in mm (cm in the table)", size=4.2, weight="bold")
    T_(c, 3, 10.5, f"Lengths 1:10 from the {datum.upper()} (datum 0); leg widths 1:2.5, not to scale across; hole symbols not to scale. "
                   f"Seen from outside the L.", size=3.2)
    T_(c, 3, 14.7, note, size=3.2)
    R_(c, x0, fe, x1 - x0, LEG * kw, fill=GREY["steel"])
    R_(c, x0, heel, x1 - x0, LEG * kw, fill=GREY["light"])
    L_(c, x0, heel, x1, heel, lw="heavy")
    L_(c, x0, sl, x1, sl, lw="thin", dash="4 1 0.8 1")
    L_(c, x0, bl, x1, bl, lw="thin", dash="4 1 0.8 1")
    L_(c, x0, 26, x0, vfe + 2, lw="heavy")
    T_(c, x0 - 19, (fe + vfe) / 2, f"{datum.upper()} · 0", size=3.4, anchor="middle", weight="bold", rotate=-90)
    T_(c, x1 + 3.5, (fe + vfe) / 2, "FAR END · extra length", size=3.2, anchor="middle", weight="bold", rotate=90)
    dimv(c, fe, sl, x0 - 4, f"{SCREW}", x_from=x0)
    dimv(c, fe, heel, x0 - 11, f"{LEG}", x_from=x0)
    dimv(c, heel, bl, x0 - 4, f"{BOLT}", x_from=x0)
    dimv(c, heel, vfe, x0 - 11, f"{LEG}", x_from=x0)
    # ordinates above the flat leg
    vals = [0] + holes + [LEN]
    xs = [x0] + [X(s) for s in holes] + [x1]
    lab = spread(xs, 4.3, lo=x0 - 1.5, hi=x1 + 1)
    for i, (xh, xl) in enumerate(zip(xs, lab)):
        ytop = fe if i in (0, len(vals) - 1) else sl - 1.5
        L_(c, xh, ytop, xh, 29, lw="dim"); L_(c, xh, 29, xl, 26.5, lw="dim"); L_(c, xl, 26.5, xl, 25.5, lw="dim")
        T_(c, xl, 24.7, num(vals[i]), size=3.2, anchor="start", rotate=-90, weight="bold" if 0 < i < len(vals) - 1 else "normal")
    nums = spread([X(s) for s in holes], 3.6)
    for i, s in enumerate(holes):
        hole(c, X(s), sl, 2.2, cross=0.5)
        T_(c, nums[i], sl + 4.3, str(i + 1), size=3.2, anchor="middle", weight="bold")
    for hpos, d, _, bpos in heels:
        fx = X(hpos) if d > 0 else X(hpos - FIT_L)
        R_(c, fx, bl - FIT_W * kw / 2, FIT_L * kx, FIT_W * kw, lw="thin", dash="1.5 0.7")
        L_(c, X(hpos), heel, X(hpos), vfe, lw="heavy")
        for b in bpos:
            hole(c, X(b), bl, 2.2, cross=0.4)
    R_(c, X(d_from), fe - 1.5, X(d_to) - X(d_from), vfe - fe + 3, lw="thin", dash="3 1.2")
    T_(c, X(d_to) + 1.5, vfe - 2.5, "DETAIL A", size=3.2, weight="bold")
    T_(c, X(1300), heel - 3.2, "FLAT LEG · against the top's underside · free edge toward the wall", size=3.2, weight="bold", anchor="middle")
    T_(c, X(1300), vfe - 3.2, "VERTICAL LEG · hangs down · outer face toward you", size=3.2, weight="bold", anchor="middle")
    T_(c, x1 - 1, heel - 1.9, "heel", size=3.2, anchor="end")
    hl = " · ".join(num(h) for h, _, _, _ in heels)
    L_(c, X(heels[-1][0]), vfe, X(heels[-1][0]) - 2, vfe + 3.2, lw="dim")
    T_(c, X(heels[-1][0]) - 2.5, vfe + 4.5, (f"heel {hl} ({' · '.join(cm(h, True) for h, _, _, _ in heels)} cm)" if heels[-1][0] else "heel 0"), size=3.2, anchor="end")
    allb = sorted(b for h in heels for b in h[3])
    nb = len(allb)
    y = vfe + 10
    T_(c, x0, y, f"{len(holes)}× {SC_LBL} THRU in the flat leg, centres on the screw line {SCREW} from the free edge, at the ordinates above.", size=3.2)
    T_(c, x0, y + 4.4, f"{nb}× {BO_LBL} THRU in the vertical leg on the bolt line {BOLT} below the heel, at {', '.join(BOLT_CM[b] for b in allb)} cm (Detail A, mm).", size=3.2)
    T_(c, x0, y + 8.8, "Positions VERIFIED from the measured fitting; drill them THROUGH the clamped fitting with the slot plug (step 6).", size=3.2, weight="bold")
    # ---- detail A at 1:2
    k2 = 0.5
    dx0, dfe = 10, 110
    dheel, dvfe = dfe + LEG * k2, dfe + 2 * LEG * k2
    D = lambda s: dx0 + (s - d_from) * k2
    dlen = (d_to - d_from) * k2
    T_(c, 3, 99, "DETAIL A · 1:2 · dashed: the fitting clamped as the template", size=3.6, weight="bold")
    R_(c, dx0, dfe, dlen, LEG * k2, fill=GREY["steel"])
    R_(c, dx0, dheel, dlen, LEG * k2, fill=GREY["light"])
    L_(c, dx0, dheel, dx0 + dlen, dheel, lw="heavy")
    ends = [dx0 + dlen] + ([dx0] if d_from > 0 else [])
    for xx in ends:
        c.raw(f'<rect x="{_f(xx - 1.6)}" y="{_f(dfe - 1)}" width="3.2" height="{_f(LEG + 2)}" fill="#fff"/>')
        zig(c, xx, dfe - 0.5, dvfe + 0.5, n=4)
    if d_from == 0:
        L_(c, dx0, dfe - 2, dx0, dvfe + 2, lw="heavy")
    dsl, dbl = dfe + SCREW * k2, dheel + BOLT * k2
    L_(c, dx0, dsl, dx0 + dlen - 2, dsl, lw="thin", dash="4 1 0.8 1")
    L_(c, dx0, dbl, dx0 + dlen - 2, dbl, lw="thin", dash="4 1 0.8 1")
    row = 0
    for i, s in enumerate(holes):
        if d_from <= s <= d_to - 10:
            hole(c, D(s), dsl, SC_D * k2, cross=1.0)
            ty = dsl + 5 + row * 4.3
            T_(c, D(s) + 3.2, ty, f"hole {i + 1} at {num(s)}", size=3.2)
            L_(c, D(s) + 2.6, ty - 0.6, D(s) + 1.0, dsl + 1.0, lw="thin")
            row += 1
    dimv(c, dfe, dsl, dx0 + dlen + 4.5, f"{SCREW}", x_from=dx0 + dlen + 1.8, left=False)
    dimv(c, dheel, dbl, dx0 + dlen + 4.5, f"{BOLT}", x_from=dx0 + dlen + 1.8, left=False)
    for hpos, d, lbl, bpos in heels:
        fx = D(hpos) if d > 0 else D(hpos - FIT_L)
        R_(c, fx, dbl - FIT_W * k2 / 2, FIT_L * k2, FIT_W * k2, lw="thin", dash="1.5 0.7")
        L_(c, D(hpos), dheel - 1.2, D(hpos), dvfe + 1.2, lw="heavy")
        for hh in FIT_H:
            slot(c, D(hpos + d * hh), dbl, SLOT_L * k2, SLOT_W * k2, fill="none", lw="thin", dash="1 0.6")
        for b in bpos:
            hole(c, D(b), dbl, BO_D * k2, cross=0.6)
            L_(c, D(b), dbl + SLOT_W * k2 / 2 + 0.6, D(b), dvfe + 2.2, lw="dim")
            T_(c, D(b) + 1.1, dvfe + 2.6, num(b), size=3.2, anchor="end", rotate=-90, weight="bold")
        arrow(c, D(hpos) + d * 1.2, dheel + 1.9, D(hpos) + d * 12, dheel + 1.9, lw="thin", h=1.4)
        T_(c, D(hpos) + d * 13.2, dheel + 1.9, "legs", size=3.2, anchor="start" if d > 0 else "end")
        T_(c, D(hpos) + d * 1.4, dheel - 2.8, f"heel {num(hpos)} ({cm(hpos, True)} cm)" if hpos else "heel 0", size=3.2, anchor="start" if d > 0 else "end", weight="bold")
    # hole table and title block
    rows = [[str(i + 1), num(s), cm(s), SC_LBL, f"flat, {SCREW} line"] for i, s in enumerate(holes)]
    for lbl, pos_ in bolt_rows:
        rows.append([lbl, num(pos_), BOLT_CM[pos_], BO_LBL, f"vertical, {BOLT}"])
    T_(c, 147, 97.4, f"Holes from the {datum}", size=3.2, weight="bold")
    yt = table(c, 147, 99.6, ["No.", "mm", "cm", "hole", "leg, line"], rows, [10, 14, 12, 27, 36])
    for i, s in enumerate(block):
        T_(c, 147, yt + 3.9 + i * 3.95, s, size=3.2, weight="bold" if i == 0 else "normal")
    return c, D, dfe, dvfe, dbl


def fig_railA():
    heels = [(HEEL_IN, -1, f"heel {HEEL_IN}: inside fitting, legs to the wall end", HOLES_AI), (HEEL_OUT, +1, f"heel {HEEL_OUT}: outside fitting, legs to the far end", HOLES_AO)]
    block = [f"P06 Rail A · {S['section']}", f"{LEG} × {LEG} × {T} mm, {cm(LEN)} cm: MEASURE first",
             f"On the desk: wall end x = {cm(RAILA_X0)} cm, outer face y = {cm(OUTF)} cm", "(datum: top A's back-left corner)"]
    c, D, dfe, dvfe, dbl = fab("P06", "RAIL A", HOLES_A, "wall end", heels, 395, 645, [("I2", HOLES_AI[1]), ("I1", HOLES_AI[0]), ("O1", HOLES_AO[0]), ("O2", HOLES_AO[1])], block,
                               fig="Fig. E-3", note="Flat leg (upper strip) and vertical leg (lower strip) unfolded about the heel. Stations SOURCE-DEFINED; bolt holes VERIFIED.")
    return save(c, "05-railA.svg", rotate=True)


def fig_railB():
    heels = [(0, +1, "heel flush with the corner end (0), legs to the far end; both fittings share these holes", HOLES_BC)]
    block = [f"P07 Rail B · {S['section']}", f"{LEG} × {LEG} × {T} mm, {cm(LEN)} cm: MEASURE first",
             f"On the desk: corner end y = {cm(OUTF)} cm, outer face x = {cm(DATA['railB']['x1'] * 10)} cm", "(datum: top A's back-left corner)"]
    c, D, dfe, dvfe, dbl = fab("P07", "RAIL B", HOLES_B, "corner end", heels, 0, 250, [("C1", HOLES_BC[0]), ("C2", HOLES_BC[1])], block,
                               fig="Fig. E-4", note="Holes 1, 2 go into top A, 3 to 10 into top B; the two bolt holes serve both fittings. Stations SOURCE-DEFINED; bolt holes VERIFIED.")
    yz = dfe - 4.5
    L_(c, D(0), yz, D(UNDER_A), yz, lw="dim"); head(c, D(UNDER_A), yz, D(0), yz, 1.4); head(c, D(0), yz, D(UNDER_A), yz, 1.4)
    L_(c, D(UNDER_A), yz - 1.5, D(UNDER_A), dfe - 0.3, lw="thin", dash="1.5 1")
    L_(c, D(UNDER_A), dvfe + 0.3, D(UNDER_A), dvfe + 3.5, lw="thin", dash="1.5 1")
    T_(c, D(UNDER_A / 2), yz - 2, f"{UNDER_A} ({cm(UNDER_A)} cm): under top A", size=3.2, anchor="middle")
    T_(c, D(UNDER_A) + 1.5, yz - 2, "top A's front edge (the joint)", size=3.2)
    return save(c, "05-railB.svg", rotate=True)


# ---------------------------------------------------------------- Fig E-5: stations with the tape and the T-square
def fig_stations():
    c = Canvas(172, 64)
    x0, fe, hl = 10, 20, 40
    R_(c, x0, fe, 140, hl - fe, fill=GREY["steel"])
    L_(c, x0, hl, x0 + 140, hl, lw="heavy")
    L_(c, x0, fe - 6, x0, hl + 4, lw="heavy")
    T_(c, x0 + 142, fe + 1.5, "free edge", size=3.2)
    T_(c, x0 + 142, hl - 1.5, "heel", size=3.2)
    T_(c, x0 - 1, hl + 7, "labelled end (0)", size=3.2)
    # tape on the leg along the free edge, hooked over the labelled end
    R_(c, x0, fe + 1, 136, 3.4, fill="#fff", lw="thin")
    for k in range(0, 136, 5):
        L_(c, x0 + k, fe + 1, x0 + k, fe + 1 + (2.2 if k % 10 == 0 else 1.1), lw="thin")
    P_(c, [(x0 - 1.4, fe - 0.5), (x0, fe - 0.5), (x0, fe + 4.9), (x0 - 1.4, fe + 4.9)], fill="#000", lw="thin")
    sx = 92
    # T-square: head below the heel with its lip over the heel edge, blade across the leg past the free edge
    R_(c, sx - 26, hl, 52, 8, fill=GREY["light"])
    R_(c, sx, fe - 8, 9, hl - fe + 8, fill="#fff")
    L_(c, sx - 0.4, fe, sx - 0.4, hl, lw="heavy")
    L_(c, sx - 0.4, fe + 1, sx - 0.4, fe + 4.4, lw="heavy")
    T_(c, sx, hl + 12, "T-square (P18): lip over the heel edge, blade across the leg", size=3.2, anchor="middle")
    leader(c, sx + 13, fe - 4, sx - 0.4, fe + 2.6, "tick the station on the tape", size=3.2)
    leader(c, sx + 13, fe + 12, sx - 0.4, fe + 12, "pencil along the blade's edge", size=3.2)
    T_(c, 4, 4, "Hook the tape over the labelled end once and tick every station from that one hook;", size=3.2)
    T_(c, 4, 8.5, "never measure from one hole to the next.", size=3.2)
    T_(c, 4, 61, "Plan: flat leg face up, vertical leg over the bench edge, labelled end at the left.", size=3.2)
    return save(c, "05-stations.svg")


# ---------------------------------------------------------------- Fig E-5b: marking gauge on both legs
def fig_gauge():
    c = Canvas(172, 90)
    k = 0.9
    for p in (0, 1):
        ox, oy = (16, 31) if p == 0 else (92, 31)
        X = lambda u: ox + u * k
        Y = lambda v: oy + v * k
        ang = [(X(0), Y(0)), (X(LEG), Y(0)), (X(LEG), Y(LEG)), (X(LEG - T), Y(LEG)), (X(LEG - T), Y(T)), (X(0), Y(T))]
        P_(c, ang, fill=GREY["steel"], lw="heavy"); c.hatch(ang, spacing=1.2)
        if p == 0:
            T_(c, 4, 5, f"a  SCREW LINE on the flat leg", size=3.4, weight="bold")
            T_(c, 4, 9.5, "lip over the free edge,", size=3.2)
            T_(c, 4, 13.7, f"pencil in the {SCREW} notch, slide", size=3.2)
            P_(c, [(X(-3), Y(-3)), (X(0), Y(-3)), (X(0), Y(6)), (X(-3), Y(6))], fill="#fff")
            P_(c, [(X(0), Y(-3)), (X(SCREW + 2.2), Y(-3)), (X(SCREW), Y(0)), (X(0), Y(0))], fill="#fff")
            c.raw(f'<circle cx="{_f(X(SCREW))}" cy="{_f(Y(-0.5))}" r="0.6" fill="#000"/>')
            P_(c, [(X(SCREW), Y(-0.5)), (X(SCREW + 8), Y(-13)), (X(SCREW + 10), Y(-12)), (X(SCREW + 1.5), Y(-1))], fill="#fff")
            dimh(c, X(0), X(SCREW), Y(T) + 6, f"{SCREW}", y_from=Y(T))
            leader(c, X(-3) + 2, Y(T) + 16, X(-1.5), Y(5), "lip on the free edge", size=3.2)
            leader(c, X(SCREW) + 14, Y(-10), X(SCREW + 5), Y(-6), "pencil", size=3.2)
        else:
            T_(c, 92, 5, f"b  BOLT LINE on the vertical leg", size=3.4, weight="bold")
            T_(c, 92, 9.5, "gauge on the outer face, lip over the heel,", size=3.2)
            T_(c, 92, 13.7, f"pencil in the {BOLT} notch, slide", size=3.2)
            P_(c, [(X(LEG - 6), Y(-3)), (X(LEG + 3), Y(-3)), (X(LEG + 3), Y(0)), (X(LEG - 6), Y(0))], fill="#fff")
            P_(c, [(X(LEG), Y(0)), (X(LEG + 3), Y(0)), (X(LEG + 3), Y(BOLT + 2.2)), (X(LEG), Y(BOLT))], fill="#fff")
            c.raw(f'<circle cx="{_f(X(LEG + 0.5))}" cy="{_f(Y(BOLT))}" r="0.6" fill="#000"/>')
            P_(c, [(X(LEG + 0.5), Y(BOLT)), (X(LEG + 13), Y(BOLT + 8)), (X(LEG + 12), Y(BOLT + 10)), (X(LEG + 1.5), Y(BOLT + 1.5))], fill="#fff")
            dimv(c, Y(0), Y(BOLT), X(LEG - T) - 5, f"{BOLT}", x_from=X(LEG - T))
            leader(c, X(LEG) - 32, Y(-8), X(LEG - 3), Y(-2.5), "lip on the heel", size=3.2)
            leader(c, X(LEG + 15), Y(BOLT + 16), X(LEG + 9), Y(BOLT + 6.5), "pencil", size=3.2)
    T_(c, 4, 87, "Sections, marking gauge (P18) in use. Run each line the full length of both rails.", size=3.2)
    return save(c, "05-gauge.svg")


# ---------------------------------------------------------------- Fig E-6: drill jig, open up, deburr
def fig_jig():
    c = Canvas(172, 62)
    titles = ["a  pilot through the jig", f"b  open to {SC_IN}", "c  deburr both faces"]
    for p in range(3):
        ox, oy = 9 + p * 57, 34
        X = lambda u: ox + u
        Y = lambda v: oy + v
        T_(c, ox - 6, 5, titles[p], size=3.2, weight="bold")
        R_(c, X(0), Y(0), 44, T, fill=GREY["steel"], lw="heavy")
        c.hatch([(X(0), Y(0)), (X(44), Y(0)), (X(44), Y(T)), (X(0), Y(T))], spacing=1.2)
        hw = (3.2 if p == 0 else SC_D) / 2
        R_(c, X(SCREW - hw), Y(0) - 0.2, 2 * hw, T + 0.4, fill="#fff", lw="thin")
        if p == 0:
            P_(c, [(X(-4), Y(-6)), (X(28), Y(-6)), (X(28), Y(0)), (X(0), Y(0)), (X(0), Y(6)), (X(-4), Y(6))], fill=GREY["light"])
            R_(c, X(SCREW - 1.75), Y(-6), 3.5, 6, fill="#fff", lw="thin")
            R_(c, X(SCREW - 1.6), Y(-22), 3.2, 22 + T + 1, fill="#fff")
            P_(c, [(X(SCREW - 1.6), Y(T + 1)), (X(SCREW + 1.6), Y(T + 1)), (X(SCREW), Y(T + 2.6))], fill="#fff")
            dimh(c, X(0), X(SCREW), Y(T) + 7.5, f"{SCREW}", y_from=Y(T))
            leader(c, X(30), Y(-12), X(26), Y(-5), "drill jig (P18)", size=3.2)
            T_(c, X(-6), Y(T) + 13, "sight grooves on the station", size=3.2)
            T_(c, X(-6), Y(T) + 17.5, "line; hold the jig down", size=3.2)
        elif p == 1:
            R_(c, X(SCREW - SC_D / 2), Y(-22), SC_D, 22 + T + 1.2, fill="#fff")
            P_(c, [(X(SCREW - SC_D / 2), Y(T + 1.2)), (X(SCREW + SC_D / 2), Y(T + 1.2)), (X(SCREW), Y(T + 4))], fill="#fff")
            for dd in (-1, 1):
                c.raw(f'<circle cx="{_f(X(SCREW + dd * 6))}" cy="{_f(Y(-1.3))}" r="0.9" fill="#000"/>')
            leader(c, X(27), Y(-12), X(SCREW + 6), Y(-2), "oil", size=3.2)
            T_(c, X(-6), Y(T) + 13, f"{SC_LBL}, low speed;", size=3.2)
            T_(c, X(-6), Y(T) + 17.5, "the bit follows the pilot", size=3.2)
        else:
            for side in (-1, 1):
                yy = Y(0) - 8 if side < 0 else Y(T) + 8
                dy = 3 if side < 0 else -3
                P_(c, [(X(SCREW - 8), yy), (X(SCREW + 8), yy), (X(SCREW + 6), yy + dy), (X(SCREW - 6), yy + dy)], fill=GREY["light"])
                arrow(c, X(SCREW + 11), yy + dy / 2, X(SCREW + 18), yy + dy / 2, lw="thin", h=1.4)
            T_(c, X(-6), Y(T) + 17.5, "file, or a larger bit by hand", size=3.2)
    return save(c, "05-jig.svg")


# ---------------------------------------------------------------- Fig E-7: where to clamp the fitting, three times
def fig_placement():
    c = Canvas(172, 124)
    k = 0.5
    rows = [(f"Rail A, outside fitting: heel on the {cm(HEEL_OUT, True)} cm mark, legs toward the far end", 400, HEEL_OUT, +1),
            (f"Rail A, inside fitting: heel on the {cm(HEEL_IN, True)} cm mark, legs toward the wall end", 400, HEEL_IN, -1),
            ("Rail B, one fitting: heel flush with the corner end (0), legs toward the far end", 0, 0, +1)]
    for i, (title, s0, hpos, d) in enumerate(rows):
        y = 10 + i * 40
        x0, span = 10, 260
        X = lambda s: x0 + (s - s0) * k
        T_(c, 4, y - 4.5, title, size=3.2, weight="bold")
        R_(c, x0, y, span * k, LEG * k, fill=GREY["light"])
        L_(c, x0, y, x0 + span * k, y, lw="heavy")
        if s0 == 0:
            L_(c, x0, y - 1.5, x0, y + LEG * k + 1.5, lw="heavy")
        bl = y + BOLT * k
        L_(c, x0, bl, x0 + span * k, bl, lw="thin", dash="4 1 0.8 1")
        for s in range(s0, s0 + span + 1, 20):
            L_(c, X(s), y + LEG * k, X(s), y + LEG * k + (3 if s % 100 == 0 else 1.6), lw="thin")
            if s % 100 == 0:
                T_(c, X(s), y + LEG * k + 5.5, cm(s), size=3.2, anchor="middle")
        T_(c, x0 + span * k + 2, y + 1.8, "heel edge", size=3.2)
        T_(c, x0 + span * k + 2, bl, f"bolt line {BOLT} mm", size=3.2)
        T_(c, x0 + span * k + 2, y + LEG * k + 5.5, "cm", size=3.2)
        fx = X(hpos) if d > 0 else X(hpos - FIT_L)
        R_(c, fx, bl - FIT_W * k / 2, FIT_L * k, FIT_W * k, fill=GREY["mid"])
        L_(c, X(hpos), y - 2.2, X(hpos), y + LEG * k + 2.2, lw="heavy")
        for hh in FIT_H:
            slot(c, X(hpos + d * hh), bl, SLOT_L * k, SLOT_W * k)
            L_(c, X(hpos + d * hh) - 1.2, bl, X(hpos + d * hh) + 1.2, bl, lw="thin"); L_(c, X(hpos + d * hh), bl - 1.2, X(hpos + d * hh), bl + 1.2, lw="thin")
        arrow(c, X(hpos) + d * 1.5, bl - FIT_W * k / 2 - 1.8, X(hpos) + d * 15, bl - FIT_W * k / 2 - 1.8, lw="thin", h=1.4)
        T_(c, X(hpos) + d * 16.5, bl - FIT_W * k / 2 - 1.8, "legs", size=3.2, anchor="start" if d > 0 else "end")
    return save(c, "05-placement.svg")


# ---------------------------------------------------------------- Fig E-7b: centring plug and opening the hole
def fig_plug():
    c = Canvas(172, 90)
    k = 1.5
    # a: plug in the fitting, pilot through it
    ox, oy = 38, 36
    X = lambda u: ox + u * k
    Y = lambda v: oy + v * k
    T_(c, 3, 5, "a  slot plug in the fitting's slot, 1/8 in pilot", size=3.2, weight="bold")
    R_(c, X(-22), Y(0), 44 * k, T * k, fill=GREY["steel"], lw="heavy")
    c.hatch([(X(-22), Y(0)), (X(22), Y(0)), (X(22), Y(T)), (X(-22), Y(T))], spacing=1.2)
    R_(c, X(-22), Y(-FIT_T), 44 * k, FIT_T * k, fill=GREY["light"])
    R_(c, X(-SLOT_L / 2), Y(-FIT_T), SLOT_L * k, FIT_T * k, fill="#fff", lw="thin")
    R_(c, X(-15), Y(-FIT_T - 3), 30 * k, 3 * k, fill=GREY["mid"])
    R_(c, X(-(SLOT_L - 0.3) / 2), Y(-FIT_T), (SLOT_L - 0.3) * k, FIT_T * k, fill=GREY["mid"])
    R_(c, X(-1.75), Y(-FIT_T - 3), 3.5 * k, (FIT_T + 3) * k, fill="#fff", lw="thin")
    R_(c, X(-1.6), Y(-FIT_T - 13), 3.2 * k, (FIT_T + 13 + T + 1) * k, fill="#fff")
    P_(c, [(X(-1.6), Y(T + 1)), (X(1.6), Y(T + 1)), (X(0), Y(T + 2.4))], fill="#fff")
    T_(c, X(23), Y(-FIT_T - 1.5), "plug (P18)", size=3.2)
    L_(c, X(22.6), Y(-FIT_T - 1.5), X(10), Y(-FIT_T - 1.5), lw="thin")
    T_(c, X(23), Y(-FIT_T / 2), "fitting (P08)", size=3.2)
    T_(c, X(23), Y(T / 2), "rail leg", size=3.2)
    # top view of the plug in the slot
    tx, ty = 26, 69
    R_(c, tx - 22, ty - 13, 44, 26, fill=GREY["light"], lw="thin")
    slot(c, tx, ty, SLOT_L * k, SLOT_W * k, fill="#fff")
    slot(c, tx, ty, (SLOT_L - 0.3) * k, (SLOT_W - 0.3) * k, fill=GREY["mid"], lw="thin")
    hole(c, tx, ty, 3.5 * k, cross=0.4)
    dimh(c, tx - SLOT_L * k / 2, tx + SLOT_L * k / 2, ty - 15.5, f"{num(SLOT_L)}", y_from=ty - SLOT_W * k / 2)
    dimv(c, ty - SLOT_W * k / 2, ty + SLOT_W * k / 2, tx + 25, f"{num(SLOT_W)}", x_from=tx + SLOT_L * k / 2 - SLOT_W * k / 4, left=False)
    for i, t in enumerate(["top view: the plug fills the", f"{SLOT_LBL}; its 1/8 in bore is", "the slot's centre, so the", f"{PILOT_LBL} pilot lands there"]):
        T_(c, 62, 61 + i * 4.3, t, size=3.2)
    # b: fitting off, open to 7/16
    ox = 136
    X = lambda u: ox + u * k
    T_(c, 102, 5, f"b  fitting off, open to {BO_IN}", size=3.2, weight="bold")
    R_(c, X(-22), Y(0), 44 * k, T * k, fill=GREY["steel"], lw="heavy")
    c.hatch([(X(-22), Y(0)), (X(22), Y(0)), (X(22), Y(T)), (X(-22), Y(T))], spacing=1.2)
    R_(c, X(-BO_D / 2), Y(0) - 0.2, BO_D * k, T * k + 0.4, fill="#fff", lw="thin")
    R_(c, X(-BO_D / 2), Y(-13), BO_D * k, (13 + T + 1.5) * k, fill="#fff")
    P_(c, [(X(-BO_D / 2), Y(T + 1.5)), (X(BO_D / 2), Y(T + 1.5)), (X(0), Y(T + 4.5))], fill="#fff")
    T_(c, 121, 54, f"{BO_LBL}, cobalt bit,", size=3.2)
    T_(c, 121, 58.3, "slow, oil; the bit follows", size=3.2)
    T_(c, 121, 62.6, "the pilot", size=3.2)
    return save(c, "05-plug.svg")


# ---------------------------------------------------------------- Fig E-8: floor test
def fig_floor():
    c = Canvas(172, 110)
    k = 0.4
    X = lambda s: 8 + (s - 330) * k      # s: mm from rail A's wall end
    oy = 72                              # rail A's outer face (toward rail B)
    T_(c, 4, 4, "Plan from above. Both rails upside down on the floor: flat legs down, vertical legs up.", size=3.2)
    T_(c, 4, 8.5, "Bolts in loosely; every one must slide in by hand.", size=3.2)
    xa0, xa1 = X(330), X(720)
    R_(c, xa0, oy, xa1 - xa0, LEG * k, fill=GREY["steel"])
    R_(c, xa0, oy, xa1 - xa0, T * k, fill=GREY["dark"])
    for xx in (xa0, xa1):
        c.raw(f'<rect x="{_f(xx - 1.3)}" y="{_f(oy - 0.5)}" width="2.6" height="{_f(LEG * k + 1)}" fill="#fff"/>')
        zig(c, xx, oy - 0.3, oy + LEG * k + 0.3, amp=1.0, n=2)
    bx1, bx0 = X(HEEL_OUT), X(HEEL_OUT - LEG)
    btop = oy - 140 * k
    R_(c, bx0, btop, LEG * k, oy - btop, fill=GREY["steel"])
    R_(c, bx1 - T * k, btop, T * k, oy - btop, fill=GREY["dark"])
    c.raw(f'<rect x="{_f(bx0 - 0.5)}" y="{_f(btop - 1.3)}" width="{_f(LEG * k + 1)}" height="2.6" fill="#fff"/>')
    fl, ft = FIT_L * k, FIT_T * k
    P_(c, [(bx1, oy), (bx1 + fl, oy), (bx1 + fl, oy - ft), (bx1 + ft, oy - ft), (bx1 + ft, oy - fl), (bx1, oy - fl)], fill=GREY["light"])
    xi = bx1 - T * k
    P_(c, [(xi, oy), (xi - fl, oy), (xi - fl, oy - ft), (xi - ft, oy - ft), (xi - ft, oy - fl), (xi, oy - fl)], fill=GREY["light"])
    for hh in FIT_H:
        for xx in (bx1 + hh * k, xi - hh * k):
            R_(c, xx - 1.9, oy - ft - 2.2, 3.8, ft + T * k + 4.4, fill="#fff", lw="thin")
        R_(c, xi - ft - 2.2, oy - hh * k - 1.9, ft * 2 + T * k + 4.4, 3.8, fill="#fff", lw="thin")
    leader(c, 118, 30, bx1 + fl * 0.75, oy - ft - 0.3, "outside fitting: far-end side", size=3.2)
    leader(c, 52, 30, xi - fl * 0.75, oy - ft - 0.3, "inside fitting: wall side", size=3.2, anchor="end")
    T_(c, 52, 34.2, "(over B's flat leg)", size=3.2, anchor="end")
    T_(c, bx1 + 3, btop + 3, "rail B", size=3.2, weight="bold")
    T_(c, 118, 48, "check 90° with the", size=3.2)
    T_(c, 118, 52.2, "combination square", size=3.2)
    L_(c, 117.2, 50, bx1 + ft + 3, oy - ft - 3, lw="thin")
    T_(c, xa1 - 2, oy + LEG * k + 4.5, "rail A", size=3.2, weight="bold", anchor="end")
    b0 = round(DATA["railB"]["x0"] * 10 - RAILA_X0)   # 469: rail B's flat leg edge on rail A's scale
    dimh(c, bx0, bx1, oy + LEG * k + 8, "", y_from=oy + LEG * k)
    T_(c, bx1 + 3, oy + LEG * k + 8, f"B's flat leg covers {cm(b0)} to {cm(HEEL_OUT, True)} cm on rail A", size=3.2)
    T_(c, bx1 - 10, oy + LEG * k + 14, f"B's outer face on rail A's {cm(HEEL_OUT, True)} cm mark; B's end touching A: no gap", size=3.2, anchor="middle", weight="bold")
    return save(c, "05-floor.svg")


# ---------------------------------------------------------------- Fig E-9b: why both rails' holes meet without a jig
def fig_meet():
    c = Canvas(172, 132)
    k = 0.5

    def strip(x0, y0, s0, s1, title):
        X = lambda st: x0 + (st - s0) * k
        T_(c, 4, y0 - 4.5, title, size=3.2, weight="bold")
        R_(c, X(s0), y0, (s1 - s0) * k, LEG * k, fill=GREY["light"])
        L_(c, X(s0), y0, X(s1), y0, lw="heavy")
        bl = y0 + BOLT * k
        L_(c, X(s0), bl, X(s1), bl, lw="thin", dash="4 1 0.8 1")
        return X, bl

    def place(X, bl, heel, d, holes):
        fx = X(heel) if d > 0 else X(heel - FIT_L)
        R_(c, fx, bl - FIT_W * k / 2, FIT_L * k, FIT_W * k, lw="thin", dash="1.5 0.7")
        L_(c, X(heel), bl - LEG * k * 0.57 - 1.5, X(heel), bl + LEG * k * 0.43 + 1.5, lw="heavy")
        for hh in FIT_H:
            slot(c, X(heel + d * hh), bl, SLOT_L * k, SLOT_W * k, fill="none", lw="thin", dash="1 0.6")
        for b in holes:
            hole(c, X(b), bl, BO_D * k, cross=0.5)

    # 1: rail A, both placements on one strip
    X, bl = strip(10, 14, 400, 650, "1  One fitting, three placements. Rail A, vertical leg:")
    place(X, bl, HEEL_IN, -1, HOLES_AI); place(X, bl, HEEL_OUT, +1, HOLES_AO)
    yb = 14 + LEG * k
    T_(c, X(HEEL_IN) - 1.5, yb + 4, f"heel on {cm(HEEL_IN, True)} cm, legs → wall end", size=3.2, anchor="end")
    T_(c, X(HEEL_OUT) + 1.5, yb + 4, f"heel on {cm(HEEL_OUT, True)} cm, legs → far end", size=3.2)
    T_(c, X(650) + 2, 14 + 6, "slot centres", size=3.2)
    T_(c, X(650) + 2, 14 + 10.2, f"{num(FIT_H[0])} and", size=3.2)
    T_(c, X(650) + 2, 14 + 14.4, f"{num(FIT_H[1])} mm from", size=3.2)
    T_(c, X(650) + 2, 14 + 18.6, "the heel", size=3.2)
    # rail B, heel flush with the corner end
    X, bl = strip(10, 53, 0, 220, "Rail B, vertical leg:")
    L_(c, X(0), 52, X(0), 53 + LEG * k + 1, lw="heavy")
    place(X, bl, 0, +1, HOLES_BC)
    T_(c, X(0) + 1.5, 53 + LEG * k + 4, "heel flush with the corner end, legs → far end", size=3.2)
    T_(c, X(220) + 2, 53 + 6, "each pilot goes through", size=3.2)
    T_(c, X(220) + 2, 53 + 10.2, "the slot plug: dead on", size=3.2)
    T_(c, X(220) + 2, 53 + 14.4, "the slot centre", size=3.2)
    # 2: bolted corner, elevation of rail A's outer face from the knee side, rail B cut just in front of the fittings
    y0 = 98
    T_(c, 4, y0 - 6.5, "2  Bolted: each slot sits over the hole it made (rail A from the knee space, rail B cut)", size=3.2, weight="bold")
    X = lambda x: 10 + (x - 400) * k
    Z = lambda z: y0 - z * k                     # z up from the top's underside (0)
    R_(c, X(400), Z(0), 250 * k, LEG * k, fill=GREY["light"])
    INB = RAILA_Y[1] - T
    for x0, x1 in ((RAILA_Y[1], RAILA_Y[1] + FIT_L), (INB - FIT_L, INB)):
        R_(c, X(x0), Z(-BOLT + FIT_W / 2), (x1 - x0) * k, FIT_W * k, fill="#fff")
    for x, hh in [(RAILA_Y[1] + h, h) for h in FIT_H] + [(INB - h, h) for h in FIT_H]:
        slot(c, X(x), Z(-BOLT), SLOT_L * k, SLOT_W * k, fill=GREY["mid"])
        hole(c, X(x), Z(-BOLT), BO_D * k, cross=0.5)
    # rail B in section (flat leg on top, vertical leg) and the two fitting B-legs in section
    sec = [(X(DATA["railB"]["x0"] * 10), Z(0)), (X(RAILA_Y[1]), Z(0)), (X(RAILA_Y[1]), Z(-LEG)), (X(INB), Z(-LEG)), (X(INB), Z(-T)), (X(DATA["railB"]["x0"] * 10), Z(-T))]
    P_(c, sec, fill=GREY["steel"], lw="heavy"); c.hatch(sec, spacing=0.8)
    for x0 in (RAILA_Y[1], INB - FIT_T):
        pts = [(X(x0), Z(-BOLT + FIT_W / 2)), (X(x0 + FIT_T), Z(-BOLT + FIT_W / 2)), (X(x0 + FIT_T), Z(-BOLT - FIT_W / 2)), (X(x0), Z(-BOLT - FIT_W / 2))]
        P_(c, pts, fill=GREY["light"]); c.hatch(pts, spacing=0.8, angle=135)
    L_(c, X(400), Z(0), X(650), Z(0), lw="heavy")
    T_(c, X(650) + 2, Z(-6), "rail A", size=3.2, weight="bold")
    T_(c, X(650) + 2, Z(-BOLT) - 2, "slots (grey)", size=3.2)
    T_(c, X(650) + 2, Z(-BOLT) + 2.2, "over the holes", size=3.2)
    T_(c, X(RAILA_Y[1]) + 1.5, Z(-LEG) + 3.6, f"rail B's end on A, outer face on the {cm(HEEL_OUT, True)} cm mark", size=3.2)
    T_(c, X(INB - FIT_L / 2), Z(-BOLT + FIT_W / 2) + 3.4, "inside fitting", size=3.2, anchor="middle")
    T_(c, X(RAILA_Y[1] + FIT_L / 2), Z(-BOLT + FIT_W / 2) + 3.4, "outside fitting", size=3.2, anchor="middle")
    return save(c, "05-meet.svg")


if __name__ == "__main__":
    os.makedirs(FIG, exist_ok=True)
    for f in (fig_length, fig_section, fig_railA, fig_railB, fig_stations, fig_gauge, fig_jig, fig_placement, fig_plug, fig_meet, fig_floor):
        print(f())
