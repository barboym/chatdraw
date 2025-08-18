
import base64
from io import BytesIO


def get_db_connection():
    """Deprecated: kept for backward compatibility in tests. Use SQLAlchemy sessions instead."""
    raise RuntimeError("get_db_connection is deprecated. Use SQLAlchemy via chatdraw.db.get_session().")
    

def encode_image_to_string(image, image_format='JPEG', quality=85):
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
    if image_format.upper() == 'JPEG':
        image.save(buffer, format=image_format, quality=quality)
    else:
        image.save(buffer, format=image_format)
    # Get bytes and encode to base64
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')
 
