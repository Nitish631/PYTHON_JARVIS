import speech_recognition as sr
import pyttsx3
import webbrowser
import time

# Initialize text-to-speech
tts = pyttsx3.init()

def speak(text: str):
    tts.say(text)
    tts.runAndWait()

# Recognizer and keyword
r = sr.Recognizer()
mic=sr.Microphone()
KEYWORD = "jarvis"
activated = False
def callback(recognizer :sr.Recognizer,audio):
    try:
        text:str=recognizer.recognize_google(audio)
        text=text.lower()
        print(f"You said: {text}")
        if KEYWORD in text:
            print("Keyword detected!")
            index=text.index(KEYWORD)+len(KEYWORD)
            query=text[index:].strip()
            if query:
                web_search(query)
            else:
                print("please say something after jarvis")
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        print("Could not request result from google")
    

def web_search(query: str):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    print(f"Searching the web for {query}")

def main():
    print("JARVIS ACTIVATED.")
    speak("SAY JARVIS")
    with mic as source:
        r.adjust_for_ambient_noise(source,duration=2)
    stop_listening=r.listen_in_background(mic,callback)
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_listening()
        print("Exiting program")
if __name__ == "__main__":
    main()
