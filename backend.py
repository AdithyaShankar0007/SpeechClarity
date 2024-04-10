from pydub import AudioSegment
from pydub.silence import split_on_silence
from noisereduce import reduce_noise  # Comment out if not using noise reduction
import speech_recognition as sr
import numpy as np
import soundfile as sf

def recognize_speech(audio_filepath, language='en-IN'):
  """
  Performs speech recognition on an audio file with error handling and format conversion.

  Args:
      audio_filepath: Path to the audio file
      language: Language code for Google Speech Recognition (defaults to en-IN)

  Returns:
      Recognized text or an empty string if errors occur
  """

  # Language code mapping
  language_code = {
      "hindi": "hi-IN",
      "malayalam": "ml-IN",
      "english": "en-IN",
      "tamil": "ta-IN"
  }

  try:
    # Attempt to convert audio to WAV format if necessary
    if not convert_to_wav(audio_filepath):
      return ""

    # Load audio (now guaranteed to be WAV)
    audio = AudioSegment.from_wav(audio_filepath)

    # Optional noise reduction (uncomment if needed)
    # audio = reduce_noise(audio.raw_data, sr=4000)

    # Split audio into segments
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
  except (FileNotFoundError, sf.SoundFileError) as e:
    print(f"Error processing audio file: {e}")
    return ""

def convert_to_wav(audio_path, output_path="temp_audio.wav"):
  """
  Converts an audio file to WAV format (if necessary)

  Args:
      audio_path: Path to the input audio file
      output_path: Path to save the converted WAV file (defaults to temp_audio.wav)

  Returns:
      True if conversion was successful, False otherwise
  """
  try:
    data, samplerate = sf.read(audio_path)
    sf.write(output_path, data, samplerate)
    return True
  except (sf.SoundFileError, FileNotFoundError) as e:
    print(f"Error converting audio: {e}")
    return False

# Example usage (for testing purposes, comment out when deploying)
# audio_path = "new.wav"
# recognized_text = recognize_speech(audio_path, language='en-IN')
# print("Recognized Text:", recognized_text)
