"""Minimal SVG drawing library for the assembly manual. Units are millimetres on the page.

    from lib.draw import Canvas
    c = Canvas(180, 120)                      # page-mm wide x tall; viewBox is in the same mm
    c.rect(10, 10, 60, 40); c.dim((10, 55), (70, 55), "60")
    c.save("figures/example.svg")

Conventions (IKEA-style): black outlines 0.5, hidden/dim lines 0.25, dimension text 3.2 mm, no colour
needed for meaning (grey fills only), callout balloons numbered from the parts inventory.
Everything is plain functions that append SVG strings; drawings are deterministic, so figure files
can be regenerated from the data files at any time.
"""
import math

LW = {"outline": 0.5, "thin": 0.25, "dim": 0.25, "hidden": 0.25, "heavy": 0.8}
GREY = {"light": "#e6e6e6", "mid": "#bfbfbf", "dark": "#808080", "steel": "#d9d9d9", "wood": "#f2f2f2"}
FONT = "Helvetica, Arial, sans-serif"


def _f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


class Canvas:
    def __init__(self, w, h, scale=1.0, origin=(0, 0), flip_y=False):
        """w, h: drawing size in page mm. scale: drawing units per page mm are 1/scale (scale=0.1 means 10 mm of
        object per 1 mm of page). origin: object coords placed at page (0,0). flip_y: object y up on the page."""
        self.w, self.h = w, h
        self.scale = scale
        self.ox, self.oy = origin
        self.flip = flip_y
        self.parts = []
        self.defs = set()

    # ---- coordinate mapping ----
    def P(self, x, y):
        px = (x - self.ox) * self.scale
        py = (y - self.oy) * self.scale
        if self.flip:
            py = self.h - py
        return px, py

    def _pt(self, p):
        return self.P(*p)

    # ---- primitives (object coordinates) ----
    def line(self, p1, p2, lw="outline", dash=None, color="#000"):
        x1, y1 = self._pt(p1); x2, y2 = self._pt(p2)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}" stroke="{color}" stroke-width="{LW.get(lw, lw)}"{d} stroke-linecap="round"/>')

    def poly(self, pts, fill="none", lw="outline", close=True, dash=None, color="#000"):
        d = " ".join(f"{_f(px)},{_f(py)}" for px, py in (self._pt(p) for p in pts))
        tag = "polygon" if close else "polyline"
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<{tag} points="{d}" fill="{fill}" stroke="{color}" stroke-width="{LW.get(lw, lw)}"{da} stroke-linejoin="round"/>')

    def rect(self, x, y, w, h, fill="none", lw="outline", dash=None, rx=0):
        """x, y is the object corner with the smaller coordinates."""
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill=fill, lw=lw, dash=dash) if rx == 0 else self._rrect(x, y, w, h, fill, lw, rx)

    def _rrect(self, x, y, w, h, fill, lw, rx):
        px, py = self._pt((x, y)); px2, py2 = self._pt((x + w, y + h))
        X, Y = min(px, px2), min(py, py2); W, H = abs(px2 - px), abs(py2 - py)
        self.parts.append(f'<rect x="{_f(X)}" y="{_f(Y)}" width="{_f(W)}" height="{_f(H)}" rx="{_f(rx * self.scale)}" fill="{fill}" stroke="#000" stroke-width="{LW.get(lw, lw)}"/>')

    def circle(self, c, r, fill="none", lw="outline", dash=None):
        px, py = self._pt(c)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<circle cx="{_f(px)}" cy="{_f(py)}" r="{_f(r * self.scale)}" fill="{fill}" stroke="#000" stroke-width="{LW.get(lw, lw)}"{d}/>')

    def hole(self, c, d, cross=True):
        """Drilled hole symbol: circle plus centre mark."""
        self.circle(c, d / 2)
        if cross:
            m = max(d * 0.9, 2.5 / self.scale)
            self.line((c[0] - m, c[1]), (c[0] + m, c[1]), lw="thin")
            self.line((c[0], c[1] - m), (c[0], c[1] + m), lw="thin")

    def text(self, p, s, size=3.2, anchor="middle", weight="normal", rotate=0, color="#000", baseline="middle"):
        px, py = self._pt(p)
        rot = f' transform="rotate({rotate} {_f(px)} {_f(py)})"' if rotate else ""
        s = s.replace("&", "&amp;").replace("<", "&lt;")
        self.parts.append(f'<text x="{_f(px)}" y="{_f(py)}" font-family="{FONT}" font-size="{size}" text-anchor="{anchor}" dominant-baseline="{baseline}" font-weight="{weight}" fill="{color}"{rot}>{s}</text>')

    def hatch(self, pts, spacing=1.5, angle=45):
        """Section hatching inside a polygon (page-space clip)."""
        Canvas._hid = getattr(Canvas, '_hid', 0) + 1
        hid = f"h{id(self) % 100000}_{Canvas._hid}"   # unique even when several SVGs are inlined into one page
        d = " ".join(f"{_f(px)},{_f(py)}" for px, py in (self._pt(p) for p in pts))
        xs = [self._pt(p)[0] for p in pts]; ys = [self._pt(p)[1] for p in pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        L = (x1 - x0) + (y1 - y0)
        lines = []
        t = -L
        while t < 2 * L:
            if angle == 45:
                lines.append(f'<line x1="{_f(x0 + t)}" y1="{_f(y0)}" x2="{_f(x0 + t + (y1 - y0))}" y2="{_f(y1)}" stroke="#000" stroke-width="0.2"/>')
            else:
                lines.append(f'<line x1="{_f(x0 + t)}" y1="{_f(y1)}" x2="{_f(x0 + t + (y1 - y0))}" y2="{_f(y0)}" stroke="#000" stroke-width="0.2"/>')
            t += spacing
        self.parts.append(f'<clipPath id="{hid}"><polygon points="{d}"/></clipPath><g clip-path="url(#{hid})">{"".join(lines)}</g>')

    # ---- annotation ----
    def arrow(self, p1, p2, lw="outline", head=1.8, both=False):
        """Arrow from p1 to p2 (page-space heads)."""
        x1, y1 = self._pt(p1); x2, y2 = self._pt(p2)
        self.parts.append(f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}" stroke="#000" stroke-width="{LW.get(lw, lw)}"/>')
        self._head(x1, y1, x2, y2, head)
        if both:
            self._head(x2, y2, x1, y1, head)

    def _head(self, x1, y1, x2, y2, head):
        a = math.atan2(y2 - y1, x2 - x1)
        pts = [(x2, y2), (x2 - head * math.cos(a - 0.35), y2 - head * math.sin(a - 0.35)), (x2 - head * math.cos(a + 0.35), y2 - head * math.sin(a + 0.35))]
        self.parts.append('<polygon points="' + " ".join(f"{_f(x)},{_f(y)}" for x, y in pts) + '" fill="#000"/>')

    def dim(self, p1, p2, label, offset=0, size=3.2, ext=True, side=1):
        """Linear dimension between object points p1 and p2, drawn offset (page mm) perpendicular; label centred."""
        x1, y1 = self._pt(p1); x2, y2 = self._pt(p2)
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L * side, dx / L * side
        ox, oy = nx * offset, ny * offset
        a1 = (x1 + ox, y1 + oy); a2 = (x2 + ox, y2 + oy)
        if ext and offset:
            e = 1.5
            self.parts.append(f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(a1[0] + nx * e)}" y2="{_f(a1[1] + ny * e)}" stroke="#000" stroke-width="{LW["dim"]}"/>')
            self.parts.append(f'<line x1="{_f(x2)}" y1="{_f(y2)}" x2="{_f(a2[0] + nx * e)}" y2="{_f(a2[1] + ny * e)}" stroke="#000" stroke-width="{LW["dim"]}"/>')
        self.parts.append(f'<line x1="{_f(a1[0])}" y1="{_f(a1[1])}" x2="{_f(a2[0])}" y2="{_f(a2[1])}" stroke="#000" stroke-width="{LW["dim"]}"/>')
        self._head(a2[0], a2[1], a1[0], a1[1], 1.6); self._head(a1[0], a1[1], a2[0], a2[1], 1.6)
        ang = math.degrees(math.atan2(dy, dx))
        if ang > 90 or ang < -90:
            ang += 180
        s_out = 1 if offset >= 0 else -1          # the label sits beside the line, on the side away from the object
        gap = size * 0.75
        tx, ty = (a1[0] + a2[0]) / 2 + nx * gap * s_out, (a1[1] + a2[1]) / 2 + ny * gap * s_out
        self.parts.append(f'<text x="{_f(tx)}" y="{_f(ty)}" font-family="{FONT}" font-size="{size}" text-anchor="middle" dominant-baseline="middle" transform="rotate({_f(ang)} {_f(tx)} {_f(ty)})">{label}</text>')

    def leader(self, p_target, p_text, label, size=3.2, anchor="start"):
        """Leader line from a text position to a target point, with a dot at the target."""
        self.arrow(p_text, p_target, lw="thin", head=1.4)
        tx, ty = self._pt(p_text)
        self.parts.append(f'<text x="{_f(tx + (1.5 if anchor == "start" else -1.5))}" y="{_f(ty)}" font-family="{FONT}" font-size="{size}" text-anchor="{anchor}" dominant-baseline="middle">{label}</text>')

    def balloon(self, p_target, p_balloon, number, r=3.6):
        """IKEA-style numbered callout: circle with the part number and a leader to the part."""
        x1, y1 = self._pt(p_balloon); x2, y2 = self._pt(p_target)
        self.parts.append(f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}" stroke="#000" stroke-width="{LW["thin"]}"/>')
        self.parts.append(f'<circle cx="{_f(x2)}" cy="{_f(y2)}" r="0.7" fill="#000"/>')
        self.parts.append(f'<circle cx="{_f(x1)}" cy="{_f(y1)}" r="{r}" fill="#fff" stroke="#000" stroke-width="{LW["outline"]}"/>')
        self.parts.append(f'<text x="{_f(x1)}" y="{_f(y1)}" font-family="{FONT}" font-size="{3.0 if len(str(number)) < 4 else 2.4}" text-anchor="middle" dominant-baseline="middle" font-weight="bold">{number}</text>')

    def centre_mark(self, c, size=3):
        s = size / self.scale
        self.line((c[0] - s, c[1]), (c[0] + s, c[1]), lw="thin")
        self.line((c[0], c[1] - s), (c[0], c[1] + s), lw="thin")

    def centreline(self, p1, p2):
        self.line(p1, p2, lw="thin", dash="4 1 0.8 1")

    def label_box(self, p, s, size=3.2, pad=1.2, weight="normal"):
        """Text in a white box (page-space), useful over hatching."""
        px, py = self._pt(p)
        w = len(s) * size * 0.56 + 2 * pad; h = size + 2 * pad
        self.parts.append(f'<rect x="{_f(px - w / 2)}" y="{_f(py - h / 2)}" width="{_f(w)}" height="{_f(h)}" fill="#fff" stroke="none"/>')
        self.parts.append(f'<text x="{_f(px)}" y="{_f(py)}" font-family="{FONT}" font-size="{size}" text-anchor="middle" dominant-baseline="middle" font-weight="{weight}">{s}</text>')

    # ---- isometric helper (object x, y, z in object units -> object 2D used with P) ----
    @staticmethod
    def iso(x, y, z, angle=30):
        """Standard isometric: x goes right-down, y goes right-up (into the page), z up. Returns 2D (u, v) with v up."""
        a = math.radians(angle)
        u = (x - y) * math.cos(a)
        v = (x + y) * math.sin(a) + z
        return u, v

    def iso_box(self, x, y, z, dx, dy, dz, fill=("#fff", "#e6e6e6", "#cccccc"), lw="outline"):
        """Draw a box in isometric projection; self must have flip_y=True and object coords = iso (u, v)."""
        I = self.iso
        top = [I(x, y, z + dz), I(x + dx, y, z + dz), I(x + dx, y + dy, z + dz), I(x, y + dy, z + dz)]
        front = [I(x, y, z), I(x + dx, y, z), I(x + dx, y, z + dz), I(x, y, z + dz)]
        side = [I(x + dx, y, z), I(x + dx, y + dy, z), I(x + dx, y + dy, z + dz), I(x + dx, y, z + dz)]
        self.poly(top, fill=fill[0], lw=lw); self.poly(front, fill=fill[1], lw=lw); self.poly(side, fill=fill[2], lw=lw)

    # ---- output ----
    def raw(self, svg):
        self.parts.append(svg)

    def svg(self, inline=True):
        body = "\n".join(self.parts)
        attrs = f'xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_f(self.w)} {_f(self.h)}" width="{_f(self.w)}mm" height="{_f(self.h)}mm"'
        return f'<svg {attrs} class="fig">\n{body}\n</svg>'

    def save(self, path):
        with open(path, "w") as f:
            f.write(self.svg())
        return path


def warning_panel(text, kind="MEASURE BEFORE DRILLING"):
    """HTML snippet for a caution panel; kind is the bold heading."""
    return f'<div class="warn"><span class="warn-icon">!</span><div><b>{kind}</b><br>{text}</div></div>'


def badge(kind):
    """Confidence label HTML: VERIFIED, SOURCE, MEASURE, ASSUMPTION."""
    k = {"VERIFIED": "VERIFIED", "SOURCE": "SOURCE-DEFINED", "MEASURE": "MEASURE ON HARDWARE", "ASSUMPTION": "ASSUMPTION / FIELD CHECK"}[kind]
    return f'<span class="badge badge-{kind.lower()}">{k}</span>'
