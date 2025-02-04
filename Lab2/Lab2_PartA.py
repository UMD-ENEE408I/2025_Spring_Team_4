
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import soundfile as sf
import wave
# Read the audio file
wav_file = wave.open("./human_voice.wav", "rb") 
framerate = wav_file.getframerate()
num_frames = wav_file.getnframes()
samplewidth = wav_file.getsampwidth()
num_channels = wav_file.getnchannels()

audio_data = wav_file.readframes(num_frames)
audio_data = np.fromstring(audio_data, np.int16)
#Get sample freq and plot!
print("Frame rate is ", framerate, "Hz\n")
plt.figure()
plt.title("Human voice")
plt.plot(audio_data)
plt.show()
#Downsample!
write_file = wave.open("./new_human_voice.wav", "wb")
