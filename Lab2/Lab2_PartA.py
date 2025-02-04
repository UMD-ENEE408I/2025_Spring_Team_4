
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import soundfile as sf
import wave
import scipy.io.wavfile

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
downsample_factor = framerate / 8000 #Target 8 kHz
downsample_audio = audio_data[::int(downsample_factor)]
out_wav = wave.open("./new_human_voice.wav", 'wb')
outframerate = out_wav.setframerate(8000)
outchannelnum = out_wav.setnchannels(num_channels)
outsamplewidth = out_wav.setsampwidth(samplewidth)

outaudiodata = out_wav.writeframes(downsample_audio.tobytes())

