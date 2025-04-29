#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import std_msgs.msg import UInt8
import RPi.GPIO as GPIO
import time

BUTTON_PIN = 17  # GPIO17 (physical pin 11)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up resistor

rate = rospy.Rate(10)
count = 0
publisherNodeName = 'button_publisher'
topicName = 'controller_topic'
rospy.init_node(publisherNodeName, anonymous = True)
publisher = rospy.Publisher(topicName, UInt8, queue_size = 1)
def main():
    try:
        while not rospy.is_shutdown():
            button_pressed = not GPIO.input(BUTTON_PIN)  # Active-low
            if button_pressed:
                count += 1
                rospy.loginfo(f"Button pressed: Count = {count}")
                publisher.publish(count)  #publish on button press!
            rate.sleep()
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
