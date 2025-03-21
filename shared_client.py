from openai import OpenAI
import os
from dotenv import load_dotenv

# Carica il file .env
load_dotenv()

# Usa la chiave standard
api_key = os.getenv("OPENAI_API_KEY")

# Inizializza il client OpenAI classico
client = OpenAI(api_key=api_key)

# Debug
print(f"Using API key: {api_key}")
