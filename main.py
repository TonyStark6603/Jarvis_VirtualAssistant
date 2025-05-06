import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os

recognizer = sr.Recognizer()
engine  = pyttsx3.init()
newsapi = "pub_84855bcbea531141750559028a4a7232e33d9"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()


def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")


    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")  # Remove the temporary file after playing




def aiProcess(command):
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    api_key = "AIzaSyA5Uy_ty3R0y3sjHluc3pdEGsuggT8EUeY"  # Ensure proper indentation

    short_command = f"{command}. Please respond in a short and concise manner."
    # Request payload
    payload = {
        "contents": [
            {
                "parts": [{"text": short_command}],
            }
        ]
    }

    # Headers
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Make the POST request
        response = requests.post(f"{api_url}?key={api_key}", json=payload, headers=headers)

        # Handle the response
        if response.status_code == 200:
            result = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            cleaned_result = result.replace("**", "").strip()
            speak(cleaned_result)  # Speak the result
        else:
            speak("Sorry, I couldn't process your request.")
    except Exception as e:
        speak("An error occurred while processing your request.")


def processCommand(c):
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        speak("Opening Youtube")
        webbrowser.open("https://www.youtube.com")
    elif "open stack overflow" in c.lower():
        speak("Opening Stack Overflow")
        webbrowser.open("https://stackoverflow.com")
    elif "open github" in c.lower():
        speak("Opening Github")
        webbrowser.open("https://github.com/Saurabh-8816")
    elif "open instagram" in c.lower():
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
    elif c.lower().startswith("play"):
       song = c.lower().split(" ")[1]
       music_dict = {key.lower(): value for key, value in musicLibrary.music.items()}
       if song in music_dict:
            link = music_dict[song]
            speak(f"Playing {song}")
            webbrowser.open(link)
       else:
            speak(f"Sorry, I couldn't find the song {song}")
    elif "tell me the news" in c.lower():
        speak("Fetching the latest news")
        try:
            # NewsData.io API endpoint and parameters
            api_url = "https://newsdata.io/api/1/news"
            params = {
                "apikey": newsapi,  # Replace with your NewsData.io API key
                "country": "in",   # Country code for India
                "language": "en"   # Language filter (English)
            }
            r = requests.get(api_url, params=params)
            if r.status_code == 200:
                data = r.json()
                articles = data.get("results", [])  # NewsData.io uses "results" for articles
                if articles:
                    for article in articles[:5]:  # Limit to the first 5 articles
                        speak(article.get("title", "No title available"))
                else:
                    speak("Sorry, I couldn't find any news articles.")
            else:
                speak(f"Failed to fetch news. Error code: {r.status_code}")
        except Exception as e:
            speak("An error occurred while fetching the news.")
            print(f"Error: {e}")


    else:
        # Let OpenAI handle the command
        output = aiProcess(c)
        speak(output)  # Speak the AI's response

if __name__ == "__main__": 
    speak("Intializing Jarvis....")
    while True:
        # Listen for the command "Jarvis"
        #obtain audio from the microphone
        r = sr.Recognizer()
       



        print("recognizing...")

        #recognize speech using Google
        try:
            with sr.Microphone() as source:
                 print("Listening...")
                 audio = r.listen(source, timeout=2, phrase_time_limit=6)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Yes, how can I help you?")
                #Listen for command
                with sr.Microphone() as source:
                   print("Jarvis Active...")
                   audio = r.listen(source)
                   command = r.recognize_google(audio)
            

                   processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))


