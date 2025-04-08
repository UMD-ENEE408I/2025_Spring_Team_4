#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import String
import argparse
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer

q = queue.Queue()

publisherNodeName='audio_sensor_publisher'
topicName='audio_topic'

rospy.init_node(publisherNodeName, anonymous=True)

publisher = rospy.Publisher(topicName, String, queue_size=2)

rate = rospy.Rate(1)

model = Model(lang="en-us")
with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype="int16", channels=1, callback=callback):
    rec = KaldiRecognizer(model, args.samplerate)
    while not rospy.is_shutdown():
            
        data = q.get()
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print(rec.PartialResult())
        if dump_fn is not None:
            dump_fn.write(data)
    
        rate.sleep()