# speech/listen.py

import whisper
import sounddevice as sd
import numpy as np

# Load Whisper tiny model once
model = whisper.load_model("tiny")

def listen():
    print("🎤 Speak now...")
    duration = 3  # Shorter for faster response
    sample_rate = 16000

    # Record audio
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    audio = np.squeeze(audio)

    # Transcribe with speed optimizations
    result = model.transcribe(audio, fp16=False, language='en')
    print(f"🗣️ You said: {result['text']}")
    return result["text"]
