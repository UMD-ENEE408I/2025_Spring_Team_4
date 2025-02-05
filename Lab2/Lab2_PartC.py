import matplotlib.pyplot as plt
import numpy as np
import wave
import scipy.io.wavfile

# 1)

spf = wave.open("Cafe_with_noise.wav", "r")

# Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.frombuffer(signal, np.int16)

# 2)

# Get FFT of the raw audio
spectrum = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(spectrum))

# 3)

# Create copies of the FFT to modify
mod_spec = spectrum.copy()
mod_freq = frequencies.copy()

# Set frequency limit to filter out noise
frequency_limit = 0.03

# Apply low pass filter
for i in range(0, len(mod_freq)):
    if mod_freq[i] > frequency_limit or mod_freq[i] < -frequency_limit:
        mod_spec[i] = 0

# Modify new_sig datatype
new_sig = np.fft.ifft(mod_spec)
new_sig = np.real(new_sig).astype(np.int16)

# Write to a new waveform file
scipy.io.wavfile.write("new_Cafe_with_noise.wav", spf.getframerate(), new_sig)

# Plot data for Q1-3

# Plot raw audio data
plt.subplot(2, 2, 1, title="Imported Waveform", xlabel="Time (s)", ylabel="Amplitude")
plt.plot(signal)

# Plot raw FFT
plt.subplot(2, 2, 2, title="FFT of Imported Waveform", xlabel="Frequency", ylabel="Amplitude")
plt.plot(frequencies, spectrum)

# Plot modified FFT
plt.subplot(2, 2, 3, title="FFT of Modified Waveform", xlabel="Frequency", ylabel="Amplitude")
plt.plot(mod_freq, mod_spec)

# Plot modified audio data
plt.subplot(2, 2, 4, title="Filtered Waveform", xlabel="Time(s)", ylabel="Amplitude")
plt.plot(new_sig)

plt.show()