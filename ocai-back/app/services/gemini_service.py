import os
import time
from fastapi import HTTPException
import google.generativeai as genai

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)

    async def generate_response(self, query_text: str, context: str = "") -> str:
        """Generate a response using the Gemini model with retries and context handling."""
        prompt = f"Context:\n{context}\n\nQuestion:\n{query_text}\n\nAnswer:"
        
        retries = 3
        for i in range(retries):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                if "429" in str(e):
                    time.sleep(2 ** i)  # Exponential backoff
                else:
                    raise e
        raise HTTPException(status_code=429, detail="Rate limit exceeded, please try again later.")
