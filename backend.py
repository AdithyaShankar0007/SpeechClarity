from pydub import AudioSegment
from pydub.silence import split_on_silence
from noisereduce import reduce_noise
import speech_recognition as sr
import numpy as np
import noisereduce as nr
from pydub.exceptions import CouldntDecodeError

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

def recognize_speech(audio_path, language='en-IN'):
    try:
        # Load audio file and reduce noise
        audio = AudioSegment.from_file(audio_path)
        audio = reduce_noise(audio)
    except CouldntDecodeError:
        raise ValueError("Unsupported audio format. Please provide WAV, MP3, or FLAC files.")

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

if __name__ == "__main__":
    audio_path = "new.wav"  # Replace with the path to your audio file
    recognized_text = recognize_speech(audio_path, language='en-IN')
    print("Recognized Text:", recognized_text)
