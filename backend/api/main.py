from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "Welcome to your AI Chatbot API!"}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        from openai import OpenAI
        from dotenv import load_dotenv
        import os

        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": request.question}
            ]
        )
        answer = response.choices[0].message.content
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}