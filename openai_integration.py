import os
import time
from shared_client import client

ASSISTANT_ID = os.getenv("ASSISTANT_ID")

def get_assistant_response(thread, user_message):
    try:
        client.beta.threads.messages.create(
            thread_id=thread,
            role="user",
            content=user_message
        )

        run = client.beta.threads.runs.create(
            thread_id=thread,
            assistant_id=ASSISTANT_ID
        )

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

        messages = client.beta.threads.messages.list(
            thread_id=thread
        )
        return messages.data[0].content[0].text.value

    except Exception as e:
        print(f"Full OpenAI error: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Response details: {e.response.text}")
        return f"Error: {str(e)}"