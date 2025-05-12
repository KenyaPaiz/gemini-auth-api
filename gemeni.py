from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
import google.generativeai as genai
from dotenv import load_dotenv
from models.promptModel import PromptModel
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

async def generate_text(prompt: PromptModel):
    try:
        if "kodigo" not in prompt.prompt.lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only questions related to Kodigo are allowed.")
        
        response = model.generate_content(prompt.prompt)
        return JSONResponse(status_code=status.HTTP_200_OK, content=response.text)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))