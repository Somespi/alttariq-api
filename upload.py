from io import BytesIO
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai 
import google.generativeai as genai
import base64
import random


genai.configure(api_key="AIzaSyCbJxmfSa9Q-RwqISvbab2iw52dk3TyLC8") # Use parentheses to call the get function and pass the key as an argument
#chatgpt = openai.OpenAI(api_key="sk-svcacct-WU5PBA3XYf7YmVMTzekjFQPOKpj5lGvA5fW6RKrTwRopxBh-qkVWbT3BlbkFJMyqGTctG5lFVsKxlXLN-YILdHkpmHs_Q_83apFuUwrz56-clAgljwA")

def ali(prompt,first_message,model_message):
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 9000 ,
   
      "response_mime_type" : "text/plain",
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
def upload_to_giemeni(path):
    genai.upload_file(path)
    
    audio_file = genai.upload_file(path)
    return audio_file   

def ali(prompt,first_message,model_message):
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 9000 ,
   
      "response_mime_type" : "text/plain",
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
def mooh(path,prompt):
    files= upload_to_giemeni(path)
    while files.state.name == "PROCESSING":
        print("processing video...")
        time.sleep(5)
        files = genai.get_file(files.name)

    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 9000 ,
   
      "response_mime_type" : "text/plain",
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
            files, 
            
          ],
        },
        {
          "role": "model",
          "parts": [
            f"I have read the video file and i want to question you about it and critical think it and i will make sure to write it in Arabic",
          ],
        }
     ]
    )
    response = chat_session.send_message(prompt)
    return str(response.text)

import google.generativeai as genai
from supabase import create_client, Client



genai.configure(api_key="AIzaSyCbJxmfSa9Q-RwqISvbab2iw52dk3TyLC8") 
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "*"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # عناوين المصادر المسموح بها
    allow_credentials=True,        # السماح بالكوكيز والمصادقة
    allow_methods=["*"],           # السماح بجميع طرق HTTP
    allow_headers=["*"],           # السماح بجميع رؤوس HTTP
)

import base64
import os

class Meet(BaseModel):
    meet: str

@app.post("/meet/analyze")
def analyze_meet(meet: Meet):
    binary = base64.b64decode(meet.meet.encode())
    
    file_path = "public/e23e12e00e92.mp4"
    
    with open(file_path, "wb") as f:
        f.write(binary)
    
    res = mooh(file_path, prompt="ok i have u already understand this file and i want you to question about it and critical think it and write the contetn in Arabic.")
    
    os.remove(file_path)
    return {"response": res}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)