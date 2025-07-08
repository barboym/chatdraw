
from PIL import Image
import re
import psycopg2
import dotenv
import os

def get_db_connection():
    dotenv.load_dotenv()
    conn = psycopg2.connect(f"host=my-postgres dbname=postgres user={os.environ['DB_CLIENUSER']} password={os.environ['DB_CLIENPASSWORD']}")
    return conn

def get_empty_image(width=500,height=500):
    return Image.new('RGB', (height, width), color='white')


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


def pixels_to_strokes(tutorial):
    d = [] 
    for el in tutorial:
        pixels = []
        for p in el["points"].split(", "):

            pixels.append(cell_to_pixel(p,res=50,cell_size=12))
        d.append(pixels)
    return d


# def convert_points_to_image(points_list, width=400, height=400, line_thickness=2) -> Image:
#     """
#     Converts a list of lists of points to a black and white PNG image.

#     Args:
#         points_list (list): List of lists, where each inner list contains point dictionaries with 'x' and 'y' keys.
#         width (int, optional): Width of the output image. Defaults to 400.
#         height (int, optional): Height of the output image. Defaults to 400.
#         line_thickness (int, optional): Thickness of the lines. Defaults to 2.

#     Returns:
#         Image if conversion was successful, None otherwise.
#     """
#     try:
#         from PIL import Image, ImageDraw

#         # Create a blank white image
#         img = Image.new('RGB', (width, height), color='white')
#         draw = ImageDraw.Draw(img)

#         # Draw each stroke
#         for stroke in points_list:
#             # Convert points to pixel coordinates
#             pixel_points = [(int(p[0] * width), int(p[1] * height)) for p in stroke]

#             # Draw lines connecting consecutive points
#             for i in range(len(pixel_points) - 1):
#                 draw.line([pixel_points[i], pixel_points[i + 1]], fill='black', width=line_thickness)

#         # Save the image
#         return img
#     except Exception as e:
#         print(f"Error converting points to PNG: {str(e)}")

