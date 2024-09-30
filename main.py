from supabase import create_client, Client
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))


def ask_gemini(prompt, first_message, model_message):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 9000,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"{first_message}",
                ],
            },
            {
                "role": "model",
                "parts": [
                    f"{model_message}",
                ],
            }
        ]
    )
    response = chat_session.send_message(prompt)
    print(type(response.text), type(str), type(str(response.text)))
    return str(response.text)



app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:5174",
    "*"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,        
    allow_methods=["*"],           
    allow_headers=["*"],           
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


class Prompt(BaseModel):
    prompt: str
    command: str
    message: str


@app.post("/prompt")
async def generate(prompt: Prompt):
    res = ask_gemini(prompt.prompt, prompt.command, prompt.message)
    print(res)
    return {"ai_model": str(res)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
