import sounddevice as sd
from vosk import Model, KaldiRecognizer
import numpy as np
import json

model = Model(lang="en-us")
samplerate = 16000
rec = KaldiRecognizer(model, samplerate)

audio_buffer = bytearray()

def callback(indata, frames, time, status):
    if status:
        print(f"Status: {status}")
    audio_buffer.extend(indata.tobytes())

stream = sd.InputStream(callback=callback, channels=1, samplerate=samplerate, dtype='int16', blocksize=8000)

count = 0

with stream:
    print("Listening for 'left' or 'right'... (Ctrl+C to quit)")
    while True:
        if len(audio_buffer) >= 4000:
            chunk = bytes(audio_buffer[:4000])
            audio_buffer = audio_buffer[4000:]

            if rec.AcceptWaveform(chunk):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower()
                print(f"Recognized: {text}")
                if "left" in text:
                    count += 1
                    print(f"Heard LEFT! Count: {count}")
                elif "right" in text:
                    count -= 1
                    print(f"Heard RIGHT! Count: {count}")
                elif "chase" in text:
                    count -= 2
                    print(f"Heard CHASE! Count: {count}")
                elif "run" in text:
                    count += 2
                    print(f"Heard RUN! Count: {count}")
