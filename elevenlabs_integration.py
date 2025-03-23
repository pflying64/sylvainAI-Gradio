# elevenlabs_integration.py
import os
import tempfile
import time
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
            voice_settings=voice_settings,
            output_format="mp3_44100_64"  # Bitrate più basso
        )
        
        # Crea la cartella audio dentro files
        output_dir = "files/audio"
        os.makedirs(output_dir, exist_ok=True)
        
        # Nome file con timestamp
        filename = f"{output_dir}/response_{int(time.time())}.mp3"
        
        total_bytes = 0
        with open(filename, "wb") as f:
            for chunk in audio_stream:
                if isinstance(chunk, bytes):
                    total_bytes += len(chunk)
                    f.write(chunk)
        
        print(f"Audio generato: {total_bytes} bytes in {filename}")
        
        # Breve pausa per garantire che il file sia completo
        time.sleep(0.2)
        
        return filename
            
    except Exception as e:
        print(f"Errore nella sintesi vocale: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Dettagli risposta: {e.response.text}")
        return None