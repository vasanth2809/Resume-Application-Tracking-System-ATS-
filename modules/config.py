from dotenv import load_dotenv
import os
from typing import Optional
import google.generativeai as genai

load_dotenv()

def configure_genai(api_key: Optional[str] = None):
    key = api_key or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise EnvironmentError("GOOGLE_API_KEY not set in environment")
    genai.configure(api_key=key)

__all__ = ["configure_genai", "genai"]
