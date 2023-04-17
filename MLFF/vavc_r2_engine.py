#==================================================
#===== SUB FUNCTION - vavc
# main_v? anpr_v? datalogger_v? vavc_v?
#==================================================

#==================================================
#===== yolov5 reference
# https://github.com/ultralytics/yolov5
# Python>=3.6.0 is required with all requirements.txt installed including PyTorch>=1.7:
#==================================================

#==================================================
#===== centernet reference
# https://medium.com/visionwizard/centernet-objects-as-points-a-comprehensive-guide-2ed9993c48bc
# https://bluehorn07.github.io/2021/06/03/CenterNet-tutorial-windows.html
# 211207 Setup Guide.txt
#==================================================

#==================================================
# HISTORY
#==================================================
# Parameter:
# 1. detection = [bbox, conf, class]
#===== 13/12/2021
# 1. study vavc
#==================================================
# PENDING
#==================================================
# 1.
#==================================================


#--------------------------------------------------
TSRT = False
draw_bbox_vehicle = False
draw_bbox_wheel = False
draw_bbox_plate = False
put_class_at_bottom = True
center_bbox = False

import os
import cv2
import numpy as np
import queue
import time
#import multiprocessing as mp

from configparser import ConfigParser
from scipy import ndimage
from scipy.ndimage import interpolation as inter  # def correct_skew
from collections import namedtuple  # def bb_intersection_over_union

import torch
import pandas as pd
from utils.torch_utils import select_device, time_sync
from models.experimental import attempt_load
from utils.general import set_logging, check_img_size, non_max_suppression, scale_coords, xyxy2xywh
from numpy import random
from utils.plots import Annotator

#==================================================
# vehicle classes
toll_dataset_vehicle_classes = [
	'class1_lightVehicle',
	'class2_mediumVehicle',
	'class3_heavyVehicle',
	'class4_taxi',
	'class5_bus' #,'class_motocycle'
	] 	

#==================================================
# variable
data_list = []
single_wheel = []
double_wheel = []
license_plate_taxi = []
license_plate = []
predicted_vehicle_data = []


