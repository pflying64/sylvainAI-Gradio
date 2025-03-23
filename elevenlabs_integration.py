# elevenlabs_integration.py
import os
import tempfile
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
CUSTOM_VOICE_ID = os.getenv("ELEVENLABS_CUSTOM_VOICE_ID")

elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def text_to_speech(text, model="eleven_flash_v2_5"):  # Versione più veloce
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
        
        # Assicurati che il file sia completamente scritto
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        total_bytes = 0
        
        for chunk in audio_stream:
            if isinstance(chunk, bytes):
                total_bytes += len(chunk)
                temp_file.write(chunk)
        
        temp_file.flush()
        os.fsync(temp_file.fileno())
        temp_file.close()
        
        print(f"Audio generato: {total_bytes} bytes")
        
        # Breve pausa per garantire che il file sia completo
        import time
        time.sleep(0.2)
        
        return temp_file.name
            
    except Exception as e:
        print(f"Errore nella sintesi vocale: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Dettagli risposta: {e.response.text}")
        return None