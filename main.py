import streamlit as st
import openai
from gtts import gTTS
import tempfile
import os
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, RTCConfiguration

# Use API key securely
openai.api_key = st.secrets["openai"]["api_key"]

# Function to call OpenAI API
def get_openai_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message["content"].strip()

# Function to convert text to audio
def speak(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# WebRTC Audio Processor (stub – STT not implemented here)
class AudioProcessor(AudioProcessorBase):
    def recv(self, frame):
        # Add speech-to-text processing here if needed
        return frame

# WebRTC config
rtc_configuration = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Streamlit App UI
st.set_page_config(page_title="Jarvis Voice Chatbot", page_icon="🤖")
st.title("🧠 Jarvis - Voice-Enabled Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a helpful assistant named Jarvis."}]

# Display chat messages
for msg in st.session_state["messages"][1:]:  # skip system message
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# Voice input UI (optional)
with st.expander("🎙️ Voice Input (Experimental)"):
    webrtc_streamer(
        key="voice",
        mode="sendonly",
        audio_processor_factory=AudioProcessor,
        rtc_configuration=rtc_configuration,
        media_stream_constraints={"audio": True, "video": False}
    )
    st.caption("Voice-to-text not implemented yet. Type below instead.")

# Text input
user_input = st.chat_input("Say something to Jarvis...")

# Handle user input
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Jarvis is thinking..."):
        reply = get_openai_response(st.session_state["messages"])
        st.session_state["messages"].append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)
        audio_path = speak(reply)
        st.audio(audio_path, format="audio/mp3")
