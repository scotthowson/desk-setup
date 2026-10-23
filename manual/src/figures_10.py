#!/usr/bin/env python3
"""Chapter J figures (final inspection and load testing) and the checklist icons -> manual/figures/10-*.svg.
Every number comes from manual/data.json, manual/facts.json or docs/build-manual.md step 9."""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from figures_09 import save, Canvas, GREY, F, D, OUT, txt, lines, dim, pill, zig_h, zig_v, datum, _f  # noqa: E402

LAY = F["layout_cm"]
L_OUT = [(0, 0), (2490, 0), (2490, 650), (650, 650), (650, 3140), (0, 3140)]


def desk_plan(c, alex=True, legs=False, joint=True):
    c.poly(L_OUT)
    if joint:
        c.line((0, 650), (650, 650), lw="thin")
    c.line((-30, -30), (2560, -30), lw="heavy"); c.line((-30, -30), (-30, 3200), lw="heavy")
    if alex:
        for a in ("alex1", "alex2"):
            A = LAY[a]
            c.rect(A["x"][0] * 10, A["y"][0] * 10, (A["x"][1] - A["x"][0]) * 10, (A["y"][1] - A["y"][0]) * 10, fill=GREY["light"], lw="thin", dash="3 1.5")
    if legs:
        for n, x, y, *_ in D["legs"]:
            c.circle((x * 10, y * 10), D["legPlate"] * 5, lw="thin", dash="1.5 1")


def fig_corners():
    """J-1a: the six corners where the surface height is measured."""
    s = 0.024
    x0, y0, x1, y1 = -420, -420, 2900, 3480
    c = Canvas((x1 - x0) * s, (y1 - y0) * s, scale=s, origin=(x0, y0))
    desk_plan(c)
    pos = [(-250, -250), (2730, -250), (2730, 830), (830, 830), (830, 3310), (-250, 3310)]
    for i, (p, q) in enumerate(zip(L_OUT, pos), 1):
        c.balloon(p, q, i, r=3.2)
    txt(c, (2227, 790), "ALEX 1", 3.0); txt(c, (720, 2930), "ALEX 2", 3.0, anchor="start")
    txt(c, (1250, 330), "top A", 3.0, weight="bold"); txt(c, (325, 1700), "top B", 3.0, weight="bold", rotate=-90)
    lines(c, (1000, 1500), ["back wall along the top,", "side wall on the left;", "corner 4 is the inside", "corner of the L"], 3.0)
    return save(c, "10-corners-plan.svg")


def fig_corner_elev():
    """J-1b: measure from the floor to the top face at each corner."""
    s = 0.085
    y0, z0, y1, z1 = -420, -60, 360, 1010
    c = Canvas((y1 - y0) * s, (z1 - z0) * s, scale=s, origin=(y0, z0), flip_y=True)
    c.line((-420, 0), (360, 0), lw="heavy")
    fl = [(-420, -50), (360, -50), (360, 0), (-420, 0)]; c.hatch(fl, spacing=1.4)
    top = [(-420, 802), (0, 802), (0, 830), (-420, 830)]
    c.poly(top, fill=GREY["wood"]); zig_v(c, -420, 795, 837, a=8)
    c.rect(-150, 0, 22, 802, fill="#fff", lw="thin")          # a leg near the corner, schematic
    txt(c, (-175, 400), "leg", 3.0, anchor="end")
    # tape
    c.rect(40, 0, 40, 830, fill="#fff", lw="thin")
    for z in range(50, 830, 50):
        c.line((40, z), (55 if z % 100 else 62, z), lw="thin")
    c.line((0, 830), (95, 830), lw="thin", dash="1 0.8")
    dim(c, (120, 0), (120, 830), "830 ± 3", 4, side=1)
    lines(c, (-400, 975), ["hook the tape on the floor;", "read at the top face, at the corner"], 3.0)
    txt(c, (-250, 870), "top (laminate up)", 3.0)
    txt(c, (-200, 30), "floor", 3.0)
    return save(c, "10-corner-elev.svg")


