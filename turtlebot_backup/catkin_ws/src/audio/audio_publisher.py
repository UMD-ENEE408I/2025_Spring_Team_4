#!/usr/bin/env python3

import rospy
import numpy as np
#import scipy.signal as signal
#import soundfile as sf
import matplotlib as plt
import pyaudio
import time
import wave


publisherNodeName = 'microphone_sensor_publisher'
topicName = 'audio_topic'

rospy.init_node(publisherNodeName, anonymous = True)
#Goals are to import a trained model to recognize left and right
#Use microphones to detect whether signal is coming from left or right 