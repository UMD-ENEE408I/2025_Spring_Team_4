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

def cross_correlation(signal1, signal2):
    len1, len2 = len(signal1), len(signal2)
    max_lag = len1 + len2 - 1
    result = np.zeros(max_lag)

    for lag in range(-len2 + 1, len1):
        sum_corr = 0
        for i in range(len1):
            j = i - lag
            if 0 <= j < len2:
                sum_corr += signal1[i] * signal2[j]
        result[lag + len2 - 1] = sum_corr  # Shift index to store in result array

    return result, np.arange(-len2 + 1, len1)

def find_time_delay(signal1, signal2, sample_rate):
    cross_corr, lags = cross_correlation(signal1, signal2)
    max_lag_index = np.argmax(cross_corr)  # Find index of maximum correlation
    lag_samples = lags[max_lag_index]  # Convert index to actual lag

    time_delay = lag_samples / sample_rate  # Convert lag to time
    return time_delay

time_delay = find_time_delay(y1,y2,8000)
print(time_delay)