def fig_joint_level():
    """J-2: level across the joint both ways, the fingertip, and the straightedge position at the inside corner."""
    s = 0.12
    x0, y0, x1, y1 = -60, 370, 1060, 935
    c = Canvas((x1 - x0) * s, (y1 - y0) * s, scale=s, origin=(x0, y0))
    c.poly([(1000, 650), (650, 650), (650, 920)], close=False)
    c.line((0, 400), (0, 920)); c.line((-30, 400), (-30, 920), lw="heavy")
    zig_h(c, 0, 650, 920, a=8); zig_h(c, 0, 1000, 400, a=8); zig_v(c, 1000, 400, 650, a=8)
    c.line((0, 650), (650, 650), lw="thin", dash="4 1.5")
    # level 1: across the joint (along y); level 2: along the joint (along x)
    c.rect(270, 470, 50, 360, fill=GREY["light"]); c.rect(282, 630, 26, 40, fill="#fff", lw="thin")
    c.rect(80, 625, 160, 50, fill=GREY["light"]); c.rect(140, 637, 40, 26, fill="#fff", lw="thin")
    # fingertip: short double arrow across the joint
    c.arrow((470, 590), (470, 710), lw="outline", head=1.8, both=True)
    # straightedge at the inside corner
    c.rect(605, 470, 22, 360, fill="#000", lw="thin")
    txt(c, (335, 445), "1  level across the joint", 3.0, anchor="start")
    txt(c, (60, 720), "2  level along it", 3.0, anchor="start")
    lines(c, (350, 735), ["3  fingertip:", "no step"], 3.0)
    lines(c, (700, 700), ["4  straightedge", "at the inside", "corner (check 5)"], 3.0)
    c.leader((627, 760), (695, 700), "", 3)
    txt(c, (800, 520), "top A", 3.2, weight="bold"); txt(c, (150, 850), "top B", 3.2, weight="bold")
    txt(c, (40, 600), "joint y = 650", 3.0, anchor="start")
    return save(c, "10-joint-level.svg")


def fig_load_plan():
    """J-3a: plan of the corner load test: 20 kg on top B's inside corner, 100 in from both edges; straightedge from L1."""
    s = 0.065
    x0, y0, x1, y1 = -90, -90, 1120, 1260
    c = Canvas((x1 - x0) * s, (y1 - y0) * s, scale=s, origin=(x0, y0))
    c.poly([(0, 1200), (0, 0), (1080, 0)], close=False)
    c.poly([(1080, 650), (650, 650), (650, 1200)], close=False)
    zig_v(c, 1080, 0, 650, a=14); zig_h(c, 0, 650, 1200, a=14)
    c.line((-30, -30), (1100, -30), lw="heavy"); c.line((-30, -30), (-30, 1220), lw="heavy")
    c.line((0, 650), (650, 650), lw="thin")
    for n, x, y, *_ in D["legs"]:
        if x * 10 < 1080 and y * 10 < 1200:
            c.circle((x * 10, y * 10), D["legPlate"] * 5, lw="thin", dash="1.5 1"); c.centre_mark((x * 10, y * 10), 1.2)
            txt(c, (x * 10 - 95, y * 10 + 95), n, 3.0, weight="bold") if n == "L1" else txt(c, (x * 10 + 70, y * 10 - 60), n, 3.0, weight="bold")
    # the case: its corner-side faces 100 in from top B's front edge and from the joint (schematic size)
    cx1, cy0 = 550, 750
    c.rect(cx1 - 260, cy0, 260, 340, fill=GREY["mid"])
    txt(c, (cx1 - 130, cy0 + 170), "20 kg", 3.2, weight="bold")
    dim(c, (cx1, 1060), (650, 1060), "", 0)
    txt(c, (670, 1060), "100", 3.0, anchor="start")
    dim(c, (300, 650), (300, cy0), "100", 0, side=-1, gap=3.0)
    # straightedge from over L1 across the corner
    a = (150, 420); b = (760, 700)
    ux, uy = (b[0] - a[0]), (b[1] - a[1]); L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
    w = 14
    c.poly([(a[0] - uy * w, a[1] + ux * w), (b[0] - uy * w, b[1] + ux * w), (b[0] + uy * w, b[1] - ux * w), (a[0] + uy * w, a[1] - ux * w)], fill="#000", lw="thin")
    c.balloon((650, 650), (820, 520), "R", r=3.2)
    lines(c, (670, 800), ["R: read the drop", "here, at the inside", "corner, beside", "the case"], 3.0)
    lines(c, (140, 230), ["straightedge from", "over leg L1's line"], 3.0)
    txt(c, (800, 300), "top A", 3.2, weight="bold"); txt(c, (130, 1150), "top B", 3.2, weight="bold")
    return save(c, "10-load-plan.svg")


