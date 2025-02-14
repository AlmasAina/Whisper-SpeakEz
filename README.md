# SpeakEz - Speech-to-Text with Pronunciation Feedback

## Overview
SpeakEz is a **Streamlit-based Speech-to-Text** application that utilizes **OpenAI's Whisper model** to transcribe speech and provide pronunciation feedback. The app records user audio, transcribes it, and allows users to edit the text and compare it with the original transcription.

## Features
- 🎙 **Record Audio**: Users can record their voice directly from the app.
- 📝 **Speech-to-Text**: Uses Whisper AI to transcribe recorded speech.
- ✍ **Editable Transcription**: Users can modify the transcribed text.
- 📊 **Pronunciation Feedback**: Calculates word-matching percentage to assess pronunciation accuracy.
- 🔊 **Correct Pronunciation Audio**: Uses Google Text-to-Speech (gTTS) to generate correct pronunciation.
- 🎧 **Listen to Transcriptions**: Compare your pronunciation with the correct audio.

## Installation

### Prerequisites
Ensure you have **Python 3.8+** installed.

### Clone the Repository
```sh
git clone https://github.com/openai/whisper.git
cd whisper
## Install Dependencies

Run the following command to install required libraries:

```sh
pip install streamlit whisper numpy scipy sounddevice gtts pydub
```

## Usage

To start the SpeakEz application, run:

```sh
streamlit run app.py
```

## Project Structure

```bash
whisper/
├── app.py                 # Main application script
├── README.md              # Project documentation
└── models/                # Whisper model files (downloaded automatically)
```

## How It Works

1. Click **Start Recording** to capture your voice.
2. Once recorded, the app will **transcribe** the speech.
3. Users can **edit** the transcription and check pronunciation.
4. The app compares the transcribed and user-edited text.
5. Generates **correct pronunciation audio** using gTTS.
6. Displays **matching percentage** and highlights errors in red.

## Technologies Used

- **Python**
- **Streamlit** (for UI)
- **Whisper AI** (for speech recognition)
- **Google Text-to-Speech (gTTS)** (for pronunciation feedback)
- **SoundDevice** (for recording audio)
- **NumPy & SciPy** (for audio processing)

## Contributing

Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the **MIT License**.

## Acknowledgments

- OpenAI's **Whisper** for speech recognition.
- Streamlit for making app development simple and interactive.

