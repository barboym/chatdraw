import pytest
from chatdraw.drawing_score.wasserstein_score import get_drawing_score
from chatdraw.sketches.svg_utils import svg_to_points
from chatdraw.sketches.tutorial_creator_sketchagent import load_tutorial
import os


@pytest.mark.skip(reason="drawing scores need to be entirely changed")
def test_get_drawing_score_identical():
    user_points = [[(0, 0), (1, 1), (2, 2)]]
    system_points = [[(0, 0), (1, 1), (2, 2)]]
    score = get_drawing_score(user_points, system_points)
    assert isinstance(score, float)
    assert score == 1.0

def test_get_drawing_score_stroke_count_difference():
    user_points = [[(0, 0), (1, 1)], [(2, 2), (3, 3)]]
    system_points = [[(0, 0), (1, 1)]]
    score = get_drawing_score(user_points, system_points)
    assert isinstance(score, float)
    assert score < 1.0

def test_get_drawing_score_point_distance():
    user_points = [[(0, 0), (1, 1), (2, 2)]]
    system_points = [[(0, 0), (2, 2), (4, 4)]]
    score = get_drawing_score(user_points, system_points)
    assert isinstance(score, float)
    assert score < 1.0

def test_get_drawing_score_empty_points():
    user_points = [[(50,50),(50,50)]]
    system_points = [[(0, 0)]]
    score = get_drawing_score(user_points, system_points)
    assert score == 0.0


def test_get_drawing_score_overall_shift_invariant():
    user_points = [[(10, 10), (11, 11), (12, 12)]]
    system_points = [[(0, 0), (1, 1), (2, 2)]]
    score_shifted = get_drawing_score(user_points, system_points)
    score_unshifted = get_drawing_score([[(-5, -5), (-4, -4), (-3, -3)]], [[(0, 0), (1, 1), (2, 2)]])
    assert abs(score_shifted - score_unshifted) < 1e-6
