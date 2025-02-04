import matplotlib.pyplot as plt
import numpy as np
import wave

spf = wave.open("./Cafe_with_noise.wav", "r")

# Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, np.int16)

plt.figure(1)
plt.title("Signal Wave...")
plt.plot(signal)
plt.show()

spectrum = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(spectrum))
plt.plot(frequencies,spectrum)
plt.show()