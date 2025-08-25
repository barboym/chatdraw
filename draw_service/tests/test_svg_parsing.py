from chatdraw.sketches.svg_parsing import parse_svg_steps, strip_svg_fence
import pytest


def test_parse_svg_steps_single_step_with_comment_and_elements():
    svg = """
    <svg>
        <!-- Step 1 -->
        <rect x="0" y="0" width="10" height="10"/>
        <circle cx="5" cy="5" r="2"/>
    </svg>
    """
    steps = parse_svg_steps(svg)
    assert len(steps) == 1
    assert steps[0]["comment"] == "Step 1"
    assert len(steps[0]["elements"]) == 2
    assert steps[0]["elements"][0].tag.endswith("rect")
    assert steps[0]["elements"][1].tag.endswith("circle")

def test_parse_svg_steps_multiple_steps():
    svg = """
    <svg>
        <!-- First -->
        <rect x="0" y="0" width="10" height="10"/>
        <!-- Second -->
        <circle cx="5" cy="5" r="2"/>
        <line x1="0" y1="0" x2="10" y2="10"/>
    </svg>
    """
    steps = parse_svg_steps(svg)
    assert len(steps) == 2
    assert steps[0]["comment"] == "First"
    assert len(steps[0]["elements"]) == 1
    assert steps[0]["elements"][0].tag.endswith("rect")
    assert steps[1]["comment"] == "Second"
    assert len(steps[1]["elements"]) == 2
    assert steps[1]["elements"][0].tag.endswith("circle")
    assert steps[1]["elements"][1].tag.endswith("line")

def test_parse_svg_steps_no_comments_all_elements_in_one_step():
    svg = """
    <svg>
        <rect x="0" y="0" width="10" height="10"/>
        <circle cx="5" cy="5" r="2"/>
    </svg>
    """
    steps = parse_svg_steps(svg)
    assert len(steps) == 1
    assert steps[0]["comment"] is None
    assert len(steps[0]["elements"]) == 2

def test_parse_svg_steps_empty_svg():
    svg = "<svg></svg>"
    steps = parse_svg_steps(svg)
    assert steps == []

def test_parse_svg_steps_comment_without_elements():
    svg = """
    <svg>
        <!-- Only a comment -->
    </svg>
    """
    steps = parse_svg_steps(svg)
    assert len(steps) == 1
    assert steps[0]["comment"] == "Only a comment"
    assert steps[0]["elements"] == []

def test_parse_svg_steps_with_code_fence():
    svg = """
    ```svg
    <svg>
        <!-- Step -->
        <rect x="0" y="0" width="10" height="10"/>
    </svg>
    ```
    """
    stripped = strip_svg_fence(svg)
    steps = parse_svg_steps(stripped)
    assert len(steps) == 1
    assert steps[0]["comment"] == "Step"
    assert steps[0]["elements"][0].tag.endswith("rect")