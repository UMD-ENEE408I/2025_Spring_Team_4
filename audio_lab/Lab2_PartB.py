import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import soundfile as sf

# 1)

#Load Audio Data and Sample Rate
y1, Fs1 = sf.read("M1.wav")
y2, Fs2 = sf.read("M2.wav")
y3, Fs3 = sf.read("M3.wav")

#Filtering out the zeros
filtered1 = y1[y1 != 0]
filtered2 = y2[y2 != 0]
filtered3 = y3[y3 != 0]

#RMS Function
def rms(arr):
    return np.sqrt(np.mean(arr**2))

#Calculating RMS values
rms_value1 = rms(filtered1)
print("The RMS value for M1.wav: ", rms_value1)

rms_value2 = rms(filtered2)
print("The RMS value for M2.wav: ", rms_value2)

rms_value3 = rms(filtered3)
print("The RMS value for M3.wav: ", rms_value3)

#The RMS value for M1.wav:  0.39026345910460114
#The RMS value for M2.wav:  0.3121995986056947
#The RMS value for M3.wav:  0.39026345910460114

#2) 
#The microphone is closer to M1 since the rms value of M1>M2.

#3)

# def cross_correlation(x, y):
#     """Compute cross-correlation of two signals manually."""
#     len_x = len(x)
#     len_y = len(y)
#     corr = np.zeros(len_x + len_y - 1)
    
#     for m in range(-(len_x - 1), len_y):
#         sum_val = 0
#         for n in range(len_x):
#             if 0 <= n - m < len_y:
#                 sum_val += x[n] * y[n - m]
#         corr[m + len_x - 1] = sum_val
    
#     return corr

# def find_time_delay(signal1, signal2, sampling_rate):
#     """Find the time delay between two signals."""
#     corr = cross_correlation(signal1, signal2)
#     delay_samples = np.argmax(corr) - (len(signal1) - 1)
#     time_delay = delay_samples / sampling_rate
#     return time_delay

# # Example usage
# sampling_rate = 8000  # 8 kHz as mentioned
# delay = find_time_delay(y1, y3, sampling_rate)
# print(f"Time delay: {delay} seconds")

def cross_correlation_fft(x, y):
    n = len(x) + len(y) - 1  # Length for FFT
    X = np.fft.fft(x, n)  # FFT of signal1
    Y = np.fft.fft(y, n)  # FFT of signal2
    corr = np.fft.ifft(X * np.conj(Y)).real  # Compute cross-correlation
    return np.fft.fftshift(corr)  # Shift for correct alignment

def find_time_delay(signal1, signal2, sampling_rate):
    corr = cross_correlation_fft(signal1, signal2)
    delay_samples = np.argmax(corr) - (len(signal1) - 1)  # Find peak index
    time_delay = delay_samples / sampling_rate
    return time_delay

# Example usage
sampling_rate = 8000  # 8 kHz
delay = find_time_delay(y1, y3, sampling_rate)
print(f"Time delay: {delay} seconds")
