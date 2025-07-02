import re
from fastapi import FastAPI, HTTPException
from PIL import Image
import io
from pydantic import BaseModel
from typing import Any
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from enum import Enum

app = FastAPI()

# Enable CORS
app.add_middleware( # change in production
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageType(Enum):
    TEXT = "text"
    IMAGE = "image"

class ChatMessage(BaseModel):
    type: MessageType
    data: str

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
    # Process message based on type
    if message.type == MessageType.TEXT:
        # Check text length
        if len(message.data) > 200:
            raise HTTPException(
                status_code=400,
                detail="Text must not exceed 200 characters"
            )

        # Check for malicious code
        if check_malicious_code(message.data):
            raise HTTPException(
                status_code=400,
                detail="Potentially unsafe content detected in text"
            )

        # Process the text (here we just echo it back)
        return ChatMessage(type=MessageType.TEXT, data=f"Processed text: {message.data}")

    elif message.type == MessageType.IMAGE:
        try:
            # Decode base64 image
            import base64
            image_data = base64.b64decode(message.data)
            img = Image.open(io.BytesIO(image_data))

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

            # Process the image (here we just echo it back with a message)
            return ChatMessage(type=MessageType.TEXT, data="Image processed successfully")

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error processing image: {str(e)}"
            )

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid message type"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
