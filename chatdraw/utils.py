
from PIL import Image
import psycopg2
import dotenv
import os
import base64
from io import BytesIO

def get_db_connection():
    dotenv.load_dotenv()
    return psycopg2.connect(f"host=postgres dbname=postgres user={os.environ['DB_CLIENUSER']} password={os.environ['DB_CLIENPASSWORD']}")
    
def get_empty_image(width=500,height=500):
    return Image.new('RGB', (height, width), color='white')

def encode_image_to_string(image, format='JPEG', quality=85):
    """
    Encode a PIL image to a base64 string for REST API transmission.
    
    Args:
        image: PIL Image object
        format: Image format ('JPEG', 'PNG', 'WEBP', etc.)
        quality: Image quality for JPEG (1-100)
    
    Returns:
        str: Base64 encoded image string
    """
    # Create a BytesIO buffer
    buffer = BytesIO()
    # Save image to buffer
    if format.upper() == 'JPEG':
        image.save(buffer, format=format, quality=quality)
    else:
        image.save(buffer, format=format)
    # Get bytes and encode to base64
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')
 
# def decode_string_to_image(encoded_string):
#     """
#     Decode base64 string back to PIL image.
    
#     Args:
#         encoded_string: Base64 encoded image string
    
#     Returns:
#         PIL Image object
#     """
#     return Image.open(BytesIO(base64.b64decode(encoded_string)))
 

if __name__=="__main__":
    get_db_connection() 
