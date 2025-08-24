from typing import List, Tuple
import re
import numpy as np 
from PIL import Image, ImageDraw
from typing import List, Tuple
import xml.etree.ElementTree as ET
from svgpathtools import parse_path


DEFAULT_RES = 50 # the resolution of the svg
DEFAULT_CELL_SIZE = 12 # the pixels size of each cell


def make_smooth_stroke(draw_stroke:str) -> List[Tuple]:
    path_vec = []
    path=parse_path(draw_stroke)
    for pos in np.linspace(0,1,100):
        loc = path.point(pos)
        path_vec.append((loc.real, loc.imag))
    return path_vec


def add_smooth_vectors_to_tutorial(tutorial: dict) -> dict:
    """
    for each stroke in the tutorial parses the points to smooth vectors. 
    """
    for step in tutorial["steps"]:
        for stroke in step["strokes"]: 
            stroke["smoothed_vector"] = np.array(make_smooth_stroke(stroke["path"]))
    return tutorial


def scale_to_display(tutorial: dict) -> dict:
    """
    Adds a scaled and shifted vectors to thetutorial
    """
    root = ET.fromstring(tutorial["svg_sketch"].strip())
    width = float(root.get("width"))
    height = float(root.get("height"))
    dims = np.array([width,height])
    scale = 600/dims.max()
    shift = (600 - dims * scale) / 2
    for step in tutorial["steps"]:
        for stroke in step["strokes"]: 
            stroke["smoothed_vector_scaled"] = stroke["smoothed_vector"] * scale + shift
    return tutorial

def render_tutorial_to_pil(strokes, res=DEFAULT_RES, cell_size=DEFAULT_CELL_SIZE, line_width=2, highlighted_strokes=None):
    # Create a white background image
    size = res*cell_size
    image = Image.new('RGB', (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw all strokes
    for _, stroke in enumerate(strokes):
        points = [(point[0], point[1]) for point in stroke]
        # If this is the last stroke and highlighting is enabled
        fill=(0, 0, 0)
        draw.line(points, fill=fill, width=line_width)
    if highlighted_strokes is not None:
        for stroke in highlighted_strokes:
            fill=(0, 255, 0)
            points = [(point[0], point[1]) for point in stroke]
            draw.line(points, fill=fill, width=line_width)
    return image 


def svg_to_points(svg_content) -> List[List[Tuple[int,int]]]:
    """
    Parses SVG content and extracts paths as lists of (x, y) points.
    Returns: List of lists of points.
    """
    tree = ET.fromstring(svg_content)
    paths = []
    for elem in tree.findall('.//{http://www.w3.org/2000/svg}path'):
        d = elem.attrib.get('d', '')
        points = make_smooth_stroke(d)
        paths.append(points)
    return paths

