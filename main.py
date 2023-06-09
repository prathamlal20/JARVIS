# Pre-defined libraries
import datetime
import os
import speech_recognition as sr
import urllib.parse
import urllib.request
import win32com.client
import webbrowser
import re
import openai
from config import openai_apikey


# User created libraries
import greetings
from browsing import sites

chatStr = ""
def chat():
    global chatStr
    openai.api_key = openai_apikey
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    respond(response['choices'][0]["text"])
    chatStr += f"{response['choices'][0]['text']}"
    return response['choices'][0]["text"]

def ai(prompt):
    openai.api_key = openai_apikey

    text = f"{prompt} \n***********************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # print(response['choices'][0]["text"])
    text += response['choices'][0]["text"]

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('openai')[1:]).strip()}.txt", "w") as f:
        f.write(text)

def respond(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            # return query

        except Exception as e:
            return "Some Error Occurred"

        return query


if __name__ == "__main__":
    greetings.greeting()
    # respond("Hello, Myself Vision! Ready to Serve You")
    while True:
        print("Listening")
        query = takecommand()

        # For opening websites
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                respond(f"Opening {site[0]}")
                webbrowser.open(site[1])

        # For playing video on YouTube
        if f"play song on YouTube" in query:
            respond("Which song you want to play")
            song = takecommand()
            song = urllib.parse.urlencode({"search_query":query})
            respond(f"Playing {song} on youtube")
            result = urllib.request.urlopen("https://www.youtube.com/results?"+song)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})]', result.read().decode())
            url = "https://www.youtube.com/watch?v="+search_results[0]
            # webbrowser.open(url, new=1)
            webbrowser.open_new(url)

        # For getting current time
        if "what's the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            respond(f"It's {hour} and {min} minutes")

        elif "Using openai".lower() in query.lower():
            ai(prompt=query)

        elif "Vision Quit".lower() in query.lower():
            respond("Thank you for using me")
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""
            respond("Chat has been reset")

        else:
            chat()





