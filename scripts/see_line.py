#!/usr/bin/env python3

import rospy
import std_msgs.msg
import cv2
from cv_bridge import CvBridge
import numpy as np
import os

HAS_USB = False

def detectLine(frame):
    """
    Process the given frame to detect and track the center of a white line.
    
    Args:
        frame (numpy.ndarray): The input frame from the webcam.
    
    Returns:
        lineCenter: A number between [-1, 1] denoting where the center of the line is relative to the frame.
        newFrame: Processed frame with the detected line marked using cv2.rectangle() and center marked using cv2.circle().
    """

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    line_image = np.copy(frame) * 0  # creating a blank to draw lines on

    upper_white = 255
    lower_white = 150
    kernel_erode = np.ones((4,4), np.uint8)
    kernel_dilate = np.ones((6,6),np.uint8)

    mask = cv2.inRange(gray, lower_white, upper_white)
    eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
    dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)
    contours, _ = cv2.findContours(dilated_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sort by area (keep only the biggest one)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
    cx = -1
    cy = -1
    if len(contours) > 0:
        M = cv2.moments(contours[0])
        # Centroid
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

    cv2.circle(line_image, (cx, cy), 10, (0, 255, 0), -1)  # Green filled circle

    lines_edges = cv2.addWeighted(frame, 0.8, line_image, 1, 0)

    return lines_edges, cx, cy

def splitFrameRegions(frame, near_ratio=0.5, far_ratio=0.5):
    """
    Splits the frame into nearsight, farsight_left, and farsight_right

    Args:
        frame (numpy.ndarray): Input frame (will be modified to show boundaries).
        near_ratio (float): Proportion of frame height for nearsight region.
        far_ratio (float): Proportion of frame height for farsight region.

    Returns:
        dict: Dictionary containing the 3 subregions.
    """
    height, width, _ = frame.shape

    near_start = int((1 - near_ratio) * height)
    far_end = int(far_ratio * height)
    half_width = width // 2

    # # Draw horizontal line for nearsight boundary
    # cv2.line(frame, (0, near_start), (width, near_start), (255, 0, 0), 2)

    # # Draw vertical line for farsight left/right boundary
    # cv2.line(frame, (half_width, 0), (half_width, far_end), (255, 0, 0), 2)

    # # Draw horizontal line for farsight bottom boundary
    # cv2.line(frame, (0, far_end), (width, far_end), (255, 0, 0), 2)

    # Extract regions
    nearsight = frame[near_start:, :]
    farsight_left = frame[:far_end, :half_width]
    farsight_right = frame[:far_end, half_width:]

    regions = {
        "nearsight": nearsight,
        "farsight_left": farsight_left,
        "farsight_right": farsight_right
    }

    return regions

def detectLinesInRegion(frame, near_ratio=0.5, far_ratio=0.5):
    regions = splitFrameRegions(frame, near_ratio, far_ratio)
    result = {}
    for region in regions:
        _, x, y = detectLine(regions[region])
        result[region] = [x, y]
    return result

publisherNodeName='line_camera'
topicName='line_camera_topic'

rospy.init_node(publisherNodeName, anonymous=True)

publisher = rospy.Publisher(topicName, std_msgs.msg.Float32, queue_size=1)

rate = rospy.Rate(1)

videoCaptureObject = cv2.VideoCapture(0)

bridgeObject = CvBridge()

while not rospy.is_shutdown():
    returnValue, capturedFrame = videoCaptureObject.read()
    if returnValue == True:
        result = detectLinesInRegion(capturedFrame)
        near_result = result["nearsight"]
        rospy.loginfo(f'Published: {near_result[0]}')
        publisher.publish(near_result[0])
        # for region in result:
        #     rospy.loginfo(f'Centroid detected in region {region}. \tCoordinates: ({result[region][0]}, {result[region][1]})')

    rate.sleep()