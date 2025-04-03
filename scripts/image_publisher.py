#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

publisherNodeName='camera_sensor_publisher'
topicName='video_topic'

rospy.init_node(publisherNodeName, anonymous=True)

publisher = rospy.Publisher(topicName, Image, queue_size=2)

rate = rospy.Rate(1)

videoCaptureObject = cv2.VideoCapture(0)

bridgeObject = CvBridge()

while not rospy.is_shutdown():
    returnValue, capturedFrame = videoCaptureObject.read()
    if returnValue == True:
        rospy.loginfo('Video frame captured and published')
        compressed_image = bridgeObject.bridgeObject.cv2_to_compressed_imgmsg(capturedFrame, dst_format="jpeg")
        publisher.publish(compressed_image)
    rate.sleep()