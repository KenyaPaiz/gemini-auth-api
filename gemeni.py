from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
import google.generativeai as genai
from dotenv import load_dotenv
from models.promptModel import PromptModel
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
#history 
chat_session = {}

async def generate_text(prompt: PromptModel, user: dict):
    try:
        if "kodigo" not in prompt.prompt.lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only questions related to Kodigo are allowed.")
        
        user_email = user.get("email")
        if user_email not in chat_session:
            chat_session[user_email] = model.start_chat(history=[])
        
        #response = model.generate_content(prompt.prompt)
        response = chat_session[user_email].send_message(prompt.prompt)
        return JSONResponse(status_code=status.HTTP_200_OK, content=response.text)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_chat(user: dict):
    user_email = user.get("email")
    session = chat_session.get(user_email)
    if not session:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content="No chat session found.")
    
    history = []
    for msg in session.history:
        parts = []
        for part in getattr(msg, "parts", []):
            try:
                parts.append(part.text)
            except AttributeError:
                parts.append(str(part))
        history.append({
            "role": getattr(msg, "role", "unknown"),
            "parts": parts
        })
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=history)
