import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# Assicuriamoci che le variabili d'ambiente vengano caricate
load_dotenv()

# Configura client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Debug
print(f"OpenAI API Key present: {bool(os.getenv('OPENAI_API_KEY'))}")
print(f"Assistant ID: {ASSISTANT_ID}")

def get_assistant_response(thread, user_message):
    """Ottieni risposta dall'assistente OpenAI"""
    try:
        # Aggiungi messaggio dell'utente
        client.beta.threads.messages.create(
            thread_id=thread,
            role="user",
            content=user_message
        )

        # Esegui l'assistente
        run = client.beta.threads.runs.create(
            thread_id=thread,
            assistant_id=ASSISTANT_ID
        )

        # Attendi il completamento
        while True:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread,
                run_id=run.id
            )
            if run.status == 'completed':
                break
            elif run.status == 'failed':
                raise Exception("Run failed")
            time.sleep(0.5)

        # Ottieni la risposta
        messages = client.beta.threads.messages.list(
            thread_id=thread
        )
        return messages.data[0].content[0].text.value

    except Exception as e:
        return f"Error: {str(e)}"