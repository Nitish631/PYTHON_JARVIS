import speech_recognition as sr
import pyttsx3
import webbrowser
from typing import Dict ,Any
import requests
import secret
import client


def playMedia(content:str):
    content.replace(" ","+")
    url=f"https://www.youtube.com/results?search_query={content}"
    webbrowser.open_new(url)

def handle_news():
    API_KEY: str = secret.NEWS_API_KEY
    URL: str = "https://newsdata.io/api/1/latest"

    params: Dict[str, str] = {
        "apikey": API_KEY,
        "q": "technology",
        "language": "en"
    }

    response: requests.Response = requests.get(URL, params=params, timeout=10)

    if response.status_code == 200:
        data: Dict[str, Any] = response.json()
        
        # Extract all titles
        news_titles: str = "\n".join(article.get("title", "") for article in data.get("results", []))
        
        speak(news_titles)
    else:
        print("Error:", response.status_code, response.text)

r=sr.Recognizer()
KEYWORD="jarvis"
 

def speak(text:str):
    tts=pyttsx3.init()
    tts.say(text)
    tts.runAndWait()
    tts.stop()
    print("SPEAK IS CALLED")

def open_web_domain(domain:str):
    url=f"https://www.{domain}.com"
    webbrowser.open_new(url)

def processCommand(c:str):
    if "open google" in c:
        open_web_domain("google")
    elif "open facebook" in c:
        open_web_domain("facebook")
    elif "open instagram" in c or "open insta" in c:
        open_web_domain("instagram")
    elif "open youtube" in c:
        open_web_domain("youtube")
    elif "news" in c:
        handle_news()
    elif "play" in c:
        prompt=f"find the single url of youtube video for the prompt \"{c}\""
        url=client.getAiOutput(prompt)
        print(url)
        # playMedia(c)
    else:
        client.streamAi(c)

def websearch(query:str):
    url:str=f"https://www.google.com/search?q={query}"
    webbrowser.open_new(url)
def getCommand(source,phrase_time_limit:float)->str:
    try:
        audio=r.listen(source,timeout=2,phrase_time_limit=phrase_time_limit)
    except sr.WaitTimeoutError:
        print("No speech detected")
        return""
    try:
        command:str=r.recognize_google(audio)
        return command.lower()
    except sr.WaitTimeoutError:
        print("No speech detected")
        return""
    except Exception:
        print("could not request result.")
        return""
    
def listenMicrophone()->str:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=3)
        r.energy_threshold=100
        r.non_speaking_duration=0.5
        r.pause_threshold=1
        r.phrase_threshold=0.3
        command:str=""
        speak("JARVIS ACTIVATED")
        while True:
            print("listening")
            command=getCommand(source=source,phrase_time_limit=2)
            if(KEYWORD in command):
                print("READY TO COMMAND.")
                speak("YA")
                command=getCommand(source=source,phrase_time_limit=5)
                if(command!=""):
                    processCommand(command)
                print(f"COMMAND IS {command}")


def main():

    print("recognizing")
    listenMicrophone()
            

if __name__== "__main__":
    # main()
    processCommand("play chillgum")