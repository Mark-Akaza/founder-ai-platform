from fastapi import APIRouter
from google import genai
from app.config import GEMINI_API_KEY
from google.genai import types

client=genai.Client(api_key=GEMINI_API_KEY)

def gen_embeddings(text:str):
    response=client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=1536
        )
    )
    return response.embeddings[0].values




