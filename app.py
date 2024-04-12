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
    audio_array = np.array(audio.get_array_of_samples())
    reduced_noise = nr.reduce_noise(audio_array, audio.frame_rate)
    reduced_audio = AudioSegment(
        reduced_noise.tobytes(),
        frame_rate=audio.frame_rate,
        sample_width=reduced_noise.dtype.itemsize,
        channels=1
    )
    return reduced_audio

# Function to recognize speech
def recognize_speech(audio_path, language='en-IN'):
    audio = AudioSegment.from_file(audio_path)
    audio = reduce_noise(audio)

    language_code = {
        "hindi": "hi-IN",
        "malayalam": "ml-IN",
        "english": "en-IN",
        "tamil": "ta-IN"
    }

    segments = split_on_silence(audio, silence_thresh=-36)

    recognized_text = ''
    recognizer = sr.Recognizer()

    for segment in segments:
        with sr.AudioFile(segment.export(format="wav")) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language=language_code[language])
                recognized_text += text + ' '
            except sr.UnknownValueError:
                st.warning("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                st.error(f"Could not request results from Google Speech Recognition service; {e}")

    return recognized_text.strip()

# Main function for Streamlit app
def main():
    st.title("Speech Recognition and Translation App")

    uploaded_file = st.file_uploader("Upload audio file", type=['wav', 'mp3', 'AIFF'])

    if uploaded_file is not None:
        with st.spinner("Processing audio..."):
            temp_audio_path = "temp_audio.wav"
            with open(temp_audio_path, "wb") as f:
                f.write(uploaded_file.read())

            st.audio(temp_audio_path, format="audio/wav")

            language = st.selectbox("Select language", ["Hindi", "Malayalam", "English", "Tamil"])

            if st.button("Transcribe"):
                try:
                    recognized_text = recognize_speech(temp_audio_path, language=language.lower())
                    st.subheader("Transcribed Text:")
                    st.write(recognized_text)
                except Exception as e:
                    st.error(f"Error during transcription: {e}")

    if st.session_state.recognized_text is not None:
        translation_language = st.selectbox("Select translation language", ["Hindi", "Malayalam", "English", "Tamil"])

        if st.button("Translate"):
            try:
                translator = Translator()
                translated_text = translator.translate(st.session_state.recognized_text, dest=translation_language.lower()).text
                st.subheader("Translated Text:")
                st.write(translated_text)
            except Exception as e:
                st.error(f"Error during translation: {e}")

if __name__ == "__main__":
    main()
