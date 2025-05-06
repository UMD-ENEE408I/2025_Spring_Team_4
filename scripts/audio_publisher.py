#!/usr/bin/env python3
import rospy
import sys
from std_msgs.msg import UInt8
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import numpy as np
import json
import queue



output_cmd = 0
publisherNodeName='audio_sensor_publisher'
topicName='audio_topic'

rospy.init_node(publisherNodeName, anonymous=True)

publisher = rospy.Publisher(topicName, UInt8, queue_size=1)


audio_buffer = queue.Queue()
model = Model(model_name="vosk-model-small-en-us-0.15")
samplerate = 16000
rec = KaldiRecognizer(model, samplerate)
rec.SetWords(True)

def callback(indata, frames, time, status):
    if status:
        print(f"Status: {status}")
    audio_buffer.put(indata.tobytes())

stream = sd.InputStream(callback=callback, channels=1, samplerate=samplerate, dtype='int16', blocksize=8000)

with stream:
    rospy.loginfo("Listening for CMDS!... (Ctrl+C to quit)")
    while not rospy.is_shutdown():
            chunk = audio_buffer.get()
            rospy.loginfo(f"AH")
            if rec.AcceptWaveform(chunk):
                text = json.loads(rec.Result())["text"].lower()
                rospy.loginfo(f"Recognized: {text}")
                if "left" in text:
                    output_cmd = 1
                    rospy.loginfo(f"Heard LEFT! CMD: {output_cmd}")
                    publisher.publish(output_cmd)
                elif "right" in text:
                    output_cmd = 2
                    rospy.loginfo(f"Heard RIGHT! CMD: {output_cmd}")
                    publisher.publish(output_cmd)
                elif "chase" in text:
                    output_cmd = 3
                    rospy.loginfo(f"Heard CHASE! CMD: {output_cmd}")
                    publisher.publish(output_cmd)
                elif "run" in text:
                    output_cmd = 4
                    rospy.loginfo(f"Heard RUN! CMD: {output_cmd}")
                    publisher.publish(output_cmd)
        