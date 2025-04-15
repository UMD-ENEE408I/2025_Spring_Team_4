#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

controllerNodeName = "brian"
visionTopicName = "line_camera_topic"
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

current_nearsight_x_val = 0

def vision_call_back(message):
    global current_nearsight_x_val
    current_nearsight_x_val = message.data

def vision_brain_line_following(nearsight_x):
    '''
    Attempts to follow a line according to the webcam. 
    ''' 
    rospy.loginfo(f'Recieved information, Nearsight coord: {nearsight_x}')


rospy.init_node(controllerNodeName, anonymous=True)
rospy.Subscriber(visionTopicName, Float32, vision_call_back)

rate = rospy.Rate(2)

while not rospy.is_shutdown():
    vision_brain_line_following(current_nearsight_x_val)
    rate.sleep()


