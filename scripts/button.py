#!/usr/bin/env python3

import rospy
from gpiozero import Button
from std_msgs.msg import UInt8

BUTTON_PIN = 17  # GPIO17
publisherNodeName = 'button_publisher'
topicName = 'button_topic'
rospy.init_node(publisherNodeName, anonymous = True)
publisher = rospy.Publisher(topicName, UInt8, queue_size = 1)
rate = rospy.Rate(10)

# Setup button with internal pull-up and debounce
button = Button(BUTTON_PIN, pull_up=True, bounce_time=0.05)

while not rospy.is_shutdown():
    if button.is_pressed:
        publisher.publish(1)
        rospy.loginfo("Button Pressed")
    else:
        publisher.publish(0)
        rospy.loginfo("Button Not Pressed")
    rate.sleep()


