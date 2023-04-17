############################
#
# Base code for detection
#
############################

# detection = [bbox, conf, class]

import os
import cv2
import time
import torch

import numpy as np
import multiprocessing as mp

from numpy import random
from configparser import ConfigParser
from utils.torch_utils import select_device
from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression, scale_coords, set_logging


toll_dataset_vehicle_classes = ['class0_emergencyVehicle', 'class1_lightVehicle', 'class2_mediumVehicle',
				'class3_heavyVehicle', 'class4_taxi', 'class5_bus' ] #'class_motocycle'

data_list = []
predicted_non_vehicle_list = []	# only detection within ROI
det_non_vehicle_data_list = [] 	# raw detection, no ROI filter
single_wheel = []
double_wheel = []
license_plate = []
license_plate_taxi = []

def nms(bounding_boxes, confidence_score, threshold, class_name):
	# If no bounding boxes, return empty list
	if len(bounding_boxes) == 0:
		return [], []

	# Bounding boxes
	boxes = np.array(bounding_boxes)

	# coordinates of bounding boxes
	start_x = boxes[:, 0]
	start_y = boxes[:, 1]
	end_x = boxes[:, 2]
	end_y = boxes[:, 3]

	# Confidence scores of bounding boxes
	score = np.array(confidence_score)

	# Picked bounding boxes
	picked_boxes = []
	picked_score = []
	picked_class = []
	real_class = []

	# Compute areas of bounding boxes
	areas = (end_x - start_x + 1) * (end_y - start_y + 1)

	# Sort by confidence score of bounding boxes
	order = np.argsort(score)

	# Iterate bounding boxes
	while order.size > 0:
		# The index of largest confidence score
		index = order[-1]

		# Pick the bounding box with largest confidence score
		picked_boxes.append(bounding_boxes[index])
		picked_score.append(confidence_score[index])
		picked_class.append(class_name[index])

		# Compute ordinates of intersection-over-union(IOU)
		x1 = np.maximum(start_x[index], start_x[order[:-1]])
		x2 = np.minimum(end_x[index], end_x[order[:-1]])
		y1 = np.maximum(start_y[index], start_y[order[:-1]])
		y2 = np.minimum(end_y[index], end_y[order[:-1]])

		# Compute areas of intersection-over-union
		w = np.maximum(0.0, x2 - x1 + 1)
		h = np.maximum(0.0, y2 - y1 + 1)
		intersection = w * h

		# Compute the ratio between intersection and union
		ratio = intersection / (areas[index] + areas[order[:-1]] - intersection)

		left = np.where(ratio < threshold)
		order = order[left]

	return picked_boxes, picked_score, picked_class


def letterbox(img, new_shape=(640, 640), color=(114,114,114), auto=True, scaleFill=False, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)



# boundingBox = [xmin, ymin, xmax, ymax]
def paintBoundingBox(img, boundingBox, color=(255, 0, 0), labelName=None):

	boundingBox = np.array(boundingBox, int)

	if labelName:
		cv2.putText(img, labelName,	(boundingBox[2], boundingBox[3]), cv2.FONT_HERSHEY_SIMPLEX,	0.9, (255, 255, 255), 2)

	img = cv2.rectangle(img, (boundingBox[0], boundingBox[1]), (boundingBox[2], boundingBox[3]), color, 2)

	bboxCenterX = int(boundingBox[0] + (boundingBox[2] - boundingBox[0]) / 2)
	bboxCenterY = int(boundingBox[1] + (boundingBox[3] - boundingBox[1]) / 2)

	return cv2.circle(img, (bboxCenterX, bboxCenterY), 4, color, thickness=-1)



def isBboxInROI(boundingBox, boundingBoxBLarger): 
	# first get the center
	bboxCenterX = int(boundingBox[0] + (boundingBox[2] - boundingBox[0]) / 2)
	bboxCenterY = int(boundingBox[1] + (boundingBox[3] - boundingBox[1]) / 2)

	if bboxCenterX > boundingBoxBLarger[2] or bboxCenterX < boundingBoxBLarger[0]:
		return False

	if bboxCenterY > boundingBoxBLarger[3] or bboxCenterY < boundingBoxBLarger[1]:
		return False

	return True


