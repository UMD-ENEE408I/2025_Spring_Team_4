from ultralytics import YOLO
import torch
from pathlib import Path

# Load a COCO-pretrained YOLOv8n model
model = YOLO("yolov8n.pt")

# # Display model information (optional)
# model.info()

# # Train the model on the COCO8 example dataset for 10 epochs
# results = model.train(data="coco8.yaml", epochs=1, imgsz=640)
# print("\n Now starting part 2 \n")

#Now let's try use YOLO to make a model to detect the burgerbot!!!!

# Path wrangling for use on different systems
cur_dir = Path().resolve() # Get the current working directory's absolute path
data_lib = cur_dir / "Lab3/data.yaml" # Append the path to the training yaml

botresults = model.train(data = data_lib, epochs = 15, imgsz = 640, batch = 16)
model.val()

# Should we use this to make a kill bot???? 
