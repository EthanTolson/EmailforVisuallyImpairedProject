from gtts import gTTS
from constants import FILEPATH
from os import system, path, remove
import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

class VoiceControl:
    def __init__(self):
        self.speech_filename = f"{FILEPATH}temp.wav"
        self.text_filename = f"{FILEPATH}temp.mp3"

    def speech_to_text(self, length):
        self.record_audio(length)
        text = self.to_text()
        self.delete_audio_file("wav")
        return text
    
    def to_text(self):
        try:
            r = sr.Recognizer()
            with sr.AudioFile(self.speech_filename) as source:
                # listen for the data (load audio to memory)
                audio_data = r.record(source)
                # recognize (convert from speech to text)
                text = r.recognize_google(audio_data)
            return text
        except:
            self.text_to_speech("Something went wrong with speech to text.")
            return "Something went wrong with speech to text."

    def record_audio(self, length):
        fs = 44100  # Sample rate
        seconds = length  # Duration of recording
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype = np.int16)
        sd.wait()  # Wait until recording is finished
        write(self.speech_filename, fs, myrecording.astype(np.int16))

    def delete_audio_file(self, type):
        if type =="tts":
            if path.exists(self.text_filename):
                remove(self.text_filename)
        else:
            if path.exists(self.speech_filename):
                remove(self.speech_filename)

    def text_to_speech(self, text):
        """
        Gets an mp3 file from googles tts plays it then deletes it
        """
        tts = gTTS(text)
        tts.save(self.text_filename)
        system(self.text_filename)
        self.delete_audio_file("tts")