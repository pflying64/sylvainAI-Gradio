import os
import tempfile
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
CUSTOM_VOICE_ID = os.getenv("ELEVENLABS_CUSTOM_VOICE_ID")

elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def text_to_speech(text, model="eleven_flash_v2_5"):
    try:
        voice_settings = {
            "stability": 0.50,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True,
            "speed": 0.93
        }
        
        audio_stream = elevenlabs_client.text_to_speech.convert(
            text=text,
            voice_id=CUSTOM_VOICE_ID,
            model_id=model,
            voice_settings=voice_settings
        )
        
        # Create unique temp file
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        
        # Write chunks to file
        for chunk in audio_stream:
            if isinstance(chunk, bytes):
                temp_file.write(chunk)
        
        temp_file.close()
        return temp_file.name
            
    except Exception as e:
        print(f"Errore nella sintesi vocale: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Dettagli risposta: {e.response.text}")
        return None