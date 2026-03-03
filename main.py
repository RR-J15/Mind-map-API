import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI(title="Mind Map Generator Gemini")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# On récupère la clé Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise HTTPException(status_code=500, detail="Clé API Gemini manquante")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

class MindMapRequest(BaseModel):
    course_title: str
    key_concepts: str
    granularity_level: str
    course_duration: str
    target_audience: str
    learning_objectives: str

@app.post("/generate-mindmap/")
async def create_mindmap(request: MindMapRequest):
    prompt = f"""Génère une carte mentale au format Markdown pour le cours '{request.course_title}'.
    Public: {request.target_audience}, Durée: {request.course_duration}, Concepts: {request.key_concepts}.
    Utilise une hiérarchie avec des '#' (ex: # Titre, ## Module). 
    Commence directement par le markdown sans balises ```."""
    
    try:
        response = model.generate_content(prompt)
        return {"markdown": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "API Gemini Active"}
