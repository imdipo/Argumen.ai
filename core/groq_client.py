import os
from groq import Groq
from dotenv import load_dotenv

def groq():
    load_dotenv()
    api_key = os.getenv("GROQ")
    if not api_key:
        raise ValueError("api key tidak ditemukan")

    return Groq(api_key=api_key)
