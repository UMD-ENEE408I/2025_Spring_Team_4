import cv2
import numpy as np
import time
import os

HAS_USB = True
# PID Controller
class PIDController:
    def __init__(self, Kp=0.05, Ki=0.001, Kd=0.05):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0
        self.integral = 0
        self.last_time = None

    def compute(self, error):
        current_time = time.time()
        dt = current_time - self.last_time if self.last_time else 0.1  # Default small dt

        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0

        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        self.prev_error = error
        self.last_time = current_time

        return output

# Initialize PID
pid = PIDController(Kp=0.05, Ki=0.001, Kd=0.05)

# Start Video Capture
camera_index = 1 if HAS_USB else 0 
if os.name == 'nt':
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
else:
    cap = cv2.VideoCapture(camera_index)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Thresholding to extract the black line
    _, binary = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)

    # Find contours of the line
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour (assuming it's the line)
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)

        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])  # X coordinate of centroid
            cy = int(M["m01"] / M["m00"])  # Y coordinate of centroid

            # Draw the detected line
            cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 3)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            # Compute error (distance from frame center)
            frame_center = frame.shape[1] // 2
            error = cx - frame_center

            # Compute PID correction
            correction = pid.compute(error)

            # Display values
            cv2.putText(frame, f"Error: {error}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(frame, f"Correction: {correction:.2f}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Show frames
    cv2.imshow("Line Following", frame)
    cv2.imshow("Binary", binary)

    # Break on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
