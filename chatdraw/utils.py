
from PIL import Image

def get_empty_image(width=500,height=500):
    return Image.new('RGB', (height, width), color='white')


def convert_points_to_image(points_list, width=400, height=400, line_thickness=2) -> Image:
    """
    Converts a list of lists of points to a black and white PNG image.

    Args:
        points_list (list): List of lists, where each inner list contains point dictionaries with 'x' and 'y' keys.
        width (int, optional): Width of the output image. Defaults to 400.
        height (int, optional): Height of the output image. Defaults to 400.
        line_thickness (int, optional): Thickness of the lines. Defaults to 2.

    Returns:
        Image if conversion was successful, None otherwise.
    """
    try:
        from PIL import Image, ImageDraw

        # Create a blank white image
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)

        # Draw each stroke
        for stroke in points_list:
            # Convert points to pixel coordinates
            pixel_points = [(int(p[0] * width), int(p[1] * height)) for p in stroke]

            # Draw lines connecting consecutive points
            for i in range(len(pixel_points) - 1):
                draw.line([pixel_points[i], pixel_points[i + 1]], fill='black', width=line_thickness)

        # Save the image
        return img
    except Exception as e:
        print(f"Error converting points to PNG: {str(e)}")

