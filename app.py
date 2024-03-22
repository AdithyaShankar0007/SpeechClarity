import streamlit as st
from backend import recognize_speech
import tempfile
import os

def main():
    st.title("Speech Recognition and Translation App")
    
    # File uploader widget
    uploaded_file = st.file_uploader("Upload audio file", type=['wav', 'mp3'])
    
    # Initialize session state
    if 'recognized_text' not in st.session_state:
        st.session_state.recognized_text = None
    
    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            temp_audio.write(uploaded_file.read())
            temp_audio_path = temp_audio.name
        
        # Display the uploaded audio file
        st.audio(temp_audio_path, format="audio/wav")
        
        # Button to trigger transcription
        if st.button("Transcribe"):
            # Call the backend function to recognize speech
            recognized_text = recognize_speech(temp_audio_path, language='ta-IN')
            
            # Update session state with transcribed text
            st.session_state.recognized_text = recognized_text
    
    # Display transcribed text
    if st.session_state.recognized_text is not None:
        st.subheader("Transcribed Text:")
        st.write(st.session_state.recognized_text)

if __name__ == "__main__":
    main()
