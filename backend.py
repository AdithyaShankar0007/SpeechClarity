from pydub import AudioSegment
from pydub.silence import split_on_silence
from noisereduce import reduce_noise
import speech_recognition as sr
import numpy as np

def recognize_speech(audio_path, language='ta-IN'):
    # Load audio file and reduce noise
    audio = AudioSegment.from_file(audio_path)
    
    # Convert audio to NumPy array
    audio_array = np.array(audio.get_array_of_samples())
    
    # Extract the sampling rate from the audio object
    sample_rate = audio.frame_rate
    
    # Pass the NumPy array to reduce_noise
    audio_array = reduce_noise(audio_array, sample_rate)

    # Convert back to AudioSegment
    audio = AudioSegment(
        audio_array.tobytes(),
        frame_rate=sample_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )

    # Split audio into segments based on silence
    segments = split_on_silence(audio, silence_thresh=-36)  # Adjust silence threshold as needed

    recognized_text = ''  # Move the recognized_text variable outside the loop

    # Instantiate the Recognizer object outside the loop
    recognizer = sr.Recognizer()

    for segment in segments:
        with sr.AudioFile(segment.export(format="wav")) as source:
            audio_data = recognizer.record(source)
            
            try:
                text = recognizer.recognize_google(audio_data, language=language)
                recognized_text += text + ' '
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

    return recognized_text.strip()

if __name__ == "__main__":
    audio_path = "new.wav"  # Replace with the path to your audio file
    recognized_text = recognize_speech(audio_path, language='ta-IN')
    print("Recognized Text:", recognized_text)
