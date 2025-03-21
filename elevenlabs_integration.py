import os
import tempfile
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

# Assicuriamoci che le variabili d'ambiente vengano caricate
load_dotenv()

# Configura ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
CUSTOM_VOICE_ID = os.getenv("ELEVENLABS_CUSTOM_VOICE_ID")

# Debug
print(f"ElevenLabs API Key present: {bool(ELEVENLABS_API_KEY)}")
print(f"Custom Voice ID: {CUSTOM_VOICE_ID}")

# Inizializza il client ElevenLabs con autenticazione esplicita negli headers
# Modifica questa parte:
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def text_to_speech(text, model="eleven_flash_v2_5"):
    """
    Converte il testo in audio usando la voce custom di ElevenLabs
    con modello Flash v2.5 e parametri ottimizzati
    """
    try:
        print(f"Tentativo di generazione audio con voice_id={CUSTOM_VOICE_ID}, model={model}")
        
        # Configura i parametri della voce personalizzati
        voice_settings = {
            "stability": 0.50,        # Stabilità media per un buon equilibrio tra coerenza e variabilità
            "similarity_boost": 0.75,  # Somiglianza alta alla voce originale
            "style": 0.0,             # Nessuna esagerazione dello stile
            "use_speaker_boost": True, # Migliora la somiglianza all'oratore originale
            "speed": 0.93             # Velocità leggermente inferiore al normale
        }
        
        # Genera l'audio con la voce custom
        print("Chiamata API ElevenLabs in corso...")
        audio_generator = elevenlabs_client.text_to_speech.convert(
            text=text,
            voice_id=CUSTOM_VOICE_ID,
            model_id=model,
            voice_settings=voice_settings
        )
        
        # Raccogliamo tutti i chunk dal generatore in un singolo buffer
        print("Raccolta chunks audio...")
        audio_data = b''
        for chunk in audio_generator:
            if isinstance(chunk, bytes):
                audio_data += chunk
        
        print(f"Audio generato: {len(audio_data)} bytes")
        
        # Salva l'audio in un file temporaneo
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(audio_data)
            return tmp.name
    except Exception as e:
        print(f"Errore nella sintesi vocale: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"Dettagli risposta: {e.response.text}")
        return None