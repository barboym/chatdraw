

from chatdraw.sketches import svg_utils
import numpy as np

def test_make_smooth_stroke_returns_100_points():
    # Simple straight line path
    path = "M 0 0 L 100 100"
    points = svg_utils.make_smooth_stroke(path)
    assert isinstance(points, list)
    assert len(points) == 100
    assert all(isinstance(pt, tuple) and len(pt) == 2 for pt in points)

def test_add_smooth_vectors_to_tutorial_adds_key():
    tutorial = {
        "steps": [
            {"strokes": [{"path": "M 0 0 L 10 10"}]},
            {"strokes": [{"path": "M 5 5 L 15 15"}]}
        ]
    }
    result = svg_utils.add_smooth_vectors_to_tutorial(tutorial)
    for step in result["steps"]:
        for stroke in step["strokes"]:
            assert "smoothed_vector" in stroke
            assert isinstance(stroke["smoothed_vector"], np.ndarray)
            assert stroke["smoothed_vector"].shape == (100, 2)

def test_scale_to_display_scales_and_shifts():
    tutorial = {
        "svg_raw": '<svg width="100" height="100"></svg>',
        "steps": [
            {"strokes": [{"smoothed_vector": np.array([[0, 0], [100, 100]])}]}
        ]
    }
    result = svg_utils.scale_to_display(tutorial, res=10, cell_size=10)
    for step in result["steps"]:
        for stroke in step["strokes"]:
            assert "smoothed_vector_scaled" in stroke
            arr = stroke["smoothed_vector_scaled"]
            assert arr.shape == (2, 2)
            # Should be shifted/scaled into a 100x100 box
            assert np.all(arr >= 0)
            assert np.all(arr <= 100)

def test_scale_to_display_missing_svg_dims(monkeypatch):
    tutorial = {
        "svg_raw": '<svg></svg>',
        "steps": [
            {"strokes": [{"smoothed_vector": np.array([[0, 0], [100, 100]])}]}
        ]
    }
    result = svg_utils.scale_to_display(tutorial, res=10, cell_size=10)
    for step in result["steps"]:
        for stroke in step["strokes"]:
            assert "smoothed_vector_scaled" in stroke

def test_render_tutorial_to_pil_with_highlighted_and_multiple_strokes():
    strokes = [[(0, 0), (50, 50)], [(10, 90), (90, 10)]]
    highlighted = [[(25, 25), (75, 75)]]
    img = svg_utils.render_tutorial_to_pil(strokes, res=10, cell_size=10, highlighted_strokes=highlighted)
    assert img.size == (100, 100)
    assert img.mode == "RGB"

def test_svg_to_points_with_path():
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<path d="M 0 0 L 10 10" /></svg>'
    )
    points = svg_utils.svg_to_points(svg)
    assert isinstance(points, list)
    assert len(points) == 1
    assert isinstance(points[0], list)
    assert len(points[0]) == 100
    assert all(isinstance(pt, tuple) and len(pt) == 2 for pt in points[0])

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

def test_svg_to_points_no_paths():
    svg = '<svg xmlns="http://www.w3.org/2000/svg"></svg>'
    result = svg_utils.svg_to_points(svg)
    assert result == []