from pydub import AudioSegment
import speech_recognition as sr
from pydub.silence import split_on_silence
import numpy as np
import noisereduce as nr

def convert_to_pcm_wav(input_file_path):
    """
    Convert audio file to PCM WAV format.

    Args:
        input_file_path (str): Path to the input audio file.

    Returns:
        str: Path to the converted PCM WAV file.
    """
    # Load the audio file
    audio = AudioSegment.from_file(input_file_path)

    # Convert to PCM WAV format
    pcm_wav_audio = audio.set_frame_rate(16000).set_sample_width(2).set_channels(1)

    # Save the converted audio to a temporary file
    output_file_path = "temp_audio.wav"
    pcm_wav_audio.export(output_file_path, format="wav")

    return output_file_path

def reduce_noise(audio):
    """
    Reduce noise from audio.

    Args:
        audio (AudioSegment): Input audio.

    Returns:
        AudioSegment: Audio with reduced noise.
    """
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
    """
    Recognize speech from audio.

    Args:
        audio_path (str): Path to the input audio file.
        language (str): Language code (default: 'en-IN').

    Returns:
        str: Recognized text.
    """
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