def fig_load_elev():
    """J-3b: elevation along the straightedge: flat over L1, gap opening toward the loaded corner (exaggerated)."""
    s = 0.17
    x0, z0, x1, z1 = -120, -330, 760, 210
    c = Canvas((x1 - x0) * s, (z1 - z0) * s, scale=s, origin=(x0, z0), flip_y=True)
    # loaded top surface, drop exaggerated
    def zt(x):
        return 0 if x < 120 else -((x - 120) / 520) ** 2 * 32
    xs = [x for x in range(-100, 660, 10)]
    c.poly([(x, zt(x)) for x in xs] + [(x, zt(x) - 28) for x in reversed(xs)], fill=GREY["wood"])
    # leg L1 under the top
    c.rect(-22, -330, 44, 302, fill="#fff", lw="thin"); zig_h(c, -40, 40, -300, a=6)
    txt(c, (0, -200), "L1", 3.0, weight="bold", rotate=-90)
    # straightedge (rigid, flat on the top over L1)
    # the case and books stand beside the straightedge (drawn behind it)
    case = [(410, zt(410)), (600, zt(600)), (600, zt(600) + 130), (410, zt(410) + 130)]
    c.poly(case, fill=GREY["mid"])
    c.poly([(430, zt(410) + 130), (585, zt(600) + 130), (585, zt(600) + 160), (430, zt(410) + 160)], fill="#fff")
    c.rect(-100, 0, 760, 10, fill="#000", lw="thin")
    txt(c, (505, zt(505) + 65), "20 kg", 3.2, weight="bold")
    txt(c, (507, zt(505) + 146), "books", 3.0)
    # reading at the corner
    dim(c, (645, zt(645)), (645, 0), "", 0)
    lines(c, (670, -30), ["≤ 2", "(est. 1)"], 3.0)
    c.arrow((-60, 70), (-60, 14), head=1.8)
    txt(c, (-60, 90), "hold flat", 3.0)
    lines(c, (80, -110), ["straightedge: flat on the top over L1,", "reaching past the corner; the case", "stands beside it, not on it.", "Drop exaggerated."], 3.0)
    txt(c, (640, -70), "R", 3.2, weight="bold")
    return save(c, "10-load-elev.svg")


def fig_pad_turn():
    """J-4: a foot pad in its printed ring on the ALEX top; turn it by hand."""
    R = F["rings"]; s = 0.40
    x0, z0, x1, z1 = -80, -40, 120, 150
    c = Canvas((x1 - x0) * s, (z1 - z0) * s, scale=s, origin=(x0, z0), flip_y=True)
    H = F["feet"]["height_set_mm"]; T = F["tops"]["thickness"]
    alex = [(-70, -22), (70, -22), (70, 0), (-70, 0)]
    c.poly(alex, fill="#fff"); c.hatch(alex, spacing=1.4); zig_v(c, -70, -26, 4, a=3); zig_v(c, 70, -26, 4, a=3)
    top = [(-70, H), (70, H), (70, H + T), (-70, H + T)]
    c.poly(top, fill="#fff"); c.hatch(top, spacing=1.6); zig_v(c, -70, H - 4, H + T + 4, a=3); zig_v(c, 70, H - 4, H + T + 4, a=3)
    # ring: flange and wall (section, black)
    fo, b, w, h, ft = R["flange_od"] / 2, R["bore"] / 2, R["wall"], R["ring_h"], R["flange_t"]
    for sg in (-1, 1):
        pts = [(sg * b, 0), (sg * fo, 0), (sg * fo, ft), (sg * (b + w), ft), (sg * (b + w), h), (sg * b, h)]
        c.poly(pts, fill="#000", lw="thin")
    # foot: pad + body 50, plate on the top underside
    pd = F["feet"]["body_and_pad_diameter"] / 2; pl = F["feet"]["plate"] / 2
    c.rect(-pd, 0, 2 * pd, 12, fill=GREY["mid"])
    c.rect(-pd, 12, 2 * pd, H - 15, fill=GREY["light"])
    c.rect(-pl, H - 3, 2 * pl, 3, fill=GREY["dark"], lw="thin")
    # rotation arrow round the pad
    cx, cz, rx, rz = 0, 30, 36, 7
    pts = [(cx + rx * math.cos(t), cz + rz * math.sin(t)) for t in [math.radians(a) for a in range(200, 520, 10)]]
    c.poly(pts, close=False, lw="outline")
    x1_, y1_ = c.P(*pts[-2]); x2_, y2_ = c.P(*pts[-1]); c._head(x1_, y1_, x2_, y2_, 3.0)
    dim(c, (-pd, -8), (pd, -8), "", 0)
    dim(c, (95, 0), (95, H), "102", 0, side=1, gap=-3.2)
    c.line((pl, H), (98, H), lw="thin", dash="1 0.8"); c.line((70, 0), (98, 0), lw="thin", dash="1 0.8")
    txt(c, (0, -32), "pad ⌀50 in a ⌀51 bore", 3.0)
    c.label_box((46, -11), "ALEX top", 3.0)
    txt(c, (0, H + T + 9), "top (face up)", 3.0)
    lines(c, (-78, 72), ["turn the", "pad by", "hand"], 3.0)
    lines(c, (32, 72), ["foot P09"], 3.0)
    lines(c, (40, 22), ["ring P10"], 3.0)
    c.leader((28, 6), (38, 22), "", 3)
    return save(c, "10-pad-turn.svg")


