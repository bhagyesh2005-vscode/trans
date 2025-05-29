import streamlit as st
from gtts import gTTS
import datetime
import wikipedia
import webbrowser
import os
import random
import smtplib
import tempfile

# Text-to-speech using gTTS
def speak(text):
    st.write(f"🧠 Jarvis says: {text}")
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format='audio/mp3')

# Greeting function
def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. How may I help you today?")

# Send email function
def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your_email@gmail.com', 'your_app_password')  # Use app password, not regular password
        server.sendmail('your_email@gmail.com', to, content)
        server.quit()
        speak("Email has been sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        speak("Sorry, I could not send the email.")

# Streamlit UI
st.set_page_config(page_title="Jarvis Assistant", page_icon="🤖")
st.title("🧠 Jarvis - Your AI Assistant")

if st.button("Greet Me"):
    wish_me()

query = st.text_input("Type your command here:")

if st.button("Execute") and query:
    query = query.lower()

    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace('wikipedia', '')
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            st.success(results)
        except:
            st.error("Couldn't find information on Wikipedia.")

    elif 'play music' in query:
        music_dir = "path_to_your_music_folder"  # Replace with your own music folder
        try:
            songs = os.listdir(music_dir)
            song = random.choice(songs)
            song_path = os.path.join(music_dir, song)
            st.write(f"Playing: {song}")
            os.startfile(song_path)  # Will work only on local desktop
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

    elif 'send email' in query:
        recipient = st.text_input("Recipient Email")
        content = st.text_area("Message to Send")
        if st.button("Send Email"):
            send_email(recipient, content)

    elif 'exit' in query or 'shutdown' in query:
        speak("Shutting down. It was a pleasure assisting you, Sir.")
        st.stop()
