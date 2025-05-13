#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from std_msgs.msg import UInt8
from turtlebot3_msgs.msg import Sound
from collections import deque
from enum import Enum
from math import floor

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
class STATES(Enum):
    TURN_STATE = 0
    WALK_STATE = 1
    CHASER_STATE = 2
    RUNNER_STATE = 3

# Audio Commands
class CMDS(Enum):
    CMD_NULL = 0
    CMD_LEFT = 1
    CMD_RIGHT = 2
    CMD_CHASER = 3
    CMD_RUNNER = 4

class FORK(Enum):
    NO_FORK = 0
    LEFT_FORK = -1
    RIGHT_FORK = 1
    BOTH_FORK = 2

# Decision Variables
LEFT = 1
RIGHT = -1

# Turtlebot Bounds
BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84
LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.3

class brian:
    def __init__(self, controller_node_name, control_commands_topic_name, rate, lost_count_threshold=50, left_guard=-0.1, right_guard=0.1, sample_window=5):
        self.control_node = rospy.init_node(controller_node_name, anonymous=True)
        self.left_guard = left_guard
        self.right_guard = right_guard
        self.angular_target = 0
        self.sample_window = sample_window
        self.nearsight_sample_queue = deque(maxlen=sample_window)
        self.far_right_sample_queue = deque(maxlen=sample_window*2)
        self.far_left_sample_queue = deque(maxlen=sample_window*2)
        self.predict_dir = 0
        self.target = Twist()
        self.state = STATES.WALK_STATE
        self.lost_count = 0
        self.lost_count_threshold = lost_count_threshold
        self.rate = rate
        self.control_publisher = rospy.Publisher(control_commands_topic_name, Twist, queue_size=10)

    def determine_angular_target(self, x_val):
        """
        For line following. Used to determine in which direction to turn to stay on the line. 

        """
        turn_rate = 0
        if x_val < self.left_guard:
            for i in range(0, floor(1/self.left_guard/2)):
                if x_val < (i+1)*self.left_guard:
                    turn_rate += ANG_VEL_STEP_SIZE
        elif x_val > self.right_guard:
            for i in range(0, floor(1/self.right_guard/2)):
                if x_val > (i+1)*self.right_guard:
                    turn_rate -= ANG_VEL_STEP_SIZE
        return turn_rate
        

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

    def look_forwards(self, x_threshold = 0.1):
        """
        Process the farsight vision to try to determine if a junction is coming up. 
        **INCOMPLETE**
        Current plan of action is to grab the x values of the 2 quadrants and compare w/ the rolling average
        of the line detected. Should a turn be detected, we should expect the left and right quadrants to read x
        values around -1 and +1 respectively (Or it should be drastically different from rolling
        average, consider having a threshold).
        Noise reduction: TBD

        Args: 
            left_xvalue
            right_xvalue
            left_yvalue
            right_yvalue
            x_threshold (should we do threshold implentation)            

        Output: -1 for left turns, 1 for right turns, 2 for both left and right, 0 otherwise
        """

        left_xvalue = vision_x_vec.y
        right_xvalue = vision_x_vec.z

        lost_left = True if left_xvalue < -1 else False
        lost_right = True if right_xvalue < -1 else False

        if len(self.far_right_sample_queue) == self.sample_window/2:
            self.far_right_sample_queue.popleft()

        if len(self.far_left_sample_queue) == self.sample_window/2:
            self.far_left_sample_queue.popleft()

        #Grab rolling averages for far left and far right quadrants
        self.far_left_sample_queue.append(left_xvalue)
        leftsum = 0
        for item in self.far_left_sample_queue:
            leftsum += item
        left_result = leftsum/len(self.far_left_sample_queue)

        self.far_right_sample_queue.append(right_xvalue)
        rightsum = 0
        for item in self.far_right_sample_queue:
            rightsum =+ item
        right_result = rightsum/len(self.far_right_sample_queue)

        #Check if there's a drastic different in y values of the quadrants
        #May not be necessary but consider

        #Compare left_result and right_result w/ threshold
        if left_result < x_threshold and right_result > -x_threshold:
            return 2
        elif left_result < x_threshold:
            return -1
        elif right_result > -x_threshold:
            return 1
        else:
            return 0

    def collect_nearsight_data(self):
        """Collects nearsighted vision data and processes it accordingly by adding a low pass filter. 

        Returns:
            detected_line_x_value (float): In the range of -1 to 1 specifying where the x value of the detected line is
            lost_track (bool): If the nearsighted vision lost track of the line 
        """
        new_value = vision_x_vec.x
        lost_track = False if new_value >= -1 and new_value <= 1 else True # Flag if the line detector lost track of the line
        averaged_line_pos = 0 # Average of the values in the queue
        if lost_track is False:
            if len(self.nearsight_sample_queue) < self.sample_window: # Checks if values need to be popped off the queue
                self.nearsight_sample_queue.append(new_value)
            else:
                self.nearsight_sample_queue.popleft()
                self.nearsight_sample_queue.append(new_value)

            for value in self.nearsight_sample_queue:
                averaged_line_pos += value
            averaged_line_pos = averaged_line_pos/len(self.nearsight_sample_queue)

        if lost_track:
            self.lost_count += 1
        else:
            self.lost_count = 0

        return averaged_line_pos, lost_track

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
        averaged_line_pos, _ = self.collect_nearsight_data()
        fork_decision = self.look_forwards()

        ## Check Command Issued ##
        new_cmd = last_heard_cmd if last_heard_cmd is not CMDS.CMD_NULL else CMDS.CMD_NULL
        last_heard_cmd = CMDS.CMD_NULL

        ## Check Button State ##
        button_state = button_pressed


        ### Decision Calculation ###
        if self.state is STATES.WALK_STATE:
            self.target.angular.z = self.determine_angular_target(averaged_line_pos)
            self.target.linear.x = -0.05
        elif self.state is STATES.TURN_STATE:
            if new_cmd is CMDS.CMD_LEFT:
                self.target.angular.z = ANG_VEL_STEP_SIZE
            elif new_cmd is CMDS.CMD_RIGHT:
                self.target.angular.z = -ANG_VEL_STEP_SIZE
            self.target.linear.x = 0
        elif self.state is STATES.CHASER_STATE:
            pass
        elif self.state is STATES.RUNNER_STATE:
            pass


        ### State Calculation ###
        next_state = self.state
        if self.state is STATES.WALK_STATE:
            if self.lost_count > self.lost_count_threshold:
                next_state = STATES.TURN_STATE
        elif self.state is STATES.TURN_STATE:
            if self.lost_count < self.lost_count_threshold:
                if averaged_line_pos >= self.left_guard and averaged_line_pos <= self.right_guard:
                    next_state = STATES.WALK_STATE
        elif self.state is STATES.CHASER_STATE:
            pass 
        elif self.state is STATES.RUNNER_STATE:
            pass
        
        state_str = f'''CS: {STATES(self.state).name}\tNS: {STATES(next_state).name}'''
        vel_str = f'''LV: {self.target.linear.x}\tAV: {self.target.angular.z}'''
        data_str = f'''ALP: {averaged_line_pos}\tCCMD: {new_cmd}\tGCMD: {last_heard_cmd}'''
        lost_count_str = f'''LC: {self.lost_count}'''
        fork_decision = f'''FD: {FORK(fork_decision).name}'''
        button_str = f'''BS: {button_state}'''
        rospy.loginfo(f'''{button_str}''')
        
        self.check_bounds()
        self.control_publisher.publish(self.target)
        self.state = next_state

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
    last_heard_cmd = CMDS(message.data)
    rospy.loginfo(f"LSH: {last_heard_cmd}")

def button_callback(message):
    global button_pressed
    button_pressed = message.data


########## Subscriber node initialization ##########
rospy.Subscriber(visionTopicName, Vector3, vision_callback)
rospy.Subscriber(audioTopicName, UInt8, audio_cmd_callback)
rospy.Subscriber(buttonTopicName, UInt8, button_callback)


########## Controller node setup ##########
brain = brian(controllerNodeName, commandTopicName, think_frequency)
rate = rospy.Rate(think_frequency)

########## Main loop ##########
while not rospy.is_shutdown():
    brain.think()
    rate.sleep()


