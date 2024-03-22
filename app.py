import streamlit as st
from backend import recognize_speech
from googletrans import Translator
import numpy as np

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
        with open("temp_audio.wav", "wb") as f:
            f.write(uploaded_file.read())
        
        # Display the uploaded audio file
        st.audio("temp_audio.wav", format="audio/wav")
        
        # Button to trigger transcription
        if st.button("Transcribe"):
            # Call the backend function to recognize speech
            recognized_text = recognize_speech("temp_audio.wav", language='ta-IN')
            
            # Update session state with transcribed text
            st.session_state.recognized_text = recognized_text
    
    # Display transcribed text
    if st.session_state.recognized_text is not None:
        st.subheader("Transcribed Text:")
        st.write(st.session_state.recognized_text)
    
    # Button to trigger translation
    if st.session_state.recognized_text is not None and st.session_state.translated_text is None:
        if st.button("Translate"):
            # Translate the text
            translator = Translator()
            translated_text = translator.translate(st.session_state.recognized_text, dest='en').text
            
            # Update session state with translated text
            st.session_state.translated_text = translated_text
    
    # Display translated text
    if st.session_state.translated_text is not None:
        st.subheader("Translated Text:")
        st.write(st.session_state.translated_text)

if __name__ == "__main__":
    main()
