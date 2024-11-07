import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import pyperclip

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with the new API style
client = OpenAI(api_key=api_key)

# Streamlit page configuration
st.set_page_config(page_title="🎤 Audio Transcription Tool", page_icon="🎶")

# Page title and description with emojis
st.title("🎤 **Audio Transcription Tool**")
st.markdown(
    """
    Convert spoken audio into text. Perfect for transcribing interviews, meetings, and more! 🎧💬
    """
)

# Sidebar for transcription settings with a more colorful design
st.sidebar.title("⚙️ **Settings**")
languages = ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Korean", "Hindi", "Arabic", "Urdu"]
selected_language = st.sidebar.selectbox("🌍 **Transcription Language**", languages)

# Upload audio file section with a nice emoji
uploaded_audio = st.file_uploader("🔊 **Upload an audio file (MP3, WAV, M4A)** 🎶", type=["mp3", "wav", "m4a"])

# Function to transcribe audio using OpenAI Whisper API
def transcribe_audio(client, audio_file, language):
    with open(audio_file, "rb") as audio_content:
        response = client.audio.transcriptions.create(
            file=audio_content,
            model="whisper-1",
            response_format="verbose_json",  # Detailed results with verbose_json
            timestamp_granularities=["word"],
            language=language[:2].lower()  # Convert language to ISO code
        )
    return response

# Transcription action with styled buttons and result display
if uploaded_audio:
    # Save the uploaded file temporarily to disk
    with open("temp_audio.mp3", "wb") as temp_file:
        temp_file.write(uploaded_audio.getbuffer())

    st.audio(uploaded_audio, format="audio/mp3")
    
    if st.button("🎧 **Transcribe Audio**"):
        try:
            # Perform transcription
            transcription_response = transcribe_audio(client, "temp_audio.mp3", selected_language)

            # Extract text from the transcription response
            transcription_text = transcription_response.text
            st.markdown("### 📝 **Transcription Result**")
            st.success(transcription_text)
            
            # Add Copy and Download buttons with emojis
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("📋 **Copy Transcription**"):
                    pyperclip.copy(transcription_text)
                    st.write("✅ **Transcription copied to clipboard!**")
            
            with col2:
                st.download_button(
                    label="📥 **Download Transcription as .txt**",
                    data=transcription_text,
                    file_name="transcription.txt",
                    mime="text/plain"
                )
        
        except Exception as e:
            st.error("❌ **An error occurred during transcription.**")
            st.write(f"Error: {e}")

# Sidebar User Guide with emoji
st.sidebar.markdown("### 💡 **How to Use**")
st.sidebar.write("""
1. **Upload an Audio File**: Select an audio file for transcription.
2. **Choose Transcription Language**: Select the language spoken in the audio.
3. **Transcribe and Download**: Click **Transcribe**, copy, or download the transcription!
""")
st.sidebar.info("✨ **Streamline your transcription process with AI-powered transcription!** 🎤")
