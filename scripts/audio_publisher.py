#!/usr/bin/env python3

import rospy
import argparse
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import numpy as np
from std_msgs.msg import UInt8

q = queue.Queue()
output_cmd = 0
publisherNodeName='audio_sensor_publisher'
topicName='audio_topic'

rospy.init_node(publisherNodeName, anonymous=True)

publisher = rospy.Publisher(topicName, UInt8, queue_size=1)

rate = rospy.Rate(50)
def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)

model = Model(lang="en-us")
if args.filename:
    dump_fn = open(args.filename, "wb")
else:
    dump_fn = None
if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])
with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype="int16", channels=1, callback=callback):
    rec = KaldiRecognizer(model, args.samplerate)
    rospy.loginfo(f"Now Recording!")
    while not rospy.is_shutdown():
            
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "").lower()
            rospy.loginfo(f"Recognized text: '{text}'")
            rospy.loginfo(rec.Result())
            if "left" in text:
                output_cmd = 1
                rospy.loginfo(f"Heard LEFT! CMD: {output_cmd}")
                publisher.publish(output_cmd)
            elif "right" in text:
                output_cmd = 2
                rospy.loginfo(f"Heard RIGHT! CMD: {output_cmd}")
                publisher.publish(output_cmd)
            elif "chaser" in text:
                output_cmd = 3
                rospy.loginfo(f"Heard CHASER! CMD: {output_cmd}")
                publisher.publish(output_cmd)
            elif "runner" in text:
                output_cmd = 4
                rospy.loginfo(f"Heard RUNNER! CMD: {output_cmd}")
                publisher.publish(output_cmd)
            
        #else:
            #   print(rec.PartialResult())
        if dump_fn is not None:
            dump_fn.write(data)

        rate.sleep()