#--------------------------------------------------
# Projection Profile Method to determine OCR image skew angle correction
def correct_skew(image, delta=1, limit=5):
	def determine_score(arr, angle):
		data = inter.rotate(arr, angle, reshape=False, order=0)
		histogram = np.sum(data, axis=1)
		score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
		return histogram, score

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

	scores = []
	angles = np.arange(-limit, limit+delta, delta)
	for angle in angles:
		histogram, score = determine_score(thresh, angle)
		scores.append(score)

	best_angle = angles[scores.index(max(scores))]

	(h, w) = image.shape[:2]
	center = (w // 2, h // 2)
	M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
	rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

	#return best_angle, rotated
	return rotated


#--------------------------------------------------
# letterbox is convert image aspect ratio to deep learning model square base in stride without distort and fill remaining part to gray.
def letterbox(img, new_shape=(640,640), color=(114,114,114), auto=True, scaleFill=False, scaleup=True, stride=32):
	# Resize and pad image while meeting stride-multiple constraints
	shape = img.shape[:2]  # current shape [height, width]
#	print(f"org img.shape: {img.shape[:2][1]}, {img.shape[:2][0]}")
	if isinstance(new_shape, int):
		new_shape = (new_shape, new_shape)

	# Scale ratio (new / old)
	r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
	if not scaleup:  # only scale down, do not scale up (for better test mAP)
		r = min(r, 1.0)

	# Compute padding
	ratio = r, r  # width, height ratios
	new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
#	print(f"new_unpad: {new_unpad[0]}, {new_unpad[1]}")
	dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
	if auto:  # minimum rectangle
		dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
	elif scaleFill:  # stretch
		dw, dh = 0.0, 0.0
		new_unpad = (new_shape[1], new_shape[0])
		ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

#	print(f"dw, dh: {dw}, {dh}")
	dw /= 2  # divide padding into 2 sides
	dh /= 2

	if shape[::-1] != new_unpad:  # resize
		img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
	top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
	left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
	img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border

#	print(f"border img.shape: {img.shape[:2][1]}, {img.shape[:2][0]}")
	return img, ratio, (dw, dh)


#--------------------------------------------------
# boundingBox = [xmin, ymin, xmax, ymax]
def paintBoundingBox(img, boundingBox, color=(255,0,0), label=None):
	boundingBox = np.array(boundingBox, int)
	if label:
		# cv2.putText(img, str(label), (boundingBox[0],boundingBox[3]-4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
		cv2.putText(img, str(label), (boundingBox[0],boundingBox[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 3) 	#make text border as black
		cv2.putText(img, str(label), (boundingBox[0],boundingBox[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2) 
		
	img = cv2.rectangle(img, (boundingBox[0],boundingBox[1]), (boundingBox[2],boundingBox[3]), color, 2)
	bboxCenterX = int((boundingBox[0] + boundingBox[2]) / 2)
	bboxCenterY = int((boundingBox[1] + boundingBox[3]) / 2)
	if center_bbox is True:
		cv2.circle(img, (bboxCenterX, bboxCenterY), 4, color, thickness=-1)
	return


#--------------------------------------------------
# non-maximum suppression is to remove redundant bounding boxes in object detection
def NMS(boxes, confidence_score, class_name, overlapThresh=0.4):
	#print(boxes)
	# if there are no boxes, return an empty list
	if len(boxes) == 0:
		return []
	# if the bounding boxes integers, convert them to floats -- this is important since we'll be doing a bunch of divisions
	if boxes.dtype.kind == "i":
		boxes = boxes.astype("float")
	#print(boxes)

	# initialize the list of picked indexes
	pick = []

	# grab the coordinates of the bounding boxes
	x1 = boxes[:,0]  # x coordinate of the top-left corner
	y1 = boxes[:,1]  # y coordinate of the top-left corner
	x2 = boxes[:,2]  # x coordinate of the bottom-right corner
	y2 = boxes[:,3]  # y coordinate of the bottom-right corner
	#print(x1)
	#print(y1)
	#print(x2)
	#print(y2)

	# compute the area of the bounding boxes and sort the bounding boxes by the bottom-right y-coordinate of the bounding box
	areas = (x2 - x1 + 1) * (y2 - y1 + 1)
	#print(areas)
	idxs = np.argsort(y2)
	#print(idxs)

	# keep looping while some indexes still remain in the indexes list
	while len(idxs) > 0:
		# grab the last index in the indexes list and add the index value to the list of picked indexes
		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)
	#	print(pick)
		# find the largest (x, y) coordinates for the start of the bounding box and the smallest (x, y) coordinates for the end of the bounding box
		xx1 = np.maximum(x1[i], x1[idxs[:last]])
		yy1 = np.maximum(y1[i], y1[idxs[:last]])
		xx2 = np.minimum(x2[i], x2[idxs[:last]])
		yy2 = np.minimum(y2[i], y2[idxs[:last]])
		# compute the width and height of the bounding box
		w = np.maximum(0, xx2 - xx1 + 1)
		h = np.maximum(0, yy2 - yy1 + 1)
		# compute the ratio of overlap
		overlap = (w * h) / areas[idxs[:last]]
		# delete all indexes from the index list that have
		idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))
	# return only the bounding boxes that were picked using the integer data type
	return boxes[pick].astype("int")


#--------------------------------------------------
def updateDetectionClass(detected_vehicle, single_wheel, double_wheel, license_plate_taxi):
	if len(license_plate_taxi) > 0:
		detected_vehicle[2] = 'class4_taxi'
		print('Change to class 4')
	if detected_vehicle[2] == 'class2_mediumVehicle':
		if len(double_wheel) <= 1:
			detected_vehicle[2] = 'class2_mediumVehicle'
		else:
			detected_vehicle[2] = 'class3_heavyVehicle'
			print('Change to class 3 ')

	if detected_vehicle[2] == 'class1_lightVehicle':
		try:
			if len(single_wheel) == 2 and len(double_wheel) == 0:
				detected_vehicle[2] = 'class1_lightVehicle'
		except:
			pass

	return detected_vehicle


#--------------------------------------------------
def vehicleDetection(model_vavc, half, device, vavc_frame, imgROI):
	frame_raw = vavc_frame.copy()
	#--------------------------------------------------
	model = model_vavc
	# # Load model
	# #	stride = int(model.stride.max())  # model stride=32
	# stride = 32
	# imgsz = 640
	# imgsz = check_img_size(imgsz, s=stride)  # check img_size
	# if half:
	# 	model.half()  # to FP16 to engine

	# Get names and colors
	names = model.module.names if hasattr(model, 'module') else model.names
	colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

	# Padded resize
	if(TSRT):
		stride = max(int(model.stride), 32)  # model stride=32
	else:
		stride = 32
	imgsz = [640,640]
	imgsz = check_img_size(imgsz, s=stride)  # check img_size
	img = letterbox(vavc_frame, imgsz, stride=stride, auto=False)[0] #to engine

	# img = letterbox(vavc_frame, imgsz, stride=stride)[0]

	# Process image
	#t1 = time_sync()
	img = img[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
	img = np.ascontiguousarray(img)
	img = torch.from_numpy(img).to(device)
	img = img.half() if half else img.float()  # uint8 to fp16/32
	img /= 255.0  # 0 - 255 to 0.0 - 1.0
	if img.ndimension() == 3:
		img = img.unsqueeze(0)
	#t2 = time_sync()

	# Inference
	if(TSRT):
		pred = model(img, augment=False)
	else:
		pred = model(img, augment=False)[0]		#to engine
	#t3 = time_sync()
	# NMS
	conf_thres = 0.45
	iou_thres = 0.5
	pred = non_max_suppression(pred, conf_thres, iou_thres)
	#t4 = time_sync()
	#--------------------------------------------------

	det_bbox_list = []
	det_conf_list = []
	det_cls_list = []
	# Process detections
	annotator = Annotator(vavc_frame, line_width=3, pil=not ascii)
	for i, det in enumerate(pred):  # detections per image
		gn = torch.tensor(vavc_frame.shape)[[1, 0, 1, 0]]  # normalization gain whwh
		if len(det):
			# Rescale boxes from img_size to vavc_frame size
			det[:, :4] = scale_coords(img.shape[2:], det[:, :4], vavc_frame.shape).round()
			# Write results
			for *xyxy, conf, cls in reversed(det):
				#print(f"{names[int(cls)]}, {float(conf):.3f}")
				if conf > 0.45:
					# annotator.box_label(xyxy, label=f"{names[int(cls)]}, {float(conf):.3f}", color=colors[int(cls)])

					det_bbox_list.append([int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])])  # [xmin, ymin, xmax, ymax]
					det_conf_list.append(round(float(conf),2))  # [conf]
					det_cls_list.append(names[int(cls)])  # [class]

	'''				
	if 'license_plate' in det_cls_list:

		print([i for i in det_cls_list if i == 'license_plate'])
		det_cls_list_i = [det_cls_list.index(i) for i in det_cls_list if i == 'license_plate']
		print(int(det_cls_list_i[0]))
		print(det_bbox_list[int(det_cls_list_i[0])])'''
					
	#print(f"det_bbox_list:\n{det_bbox_list}")
	#print(f"det_conf_list:\n{det_conf_list}")
	#print(f"det_cls_list:\n{det_cls_list}")

	crop_img = None
	crop_conf = 'no plate detect'
	if not det_bbox_list:  # no class detect
		#print("no class detect")
		return vavc_frame, 'no class detect', crop_img, crop_conf, "", "", "", "", ""



	#--------------------------------------------------
	# vehicle class filter
	data_list = []  # [[0,0,0,0, 0.0, '']]
	ctr_y_data_list = 0
	for index in range(len(det_cls_list)):
		if det_cls_list[index] in toll_dataset_vehicle_classes:  # filter toll_vehicle class (class0 - class6)
			ctr_x = int((det_bbox_list[index][0] + det_bbox_list[index][2]) / 2)
			ctr_y = int((det_bbox_list[index][1] + det_bbox_list[index][3]) / 2)
			#print(ctr_x, ctr_y)
			if imgROI[ctr_y, ctr_x] > 127:  # in detection roi range
				# select front vehicle
				if not data_list:
					data_list.clear()
					data_list.append(det_bbox_list[index])
					data_list.append(det_conf_list[index])
					data_list.append(det_cls_list[index])
					ctr_y_data_list = ctr_y
				elif ctr_y > ctr_y_data_list:
					data_list.clear()
					data_list.append(det_bbox_list[index])
					data_list.append(det_conf_list[index])
					data_list.append(det_cls_list[index])
					ctr_y_data_list = ctr_y
	if data_list:
		# print(f"data_list:\n{data_list}")
		if draw_bbox_vehicle:
			# paintBoundingBox(vavc_frame, data_list[0], label=f'{data_list[2]} {data_list[1]:.2f}', color=colors[names.index(data_list[2])])
			paintBoundingBox(vavc_frame, data_list[0], label=f'{data_list[2]} {data_list[1]:.2f}', color=(255,255,0))

	#--------------------------------------------------
	# wheel filter
	single_wheel.clear()
	double_wheel.clear()
	license_plate_taxi.clear()
	predicted_vehicle_data = None
	if len(data_list) > 0:
		for index in range(len(det_cls_list)):
			if det_cls_list[index] not in toll_dataset_vehicle_classes:  # filter not toll_vehicle class
				ctr_x = int((det_bbox_list[index][0] + det_bbox_list[index][2]) / 2)
				ctr_y = int((det_bbox_list[index][1] + det_bbox_list[index][3]) / 2)
				#print(ctr_x, ctr_y)
				if(ctr_x > int(data_list[0][0]))and(ctr_y > int(data_list[0][1]))and(ctr_x < int(data_list[0][2]))and(ctr_y < int(data_list[0][3])):  # in vehicle roi range
					if det_cls_list[index] == 'singleWheel':
						# single_wheel.append(True)
						single_wheel.append(det_bbox_list[index])
					elif det_cls_list[index] == 'doubleWheel':
						# double_wheel.append(True)
						double_wheel.append(det_bbox_list[index])
					elif det_cls_list[index] == 'license_plate_taxi':
						# license_plate_taxi.append(True)
						license_plate_taxi.append(det_bbox_list[index])
					elif det_cls_list[index] == 'license_plate':
						# license_plate.append(True)
						# license_plate.append(det_bbox_list[index])
						crop_conf = det_conf_list[index]
						x, y, w, h = int(det_bbox_list[index][0]), int(det_bbox_list[index][1]), int(det_bbox_list[index][2] - det_bbox_list[index][0]), int(det_bbox_list[index][3] - det_bbox_list[index][1])
						crop_img = frame_raw[max(y-3,0):min(y+h+3,frame_raw.shape[0]), max(x-3,0):min(x+w+3,frame_raw.shape[1])]
						try:
							crop_img = correct_skew(crop_img)
						except:
							print("ERROR: correct_skew.")
					if draw_bbox_wheel and det_cls_list[index] != 'license_plate':
						# paintBoundingBox(vavc_frame, det_bbox_list[index], label=f'{det_cls_list[index]} {det_conf_list[index]:.2f}', color=colors[names.index(det_cls_list[index])])
						paintBoundingBox(vavc_frame, det_bbox_list[index], label=f'{det_cls_list[index]} {det_conf_list[index]:.2f}', color=(255,255,0))

					if draw_bbox_plate and det_cls_list[index] == 'license_plate':
						# paintBoundingBox(vavc_frame, det_bbox_list[index], label=f'{det_cls_list[index]} {det_conf_list[index]:.2f}', color=colors[names.index(det_cls_list[index])])
						paintBoundingBox(vavc_frame, det_bbox_list[index], label=f'{det_cls_list[index]} {det_conf_list[index]:.2f}', color=(255,255,0))

		predicted_vehicle_data = updateDetectionClass(data_list[0], single_wheel, double_wheel, license_plate_taxi)
		if put_class_at_bottom is True:
			cv2.putText(vavc_frame, "Class: " + str(data_list[2]), (70,672), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4, cv2.LINE_AA)
		
		# if draw_bbox_vehicle:
		# print("predicted_vehicle_data", predicted_vehicle_data)
		# print("crop_conf", crop_conf)
		# 	print("data_list[0]",data_list[0])
		# 	print("data_list[1]",data_list[1])
		# 	print("data_list[2]",data_list[2])
		# 	print("predicted_vehicle_data : ", predicted_vehicle_data)
		# 	print("single_wheel :", single_wheel)
		# 	print("double_wheel :", double_wheel)
		# 	print("license_plate_taxi : ", license_plate_taxi)
		# 	print("license_plate : ", license_plate)
			#cv2.putText(vavc_frame, "CLASS: " + str(data_list[2]), (128,672), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
		#for xml
		return vavc_frame, predicted_vehicle_data, crop_img, crop_conf, data_list, single_wheel, double_wheel, license_plate_taxi, license_plate
	return vavc_frame, predicted_vehicle_data, crop_img, crop_conf, data_list, single_wheel, double_wheel, license_plate_taxi, license_plate


		# return vavc_frame, predicted_vehicle_data, crop_img, crop_conf
	# return vavc_frame, 'no class detect', crop_img, crop_conf


