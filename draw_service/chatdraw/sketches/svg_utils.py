from typing import List, Tuple
from scipy.interpolate import interp1d
import re
import numpy as np 
from PIL import Image, ImageDraw
from typing import List, Tuple
import xml.etree.ElementTree as ET


DEFAULT_RES = 50 # the resolution of the svg
DEFAULT_CELL_SIZE = 12 # the pixels size of each cell


def parse_point(s):
    s = s.strip("'")
    match = re.fullmatch(r"x(\d+)y(\d+)", s)
    if not match:
        raise ValueError(f"Invalid format: {s}")
    x, y = map(int, match.groups())
    return x, y


def cell_to_pixel(text,res=DEFAULT_RES,cell_size=DEFAULT_CELL_SIZE):
    x,y = parse_point(text)
    j,i = x-1,y-1
    img_height = (res + 1) * cell_size
    center_y = int(img_height - cell_size - (i * cell_size) - cell_size / 2)
    center_x = int(j * cell_size + cell_size / 2 + cell_size)
    return center_x,center_y


def parse_point_string_to_vector(points_str:str,res=DEFAULT_RES,cell_size=DEFAULT_CELL_SIZE) -> List[Tuple[int,int]]:
    """
    caclulate strock vector for the tutorial 
    """
    pixels = []
    for p in points_str.split(" "):
        pixels.append(cell_to_pixel(p,res=res,cell_size=cell_size))
    if len(pixels)==1: # treat single point case
        pixels = list(map(tuple,(np.array(pixels*5) + np.array([[0,0],[1,0],[1,1],[0,1],[-1,-1]])).astype(int)))
    return pixels


def make_smooth_stroke(draw_stroke:List[Tuple]) -> List[Tuple]:
    n=len(draw_stroke)
    interp_method=None
    if n in [1,2]:
        return draw_stroke
    elif n==3:
        interp_method='quadratic'
    else:
        interp_method='cubic'
    draw_stroke_np = np.array(draw_stroke)
    smoothed_strokes =  np.c_[
        interp1d(np.linspace(0,1,len(draw_stroke)),draw_stroke_np[:,0],kind=interp_method)(np.linspace(0,1,100)), 
        interp1d(np.linspace(0,1,len(draw_stroke)),draw_stroke_np[:,1],kind=interp_method)(np.linspace(0,1,100))
    ]
    smoothed_strokes = smoothed_strokes.tolist()
    smoothed_strokes = list(map(tuple,smoothed_strokes))
    return smoothed_strokes


def add_smooth_vectors_to_tutorial(tutorial: List[dict]) -> List[dict]:
    """
    for each stroke in the tutorial parses the points to smooth vectors. 
    """
    for step in tutorial:
        for stroke in step["strokes"]: 
            stroke["vector"] = parse_point_string_to_vector(stroke["points"])
            stroke["smoothed_vector"] = make_smooth_stroke(stroke["vector"])
    return tutorial

def render_tutorial_to_pil(strokes, res=DEFAULT_RES, cell_size=DEFAULT_CELL_SIZE, line_width=2, highlighted_strokes=None):
    # Create a white background image
    size = res*cell_size
    image = Image.new('RGB', (size, size), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw all strokes
    for i, stroke in enumerate(strokes):
        points = [(point[0], size - point[1]) for point in stroke]
        # If this is the last stroke and highlighting is enabled
        fill=(0, 0, 0)
        draw.line(points, fill=fill, width=line_width)
    if highlighted_strokes is not None:
        for stroke in highlighted_strokes:
            fill=(0, 255, 0)
            points = [(point[0], size - point[1]) for point in stroke]
            draw.line(points, fill=fill, width=line_width)
    return image 


def parse_path(d):
    points = []
    for  x, y in zip(d.split()[1::3],d.split()[2::3]):
        points.append((int(float(x)), int(float(y))))
    return points


def svg_to_points(svg_content) -> List[List[Tuple[int,int]]]:
    """
    Parses SVG content and extracts paths as lists of (x, y) points.
    Returns: List of lists of points.
    """
    tree = ET.fromstring(svg_content)
    paths = []
    for elem in tree.findall('.//{http://www.w3.org/2000/svg}path'):
        d = elem.attrib.get('d', '')
        points = parse_path(d)
        if points:
            paths.append(points)
    return paths

