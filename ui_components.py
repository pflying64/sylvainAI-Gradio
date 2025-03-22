# CSS personalizzato
css = """
body, .gradio-container, .gradio-container > div {
    background-color: transparent !important;
}

body::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(30, 30, 30, 0.85);
    z-index: -1;
}

.gradio-container {
    max-width: 90% !important;
    margin: 0 auto !important;
}

.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    margin: 0 auto;
    max-width: 800px;
}

.main-title {
    font-family: 'Helvetica Neue', sans-serif;
    font-size: 2.5em;
    color: #FFFFFF;
    text-align: center;
    margin-bottom: 0;
    font-weight: 300;
}

.subtitle {
    font-family: 'Helvetica Neue', sans-serif;
    font-size: 1.5em;
    color: #E0E0E0;
    text-align: center;
    margin-bottom: 1rem;
    font-weight: 300;
}

.version {
    font-family: 'Helvetica Neue', sans-serif;
    color: #808080;
    text-align: center;
    font-size: 1.1em;
    margin-top: 0;
    margin-bottom: 2rem;
}

.introduction {
    font-family: 'Helvetica Neue', sans-serif;
    color: #FFFFFF;
    text-align: center;
    margin-bottom: 2rem;
}

.audio-input audio {
    display: none !important;
}

.audio-input {
    margin-top: 0.5rem;
    background-color: #2D2D2D !important;
    border-radius: 10px;
    padding: 0.5rem;
}

.audio-output {
    margin-top: 1rem;
    background-color: rgba(45, 45, 45, 0.7) !important;
    border-radius: 10px;
    padding: 1rem;
}

footer {
    display: none !important;
}
"""

# Custom JavaScript per cambiare il testo del pulsante
custom_js = """
<script>
function updateRecordButton() {
    const recordBtn = document.querySelector('.record');
    if (recordBtn) {
        recordBtn.textContent = 'SPEAK';
    }
}

// Esegui al caricamento
document.addEventListener('DOMContentLoaded', updateRecordButton);

// Osserva cambiamenti nel DOM
const observer = new MutationObserver(updateRecordButton);
observer.observe(document.body, { childList: true, subtree: true });
</script>
"""

bg_style = """
body {
    background-image: url("file=img/background.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
""" + custom_js