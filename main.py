import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from your_file import get_openai_response

recognizer=sr.Recognizer()
engine = pyttsx3.init()
newsapi="YOUR_API"

def speak(text):
    engine.say(text)
    engine.runAndWait()


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1] #what it does mean if we say play nirvana then a lis is formed like ["play","nirvana"] the list therefore splitted and take index first ele which is nirvana 
        link=musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()  # Convert response to JSON
            articles = data.get("articles", [])  # Extract articles list

            print("\nTop News Headlines:\n")
            for i, article in enumerate(articles, 1):
                speak(article['title'])
                print(f"{i}. {article['title']}")  # Extract and print headlines
        
    else:
        #Let OpenAI take over
        output=get_openai_response(c)
        speak(output)
        

if __name__ == "__main__":
    speak("Initialising, JARVIS!")
    while True:
        
        r = sr.Recognizer()

       
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source,timeout=2,phrase_time_limit=1)
            word=r.recognize_google(audio)
            if (word.lower() == "jarvis" or word.lower()=="javeez"):
                speak("yes sir, How may i help you")
                with sr.Microphone() as source:
                    print("Jarvis Active....")
                    audio = r.listen(source,timeout=2,phrase_time_limit=1)
                    command=r.recognize_google(audio)

                    processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))
