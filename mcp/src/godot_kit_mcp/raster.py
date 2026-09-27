"""Tiny rasterizer for greybox shapes (spec: gdd.md visual language tables)."""

import math

from .png import encode_png

Color = tuple[int, int, int, int]


def parse_color(value: str) -> Color:
    v = value.strip().lstrip("#")
    if len(v) not in (6, 8) or any(ch not in "0123456789abcdefABCDEF" for ch in v):
        raise ValueError(f"color must be #RRGGBB or #RRGGBBAA, got {value!r}")
    r, g, b = (int(v[i:i + 2], 16) for i in (0, 2, 4))
    a = int(v[6:8], 16) if len(v) == 8 else 255
    return r, g, b, a


def _inside_polygon(px: float, py: float, pts: list[tuple[float, float]]) -> bool:
    inside, j = False, len(pts) - 1
    for i, (xi, yi) in enumerate(pts):
        xj, yj = pts[j]
        if (yi > py) != (yj > py) and px <= (xj - xi) * (py - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


class Canvas:
    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height
        self.buf = bytearray(width * height * 4)

    def get(self, x: int, y: int) -> Color:
        i = (y * self.width + x) * 4
        return tuple(self.buf[i:i + 4])  # type: ignore[return-value]

    def _set(self, x: int, y: int, color: Color) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            i = (y * self.width + x) * 4
            self.buf[i:i + 4] = bytes(color)

    def fill_rect(self, x: int, y: int, w: int, h: int, color: Color) -> None:
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self._set(xx, yy, color)

    def fill_shape(self, shape: str, x: int, y: int, w: int, h: int, color: Color) -> None:
        if shape == "rect":
            self.fill_rect(x, y, w, h, color)
            return
        if shape == "circle":
            cx, cy, rx, ry = x + w / 2, y + h / 2, w / 2, h / 2
            test = lambda px, py: ((px - cx) / rx) ** 2 + ((py - cy) / ry) ** 2 <= 1.0  # noqa: E731
        elif shape == "triangle":
            pts = [(x, y), (x + w, y + h / 2), (x, y + h)]
            test = lambda px, py: _inside_polygon(px, py, pts)  # noqa: E731
        elif shape == "hexagon":
            cx, cy = x + w / 2, y + h / 2
            pts = [(cx + w / 2 * math.cos(a), cy + h / 2 * math.sin(a)) for a in (k * math.pi / 3 for k in range(6))]
            test = lambda px, py: _inside_polygon(px, py, pts)  # noqa: E731
        else:
            raise ValueError(f"unknown shape {shape!r}; use rect, circle, triangle or hexagon")
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if test(xx + 0.5, yy + 0.5):
                    self._set(xx, yy, color)

    def outline(self, color: Color) -> None:
        edge = []
        for yy in range(self.height):
            for xx in range(self.width):
                if self.get(xx, yy)[3] == 0:
                    continue
                around = [(xx + 1, yy), (xx - 1, yy), (xx, yy + 1), (xx, yy - 1)]
                if any(not (0 <= a < self.width and 0 <= b < self.height) or self.get(a, b)[3] == 0 for a, b in around):
                    edge.append((xx, yy))
        for xx, yy in edge:
            self._set(xx, yy, color)

    def png(self) -> bytes:
        return encode_png(self.width, self.height, self.buf)
