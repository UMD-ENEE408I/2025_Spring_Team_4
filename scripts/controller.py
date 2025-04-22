#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from turtlebot3_msgs.msg import Sound
from collections import deque

controllerNodeName = "brian"
visionTopicName = "line_camera_topic"
commandTopicName = 'cmd_vel'
soundTopicName = 'sound'
x_vec = Vector3()

TURN_STATE = 0
WALK_STATE = 1

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84
LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.3

class brian:
    def __init__(self, rate, left_guard=-0.1, right_guard=0.1, sample_window=5):
        self.left_guard = left_guard
        self.right_guard = right_guard
        self.x_lin_target = 0
        self.angular_target = 0
        self.sample_queue = deque(maxlen=sample_window)
        self.target = Twist()
        self.state = 0
        self.state_count = 0
        self.rate = rate
        self.control_publisher = rospy.Publisher(commandTopicName, Twist, queue_size=10)
    
    def process_nearsight(self, line_x_value):
        """
        Given the x value of where the nearsight vision detected the line, determines if the turtlebot should veer left or right. 
        
        Args:
            line_x_value (float64): The x coordinate of the line in the near sight vision (value from -1 to 1).
            left_guard (float64): If the x coord is futher left than this limit, this func will return 1 to turn right.
            right_guard (float64): If the x coord is further right than this limit, this func will return -1 to turn left.   
        
        Returns:
            result (int): -1, 0, or 1. -1 is turn left, 0 is do nothing, 1 is turn right
        """
        try:
            self.sample_queue.popleft()
        except IndexError:
            pass

        self.sample_queue.append(line_x_value)
        sum = 0
        for item in self.sample_queue:
            sum += item
        result = sum/len(self.sample_queue)

        if result < self.left_guard:
            return 1
        elif result > self.right_guard:
            return -1
        else:
            return 0

    def determine_angular_target(self):
        rl = self.process_nearsight(x_vec.x)
        if rl == -1: # turn left
            self.target.angular.z = -ANG_VEL_STEP_SIZE
        elif rl == 1:
            self.target.angular.z = ANG_VEL_STEP_SIZE
        else:
            self.target.angular.z = 0

    def check_bounds(self):
        if self.target.angular.z > BURGER_MAX_ANG_VEL:
            self.target.angular.z = BURGER_MAX_ANG_VEL
        elif self.target.angular.z < -BURGER_MAX_ANG_VEL:
            self.target.angular.z = -BURGER_MAX_ANG_VEL

        if self.target.linear.x > BURGER_MAX_LIN_VEL:
            self.target.linear.x = BURGER_MAX_LIN_VEL
        elif self.target.linear.x < -BURGER_MAX_LIN_VEL:
            self.target.linear.x = -BURGER_MAX_LIN_VEL

    def look_forwards(self):
        pass

    def think(self):
        if self.state_count < self.rate:
            self.state_count = self.state_count + 1
        else:
            self.state = TURN_STATE if self.state is not TURN_STATE else WALK_STATE
            self.state_count = 0
        
        if self.state is TURN_STATE:
            self.target.linear.x = 0
            self.determine_angular_target()
        elif self.state is WALK_STATE:
            self.target.linear.x = -0.05
            self.target.angular.z = 0

        self.check_bounds()
        rospy.loginfo(f'Angular: {self.target.angular.z}\tLinear: {self.target.linear.x}\tState: {self.state}')
        self.control_publisher.publish(self.target)

def vision_call_back(message):
    global x_vec
    x_vec = message


rospy.init_node(controllerNodeName, anonymous=True)
rospy.Subscriber(visionTopicName, Vector3, vision_call_back)
frequency = 50
rate = rospy.Rate(frequency)
brain = brian(frequency)

while not rospy.is_shutdown():
    brain.think()
    rate.sleep()


