import streamlit as st
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
import noisereduce as nr
from googletrans import Translator
import os

# Function to reduce noise in audio
def reduce_noise(audio):
    # Convert audio to numpy array
    audio_array = np.array(audio.get_array_of_samples())

    # Perform noise reduction
    reduced_noise = nr.reduce_noise(audio_array, audio.frame_rate)

    # Convert back to AudioSegment
    reduced_audio = AudioSegment(
        reduced_noise.tobytes(), 
        frame_rate=audio.frame_rate, 
        sample_width=reduced_noise.dtype.itemsize, 
        channels=1
    )

    return reduced_audio

# Function to recognize speech
def recognize_speech(audio_path, language='en-IN'):
    # Load audio file and reduce noise
    audio = AudioSegment.from_file(audio_path)
    audio = reduce_noise(audio)

    # Language code mapping
    language_code = {
        "hindi": "hi-IN",
        "malayalam": "ml-IN",
        "english": "en-IN",
        "tamil": "ta-IN"
    }

    # Split audio into segments based on silence
    segments = split_on_silence(audio, silence_thresh=-36)  # Adjust silence threshold as needed

    recognized_text = ''
    recognizer = sr.Recognizer()

    for segment in segments:
        with sr.AudioFile(segment.export(format="wav")) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language=language_code[language])
                recognized_text += text + ' '
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

    return recognized_text.strip()

# Main function for Streamlit app
def main():
    st.title("Speech Recognition and Translation App")

    # File uploader widget
    uploaded_file = st.file_uploader("Upload audio file", type=['wav', 'mp3', 'AIFF'])

    # Initialize session state
    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = None
    if 'translated_text' not in st.session_state:
        st.session_state.translated_text = None

    if uploaded_file is not None:

        temp_audio_path = "temp_audio"
        # Save the uploaded file to a temporary location
        with open("temp_audio", "wb") as f:
            f.write(uploaded_file.read())

        # Display the uploaded audio file
        st.audio("temp_audio", format="audio/wav")

        st.write(f"Temporary audio file path: {os.path.abspath(temp_audio_path)}")

        # Language selection dropdown with options for different languages
        language = st.selectbox("Select language", ["Hindi", "Malayalam", "English", "Tamil"])

        # Button to trigger transcription
        if st.button("Transcribe"):
            try:
                # Call the backend function with selected language
                recognized_text = recognize_speech("temp_audio", language=language.lower())
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
