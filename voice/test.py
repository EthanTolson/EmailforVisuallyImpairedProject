from gtts import gTTS

from os import system, path
import speech_recognition as sr
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

# from pydub import AudioSegment

import subprocess

directory = f"{path.dirname(path.abspath(__file__))}/"
filename = f"{directory}test3.mp3"
wav = f"{directory}test4.wav"

# test = "The red tiger ate the children.."


# tts = gTTS(test)

# tts.save(filename)

# system(filename)

# subprocess.call(['ffmpeg', '-i', f'{filename.replace("//", "/")}', f'{wav.replace("//", "/")}'])
# AudioSegment.from_mp3("test1.mp3").export("test1.wav", format="wav")

file = "test1.mp3"

fs = 44100  # Sample rate
seconds = 3  # Duration of recording
print("______________Recording Beginning_____________________")
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype = np.int16)
sd.wait()  # Wait until recording is finished
print("______________Recording Finished______________________")
write(wav, fs, myrecording.astype(np.int16))

r = sr.Recognizer()
with sr.AudioFile(wav) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data)
    print(text)



