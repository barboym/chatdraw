import re
from fastapi import FastAPI, HTTPException
from typing import Any
from fastapi.staticfiles import StaticFiles

from chatdraw.chatflows.chat_system import ChatMessage, ChatResponse, ChatHandler
from chatdraw.chatflows.drawtutorial import DrawingProject


chat_handler = ChatHandler("greeting_start")
chat_handler.register_project("greeting",DrawingProject())

app = FastAPI()

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


@app.post("/", response_model=ChatResponse)
async def send(
    message: ChatMessage
) -> Any:
    if check_malicious_code(message.message.content) or check_malicious_code(message.context):
        raise HTTPException(
            status_code=400,
            detail="Potentially unsafe content detected in text"
        )
    return chat_handler.process_message(message)

app.mount("/", StaticFiles(directory='dist', html=True), name='static')

