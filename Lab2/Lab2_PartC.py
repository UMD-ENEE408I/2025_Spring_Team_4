import matplotlib.pyplot as plt
import numpy as np
import wave
import scipy.io.wavfile

spf = wave.open("Cafe_with_noise.wav", "r")

# Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.frombuffer(signal, np.int16)

spectrum = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(spectrum))

mod_spec = spectrum.copy()
mod_freq = frequencies.copy()

frequency_limit = 0.025
for i in range(0, len(mod_freq)):
    if mod_freq[i] > frequency_limit or mod_freq[i] < -frequency_limit:
        mod_freq[i] = 0
        mod_spec[i] = 0

new_sig = np.fft.ifft(mod_spec)
new_sig = np.real(new_sig)  # Take only the real part (discard numerical noise from IFFT)
new_sig = np.int16(new_sig)  # Convert to 16-bit integer format

scipy.io.wavfile.write("new_Cafe_with_noise.wav", spf.getframerate(), new_sig)


plt.subplot(2, 2, 1, title="Imported Waveform", xlabel="Time (s)", ylabel="Amplitude")
plt.plot(signal)
plt.subplot(2, 2, 2, title="FFT of Imported Waveform", xlabel="Frequency", ylabel="Amplitude")
plt.plot(frequencies, spectrum)
plt.subplot(2, 2, 3, title="FFT of Modified Waveform", xlabel="Frequency", ylabel="Amplitude")
plt.plot(mod_freq, mod_spec)
plt.subplot(2, 2, 4, title="", xlabel="Time(s)", ylabel="Amplitude")
plt.plot(new_sig)

plt.show()