def fig_joint_step():
    """J-5: section across the joint at the inside corner: straightedge across, measure any step (exaggerated)."""
    s = 0.3
    y0, z0, y1, z1 = 430, -40, 1000, 66
    c = Canvas((y1 - y0) * s, (z1 - z0) * s, scale=s, origin=(y0, z0), flip_y=True)
    T = F["tops"]["thickness"]; st = 10  # drawn step, exaggerated
    a = [(450, 0), (650, 0), (650, T), (450, T)]; b = [(650, -st), (860, -st), (860, T - st), (650, T - st)]
    for p in (a, b):
        c.poly(p, fill="#fff"); c.hatch(p, spacing=1.5)
    zig_v(c, 450, -4, T + 4, a=4); zig_v(c, 860, -st - 4, T - st + 4, a=4)
    c.rect(470, T, 380, 6, fill="#000", lw="thin")
    lines(c, (875, T - st / 2), ["step:", "write it", "down"], 3.0)
    c.leader((700, T - st / 2), (870, T - st / 2), "", 3)
    txt(c, (550, -18), "top A", 3.0, weight="bold"); txt(c, (760, -st - 18), "top B", 3.0, weight="bold")
    txt(c, (650, T + 22), "straightedge across the joint (step exaggerated)", 3.0)
    return save(c, "10-joint-step.svg")


def fig_push():
    """J-6: push sideways along each wall."""
    s = 0.024
    x0, y0, x1, y1 = -260, -260, 2760, 3330
    c = Canvas((x1 - x0) * s, (y1 - y0) * s, scale=s, origin=(x0, y0))
    desk_plan(c)
    c.arrow((1000, 820), (1700, 820), lw="heavy", head=3); c.arrow((1700, 820), (1000, 820), lw="heavy", head=3)
    c.arrow((820, 1500), (820, 2200), lw="heavy", head=3); c.arrow((820, 2200), (820, 1500), lw="heavy", head=3)
    lines(c, (1000, 990), ["push along the back wall"], 3.0)
    lines(c, (950, 1850), ["push along", "the side wall"], 3.0)
    lines(c, (1000, 2500), ["sway at the top:", "a few mm at most;", "no top moves", "on its ALEX (grey)"], 3.0)
    return save(c, "10-push.svg")


