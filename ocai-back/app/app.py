from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, get_db
from pydantic import BaseModel
import uuid
import google.generativeai as genai
from .ai.promts import INITIAL_INSTRUCTIONS, CHAT_PROMPT, RAG_PROMPT
import dotenv
import json
import os
from .ai.indexer.indexer import search_in_milvus

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# app.include_router(users.router)

class ChatRequest(BaseModel):
  newChat: bool
  email: str
  message: str | None = None
  chatId: str | None = None

@app.get("/")
async def read_root():
  return {"Hello": "World"}


@app.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
  if request.newChat:
    user_id = db.execute(text("SELECT id FROM users WHERE email = :email"), {"email": request.email}).fetchone()[0]
    initial_chat = "{ role: 'user', content: '%s' }, { role: 'assistant', content: '%s' }" % (request.message, INITIAL_INSTRUCTIONS)
    id = str(uuid.uuid4())
    db.execute(text('INSERT INTO session (id, "userId", "chatHistory", active, result, "lastActive") VALUES (:id, :user_id, :initial_chat, :active, NULL, NOW())'), {"id": id, "user_id": user_id, "initial_chat": initial_chat, "active": True})
    db.commit()

    return {"message": {"role": "assistant", "content": INITIAL_INSTRUCTIONS}, "chatId": id}
  else:
    dotenv.load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=api_key)

    # Get chat history from database (chat ID), feed it into LLM, return response
    chat_history = db.execute(text('SELECT "chatHistory" FROM session WHERE id = :id'), {"id": request.chatId}).fetchone()[0].tobytes().decode('utf-8')

    # Update chat history with received message
    formatted_request_message = {"message": {"role": 'user', "content": request.message}}
    new_chat_history = chat_history + json.dumps(formatted_request_message)

    rag_prompt = RAG_PROMPT.format(chatHistory=new_chat_history)

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(rag_prompt)
    rag_response_text = response.text.strip()

    retrieved_texts = await search_in_milvus("knowledge_base", rag_response_text, top_k=5)

    print(retrieved_texts)

    # Send chat history to LLM, get response
    final_prompt = CHAT_PROMPT.format(chatHistory=new_chat_history, services=retrieved_texts)

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(final_prompt)

    response_text = response.text.strip()
    response_text = response_text.replace("```", '')
    response_text = response_text.replace("json", '')
    # print(response_text)
    # print(type(response_text))
    response_json = json.loads(response_text)
    response_message = response_json["message"]

    # # # Update chat history with models response
    formatted_response_message = {"message": {"role": 'assistant', "content": response_message}}
    new_chat_history = chat_history + f", {json.dumps(formatted_response_message)}"

    try:
      db.execute(text('UPDATE session SET "chatHistory" = :new_chat_history WHERE id = :id'), {"new_chat_history": new_chat_history, "id": request.chatId})
      db.commit()
    except Exception as e:
      print(e)

    return {"message": {"role": "assistant", "content": response_message}, "chatId": request.chatId}