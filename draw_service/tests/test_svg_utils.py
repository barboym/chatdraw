

from chatdraw.sketches.svg_utils import svg_to_points
from chatdraw.sketches import svg_utils
import pytest


def test_parse_point_valid():
    assert svg_utils.parse_point("x4y10") == (4, 10)
    assert svg_utils.parse_point("x15y25") == (15, 25)

def test_parse_point_invalid():
    with pytest.raises(ValueError):
        svg_utils.parse_point("4y10")
    with pytest.raises(ValueError):
        svg_utils.parse_point("x4z10")
    with pytest.raises(ValueError):
        svg_utils.parse_point("x4y")

def test_cell_to_pixel():
    # Using default res=50, cell_size=12
    assert svg_utils.cell_to_pixel("x6y7") == (78, 522)
    # Test with different values
    assert svg_utils.cell_to_pixel("x1y1", res=10, cell_size=10) == (15, 95)

def test_parse_point_string_to_vector_multiple():
    points_str = "x1y1 x2y2 x3y3"
    result = svg_utils.parse_point_string_to_vector(points_str, res=10, cell_size=10)
    assert isinstance(result, list)
    assert len(result) == 3
    assert all(isinstance(pt, tuple) and len(pt) == 2 for pt in result)

def test_parse_point_string_to_vector_single():
    points_str = "x1y1"
    result = svg_utils.parse_point_string_to_vector(points_str, res=10, cell_size=10)
    assert isinstance(result, list)
    assert len(result) == 5
    assert all(isinstance(pt, tuple) and len(pt) == 2 for pt in result)

def test_make_smooth_stroke_short():
    # 1 point
    pts = [(1, 2)]
    assert svg_utils.make_smooth_stroke(pts) == pts
    # 2 points
    pts = [(1, 2), (3, 4)]
    assert svg_utils.make_smooth_stroke(pts) == pts

def test_make_smooth_stroke_quadratic():
    pts = [(0, 0), (5, 10), (10, 0)]
    smoothed = svg_utils.make_smooth_stroke(pts)
    assert isinstance(smoothed, list)
    assert len(smoothed) == 100
    assert all(isinstance(pt, tuple) and len(pt) == 2 for pt in smoothed)

def test_make_smooth_stroke_cubic():
    pts = [(0, 0), (5, 10), (10, 0), (15, 5)]
    smoothed = svg_utils.make_smooth_stroke(pts)
    assert isinstance(smoothed, list)
    assert len(smoothed) == 100

def test_add_smooth_vectors_to_tutorial():
    tutorial = [
        {"strokes": [{"points": "x1y1 x2y2"}]},
        {"strokes": [{"points": "x3y3 x4y4"}]}
    ]
    result = svg_utils.add_smooth_vectors_to_tutorial(tutorial)
    for step in result:
        for stroke in step["strokes"]:
            assert "vector" in stroke
            assert "smoothed_vector" in stroke
            assert isinstance(stroke["vector"], list)
            assert isinstance(stroke["smoothed_vector"], list)

def test_render_tutorial_to_pil_basic():
    strokes = [[(10, 10), (20, 20)], [(30, 30), (40, 40)]]
    img = svg_utils.render_tutorial_to_pil(strokes, res=10, cell_size=10)
    assert img.size == (100, 100)
    assert img.mode == "RGB"

def test_render_tutorial_to_pil_highlighted():
    strokes = [[(10, 10), (20, 20)]]
    highlighted = [[(30, 30), (40, 40)]]
    img = svg_utils.render_tutorial_to_pil(strokes, res=10, cell_size=10, highlighted_strokes=highlighted)
    assert img.size == (100, 100)

def test_parse_path():
    d = "M 10 20 L 30 40 L 50 60"
    points = svg_utils.parse_path(d)
    assert points == [(10, 20), (30, 40), (50, 60)]

def test_svg_to_points_simple_path():
    svg = '''
    <svg xmlns="http://www.w3.org/2000/svg">
        <path d="M 10 20 L 30 40 L 50 60" />
    </svg>
    '''
    result = svg_utils.svg_to_points(svg)
    assert result == [[(10, 20), (30, 40), (50, 60)]]

def test_svg_to_points_multiple_paths():
    svg = '''
    <svg xmlns="http://www.w3.org/2000/svg">
        <path d="M 1 2 L 3 4" />
        <path d="M 5 6 L 7 8" />
    </svg>
    '''
    result = svg_utils.svg_to_points(svg)
    assert result == [[(1, 2), (3, 4)], [(5, 6), (7, 8)]]

def test_svg_to_points_no_paths():
    svg = '<svg xmlns="http://www.w3.org/2000/svg"></svg>'
    result = svg_utils.svg_to_points(svg)
    assert result == []