def fig_knee():
    """J-7: section through the front of top A at rail A: rail lower edge 751 from the floor, 120 back from the edge."""
    s = 0.095
    y0, z0, y1, z1 = 180, -50, 1010, 950
    c = Canvas((y1 - y0) * s, (z1 - z0) * s, scale=s, origin=(y0, z0), flip_y=True)
    c.line((180, 0), (960, 0), lw="heavy")
    fl = [(180, -40), (960, -40), (960, 0), (180, 0)]; c.hatch(fl, spacing=1.4)
    U = F["heights_mm"]["underside"]; T = F["tops"]["thickness"]; leg = F["steel"]["leg"]; th = F["steel"]["thickness"]
    top = [(200, U), (650, U), (650, U + T), (200, U + T)]
    c.poly(top, fill=GREY["wood"]); zig_v(c, 200, U - 6, U + T + 6, a=10)
    ry = LAY["rails"]["A"]["y"][1] * 10
    ang = [(ry - leg, U), (ry, U), (ry, U - leg), (ry - th, U - leg), (ry - th, U - th), (ry - leg, U - th)]
    c.poly(ang, fill="#000", lw="thin")
    dim(c, (900, 0), (900, U + T), "830", 4, side=1)
    dim(c, (760, 0), (760, U - leg), "751", 4, side=1)
    c.line((ry, U - leg), (775, U - leg), lw="thin", dash="1 0.8"); c.line((650, U + T), (915, U + T), lw="thin", dash="1 0.8")
    dim(c, (ry, U + T + 40), (650, U + T + 40), "120", 0, side=-1, gap=3.0)
    c.line((650, U + T), (650, U + T + 50), lw="thin", dash="1 0.8"); c.line((ry, U), (ry, U + T + 50), lw="thin", dash="1 0.8")
    lines(c, (220, 630), ["rail A in section", "(vertical leg hangs", "under the top)"], 3.0)
    c.leader((ry - 20, U - 20), (300, 665), "", 3)
    lines(c, (300, 400), ["knee space:", "nothing in reach", "of a knee or thigh"], 3.0)
    txt(c, (560, 30), "floor", 3.0)
    txt(c, (690, U + T + 40), "front edge", 3.0, anchor="start")
    return save(c, "10-knee.svg")


# ---- checklist icons (12 x 12 mm) ----
def icon(name, draw):
    c = Canvas(12, 12)
    draw(c)
    return save(c, f"10-icon-{name}.svg")


def _tape(c):
    c.rect(1, 3, 6.5, 6.5, rx=0, lw="outline"); c.circle((4.25, 6.25), 1.6, lw="thin")
    c.rect(7.5, 7.3, 4, 3.0, lw="thin")
    for x in (8.5, 9.5, 10.5):
        c.line((x, 7.3), (x, 8.2), lw="thin")


def _level(c):
    c.rect(0.8, 4.5, 10.4, 3.2, lw="outline"); c.rect(4.4, 5.1, 3.2, 3.0, lw="thin"); c.circle((6, 6.1), 0.6, fill="#000", lw="thin")


def _drill(c):
    c.line((1, 6), (5, 6), lw=1.4); c.poly([(5, 5), (11, 6), (5, 7)], fill="#000", lw="thin")
    for x in (6.2, 7.6, 9.0):
        c.line((x, 5.3), (x + 0.8, 6.7), lw="thin", color="#fff")


def _wrench(c):
    c.line((2.5, 9.5), (8, 4), lw=1.6)
    c.circle((9, 3), 3.0, fill="#fff", lw="outline"); c.rect(8.4, 0.2, 1.4, 3.0, fill="#fff", lw="thin")
    c.circle((2.2, 9.8), 1.4, fill="#fff", lw="outline")


def _weight(c):
    c.rect(1.5, 3.5, 9, 7, fill=GREY["mid"], lw="outline"); c.text((6, 7.2), "20", size=3.4, weight="bold")


def _calendar(c):
    c.rect(1.2, 3.0, 9.6, 8.6, lw="outline"); c.line((1.2, 4.6), (10.8, 4.6), lw="thin")
    c.line((3.8, 1), (3.8, 3.2), lw="outline"); c.line((8.2, 1), (8.2, 3.2), lw="outline")
    for x in (3, 5.2, 7.4, 9.4):
        for y in (6.4, 8.6):
            c.rect(x - 0.6, y - 0.6, 1.2, 1.2, fill="#000", lw=0.1)


def _eye(c):
    c.poly([(1, 6), (3.5, 3.6), (6, 3), (8.5, 3.6), (11, 6), (8.5, 8.4), (6, 9), (3.5, 8.4)], lw="outline")
    c.circle((6, 6), 1.8, fill="#000", lw="thin")


def _caliper(c):
    c.rect(1, 2, 10, 2, lw="outline"); c.rect(1, 4, 2, 6, lw="outline"); c.rect(6, 4, 2, 5, lw="outline"); c.rect(5.5, 1.5, 3, 3, lw="thin")


def icons():
    return [icon(n, f) for n, f in (("tape", _tape), ("level", _level), ("drill", _drill), ("wrench", _wrench),
                                       ("weight", _weight), ("calendar", _calendar), ("eye", _eye), ("caliper", _caliper))]


if __name__ == "__main__":
    for f in (fig_corners, fig_corner_elev, fig_joint_level, fig_load_plan, fig_load_elev, fig_pad_turn, fig_joint_step, fig_push, fig_knee):
        print(f())
    for p in icons():
        print(p)
