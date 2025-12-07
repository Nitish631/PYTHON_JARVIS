import speech_recognition as sr
import pyttsx3
import webbrowser
import time

r=sr.Recognizer()
KEYWORD="jarvis"
def speak(text:str):
    tts=pyttsx3.init()
    tts.say(text)
    tts.runAndWait()
    tts.stop()
    print("SPEAK IS CALLED")



def websearch(query:str):
    url:str=f"https://www.google.com/search?q={query}"
    webbrowser.open_new(url)

def listenMicrophone(phrase_time_limit:int)->str:
    command:str=""
    with sr.Microphone() as source:
        # r.adjust_for_ambient_noise(source,duration=2)
        r.energy_threshold=100
        r.non_speaking_duration=0.5
        r.pause_threshold=1
        r.phrase_threshold=0.3
        print("listening")
        command:str=""
        try:
            audio=r.listen(source,timeout=2,phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("No speech detected")
            return""
    try:
        command=r.recognize_google(audio)
    except sr.UnknownValueError as e:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request result.")
    return command.lower()


def main():
    print("recognizing")
    speak("JARVIS ACTIVATED")
    while True:
        command:str=listenMicrophone(phrase_time_limit=1.5)
        if(KEYWORD in command):
            speak("YA")
            print("READY TO COMMAND")
            command:str=listenMicrophone(5)
            if command !="":
                websearch(command)
                print(f"Your command is{command}")
            

if __name__== "__main__":
    main()