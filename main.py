# main.py

from speech.listen import listen
from agent import run_agent
from speech.speak import speak, stop

def main():
    speak("Hello! I’m your AI assistant. Type 'speak' to talk or 'type' to enter text.")
    mode = input("Mode [speak/type]: ").strip().lower()

    if mode not in ["speak", "type"]:
        speak("Invalid input mode. Please restart and choose 'speak' or 'type'.")
        return

    while True:
        if mode == "speak":
            query = listen()
        else:
            query = input("You: ")

        if not query or not query.strip():
            speak("I didn't catch that. Please ask again.")
            continue

        lower_query = query.lower()

        if any(exit_word in lower_query for exit_word in ["exit", "quit", "bye"]):
            stop()
            speak("Goodbye!")
            break

        if any(stop_word in lower_query for stop_word in ["stop", "cancel"]):
            stop()
            speak("Okay, stopped speaking. You can continue asking.")
            continue

        response = run_agent(query)
        speak(response)

if __name__ == "__main__":
    main()