def updateDetectionClass(detected_vehicle, single_wheel, double_wheel, license_plate_taxi):
	if len(license_plate_taxi) > 0:
		detected_vehicle[2] = 'class4_taxi'
		print('Update to class 4')

	if detected_vehicle[2] == 'class2_mediumVehicle':
		#if len(single_wheel) > 1 and len(double_wheel) < 1:
		#	detected_vehicle[2] = 'class1_lightVehicle'
		#	print('Changed to class 1')

		if len(double_wheel) <= 1:  # it may not detect any wheels at all
			detected_vehicle[2] = 'class2_mediumVehicle'
	
		else:
			detected_vehicle[2] = 'class3_heavyVehicle'
			print('Changed to class 3')

	return detected_vehicle


def vehicleDetection(model, half, device, frame, acceptable_bounding_box_area):

	# Load model
	stride = int(model.stride.max())  # model stride=32
	imgsz = 640
	imgsz = check_img_size(imgsz, s=stride)  # check img_size
	if half:
		model.half()  # to FP16

	names = model.module.names if hasattr(model, 'module') else model.names

	# Padded resize
	img = letterbox(frame, imgsz, stride=stride)[0]

	# Convert
	img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
	img = np.ascontiguousarray(img)

	img = torch.from_numpy(img).to(device)
	img = img.half() if half else img.float()  # uint8 to fp16/32
	img /= 255.0  # 0 - 255 to 0.0 - 1.0

	if img.ndimension() == 3:
		img = img.unsqueeze(0)

	# Inference
	pred = model(img, augment=False)[0]
	
	# Apply NMS
	conf_thres = 0.45
	iou_thres = 0.5
	pred = non_max_suppression(pred, conf_thres, iou_thres)

	det_bbox_list = []
	det_conf_list = []
	det_cls_list = []
	predicted_vehicle_data = None

	#print('\nAll detected class : ')

	frame = cv2.rectangle(frame, (int(acceptable_bounding_box_area[0]), int(acceptable_bounding_box_area[1])), (int(acceptable_bounding_box_area[2]), int(acceptable_bounding_box_area[3])),
		(255,0,255), 2)

	for i, det in enumerate(pred):  # detections per image

		gn = torch.tensor(frame.shape)[[1, 0, 1, 0]]  # normalization gain whwh

		if len(det):
			# Rescale boxes from img_size to frame size
			det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()

			# Write results
			for *xyxy, conf, cls in det:	# for every det / every bbox in a frame
				#print(names[int(cls)], ' : ', float(conf))
	
				if conf > 0.45:
					bbox = [int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])]		# bbox = [xmin, ymin, xmax, ymax]

					det_bbox_list.append(bbox)
					det_conf_list.append(float(conf))
					det_cls_list.append(names[int(cls)])

	if not len(det_bbox_list) > 0:	# no detection at all
		#print('No detection')
		return frame, 'no_detection', None, None, None, None, None

	#bbox_list, conf_list, class_list = nms(det_bbox_list, det_conf_list, 0.45, det_cls_list)
	#print(class_list)	
	bbox_list = det_bbox_list
	conf_list = det_conf_list
	class_list = det_cls_list

	front_vehicle_x = -1
	det_non_vehicle_data_list.clear()

	# loop every detection
	for index in range(len(class_list)):
		if any(_cls in class_list[index] for _cls in toll_dataset_vehicle_classes):		# filter only toll_vehicle class (class0 - class6)
			if isBboxInROI(bbox_list[index], acceptable_bounding_box_area):	
				# select front vehicle
				if front_vehicle_x == -1:	
					front_vehicle_x = bbox_list[index]

					data_list.clear()
					data_list.append(bbox_list[index])
					data_list.append(conf_list[index])
					data_list.append(class_list[index])
					predicted_vehicle_data = data_list.copy()
					#print('Select : ', predicted_vehicle_data[2])

				elif bbox_list[0] < front_vehicle_x: 
					front_vehicle_x = bbox_list[index]

					data_list.clear()
					data_list.append(bbox_list[index])
					data_list.append(conf_list[index])
					data_list.append(class_list[index])
					predicted_vehicle_data = data_list.copy()
					#print('Select : ', predicted_vehicle_data[2])
				
		# select non_vehicle detection
		else:
			#print('non-vehicle : ', class_list[index])			
			data_list.clear()
			data_list.append(bbox_list[index])
			data_list.append(conf_list[index])
			data_list.append(class_list[index])
			det_non_vehicle_data_list.append(data_list[:])

		frame = paintBoundingBox(frame, bbox_list[index], color=(0, 255, 0), labelName=class_list[index])

	single_wheel.clear()
	double_wheel.clear()
	license_plate.clear()
	license_plate_taxi.clear()
	predicted_non_vehicle_list.clear()

	# no vehicle class detected, just draw non-vehicle detection and pass result
	if predicted_vehicle_data is None :
		#print('No vehicle class')

		for index in range(len(det_non_vehicle_data_list)): 
		
			if det_non_vehicle_data_list[index][2] == 'singleWheel':
				single_wheel.append(det_non_vehicle_data_list[index][0])			
			elif det_non_vehicle_data_list[index][2] == 'doubleWheel':
				double_wheel.append(det_non_vehicle_data_list[index][0])
			elif det_non_vehicle_data_list[index][2] == 'license_plate':
				license_plate.append(det_non_vehicle_data_list[index][0])
			elif det_non_vehicle_data_list[index][2] == 'license_plate_taxi':
				license_plate_taxi.append(det_non_vehicle_data_list[index][0])
		
			predicted_non_vehicle_list.append(det_non_vehicle_data_list[index][:])			
			frame = paintBoundingBox(frame, det_non_vehicle_data_list[index][0], color=(0, 255, 0), labelName=det_non_vehicle_data_list[index][2])
		return frame, 'no_detection', None, single_wheel, double_wheel, license_plate, license_plate_taxi

	# loop non_vehicle detection, select only detection inside predicted_vehicle_data bbox	
	for index in range(len(det_non_vehicle_data_list)): 
		
		if isBboxInROI(det_non_vehicle_data_list[index][0], predicted_vehicle_data[0]):
			if det_non_vehicle_data_list[index][2] == 'singleWheel':
				single_wheel.append(det_non_vehicle_data_list[index][0])			# just append True for total calculation
			elif det_non_vehicle_data_list[index][2] == 'doubleWheel':
				double_wheel.append(det_non_vehicle_data_list[index][0])
			elif det_non_vehicle_data_list[index][2] == 'license_plate':
				license_plate.append(det_non_vehicle_data_list[index][0])
			elif det_non_vehicle_data_list[index][2] == 'license_plate_taxi':
				license_plate_taxi.append(det_non_vehicle_data_list[index][0])
			
			predicted_non_vehicle_list.append(det_non_vehicle_data_list[index][:])	

			#frame = paintBoundingBox(frame, det_non_vehicle_data_list[index][0], color=(0, 255, 0), labelName=det_non_vehicle_data_list[index][2])


	# update prediction based on number of wheels and license plate
	predicted_vehicle_data = updateDetectionClass(predicted_vehicle_data, single_wheel, double_wheel, license_plate_taxi)
	frame = paintBoundingBox(frame, predicted_vehicle_data[0] , color=(0, 255, 0), labelName=predicted_vehicle_data[2])

	#predicted_vehicle_data.append(predicted_non_vehicle_list[:])	# combined vehicle detection with non-vehicle detection
	
	#print('predicted_class : ', predicted_vehicle_data[2], '\n')

	return frame, predicted_vehicle_data[2], predicted_vehicle_data[0], single_wheel, double_wheel, license_plate, license_plate_taxi





