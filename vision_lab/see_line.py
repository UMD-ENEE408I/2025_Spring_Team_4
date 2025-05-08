#!/usr/bin/env python3

import cv2
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
    lower_white = np.mean(gray) + 50
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
    height, width = frame.shape[:2]
    cx = cy = -1
    norm_cx = norm_cy = None
    if len(contours) > 0:
        M = cv2.moments(contours[0])
        # Centroid
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        # Normalize so that center is (0,0), bottom-right is (1,1), top-left is (-1,-1)
        norm_cx = (cx - width / 2) / (width / 2)
        norm_cy = (cy - height / 2) / (height / 2)

    cv2.circle(line_image, (cx, cy), 10, (0, 255, 0), -1)  # Green filled circle

    cv2.circle(line_image, (width // 2, height // 2), 10, (0, 0, 255), -1)  # Red dot at normalized (0,0)

    # Draw the lines on the  image
    processed_image = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
    return processed_image, norm_cx, norm_cy

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


print("EHIOUUAHd")
camera_index = 1 if HAS_USB else 0 
if os.name == 'nt':
    cam = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
else:
    cam = cv2.VideoCapture(camera_index)

while cam.isOpened():
    ret, frame = cam.read()
    if not ret:
        print("AHH")
        break

    # Make a copy to draw detections on
    display_frame = frame.copy()

    # Split regions (draws blue boundaries & prints detection)
    regions = splitFrameRegions(display_frame, 0.1, 0.9)

    # Apply detectLine to each region
    ns_str = None
    fsl_str = None
    fsr_str = None
    for name in ["nearsight", "farsight_left", "farsight_right"]:
        region = regions[name]
        processed, norm_cx, norm_cy = detectLine(region)

        if processed is not None:
            # Put the processed region back into display_frame
            if name == "nearsight":
                display_frame[-region.shape[0]:, :] = processed
                ns_str = f"""Nearsight: {norm_cx}"""
            elif name == "farsight_left":
                display_frame[:region.shape[0], :region.shape[1]] = processed
                fsl_str = f"""FS L: {norm_cx}"""
            elif name == "farsight_right":
                display_frame[:region.shape[0], -region.shape[1]:] = processed
                fsr_str = f"""FS R: {norm_cx}"""
    print(f'''{ns_str}\t{fsl_str}\t{fsr_str}''')
    # Show the final combined frame
    cv2.imshow("process frames", display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

