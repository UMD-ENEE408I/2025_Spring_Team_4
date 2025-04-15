#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3

controllerNodeName = "brian"
visionTopicName = "line_camera_topic"
commandTopicName = '/cmd_vel'
x_vec = Vector3()

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84
LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1

def vision_call_back(message):
    global x_vec
    x_vec = message

def vision_brain_line_following():
    '''
    Attempts to follow a line according to the webcam. 
    ''' 
    current_nearsight_x_val = x_vec.x

    twist = Twist()
    twist.linear.x = -0.05

    if current_nearsight_x_val > 0:
        twist.angular.z = -0.1
    elif current_nearsight_x_val < -0.2:
        twist.angular.z = 0.1
    elif current_nearsight_x_val is None:
        rospy.loginfo("None!")
        twist.angular.z = 0.0
        twist.linear.x = 0.0

    rospy.loginfo(f'Angular: {twist.angular.z}\tX Value: {current_nearsight_x_val}')
    control_publisher.publish(twist)  


rospy.init_node(controllerNodeName, anonymous=True)
rospy.Subscriber(visionTopicName, Vector3, vision_call_back)
control_publisher = rospy.Publisher(commandTopicName, Twist, queue_size=10)
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    vision_brain_line_following()
    rate.sleep()


