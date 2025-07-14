


from typing import Dict, List, Tuple
from scipy.interpolate import interp1d
import re
import numpy as np 


def parse_point(s):
    s = s.strip("'")
    match = re.fullmatch(r"x(\d+)y(\d+)", s)
    if not match:
        raise ValueError(f"Invalid format: {s}")
    x, y = map(int, match.groups())
    return x, y


assert parse_point("x4y10") == (4,10)
assert parse_point("x15y25") == (15,25)

def cell_to_pixel(text,res=50,cell_size=12):
    x,y = parse_point(text)
    j,i = x-1,y-1
    img_height = (res + 1) * cell_size
    center_y = int(img_height - cell_size - (i * cell_size) - cell_size / 2)
    center_x = int(j * cell_size + cell_size / 2 + cell_size)
    return center_x,center_y

assert cell_to_pixel("x6y7",res=50,cell_size=12) == (78, 522)


def add_vectors_to_tutorial(tutorial: Dict) -> Dict:
    """
    caclulate strock vector for the tutorial 
    """
    strokes = tutorial["answer"]["strokes"]
    for el in strokes:
        pixels = []
        for p in el["points"].split(", "):

            pixels.append(cell_to_pixel(p,res=50,cell_size=12))
        el["vector"] = pixels
    return tutorial


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


def add_smooth_vectors_to_tutorial(tutorial: Dict) -> Dict:
    """
    caclulate strock vector for the tutorial 
    """
    strokes = tutorial["answer"]["strokes"]
    for el in strokes:
        el["smoothed_vector"] = make_smooth_stroke(el["vector"])
    return tutorial
