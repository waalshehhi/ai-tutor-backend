from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

class Question(BaseModel):
    language: str
    level: str
    subject: str
    topic: str
    question: str

@app.get("/")
def root():
    return {"message": "AI Tutor Backend is running"}

@app.post("/ask")
async def ask_question(q: Question):
    prompt = f"""
    You are a private school tutor for {q.level} level students, explaining in {q.language}.
    Subject: {q.subject}
    Topic: {q.topic}
    Student's question: {q.question}
    
    Respond clearly and use engaging language for children.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful tutor who explains topics to school students."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=700
        )
        return {"answer": response["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}
