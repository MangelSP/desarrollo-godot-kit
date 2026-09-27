import pytest

from godot_kit_mcp.png import decode_png, encode_png
from godot_kit_mcp.raster import Canvas, parse_color


def test_png_round_trip():
    rgba = bytes([255, 0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 255, 0, 0, 0, 0])
    data = encode_png(2, 2, rgba)
    assert data.startswith(b"\x89PNG\r\n\x1a\n")
    assert decode_png(data) == (2, 2, rgba)


def test_png_rejects_bad_buffer():
    with pytest.raises(ValueError):
        encode_png(2, 2, b"\x00" * 3)


def test_parse_color():
    assert parse_color("#FFD23F") == (255, 210, 63, 255)
    assert parse_color("#11223380") == (17, 34, 51, 128)
    with pytest.raises(ValueError):
        parse_color("yellow")


def test_triangle_points_right():
    c = Canvas(24, 16)
    c.fill_shape("triangle", 0, 0, 24, 16, parse_color("#FFD23F"))
    assert c.get(2, 8)[3] == 255      # base, middle
    assert c.get(22, 8)[3] == 255     # tip
    assert c.get(22, 1)[3] == 0       # outside near the tip
    assert c.get(0, 0)[3] == 0 or c.get(0, 0)[3] == 255  # corner is on the edge, either is fine


def test_circle_and_outline():
    c = Canvas(10, 10)
    c.fill_shape("circle", 0, 0, 10, 10, parse_color("#111111"))
    assert c.get(5, 5) == (17, 17, 17, 255)
    assert c.get(0, 0)[3] == 0
    c.outline(parse_color("#FFFFFF"))
    assert c.get(5, 0) == (255, 255, 255, 255)  # top edge becomes outline
    assert c.get(5, 5) == (17, 17, 17, 255)     # inside unchanged


def test_canvas_png_has_size():
    c = Canvas(3, 5)
    c.fill_rect(0, 0, 3, 5, parse_color("#5C5F66"))
    w, h, rgba = decode_png(c.png())
    assert (w, h) == (3, 5) and rgba[:4] == bytes([92, 95, 102, 255])
