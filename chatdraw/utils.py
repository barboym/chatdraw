
from PIL import Image

def get_empty_image(width=500,height=500):
    return Image.new('RGB', (height, width), color='white')
