#==================================================
#===== SUB FUNCTION - anpr
# main_v? anpr_v? datalogger_v? vavc_v?
#==================================================

#==================================================
#===== yolov5 reference 
# https://github.com/ultralytics/yolov5
# Python>=3.6.0 is required with all requirements.txt installed including PyTorch>=1.7:
#==================================================

#==================================================
# HISTORY
#==================================================
# Parameter:
# 1. threshold = 0.45
# 2. iou = 0.5
#===== 20/9/2021
# 1. modify to 2 cameras
# 2. plate size define 1row h>32, 2row h>48
# 3. ROI using image mask to define
#===== 12/10/2021
# 1. flask request to save image while unrecognize if conf<0.8, small plate and not in ROI
#===== 1/11/2021
# 1. restructure program
#===== 8/11/2021
# 1. model renew without stop program
#===== 3/1/2022
# 1. remove some img buffer to shorter time
#===== 10/8/2022
# 1. increase speed
# 2. modify to tensorRT
#==================================================
# PENDING
#==================================================
# 1.
#==================================================

TSRT = True  # use TensorRT (.engine)

import os
import cv2
import numpy as np
import queue
import time
#import matplotlib.pyplot as plt

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
from utils.plots import Annotator, colors
#from utils.plots import plot_one_box
#from utils.datasets import LoadImages

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
def letterbox(img, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
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
# Intersection over Union is an evaluation metric used to measure the accuracy of an object detector on a particular dataset
def bb_intersection_over_union(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])

	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)

	# return the intersection over union value
	return iou

#--------------------------------------------------
# cases of duplicated 1
def checkForOnes(_final_bbox):
	final_bbox = []
	final_plate = []

	index = 0
	plate_index = 0
	while index < len(_final_bbox):
		if index > 0:
			if _final_bbox[index][4] == '1':			
				iou_bbox = bb_intersection_over_union(_final_bbox[index-1][6], _final_bbox[index][6])
				#print('1 - ', iou_bbox)
				if iou_bbox < 0.15:
					index = index + 1
					continue
			elif _final_bbox[index-1][4] == '1':		
				iou_bbox = bb_intersection_over_union(_final_bbox[index-1][6], _final_bbox[index][6])
				#print('2 - ', iou_bbox)
				if iou_bbox > 0.9:
					final_bbox[plate_index-1] = _final_bbox[index]					# replace previous word
					final_plate[plate_index-1] = _final_bbox[index][4]
					index = index + 1
					continue
		final_bbox.append(_final_bbox[index])
		final_plate.append(_final_bbox[index][4])
		index = index + 1
		plate_index = plate_index + 1
	return final_plate

