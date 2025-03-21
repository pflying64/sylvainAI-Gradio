import gradio as gr
import os
from dotenv import load_dotenv

from ui_components import css, bg_style
from openai_integration import client as openai_client, get_assistant_response
from elevenlabs_integration import text_to_speech
from audio_processing import transcribe_audio

os.system('pip show openai')


load_dotenv()

def process_audio_input(audio_path, thread_id):
    if audio_path is None:
        return thread_id, None
    
    transcription = transcribe_audio(audio_path)
    if not transcription:
        return thread_id, None
    
    if not thread_id:
        thread = openai_client.beta.threads.create()
        thread_id = thread.id
    
    response = get_assistant_response(thread_id, transcription)
    audio_path = text_to_speech(response)
    
    return thread_id, audio_path

def reset_input():
    return None

with gr.Blocks(css=css + bg_style) as demo:
    thread_id = gr.State(None)
    
    with gr.Column(elem_classes="container"):
        gr.HTML('<h1 class="main-title">SYLVAIN LEVY</h1>')
        gr.HTML('<h2 class="subtitle">Art and Technologies</h2>')
        gr.HTML('<p class="version">V α 0.2</p>')
        gr.HTML('<p class="introduction">Hello, I\'m Karen, Sylvain\'s daughter. Ask me anything about his pioneering work in art collection and digital technologies...</p>')
        
        waveform_options = gr.WaveformOptions(show_recording_waveform=False)
        audio_input = gr.Audio(sources=["microphone"], type="filepath", label="User", elem_classes="audio-input", waveform_options=waveform_options)
        audio_output = gr.Audio(label="Karen", elem_classes="audio-output", autoplay=True)
    
    audio_input.change(
        process_audio_input,
        [audio_input, thread_id],
        [thread_id, audio_output]
    )
    
    audio_output.stop(
        reset_input,
        None,
        [audio_input]
    )

if __name__ == "__main__":
    demo.launch(inbrowser=True, allowed_paths=["img"])