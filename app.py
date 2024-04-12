import streamlit as st
import numpy as np
from backend import recognize_speech, convert_to_pcm_wav
from googletrans import Translator

def main():
    st.title("Speech Recognition and Translation App")

    # File uploader widget
    uploaded_file = st.file_uploader("Upload audio file", type=['wav', 'mp3'])

    # Initialize session state
    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = None
    if 'translated_text' not in st.session_state:
        st.session_state.translated_text = None

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with open("temp_audio", "wb") as f:
            f.write(uploaded_file.read())

        # Convert uploaded file to PCM WAV format
        pcm_wav_file = convert_to_pcm_wav("temp_audio")
        
        # Display the uploaded audio file
        st.audio(pcm_wav_file, format="audio/wav")

        # Language selection dropdown with options for different languages
        language = st.selectbox("Select language", ["Hindi", "Malayalam", "English", "Tamil"])

        # Button to trigger transcription
        if st.button("Transcribe"):
            try:
                # Call the backend function with selected language
                recognized_text = recognize_speech(pcm_wav_file, language=language.lower())
                st.session_state.recognized_text = recognized_text
            except Exception as e:
                st.error(f"Error during transcription: {e}")  # Display error message

    # Display transcribed text
    if st.session_state.recognized_text is not None:
        st.subheader("Transcribed Text:")
        st.write(st.session_state.recognized_text)

        # Check if transcription is done before asking for translation language
        if st.session_state.recognized_text:
            # Language selection dropdown for translation
            translation_language = st.selectbox("Select translation language", ["Hindi", "Malayalam", "English", "Tamil"])

            # Button to trigger translation
            if st.button("Translate"):
                try:
                    # Translate the text
                    translator = Translator()
                    translated_text = translator.translate(st.session_state.recognized_text, dest=translation_language.lower()).text
                    st.session_state.translated_text = translated_text
                except Exception as e:
                    st.error(f"Error during translation: {e}")

    # Display translated text
    if st.session_state.translated_text is not None:
        st.subheader("Translated Text:")
        st.write(st.session_state.translated_text)

if __name__ == "__main__":
    main()
