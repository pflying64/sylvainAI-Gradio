from pathlib import Path
import gradio as gr
import base64

class AutoStopAudio(gr.Audio):
    """Audio component with automatic silence detection"""
    
    def __init__(self, **kwargs):
        print("Initializing AutoStopAudio")
        super().__init__(
            type="filepath",
            **kwargs
        )
        print("AutoStopAudio initialized")
    
    def get_template_context(self):
        ctx = super().get_template_context()
        ctx["custom_js"] = """
function silenceDetector(opts) {
    let mediaRecorder;
    let audioChunks = [];
    let silenceStart = null;
    let audioContext;
    let analyzer;
    
    const SILENCE_THRESHOLD = -50;
    const SILENCE_DURATION = 2000;
    const MIN_RECORDING_TIME = 3000;
    
    async function startRecording(el) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioContext = new AudioContext();
            const source = audioContext.createMediaStreamSource(stream);
            analyzer = audioContext.createAnalyser();
            source.connect(analyzer);
            
            audioChunks = [];
            const startTime = Date.now();
            
            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });
            
            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks);
                el.value = audioBlob;
                opts.trigger("change");
            });
            
            mediaRecorder.start();
            el.querySelector(".status").textContent = "Recording...";
            
            const buffer = new Float32Array(analyzer.frequencyBinCount);
            
            function checkSilence() {
                if (mediaRecorder.state !== "recording") return;
                
                analyzer.getFloatTimeDomainData(buffer);
                const rms = Math.sqrt(buffer.reduce((acc, val) => acc + val * val, 0) / buffer.length);
                const db = 20 * Math.log10(rms);
                
                if (db < SILENCE_THRESHOLD) {
                    if (!silenceStart) silenceStart = Date.now();
                    else if (Date.now() - silenceStart > SILENCE_DURATION && 
                            Date.now() - startTime > MIN_RECORDING_TIME) {
                        stopRecording(el);
                        return;
                    }
                } else {
                    silenceStart = null;
                }
                
                requestAnimationFrame(checkSilence);
            }
            
            checkSilence();
            
        } catch (err) {
            console.error("Recording error:", err);
            el.querySelector(".status").textContent = "Error starting recording";
        }
    }
    
    function stopRecording(el) {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
            el.querySelector(".status").textContent = "Click to record";
        }
    }
    
    return {
        start: startRecording,
        stop: stopRecording
    };
}
"""
        return ctx