#--------------------------------------------------
# remove redundancy and sort word
def plate_finetune(bbox_list):
	#bbox_list = xywh, cls, conf, [xyxy]
	bbox1 = []
	bbox2 = []
	final_bbox = []
	final_plate = []
	overlap = 0.25
	#print('Received : ', bbox_list)

	index = 0
	plate_index = 0
	while index < len(bbox_list):
		#print(bbox_list[index][4], ' == ',  bbox_list[index][5])
		if index > 0:
			overlap_region = overlap * final_bbox[plate_index-1][2]
			left_overlap = bbox_list[index-1][6][0] - overlap_region
			right_overlap = bbox_list[index-1][6][0] + overlap_region
			if bbox_list[index][6][0] >= left_overlap and bbox_list[index][6][0] <= right_overlap:  # if overlap
				if bbox_list[index][5] > final_bbox[plate_index-1][5]:  # check if confidence value is more
					#print('update new : ', bbox_list[index][4], ' --> ', bbox_list[index-1][4])
					final_bbox[plate_index-1] = bbox_list[index]  # replace previous word
					index = index + 1
					continue
				else:  # keep previous word
					#print('keep previous: ', bbox_list[index-1][4])
					index = index + 1
					continue
		final_bbox.append(bbox_list[index])
		#final_plate.append(bbox_list[index][4])
		index = index + 1
		plate_index = plate_index + 1
	final_plate = checkForOnes(final_bbox)
	if len(final_plate) > 0:
		plate_number = ''.join(final_plate)
	else:
		plate_number = ''

	
	# special number plate

	NBOS_list = ['NBOS', 'NB0S', 'NBQS']

	if plate_number[:2] == '1Q':
		plate_number = 'IQ' + plate_number[2:]
	if plate_number[:2] == '1M':
		plate_number = 'IM' + plate_number[2:]

	if plate_number[:3] == 'V1P':
		plate_number = 'VIP' + plate_number[3:]
	if plate_number[:3] == 'Q1Q':
		plate_number = 'QIQ' + plate_number[3:]
	if plate_number[:3] == 'GIM':
		plate_number = 'G1M' + plate_number[3:]

	if plate_number[:4] in NBOS_list:
		plate_number = 'NBOS' + plate_number[4:]
	if plate_number[:4] == 'U1TM':
		plate_number = 'UITM' + plate_number[4:]
	if plate_number[:4] == '11UM':
		plate_number = 'IIUM' + plate_number[4:]
	if plate_number[:4] == 'X01C':
		plate_number = 'XOIC' + plate_number[4:]
	if plate_number[:4] == 'IM4U':
		plate_number = '1M4U' + plate_number[4:]

	if plate_number[:5] == 'R1MAU':
		plate_number = 'RIMAU' + plate_number[5:]
	if plate_number[:5] == 'SUK0M':
		plate_number = 'SUKOM' + plate_number[5:]

	if plate_number[:6] == 'XXX1DB':
		plate_number = 'XXXIDB' + plate_number[6:]

	if plate_number[:7] == 'X111NAM':
		plate_number = 'XIIINAM' + plate_number[7:]

	

	
	


	return plate_number


#--------------------------------------------------
# recognize plate number
def recognize_plate(model_recognize, half, device, plate_img):
	#--------------------------------------------------
	# Load model
	model = model_recognize

	# Get names and colors
	names = model.module.names if hasattr(model, 'module') else model.names
	colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
