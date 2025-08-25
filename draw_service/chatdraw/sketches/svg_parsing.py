from typing import List
import xml.etree.ElementTree as ET
import re

class CommentedTreeBuilder(ET.TreeBuilder):
    """Custom TreeBuilder that preserves comments in the XML parse tree."""
    def __init__(self):
        super().__init__()

    def comment(self, data: str | None):
        self.start(ET.Comment, {})
        self.data(data if data is not None else "")
        return self.end("!--")
        

def strip_svg_fence(svg_str: str) -> str:
    """
    Strip markdown-style code fences (```svg ... ```) from an SVG string.
    Returns only the raw <svg>...</svg>.
    """
    # Remove leading/trailing whitespace
    s = svg_str.strip()

    # Regex to remove fences like ```svg ... ``` or ``` ... ```
    s = re.sub(r"^```(?:svg)?\s*", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*```$", "", s)

    return s.strip()
        
def parse_svg_steps(svg_str) -> List[dict]:
    """
    Parse an SVG file into steps defined by comments.
    Each step is a dict with {"comment": str, "elements": [XML elements]}.
    """
    parser = ET.XMLParser(target=CommentedTreeBuilder())
    root = ET.fromstring(svg_str, parser=parser)

    steps = []
    current_step = {"comment": None, "elements": []}

    for node in list(root):
        if node.tag is ET.Comment:  # comment found
            # If we already collected elements under a previous comment, store it
            if current_step["comment"] or current_step["elements"]:
                steps.append(current_step)
            # Start new step
            current_step = {"comment": str(node.text).strip(), "elements": []}
        else:
            # Normal SVG element
            current_step["elements"].append(node)

    # Append last step
    if current_step["comment"] or current_step["elements"]:
        steps.append(current_step)

    return steps




def rect_to_path(el: ET.Element) -> ET.Element:
    x = float(el.get("x", 0))
    y = float(el.get("y", 0))
    w = float(el.get("width", 0))
    h = float(el.get("height", 0))
    rx = float(el.get("rx", 0) or 0)
    ry = float(el.get("ry", 0) or 0)

    if rx == 0 and ry == 0:
        d = f"M{x},{y} h{w} v{h} h{-w} Z"
    else:
        # Rounded rect
        d = (
            f"M{x+rx},{y} "
            f"H{x+w-rx} A{rx},{ry} 0 0 1 {x+w},{y+ry} "
            f"V{y+h-ry} A{rx},{ry} 0 0 1 {x+w-rx},{y+h} "
            f"H{x+rx} A{rx},{ry} 0 0 1 {x},{y+h-ry} "
            f"V{y+ry} A{rx},{ry} 0 0 1 {x+rx},{y} Z"
        )

    return ET.Element("path", {"d": d})


def circle_to_path(el: ET.Element) -> ET.Element:
    cx = float(el.get("cx", 0))
    cy = float(el.get("cy", 0))
    r = float(el.get("r", 0))
    d = (
        f"M{cx-r},{cy} "
        f"A{r},{r} 0 1,0 {cx+r},{cy} "
        f"A{r},{r} 0 1,0 {cx-r},{cy} Z"
    )
    return ET.Element("path", {"d": d})


def ellipse_to_path(el: ET.Element) -> ET.Element:
    cx = float(el.get("cx", 0))
    cy = float(el.get("cy", 0))
    rx = float(el.get("rx", 0))
    ry = float(el.get("ry", 0))
    d = (
        f"M{cx-rx},{cy} "
        f"A{rx},{ry} 0 1,0 {cx+rx},{cy} "
        f"A{rx},{ry} 0 1,0 {cx-rx},{cy} Z"
    )
    return ET.Element("path", {"d": d})


def line_to_path(el: ET.Element) -> ET.Element:
    x1 = float(el.get("x1", 0))
    y1 = float(el.get("y1", 0))
    x2 = float(el.get("x2", 0))
    y2 = float(el.get("y2", 0))
    d = f"M{x1},{y1} L{x2},{y2}"
    return ET.Element("path", {"d": d})


def polyline_to_path(el: ET.Element) -> ET.Element:
    points = el.get("points", "").strip()
    d = "M" + " L".join(points.split())
    return ET.Element("path", {"d": d})


def polygon_to_path(el: ET.Element) -> ET.Element:
    points = el.get("points", "").strip()
    d = "M" + " L".join(points.split()) + " Z"
    return ET.Element("path", {"d": d})


SUPPORTED_ELEMENTS = (
    "rect",
    "circle",
    "ellipse",
    "line",
    "polyline",
    "polygon",
    "path",
)

def element_to_path(el: ET.Element) -> ET.Element:
    tag = el.tag.split("}")[-1]  # strip namespace if present
    if tag == "rect":
        return rect_to_path(el)
    elif tag == "circle":
        return circle_to_path(el)
    elif tag == "ellipse":
        return ellipse_to_path(el)
    elif tag == "line":
        return line_to_path(el)
    elif tag == "polyline":
        return polyline_to_path(el)
    elif tag == "polygon":
        return polygon_to_path(el)
    elif tag == "path":
        return el  # already a path
    else:
        raise ValueError(f"unsupported element tag: {tag}")