#!/usr/bin/env python3

import rospy
import os
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from ultralytics import YOLO

model_directory = os.getenv("MODEL_WEIGHTS_DIR")

subscriberNodeName='camera_sensor_subscriber'
topicName='video_topic'

model = YOLO(model_directory)

def callbackFunction(message):
    bridgeObject = CvBridge()

    rospy.loginfo("received a video message/frame")

    convertedFrameBackToCV = bridgeObject.imgmsg_to_cv2(message)

    results = model(frame)

    annotated_frame = results[0].plot()

    cv2.imshow("Detect Burgerbot!!", annotated_frame)

    cv2.waitKey(1)

rospy.init_node(subscriberNodeName, anonymous=True)
rospy.Subscriber(topicName, Image, callbackFunction)
rospy.spin()
cv2.destroyAllWindows()