##	colors = model.colors

	# Padded resize	
	if(TSRT):
		stride = max(int(model.stride), 32)  # model stride=32
	else:
		stride = 32  # model stride=32
	imgsz = [640,640]
	imgsz = check_img_size(imgsz, s=stride)  # check img_size
	img = letterbox(plate_img, imgsz, stride=stride, auto=False)[0]

	# Process image
	#t1 = time_sync()
	img = img[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
	img = np.ascontiguousarray(img)
	img = torch.from_numpy(img).to(device)
	img = img.half() if half else img.float()  # uint8 to fp16/32
	img /= 255.0  # 0 ~ 255 to 0.0 ~ 1.0
	if img.ndimension() == 3:
		img = img.unsqueeze(0)
	#t2 = time_sync()

	# Inference
	if(TSRT):
		pred = model(img, augment=False)
	else:
		pred = model(img, augment=False)[0]
	#t3 = time_sync()
	# NMS
	conf_thres = 0.45
	iou_thres = 0.5
	pred = non_max_suppression(pred, conf_thres, iou_thres)
	#t4 = time_sync()
	#--------------------------------------------------

	data_list = []	# x_center, width_val, detected_class, confidence
	bbox_list = []
	bbox_1 = []
	bbox_2 = []
	conf_lvl = []
	final_plate_num = ''
	avg_conf = ''

	# Process detections
	#annotator = Annotator(plate_img, line_width=1, pil=not ascii)
	for i, det in enumerate(pred):  # per image
		gn = torch.tensor(plate_img.shape)[[1, 0, 1, 0]]  # normalization gain whwh
		if len(det):
			# Rescale boxes from img_size to plate_img size
			det[:, :4] = scale_coords(img.shape[2:], det[:, :4], plate_img.shape).round()
			# Write results
			for *xyxy, conf, cls in reversed(det):
				xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
				_xyxy = ((torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()
				conf_lvl.append(round(float(conf), 2))
				data_list.clear()
				data_list.append(float(xywh[0]))
				data_list.append(float(xywh[1]))
				data_list.append(float(xywh[2]))
				data_list.append(float(xywh[3]))
				data_list.append(names[int(cls)])
				data_list.append(round(float(conf), 5))
				data_list.append(_xyxy)  # character (Xmin,Ymin),(Xmax,Ymax)
				bbox_list.append(data_list[:])
				#plot_one_box(xyxy, plate_img, label=f'{names[int(cls)]} {conf:.2f}', color=colors[int(cls)], line_thickness=1)
				#annotator.box_label(xyxy, label=f'{names[int(cls)]} {conf:.2f}', color=colors[int(cls)])
			
			# plate sorting
			bbox_arr = np.array(bbox_list, dtype=object)
			df = pd.DataFrame(bbox_arr, columns=['x', 'y', 'w', 'h', 'cls', 'conf', 'xyxy'])
			diff = float(df['y'].max()) - float(df['y'].min())
			ymax = float(df['y'].max())
			_ymin = df['y'].min()
			ymin = float(_ymin)
			min_index = ((df[df['y']==_ymin].index).tolist())[0]
			hmin = float(df.at[min_index,'h'])
			min_center = (hmin/2)+ymin

			# if 2 line = sort & pass to a process, if 1 line, sort all	
			if ymax < min_center:
				#print('1 line')
				bbox_list.sort(key = lambda bbox_list:(bbox_list[0]))
			else:
				#print('2 lines')
				bbox_1.clear()
				bbox_2.clear()
				for data in bbox_list:
					if data[1] < min_center:
						bbox_1.append(data)
						bbox_1.sort(key = lambda bbox_1:(bbox_1[0]))
					else:
						bbox_2.append(data)
						bbox_2.sort(key = lambda bbox_2:(bbox_2[0]))
				bbox_list.clear()
				bbox_list.extend(bbox_1)
				bbox_list.extend(bbox_2)
		
		final_plate_num = plate_finetune(bbox_list)
		
		try:
			avg_conf = round(float(sum(conf_lvl)/len(conf_lvl)), 2)
		except:
			pass
		
	return final_plate_num.replace(" ",""), avg_conf


#--------------------------------------------------
# detect plate number (image)
def runPlateDetection_Img(model_detection, model_recognize, half, device, frame, imgROI):
	#--------------------------------------------------
	# Load model
	model = model_detection

	# Get names and colors
	names = model.module.names if hasattr(model, 'module') else model.names
	colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
##	colors = model.colors

	# Padded resize
	stride = 32  # model stride=32
	imgsz = [640, 640]
	imgsz = check_img_size(imgsz, s=stride)  # check img_size
	img = letterbox(frame, imgsz, stride=stride)[0]

	# Process image
	#t1 = time_sync()
	img = img[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
	img = np.ascontiguousarray(img)
	img = torch.from_numpy(img).to(device)
	img = img.half() if half else img.float()  # uint8 to fp16/32
	img /= 255.0  # 0~255 to 0.0~1.0
	if img.ndimension() == 3:
		img = img.unsqueeze(0)
	#t2 = time_sync()

	# Inference
	pred = model(img, augment=False)[0]
	#t3 = time_sync()
	# NMS
	conf_thres = 0.7
	iou_thres = 0.8
	pred = non_max_suppression(pred, conf_thres, iou_thres)
	#t4 = time_sync()
	#--------------------------------------------------

	platenum = ''
	avg_conf = ''
	crop_img = None
	# Process detections
	annotator = Annotator(frame, line_width=2, pil=not ascii)
	for i, det in enumerate(pred):  # detections per image
		gn = torch.tensor(frame.shape)[[1, 0, 1, 0]]  # normalization gain whwh
		if len(det):
			# Rescale boxes from img_size to frame size
			det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()
			# Write results
			for *xyxy, conf, cls in reversed(det):
				x, y, w, h = int(xyxy[0]), int(xyxy[1]), int(xyxy[2] - xyxy[0]), int(xyxy[3] - xyxy[1])
				#print("x, y, w, h:", x, y, w, h)
			ctr_x = int(x + (w/2))
			ctr_y = int(y + (h/2))
			if imgROI[ctr_y, ctr_x]>127:  # within detection roi range
				img_ = frame.astype(np.uint8)
				crop_img = img_[max(y-3,0):min(y+h+3,img_.shape[0]), max(x-3,0):min(x+w+3,img_.shape[1])]
				try:
					crop_img = correct_skew(crop_img)
				except:
					print("ERROR: correct_skew.")
					pass
				try:				
					platenum, avg_conf = recognize_plate(model_recognize, half, device, crop_img)  # recognize plate number!
				except:
					platenum = ''
					avg_conf = 0.0
			#plot_one_box(xyxy, frame, label=f'{names[int(cls)]}', color=colors[int(cls)], line_thickness=1)
			annotator.box_label(xyxy, label=f'{names[int(cls)]}', color=colors[int(cls)])
			

	return crop_img, conf, platenum, avg_conf

#--------------------------------------------------
# detect plate number (video)
def runPlateDetection(model_detection, half, device, img, detect_img, imgROI):
	#--------------------------------------------------
	# Load model
	#t0 = time_sync()
	model = model_detection

	# Get names and colors
	names = model.module.names if hasattr(model, 'module') else model.names  # get class names
	colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
##	colors = model.colors

	# Padded resize
#	stride = 32  # model stride=32
#	imgsz = [640, 640]
#	imgsz = check_img_size(imgsz, s=stride)  # check img_size
#	img = letterbox(detect_img, imgsz, stride=stride, auto=False)[0]

	# Process image
	#t1 = time_sync()
#	img = img[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
#	img = np.ascontiguousarray(img)
#	img = torch.from_numpy(img).to(device)
#	img = img.half() if half else img.float()  # uint8 to fp16/32
#	img /= 255.0  # 0~255 to 0.0~1.0
#	if img.ndimension() == 3:
#		img = img.unsqueeze(0)
	#t2 = time_sync()

	# Inference
	if(TSRT):
		pred = model(img, augment=False)
	else:
		pred = model(img, augment=False)[0]
	#t3 = time_sync()
	# NMS
	conf_thres = 0.7
	iou_thres = 0.8
	pred = non_max_suppression(pred, conf_thres, iou_thres)
	#t4 = time_sync()
	#--------------------------------------------------

	conf = ''
	crop_img = None
	# Process detections
	annotator = Annotator(detect_img, line_width=2, pil=not ascii)
	for i, det in enumerate(pred):  # detections per image
		gn = torch.tensor(detect_img.shape)[[1, 0, 1, 0]]  # normalization gain whwh
		if len(det):
			# Rescale boxes from img size to detect_img size
			det[:, :4] = scale_coords(img.shape[2:], det[:, :4], detect_img.shape).round()
			# Write results
			for *xyxy, conf, cls in reversed(det):
				x, y, w, h = int(xyxy[0]), int(xyxy[1]), int(xyxy[2] - xyxy[0]), int(xyxy[3] - xyxy[1])
				#print("x, y, w, h:", x, y, w, h)
			ctr_x = int(x + (w/2))
			ctr_y = int(y + (h/2))
			if imgROI[ctr_y, ctr_x]>127:  # within detection roi range
				# crop plate when detected
				crop_img = detect_img[max(y-3,0):min(y+h+3,detect_img.shape[0]), max(x-3,0):min(x+w+3,detect_img.shape[1])].copy()
#				try:
#					crop_img = correct_skew(crop_img)
#				except:
#					print("ERROR: correct_skew.")
#					pass
			else:
				conf = 'not in ROI'
			#plot_one_box(xyxy, detect_img, label=f'{names[int(cls)]}', color=colors[int(cls)], line_thickness=2)
			annotator.box_label(xyxy, label=f'{names[int(cls)]}', color=colors[int(cls)])
		else:
			conf = 'no plate detect'

	#t5 = time_sync()
	# print(f"Model, Total:{(t5-t0):.4f} Resize:{(t1-t0):.4f} Numpy:{(t2-t1):.4f} Numpy2:{(t2_5-t1_5):.4f} Inference: {(t3-t2):.4f},  nms: {(t4-t3):-3} annotate:{(t5-t4):.4f}")
	# print(f"Total:{(t5-t0):.4f} Pre:{(t2-t1):.4f} Pre:{(t2_5-t1_5):.4f} nms:{(t4-t3):.3} annotate:{(t5-t4):.4f} Inference:{(t3-t2):.4f}")
		
	return crop_img, conf

#==================================================
# END
