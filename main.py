import streamlit as st
from gtts import gTTS
import datetime
import wikipedia
import webbrowser
import os
import random
import smtplib
import tempfile

# Function to speak and return audio path
def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# Greet based on time
def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        return "Good Morning!"
    elif 12 <= hour < 18:
        return "Good Afternoon!"
    else:
        return "Good Evening!"

# Send email
def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your_email@gmail.com', 'your_app_password')  # Replace securely
        server.sendmail('your_email@gmail.com', to, content)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {e}"

# Set up Streamlit UI
st.set_page_config(page_title="Jarvis Chatbot", page_icon="🤖")
st.title("🧠 Jarvis - AI Assistant Chatbot")

# Initialize session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.greeted = False

# Greeting
if not st.session_state.greeted:
    greeting = wish_me()
    reply = f"{greeting} I am Jarvis. How may I help you today?"
    audio_path = speak(reply)
    st.session_state.history.append(("Jarvis", reply, audio_path))
    st.session_state.greeted = True

# Chat interface
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.history.append(("You", user_input, None))
    query = user_input.lower()
    response = ""

    if 'wikipedia' in query:
        try:
            speak("Searching Wikipedia...")
            query = query.replace('wikipedia', '')
            result = wikipedia.summary(query, sentences=2)
            response = f"According to Wikipedia: {result}"
        except:
            response = "Sorry, I couldn't find anything on Wikipedia."
    elif 'play music' in query:
        response = "Sorry, playing music is not supported in this web version."
    elif 'open youtube' in query:
        webbrowser.open("https://youtube.com")
        response = "Opening YouTube..."
    elif 'open google' in query:
        webbrowser.open("https://google.com")
        response = "Opening Google..."
    elif 'open hotstar' in query:
        webbrowser.open("https://hotstar.com")
        response = "Opening Hotstar..."
    elif 'the time' in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"The current time is {str_time}"
    elif 'send email' in query:
        response = "Email feature requires additional UI. Please implement securely."
    elif 'exit' in query or 'shutdown' in query:
        response = "Shutting down. It was a pleasure assisting you."
    else:
        response = "Sorry, I didn't understand that. Try asking something else."

    # Generate audio and append response
    audio_path = speak(response)
    st.session_state.history.append(("Jarvis", response, audio_path))

# Display chat history
for sender, message, audio in st.session_state.history:
    with st.chat_message(sender):
        st.markdown(message)
        if audio:
            st.audio(audio, format='audio/mp3')
