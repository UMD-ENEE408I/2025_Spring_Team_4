import cv2
import numpy as np
import os
import time
HAS_USB = False

# def detectLine(frame):
#     """
#     Process the given frame to detect and track the center of a white line.
    
#     Args:
#         frame (numpy.ndarray): The input frame from the webcam.
    
#     Returns:
#         lineCenter: A number between [-1, 1] denoting where the center of the line is relative to the frame.
#         newFrame: Processed frame with the detected line marked using cv2.rectangle() and center marked using cv2.circle().
#     """

#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     line_image = np.copy(frame) * 0  # creating a blank to draw lines on

#     upper_white = 255
#     lower_white = 150
#     kernel_erode = np.ones((4,4), np.uint8)
#     kernel_dilate = np.ones((6,6),np.uint8)

#     mask = cv2.inRange(gray, lower_white, upper_white)
#     eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
#     dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)
#     contours, _ = cv2.findContours(dilated_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


#     kernel_size = 5
#     low_threshold = 175
#     high_threshold = 200
#     rho = 1  # distance resolution in pixels of the Hough grid
#     theta = np.pi / 180  # angular resolution in radians of the Hough grid
#     threshold = 15  # minimum number of votes (intersections in Hough grid cell)
#     min_line_length = 15  # minimum number of pixels making up a line
#     max_line_gap = 15  # maximum gap in pixels between connectable line segments

#     blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)
#     edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    
#     # Sort by area (keep only the biggest one)
#     contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]
#     cx = -1
#     cy = -1
#     height, width = frame.shape[:2]
#     cx = cy = -1
#     norm_cx = norm_cy = None
#     if len(contours) > 0:
#         M = cv2.moments(contours[0])
#         # Centroid
#         cx = int(M['m10']/M['m00'])
#         cy = int(M['m01']/M['m00'])

#         # Normalize so that center is (0,0), bottom-right is (1,1), top-left is (-1,-1)
#         norm_cx = (cx - width / 2) / (width / 2)
#         norm_cy = (cy - height / 2) / (height / 2)


#     # lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
    

#     #if lines is None or cx == -1 or cy == -1:
#         #return None, cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    
#    # for line in lines:
#     #    for x1,y1,x2,y2 in line:
#      #       cv2.line(line_image,(x1,y1),(x2,y2),(0,0,255),5)

#     #cv2.line(line_image, (cx, 0), (cx, len(frame)), (0,255,0), 5)
#     #cv2.line(line_image, (0, cy), (len(frame[0]), cy), (0,255,0), 5)
#     cv2.circle(line_image, (cx, cy), 10, (0, 255, 0), -1)  # Green filled circle

#     cv2.circle(line_image, (width // 2, height // 2), 10, (0, 0, 255), -1)  # Red dot at normalized (0,0)

#     # Draw the lines on the  image
#     lines_edges = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
#     #line_center = cx/len(frame)
#     return norm_cx, norm_cy, lines_edges
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
<<<<<<< HEAD
    lower_white = 240
=======
    lower_white = 180
>>>>>>> 49ca0369ad6e362f90e2ba6a64ec600eead4d767
    kernel_erode = np.ones((4,4), np.uint8)
    kernel_dilate = np.ones((6,6),np.uint8)

    mask = cv2.inRange(gray, lower_white, upper_white)
    eroded_mask = cv2.erode(mask, kernel_erode, iterations=1)
    dilated_mask = cv2.dilate(eroded_mask, kernel_dilate, iterations=1)
    contours, _ = cv2.findContours(dilated_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
<<<<<<< HEAD
=======


    kernel_size = 5
    low_threshold = 185
    high_threshold = 225
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 15  # minimum number of pixels making up a line
    max_line_gap = 15  # maximum gap in pixels between connectable line segments

    blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

>>>>>>> 49ca0369ad6e362f90e2ba6a64ec600eead4d767
    
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
<<<<<<< HEAD
    processed_image = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
    return processed_image, norm_cx, norm_cy

def splitFrameRegionsWithDetection(frame, near_ratio=0.5, far_ratio=0.5):
=======
    lines_edges = cv2.addWeighted(frame, 0.8, line_image, 1, 0)
    #line_center = cx/len(frame)
    return norm_cx, norm_cy, lines_edges
def splitFrameRegionsWithDetection(frame, near_ratio=0.05, far_ratio=0.95):
>>>>>>> 49ca0369ad6e362f90e2ba6a64ec600eead4d767
    """
    Splits the frame into nearsight, farsight_left, and farsight_right,
    draws blue boundaries, and prints detection status in each zone.

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
    half_height = height // 2
    # Draw horizontal line for nearsight boundary
    cv2.line(frame, (0, near_start), (width, near_start), (255, 0, 0), 2)

    # Draw vertical line for farsight left/right boundary
    cv2.line(frame, (half_width, 0), (half_width, far_end), (255, 0, 0), 2)

    # Draw horizontal line for farsight bottom boundary
    cv2.line(frame, (0, far_end), (width, far_end), (255, 0, 0), 2)

    # Extract regions
    nearsight = frame[near_start:, :]
    farsight_left = frame[:far_end, :half_width]
    farsight_right = frame[:far_end, half_width:]

    regions = {
        "nearsight": nearsight,
        "farsight_left": farsight_left,
        "farsight_right": farsight_right
    }

    # Check for white line presence in each region
    #for name, region in regions.items():
     #   gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
      #  mask = cv2.inRange(gray, 175, 255)  # Threshold for white
       # contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #if contours:
         #   print(f"White line detected in {name}")
        #else:
         #   print(f"No line detected in {name}")

    return regions




def main():
    camera_index = 1 if HAS_USB else 0 
    if os.name == 'nt':
        cam = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    else:
        cam = cv2.VideoCapture(camera_index)

    while cam.isOpened():
        ret, frame = cam.read()
        if not ret:
            break

        # Make a copy to draw detections on
        display_frame = frame.copy()

        # Split regions (draws blue boundaries & prints detection)
        regions = splitFrameRegionsWithDetection(display_frame)

        # Apply detectLine to each region
        for name in ["nearsight", "farsight_left", "farsight_right"]:
            region = regions[name]
<<<<<<< HEAD
            processed, norm_cx, norm_cy = detectLine(region)
=======
            processed = detectLine(region)
            norm_cx, norm_cy, processed = detectLine(region)
            #print(f"{name}: ({norm_cx:.2f}, {norm_cy:.2f})")
>>>>>>> 49ca0369ad6e362f90e2ba6a64ec600eead4d767

            if processed is not None:
                # Put the processed region back into display_frame
                if name == "nearsight":
                    display_frame[-region.shape[0]:, :] = processed
                elif name == "farsight_left":
                    display_frame[:region.shape[0], :region.shape[1]] = processed
                elif name == "farsight_right":
                    display_frame[:region.shape[0], -region.shape[1]:] = processed

        # Show the final combined frame
        cv2.imshow("process frames", display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()