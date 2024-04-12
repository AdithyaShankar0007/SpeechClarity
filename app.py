import streamlit as st
from backend import recognize_speech
from googletrans import Translator
import wave

def main():
    st.title("Speech Recognition and Translation App")

    # File uploader widget
    uploaded_file = st.file_uploader("Upload audio file", type=['wav', 'mp3','flac'])

    # Initialize session state
    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = None
    if 'translated_text' not in st.session_state:
        st.session_state.translated_text = None

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with open("temp_audio.wav", "wb") as f:
            f.write(uploaded_file.read())

        # Display the uploaded audio file
        st.audio("temp_audio.wav", format="audio/wav")

        # Language selection dropdown with options for different languages
        language = st.selectbox("Select language", ["Hindi", "Malayalam", "English", "Tamil"])

        # Button to trigger transcription
        if st.button("Transcribe"):
            try:
                # Call the backend function with selected language
                recognized_text = recognize_speech("temp_audio.wav", language=language.lower())
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

    # Debug: Inspect audio file properties using wave module
    if uploaded_file is not None:
        try:
            with wave.open("temp_audio.wav", "rb") as wav_file:
                params = wav_file.getparams()
                st.subheader("Audio File Properties:")
                st.write(f"Audio format: {params[0]}")
                st.write(f"Number of channels: {params[0]}")
                st.write(f"Sample width: {params[1]}")
                st.write(f"Frame rate: {params[2]}")
                st.write(f"Number of frames: {params[3]}")
        except Exception as e:
            st.error(f"Error opening WAV file: {e}")

if __name__ == "__main__":
    main()
