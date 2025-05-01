#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from std_msgs.msg import UInt8
from turtlebot3_msgs.msg import Sound
from collections import deque

# Topic and Node names for this script
controllerNodeName = "brian"
visionTopicName = "line_camera_topic"
commandTopicName = 'cmd_vel'
audioTopicName = 'audio_topic'
buttonTopicName = 'button_topic'

# Global parameters
think_frequency = 50

# Global variables (used to store data from topics for polling later)
vision_x_vec = Vector3()
last_heard_cmd = 0
button_pressed = 0

# Constant Values

# Brian States
TURN_STATE = 0
WALK_STATE = 1

# Audio Commands
CMDS = enumerate(["CMD_NULL", "CMD_LEFT", "CMD_RIGHT", "CMD_CHASER", "CMD_RUNNER"])
CMD_NULL = 0
CMD_LEFT = 1
CMD_RIGHT = 2
CMD_CHASER = 3
CMD_RUNNER = 4

# Decision Variables
LEFT = 1
RIGHT = -1

# Turtlebot Bounds
BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84
LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.3

class brian:
    def __init__(self, controller_node_name, control_commands_topic_name, rate, left_guard=-0.1, right_guard=0.1, sample_window=5):
        self.control_node = rospy.init_node(controller_node_name, anonymous=True)
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
        self.control_publisher = rospy.Publisher(control_commands_topic_name, Twist, queue_size=10)

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
        """
        For line following. Used to determine in which direction to turn to stay on the line. 

        """
        rl = self.process_nearsight(vision_x_vec.x)
        if rl == -1: # turn left
            self.target.angular.z = -ANG_VEL_STEP_SIZE
        elif rl == 1:
            self.target.angular.z = ANG_VEL_STEP_SIZE
        else:
            self.target.angular.z = 0

    def check_bounds(self):
        """
        Checks the target linear and angular velocities. Floors to the limit values if the target is past the burgerbot limits. 
        """
        if self.target.angular.z > BURGER_MAX_ANG_VEL:
            self.target.angular.z = BURGER_MAX_ANG_VEL
        elif self.target.angular.z < -BURGER_MAX_ANG_VEL:
            self.target.angular.z = -BURGER_MAX_ANG_VEL

        if self.target.linear.x > BURGER_MAX_LIN_VEL:
            self.target.linear.x = BURGER_MAX_LIN_VEL
        elif self.target.linear.x < -BURGER_MAX_LIN_VEL:
            self.target.linear.x = -BURGER_MAX_LIN_VEL

    def look_forwards(self):
        """
        Process the farsight vision to try to determine if a junction is coming up. 
        **INCOMPLETE**
        """
        if len(self.far_right_sample_queue) == self.sample_window*2:
            self.far_right_sample_queue.popleft()

        if len(self.far_left_sample_queue) == self.sample_window*2:
            self.far_left_sample_queue.popleft()

    def think(self):
        """
        Main function which processes all available data and makes a action decision.

        Plan for futher development:
            - Organize the think task into stages:
                - 1st stage: Data collection and processing
                - 2nd stage: Decision Calculation
                    - Determines what to do depending on collected data and the current state.
                - 3rd stage: State determination
                    - Determines which state should be next depending on the data collected and the current state.
                - 4th stage: Execution
                    - Sends the commands to carry out the decisions made in stage 2. 
                - 5th stage: Log
                    - Log relevant data
            - For each stage, lay out what needs to be accomplished and what data is available.
            - Organize the log step so it can be customized easier with a glob var
            - Make constants better because we have a very ugly implementation rn.
            - Determine what data is available to Brian. 
        """
        global last_heard_cmd

        ### Data Collection and Processing ###
        
        ## Check Line Detector ##
        new_value = vision_x_vec[0] 
        lost_track = False if new_value in range(-1, 1) else True # Flag if the line detector lost track of the line
        if len(self.nearsight_sample_queue) < self.sample_window and lost_track is False: # Checks if values need to be popped off the queue
            self.nearsight_sample_queue.append(new_value)
        else:
            self.nearsight_sample_queue.popleft()
            self.nearsight_sample_queue.append(new_value)

        averaged_line_pos = 0 # Average of the values in the queue
        averaged_line_pos = (averaged_line_pos + value for value in self.nearsight_sample_queue)/len(self.nearsight_sample_queue)

        ## Check Command Issued ##
        if last_heard_cmd is not CMD_NULL:
            new_cmd = last_heard_cmd
            last_heard_cmd = CMD_NULL

        ## Check Button State ##
        button_state = button_pressed


        # # Averaging the nearsight data in an attempt to reduce the effect of small errors in the data
        # val = 0
        # for value in self.nearsight_sample_queue:
        #     val += value

        # try: # When this script first launches, the sample queue will be empty so we just ignore it for one cycle
        #     val = val/len(self.nearsight_sample_queue)

        #     if (val < -1) and (self.state is not TURN_STATE):
        #         self.state = TURN_STATE
        #         self.target.linear.x = 0
        #     else:
        #         if last_heard_cmd is CMD_CHASER:
        #             self.state = WALK_STATE
        #             last_heard_cmd = CMD_NULL
        # except ZeroDivisionError:
        #     self.state = WALK_STATE
        
        # if self.state is TURN_STATE:
        #     if val > -1:
        #         rospy.loginfo("reset")
        #         last_heard_cmd = CMD_NULL

        #     if last_heard_cmd is CMD_RIGHT:
        #         self.target.angular.z = -ANG_VEL_STEP_SIZE
        #     elif last_heard_cmd is CMD_LEFT:
        #         self.target.angular.z = ANG_VEL_STEP_SIZE
        #     else:
        #         self.target.angular.z = 0
        #         self.target.linear.x = 0

        # elif self.state is WALK_STATE:
        #     self.determine_angular_target()
        #     self.target.linear.x = -0.05

        # # Check valid target velocities
        # self.check_bounds()

        # # Log the decision variables
        # state_string = "WALK" if self.state is WALK_STATE else "TURN" # This may need to be changed if we will add more states
        # CMD_string = CMDS[last_heard_cmd] # Untested ! Don't know what is the right way to index the CMD list
        # fstring = f'''Angular: {self.target.angular.z}\tLinear: {self.target.linear.x}\tState: {state_string}\tCMD: {CMD_string}'''
        # rospy.loginfo(fstring)

        # # Send target linear and angular velocities
        # self.control_publisher.publish(self.target)

########## Call back functions for getting information from sensors. ##########

# Updates the x_vec global variable which stores the near and far sight x values. 
def vision_callback(message): 
    global vision_x_vec
    vision_x_vec = message

# Updates the last_hear_cmd global variable every time the audio listener node hears a command. 
def audio_cmd_callback(message): 
    global last_heard_cmd
    last_heard_cmd = message.data

def button_callback(message):
    global button_pressed
    button_pressed = message.data


########## Subscriber node initialization ##########
rospy.Subscriber(visionTopicName, Vector3, vision_callback)
rospy.Subscriber(audioTopicName, UInt8, audio_cmd_callback)
rospy.Subscriber(buttonTopicName, UInt8, button_callback)


########## Controller node setup ##########
rate = rospy.Rate(think_frequency)
brain = brian(think_frequency, controllerNodeName, commandTopicName)


########## Main loop ##########
while not rospy.is_shutdown():
    brain.think()
    rate.sleep()


