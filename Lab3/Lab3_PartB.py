from ultralytics import YOLO
import torch

# Load a COCO-pretrained YOLOv8n model
model = YOLO("yolov8n.pt")

# Display model information (optional)
model.info()

# Train the model on the COCO8 example dataset for 25 epochs
results = model.train(data="coco8.yaml", epochs=25, imgsz=640)

 #Now let's try use YOLO to make a model to detect the burgerbot!!!!

