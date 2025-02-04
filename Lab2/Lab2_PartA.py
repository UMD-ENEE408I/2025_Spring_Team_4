
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import soundfile as sf
import wave
# Read the audio file
#y, Fs = sf.read("Cafe_with_noise.wav")  # Load audio data and sampling rate
test =wave.open("human_voice.wav", "r")
# Generate time vector
#t = np.linspace(0, len(y) / Fs, len(y))
# Plot the waveform
#plt.figure()
#plt.plot(t, y)
#plt.xlabel("Time (s)")
#plt.ylabel("Amplitude")
#plt.title("Waveform of the Audio Signal")
#plt.show()

# Create a Hann window
#win = signal.windows.hann(100, sym=False)  # Equivalent to MATLAB 'periodic'

# Compute STFT
#f, T, S = signal.stft(y, Fs, window=win)

# Convert magnitude to decibels
#smag = 20 * np.log10(np.abs(S) + 1e-6)  # Avoid log(0) by adding a small offset

# Plot spectrogram
#plt.figure()
#plt.pcolormesh(T, f, smag, shading='flat')  # Use pcolormesh for better visualization
#plt.xlabel("Time (s)")
#plt.ylabel("Frequency (Hz)")
#plt.colorbar(label="Magnitude (dB)")
#plt.clim(np.max(smag) - 60, np.max(smag))  # Set color limits for a 60 dB range
#plt.title("Spectrogram of the Audio Signal")
#plt.show()
