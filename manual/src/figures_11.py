#!/usr/bin/env python3
"""Chapter K figure: repairing a stripped screw hole (guide.html "If something goes wrong") -> manual/figures/11-*.svg.
No dimensions: the repair is glue and matchsticks, then the step's own pilot."""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from figures_09 import save, Canvas, GREY, txt  # noqa: E402


def panel(c, x0, n, caption):
    blk = [(x0, 0), (x0 + 44, 0), (x0 + 44, 18), (x0, 18)]
    c.poly(blk, fill="#fff"); c.hatch(blk, spacing=1.4)
    c.rect(x0 + 19.5, 0, 5, 12, fill="#fff", lw="thin")            # the worn hole, opening at the face
    c.circle((x0 + 4, 46), 3.4, fill="#fff"); txt(c, (x0 + 4, 46), str(n), 3.2, weight="bold")
    txt(c, (x0 + 22, -6), caption, 3.0)


def fig_screw_repair():
    c = Canvas(172, 62, scale=1.0, origin=(-2, -10), flip_y=True)
    # 1: back the screw out
    panel(c, 0, 1, "back the screw out")
    c.rect(20.5, 14, 3, 14, fill=GREY["mid"], lw="thin"); c.rect(18, 28, 8, 3, fill=GREY["mid"], lw="thin")
    c.arrow((32, 20), (32, 36), head=2.0)
    # 2: glue and matchsticks
    panel(c, 60, 2, "wood glue + matchsticks")
    c.rect(80.2, 0.5, 3.6, 11, fill=GREY["light"], lw="thin")
    for x in (80.8, 82.3):
        c.line((x, 1), (x, 30), lw="thin"); c.line((x + 1.0, 1), (x + 1.0, 30), lw="thin")
    c.arrow((92, 36), (92, 22), head=2.0)
    txt(c, (100, 40), "let it dry", 3.0, anchor="start")
    # 3: re-pilot
    panel(c, 120, 3, "re-pilot, drive the screw")
    c.rect(140.2, 0.5, 3.6, 11, fill=GREY["light"], lw="thin")
    c.rect(141.2, 4, 1.6, 30, fill="#000", lw="thin")
    c.arrow((152, 36), (152, 22), head=2.0)
    return save(c, "11-screw-repair.svg")


if __name__ == "__main__":
    print(fig_screw_repair())
