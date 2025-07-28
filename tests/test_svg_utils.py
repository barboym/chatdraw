

from chatdraw.sketches.svg_utils import svg_to_points


def test_svg_to_points_simple_path():

    svg = '''
    <svg xmlns="http://www.w3.org/2000/svg">
        <path d="M 10,20 L 30,40 L 50,60" />
    </svg>
    '''
    result = svg_to_points(svg)
    assert result == [[(10.0, 20.0), (30.0, 40.0), (50.0, 60.0)]]
