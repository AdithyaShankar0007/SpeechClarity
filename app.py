import streamlit as st
from backend import recognize_speech
from googletrans import Translator
import tempfile
import soundfile as sf
import sounddevice as sd
import numpy as np

def record_audio(file_path, duration=5):
    fs = 44100
    seconds = duration

    st.info("Recording audio...")
    my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, dtype=np.int16)
    sd.wait()

    st.info("Finished recording")
    sf.write(file_path, my_recording, fs)

def main():
    st.title("Speech Recognition and Translation App")

    # Record audio
    st.subheader("Record Audio")
    recording = st.button("Start Recording")
    audio_file_path = None
    if recording:
        with st.spinner("Recording..."):
            audio_file_path = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
            record_audio(audio_file_path)
            st.success("Recording complete!")
            st.audio(audio_file_path, format="audio/wav")

    # File uploader widget
    uploaded_file = st.file_uploader("Or upload an audio file", type=['wav', 'mp3'])

    # Language selection dropdown with options for different languages
    language = st.selectbox("Select language", ["Hindi", "Malayalam", "English", "Tamil"])

    # Initialize session state
    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = None
    if 'translated_text' not in st.session_state:
        st.session_state.translated_text = None

    # If audio is recorded or uploaded
    if audio_file_path or uploaded_file:
        if audio_file_path:
            audio_path = audio_file_path
        else:
            # Save uploaded audio to a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(uploaded_file.read())
                audio_path = f.name

        # Display the uploaded or recorded audio file
        st.audio(audio_path, format="audio/wav")

        # Button to trigger transcription
        if st.button("Transcribe"):
            # Call the backend function with selected language
            recognized_text = recognize_speech(audio_path, language=language.lower())
            st.session_state.recognized_text = recognized_text

    # Display transcribed text
    if st.session_state.recognized_text is not None:
        st.subheader("Transcribed Text:")
        st.write(st.session_state.recognized_text)

    # Reactive function to translate text when language selection changes
    @st.cache
    def translate_text(text, dest_language):
        translator = Translator()
        translated_text = translator.translate(text, dest=dest_language).text
        return translated_text

    # Check if transcription is done before asking for translation language
    if st.session_state.recognized_text:
        # Language selection dropdown for translation
        translation_language = st.selectbox("Select translation language", ["Hindi", "Malayalam", "English", "Tamil"])
        st.session_state.translation_language = translation_language.lower()

        # Button to trigger translation
        if st.button("Translate"):
            # Translate the text
            st.session_state.translated_text = translate_text(st.session_state.recognized_text, st.session_state.translation_language)

    # Display translated text
    if st.session_state.translated_text is not None:
        st.subheader("Translated Text:")
        st.write(st.session_state.translated_text)

if __name__ == "__main__":
    main()
