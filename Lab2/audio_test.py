import numpy as np
import scipy.signal as signal
import matplotlib as plt
import pyaudio
import time
import wave
import pyaudio
import wave
# Parameters
FORMAT = pyaudio.paInt16  # 16-bit audio
CHANNELS = 1  # Mono audio
RATE = 44100  # Sample rate in Hz
CHUNK = 1024  # Buffer size
RECORD_SECONDS = 5  # Duration of recording
OUTPUT_FILENAME = "output.wav"  # Output file name

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open the stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")
frames = []

# Record the audio
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording finished.")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recorded data to a WAV file
with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Audio recorded and saved as {OUTPUT_FILENAME}")
