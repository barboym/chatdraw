import re
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
from pydantic import BaseModel
from typing import Any, Optional
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Enable CORS
app.add_middleware( # change in production
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    text: Optional[str] = None
    image: Optional[str] = None

def check_malicious_code(text: str) -> bool:
    # Check for potential script tags or suspicious patterns
    suspicious_patterns = [
        r'<script.*?>',
        r'javascript:',
        r'eval\(',
        r'document\.cookie',
        r'window\.location',
        r'fetch\(',
        r'exec\(',
        r'system\(',
    ]

    for pattern in suspicious_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

@app.post("/process", response_model=ChatMessage)
async def process(
    message: ChatMessage
) -> Any:
    # return message
    text = message.text
    image = message.image
    # Check that either text or image is provided, but not both
    if (text is None and image is None) or (text is not None and image is not None):
        raise HTTPException(
            status_code=400,
            detail="You must provide either text or an image, but not both or neither"
        )

    
    response = None 
    # Process text
    if text is not None:
        # Check text length
        if len(text) > 200:
            raise HTTPException(
                status_code=400,
                detail="Text must not exceed 200 characters"
            )

        # Check for malicious code
        if check_malicious_code(text):
            raise HTTPException(
                status_code=400,
                detail="Potentially unsafe content detected in text"
            )

        # Process the text (here we just echo it back)
        response = ChatMessage(text = f"Processed text: {text}")

    # Process image
    if image is not None:
        try:
            contents = await image.read()
            img = Image.open(io.BytesIO(contents))

            # Check if it's a PNG
            if img.format != "PNG":
                raise HTTPException(
                    status_code=400,
                    detail="Image must be in PNG format"
                )

            # Check if width is 200px
            if img.width != 200:
                raise HTTPException(
                    status_code=400,
                    detail=f"Image width must be 200px (got {img.width}px)"
                )

            # Process the image (here we just echo it back as base64)
            import base64
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            response = ChatMessage(text = "Image processed successfully",mage_data = img_str)

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error processing image: {str(e)}"
            )

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
