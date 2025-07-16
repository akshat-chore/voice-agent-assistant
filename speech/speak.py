import pyttsx3
import re
import threading
import pythoncom  # ✅ Required for COM initialization in threads

speak_thread = None

def get_engine():
    engine = pyttsx3.init()
    engine.setProperty("rate", 180)

    # Optional: Set English voice explicitly
    voices = engine.getProperty('voices')
    for voice in voices:
        if "english" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    return engine

def clean_text(text):
    return re.sub(r"[*_`~]", "", text).strip()

def speak(text):
    global speak_thread

    if not text or not text.strip():
        text = "I'm sorry, I didn't understand that."

    text = clean_text(text)
    print("🤖 Assistant:", text)

    def speak_text():
        pythoncom.CoInitialize()  # ✅ Fix COM error
        engine = get_engine()
        engine.say(text)
        engine.runAndWait()

    stop()
    speak_thread = threading.Thread(target=speak_text)
    speak_thread.start()

def stop():
    try:
        engine = pyttsx3.init()
        engine.stop()
    except Exception:
        pass
