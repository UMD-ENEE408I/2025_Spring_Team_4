#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from std_msgs.msg import UInt8
from turtlebot3_msgs.msg import Sound
from collections import deque

controllerNodeName = "brian"
visionTopicName = "line_camera_topic"
commandTopicName = 'cmd_vel'
audioTopicName = 'audio_topic'

x_vec = Vector3()
last_heard_cmd = 0

TURN_STATE = 0
WALK_STATE = 1

CMD_NULL = 0
CMD_LEFT = 1
CMD_RIGHT = 2
CMD_CHASER = 3
CMD_RUNNER = 4

LEFT = 1
RIGHT = -1

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
        self.sample_window = sample_window
        self.nearsight_sample_queue = deque(maxlen=sample_window)
        self.far_right_sample_queue = deque(maxlen=sample_window*2)
        self.far_left_sample_queue = deque(maxlen=sample_window*2)
        self.predict_dir = 0
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
        if len(self.nearsight_sample_queue) == self.sample_window:
            self.nearsight_sample_queue.popleft()

        self.nearsight_sample_queue.append(line_x_value)
        sum = 0
        for item in self.nearsight_sample_queue:
            sum += item
        result = sum/len(self.nearsight_sample_queue)

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
        if len(self.far_right_sample_queue) == self.sample_window*2:
            self.far_right_sample_queue.popleft()

        if len(self.far_left_sample_queue) == self.sample_window*2:
            self.far_left_sample_queue.popleft()

        

    

    def think(self):
        global last_heard_cmd
        val = 0
        for value in self.nearsight_sample_queue:
            val += value

        try:
            if (val/len(self.nearsight_sample_queue) < -1) and (self.state is not TURN_STATE):
                self.state = TURN_STATE
                self.target.linear.x = 0
            else:
                if last_heard_cmd is CMD_CHASER:
                    self.state = WALK_STATE
                    last_heard_cmd = CMD_NULL
        except ZeroDivisionError:
            self.state = WALK_STATE

        if self.state is TURN_STATE:
            if val/len(self.nearsight_sample_queue) > -1:
                rospy.loginfo("reset")
                last_heard_cmd = CMD_NULL

            if last_heard_cmd is CMD_RIGHT:
                self.target.angular.z = -ANG_VEL_STEP_SIZE
            elif last_heard_cmd is CMD_LEFT:
                self.target.angular.z = ANG_VEL_STEP_SIZE
            else:
                self.target.angular.z = 0
                self.target.linear.x = 0

        elif self.state is WALK_STATE:
            self.determine_angular_target()
            self.target.linear.x = -0.05

        self.check_bounds()
        rospy.loginfo(f'Angular: {self.target.angular.z}\tLinear: {self.target.linear.x}\tState: {self.state}\tCMD: {last_heard_cmd}')
        self.control_publisher.publish(self.target)

def vision_call_back(message):
    global x_vec
    x_vec = message

def audio_cmd_callback(message):
    global last_heard_cmd
    last_heard_cmd = message.data

rospy.init_node(controllerNodeName, anonymous=True)
rospy.Subscriber(visionTopicName, Vector3, vision_call_back)
rospy.Subscriber(audioTopicName, UInt8, audio_cmd_callback)

frequency = 50
rate = rospy.Rate(frequency)
brain = brian(frequency)

while not rospy.is_shutdown():
    brain.think()
    rate.sleep()


