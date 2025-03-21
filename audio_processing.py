from openai import OpenAI
import os

# Client OpenAI per Whisper
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(audio_path):
    """Trascrivi audio usando OpenAI Whisper API"""
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        print(f"Errore nella trascrizione: {str(e)}")
        return None