from ultralytics import YOLO
import torch

# Load a COCO-pretrained YOLOv8n model
model = YOLO("yolov8n.pt")

# Display model information (optional)
model.info()

# Train the model on the COCO8 example dataset for 10 epochs
results = model.train(data="coco8.yaml", epochs=10, imgsz=640)
print("\n Now starting part 2 \n")

 #Now let's try use YOLO to make a model to detect the burgerbot!!!!

botresults = model.train(data = r"C:\Users\andyn\408I\2025_Spring_Team_4-1\Lab3\data.yaml", epochs = 15, imgsz = 640, batch = 16)
model.val()
