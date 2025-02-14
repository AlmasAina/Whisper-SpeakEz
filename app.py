import streamlit as st
import whisper
import os
import tempfile
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from gtts import gTTS
import pydub

# Load the Whisper model
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# Streamlit UI
st.title("🎤 SpeakEz - Speech-to-Text with Pronunciation Feedback")

# **Initialize session state**
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None
if "transcription" not in st.session_state:
    st.session_state.transcription = ""
if "edited_transcription" not in st.session_state:
    st.session_state.edited_transcription = ""
if "check_pronunciation_clicked" not in st.session_state:
    st.session_state.check_pronunciation_clicked = False

# **Audio Recording Function**
def record_audio(fs=44100, duration=5):
    """Record audio and save it to session state."""
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.int16)
    sd.wait()

    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, "recorded_audio.wav")
    wav.write(audio_path, fs, recording)

    return audio_path

# **Audio Recording Section**
st.subheader("🎙 Record Your Audio")
if st.button("▶ Start Recording"):
    st.session_state.audio_path = record_audio()
    st.session_state.transcription = ""  # Reset transcription when recording new audio
    st.session_state.edited_transcription = ""

# **Ensure recorded audio is always displayed**
if st.session_state.audio_path:
    st.subheader("🔊 Your Recorded Audio")
    st.audio(st.session_state.audio_path, format="audio/wav")

# **Transcription Section**
if st.session_state.audio_path and not st.session_state.transcription:
    st.subheader("📝 Transcription")
    with st.spinner("Transcribing... ⏳"):
        try:
            result = model.transcribe(st.session_state.audio_path, language="en")  # Always transcribe in English
            transcription_text = result.get("text", "").strip()

            if not transcription_text:
                st.warning("⚠️ No speech detected! Please try again.")
                transcription_text = "No transcription available."

            st.session_state.transcription = transcription_text  # Store once
            st.session_state.edited_transcription = transcription_text  # Keep editable version the same

        except Exception as e:
            st.error(f"❌ Error during transcription: {e}")
            st.session_state.transcription = "Error in transcription"
            st.session_state.edited_transcription = "Error in transcription"

# **Editable Transcription (Persistent)**
st.subheader("✍ Edit Transcription")
st.session_state.edited_transcription = st.text_area("Edit the transcription:", st.session_state.edited_transcription)

# **Check Pronunciation Button**
if st.button("🔍 Check Pronunciation"):
    st.session_state.check_pronunciation_clicked = True

# **Ensure recorded audio remains visible**
if st.session_state.audio_path:
    st.subheader("🎧 Your Recorded Audio")
    st.audio(st.session_state.audio_path, format="audio/wav")

# **Pronunciation Check Section**
if st.session_state.check_pronunciation_clicked:
    st.subheader("📊 Word Matching Percentage")

    # **Step 1: Compare Transcription with User's Edited Text**
    def calculate_word_match_percentage(correct_text, user_text):
        correct_words = set(correct_text.lower().split())
        user_words = set(user_text.lower().split())

        if not correct_words or not user_words:
            return 0  # Avoid errors if text is missing

        matching_words = correct_words.intersection(user_words)
        match_percentage = (len(matching_words) / len(correct_words)) * 100
        return match_percentage

    match_percentage = calculate_word_match_percentage(st.session_state.transcription, st.session_state.edited_transcription)
    
    if match_percentage == 0:
        st.error("❌ No matching words found! The text and audio seem completely different.")
    else:
        st.write(f"🔵 Words matched percentage: **{match_percentage:.2f}%**")

    # **Step 2: Generate Correct Pronunciation Audio**
    if st.session_state.edited_transcription:
        tts = gTTS(text=st.session_state.edited_transcription, lang="en")  # Always generate English pronunciation
        correct_audio_path = "correct_pronunciation.mp3"
        tts.save(correct_audio_path)

        # Convert to WAV format
        sound = pydub.AudioSegment.from_mp3(correct_audio_path)
        sound.export("correct_pronunciation.wav", format="wav")

        st.subheader("🔊 Listen to Correct Pronunciation")
        st.audio("correct_pronunciation.wav", format="audio/wav")

    # **Step 3: Display Pronunciation Issues**
    def highlight_mistakes(correct, user):
        correct_words = set(correct.split())
        user_words = set(user.split())

        highlighted_text = []
        for word in correct.split():
            if word.lower() in user_words:
                highlighted_text.append(f'<span style="color:green;">{word}</span>')  # Correct words
            else:
                highlighted_text.append(f'<span style="color:red;">{word}</span>')  # Incorrect words

        return " ".join(highlighted_text)

    highlighted_output = highlight_mistakes(st.session_state.transcription, st.session_state.edited_transcription)
    st.markdown(f"**🔍 Previous Output:** {highlighted_output}", unsafe_allow_html=True)
