import speech_recognition as sr
import pyttsx3
# import whisper
import time
import webbrowser
import asyncio

tts=pyttsx3.init()
def speak(text:str):
    tts.say(text)
    tts.runAndWait()

async def speak_async(text:str):
    loop=asyncio.get_running_loop()
    await loop.run_in_executor(None,speak,text)

r=sr.Recognizer()
KEYWORD="jarvis"
activated:bool=False

async def listen():
    with sr.Microphone() as source:
        print("Listening............")
        global activated
        if not activated:
            await speak_async("Jarvis activated")
            activated=True
        # await speak_async("Listening")
        r.adjust_for_ambient_noise(source,0.5)
        audio=r.listen(source)
    try:
        text:str=r.recognize_google(audio)
        print(f"You said:{text.lower()}")
        print("listening stop")
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio")
        print("listening stop")
        return ""
    except sr.RequestError:
        print("Could not request results from Google")
        print("listening stop")
        return ""

async def web_search(query:str):
    url=f"https://www.google.com/search?q={query}"
    loop= asyncio.get_running_loop()
    await loop.run_in_executor(None,webbrowser.open,url)
    # await webbrowser.open(url)
    await speak_async(f"Searching the web for {query}")
    print(f"Searching the web for {query}")
async def main():
    while True:
        text= await listen()
        if KEYWORD in text:
            print("WORD DETECTED AFTER SPEAKING")
            # text_temp:str=text
            index=text.index( KEYWORD)+len(KEYWORD)
            # text=listen(5)
            query=text[index:].strip()
            if query:
                print(f"Query:{query}")
                await web_search(query)
            else:
                await speak_async("please say something after jarvis")
        await asyncio.sleep(1)


if __name__=="__main__":
    asyncio.run(main())