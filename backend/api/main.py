from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import OpenAI

# Initialize FastAPI
app = FastAPI()

# Initialize OpenAI client with your API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request model
class ChatRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "Welcome to your AI Chatbot API!"}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # lightweight model for testing
            messages=[{"role": "user", "content": request.question}]
        )
        answer = response.choices[0].message.content
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}