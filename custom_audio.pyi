import gradio as gr
from gradio.events import Dependency

class CustomAudio(gr.Audio):
    """Audio component with custom record button text"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.predict_button_text = "SPEAK"
    from typing import Callable, Literal, Sequence, Any, TYPE_CHECKING
    from gradio.blocks import Block
    if TYPE_CHECKING:
        from gradio.components import Timer