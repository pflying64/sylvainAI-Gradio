import gradio as gr

class CustomAudio(gr.Audio):
    """Audio component with custom record button text"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.predict_button_text = "SPEAK"