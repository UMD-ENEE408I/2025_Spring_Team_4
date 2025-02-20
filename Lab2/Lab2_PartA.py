
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

#Get sample freq and start subplot!
print("Frame rate is ", framerate, "Hz\n")
plt.figure(1)
plt.subplot(2, 1, 1)
plt.title("Human voice")
plt.plot(audio_data)

#Downsample!
downsample_factor = framerate / 8000 #Target 8 kHz
downsample_audio = audio_data[::int(downsample_factor)]
out_wav = wave.open("./new_human_voice.wav", 'wb')
outframerate = out_wav.setframerate(8000)
outchannelnum = out_wav.setnchannels(num_channels)
outsamplewidth = out_wav.setsampwidth(samplewidth)
#Get output audio data
out_wav.writeframes(downsample_audio.tobytes())

#Plotting!
print("Audio samples of down sample is ", len(downsample_audio))
plt.subplot(2, 1, 2)
plt.title("Downsampled Voice")
plt.plot(downsample_audio)
plt.show()


#A notable difference in the 2 waveforms is that the high frequency content within the original sample is now removed in the downsampled audio.
#This will result in a lower quality/less detailed audio.
#There are also minor amplitude changes in the waveform