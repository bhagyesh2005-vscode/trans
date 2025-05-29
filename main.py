import streamlit as st
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random
import smtplib

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    st.write(f"Jarvis says: {text}")
    engine.say(text)
    engine.runAndWait()

def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Jarvis. How may I help you today?")

def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('your_email@gmail.com', 'your_password')  # Replace with credentials
        server.sendmail('your_email@gmail.com', to, content)
        server.close()
        speak("Email has been sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        speak("Sorry, I could not send the email.")

# Streamlit UI
st.title("🧠 Jarvis - Your Voice Assistant in a Web App")

wish = st.button("Greet Me")
if wish:
    wish_me()

query = st.text_input("Type your command here:")

if st.button("Execute Command") and query:
    query = query.lower()

    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace('wikipedia', '')
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            st.success(results)
            speak(results)
        except:
            st.error("Couldn't find information on Wikipedia.")

    elif 'play music' in query:
        music_dir = "path_to_your_music_folder"
        try:
            songs = os.listdir(music_dir)
            song = random.choice(songs)
            song_path = os.path.join(music_dir, song)
            st.write(f"Playing: {song}")
            os.startfile(song_path)  # May not work in web environments
        except Exception as e:
            st.error(f"Could not play music: {e}")

    elif 'open youtube' in query:
        webbrowser.open("https://youtube.com")

    elif 'open google' in query:
        webbrowser.open("https://google.com")

    elif 'open hotstar' in query:
        webbrowser.open("https://hotstar.com")

    elif 'the time' in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {str_time}")

    elif 'open brave' in query:
        brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
        try:
            os.startfile(brave_path)
        except Exception as e:
            st.error("Could not open Brave browser.")

    elif 'send email' in query:
        recipient = st.text_input("Enter recipient email:")
        content = st.text_area("Enter email content:")
        if st.button("Send Email"):
            send_email(recipient, content)

    elif 'jarvis exit' in query:
        speak("Shutting down. It was a pleasure assisting you, Sir.")
        st.stop()
