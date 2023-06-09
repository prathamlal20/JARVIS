import datetime
import win32com.client

def greeting():
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour <= 12:
        speaker.Speak("Good Morning")

    elif hour>12 and hour<=18:
        speaker.Speak("Good Afternoon")

    else:
        speaker.Speak("Good Evening!")
