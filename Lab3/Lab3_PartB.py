from ultralytics import YOLO
import torch
import cv2

# Load a COCO-pretrained YOLOv8n model
model = YOLO("yolov8n.pt")
# Train the model on the COCO8 example dataset for 6 epochs
#run below line to train
#results = model.train(data="coco8.yaml", epochs= 6, imgsz=640)
#Open cam
cam = cv2.VideoCapture(0)
while cam.isOpened(): 
    ret, frame = cam.read()
    if not ret:
        break

    #Run model
    results = model(frame)
    #Render detections
    annotated_frame = results[0].plot()
    #Show
    cv2.imshow("Pretrained model", annotated_frame)

    #Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cam.release()
cv2.destroyAllWindows

print("\n Now starting part 2 \n")

 #Now let's try use YOLO to make a model to detect the burgerbot!!!!
#Run below line to train a new batch of weights
#model = model.train(data = r"C:\Users\andyn\408I\2025_Spring_Team_4-1\Lab3\data.yaml", epochs = 10, imgsz = 640, batch = 16)

#Load trained model
model = YOLO(r"C:\Users\andyn\408I\2025_Spring_Team_4-1\runs\detect\train12\weights\best.pt")

#Open camera
cam = cv2.VideoCapture(0)

while cam.isOpened():
    ret, frame = cam.read()
    if not ret:
        break
    #Run model on frame
    results = model(frame)

    #Draw boundary
    annotated_frame = results[0].plot()

    #Show frame with detections
    cv2.imshow("Detect Burgerbot!!", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cam.release()
cv2.destroyAllWindows()

#In short, YOLO is great for real time processing and for more intricate, complex image recognition tasks. YOLO image recognition 
#yields high accuracy as a result, but is more demanding in terms of processing power, and is more "unexplainable"
#Open CV is pretty much the opposite of YOLO in this regard, its quick, lightweight and interpretable, but with less accuracy and lower 
#capabilites