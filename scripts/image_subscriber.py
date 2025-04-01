#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

subscriberNodeName='camera_sensor_subscriber'
topicName='video_topic'

model = YOLO("~/Model_Weights/vision_weights.pt")

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