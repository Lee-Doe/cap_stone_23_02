import cv2
import numpy as np
import os

y_path = r"D:\Python_Excercise\yolo3_files"
img_path = os.path.join(y_path, "test_img")
yolov3_weights = os.path.join(y_path, "yolov3-tiny.weights")
yolov3_cfg = os.path.join(y_path, "yolov3-tiny.cfg")
coco_names = os.path.join(y_path, "coco.names")

# Load Yolo
net = cv2.dnn.readNet(yolov3_weights, yolov3_cfg)
classes = []
with open(coco_names, "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading image
img = cv2.imread(img_path+"/yolo_sample_image.jpg")
img = cv2.resize(img, None, fx=0.4, fy=0.4)
height, width, channels = img.shape