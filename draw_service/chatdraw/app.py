import re
import uuid
from fastapi import Cookie, FastAPI, HTTPException, Response
from typing import Any, Dict, Optional
from fastapi.staticfiles import StaticFiles

from chatdraw.chatflows.chat_system import ChatMessage, ChatResponse, ChatHandler
from chatdraw.chatflows.drawtutorial import DrawingProject


chat_handler = ChatHandler("greeting_start")
chat_handler.register_project("greeting",DrawingProject())

app = FastAPI()


session_store: Dict[str, str] = {}
SESSION_COOKIE_NAME = "session_id"


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
    message: ChatMessage,
    response: Response,
    session_id: Optional[str] = Cookie(default=None, alias=SESSION_COOKIE_NAME)
) -> Any:
    # Session management
    if session_id is None: 
        session_id = str(uuid.uuid4())
    if session_id not in session_store:
        session_store[session_id] = "greeting_start"
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=session_id,
            httponly=True,
            secure=False,  # Set to True if using HTTPS
            samesite="lax",
            max_age=60 * 60  # 1 hour
        )
    # Security check
    if check_malicious_code(message.message.content) or check_malicious_code(message.context):
        raise HTTPException(
            status_code=400,
            detail="Potentially unsafe content detected in text"
        )
    answer = chat_handler.process_message(message)
    session_store[session_id] = answer.next_context
    return answer


app.mount("/", StaticFiles(directory='./dist', html=True), name='static')


