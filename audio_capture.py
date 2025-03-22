from pathlib import Path
import gradio as gr

class AutoStopAudio(gr.Audio):
    def __init__(self, **kwargs):
        kwargs["sources"] = ["microphone"]  # sources, non source
        super().__init__(**kwargs)
    
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
    const MAX_RECORDING_TIME = 30000;
    
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
                el.querySelector(".record-button").classList.remove("recording");
                opts.trigger("change");
            });
            
            mediaRecorder.start(100);
            el.querySelector(".record-button").classList.add("recording");
            
            const buffer = new Float32Array(analyzer.frequencyBinCount);
            
            function checkSilence() {
                if (mediaRecorder.state !== "recording") return;
                
                analyzer.getFloatTimeDomainData(buffer);
                const rms = Math.sqrt(buffer.reduce((acc, val) => acc + val * val, 0) / buffer.length);
                const db = 20 * Math.log10(rms);
                
                const currentTime = Date.now();
                const recordingDuration = currentTime - startTime;
                
                if (recordingDuration >= MAX_RECORDING_TIME) {
                    stopRecording(el);
                    return;
                }
                
                if (db < SILENCE_THRESHOLD) {
                    if (!silenceStart) {
                        silenceStart = currentTime;
                    } else if (currentTime - silenceStart > SILENCE_DURATION && 
                             recordingDuration > MIN_RECORDING_TIME) {
                        stopRecording(el);
                        return;
                    }
                } else {
                    silenceStart = null;
                }
                
                requestAnimationFrame(checkSilence);
            }
            
            checkSilence();
            
            if (opts.start_recording_trigger) {
                opts.start_recording_trigger();
            }
            
        } catch (err) {
            console.error("Recording error:", err);
            el.querySelector(".record-button").classList.remove("recording");
        }
    }
    
    function stopRecording(el) {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.stop();
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
            el.querySelector(".record-button").classList.remove("recording");
        }
    }
    
    return {
        start: startRecording,
        stop: stopRecording
    };
}
"""
        return ctx