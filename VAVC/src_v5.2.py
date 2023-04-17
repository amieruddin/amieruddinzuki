#######################################
#
# 1 - VAVC with online (RS232) connection
# (Jetson Xavier)
# 2 - Read OB & loop sensor 
#
# 3 - Add data logging
#
######################################

######################################
# update src_v4.1
#
# 1 - emergency & no detection = class 1
# 2 - if external HD=126 GB, VAVC still run, detection class send to RS232 and data(img, xml) not save
# 3 - add class in tracking.csv
# 4 - changing external HD no need to close program, data will save on pc memory until new external HD is mount
#
######################################

######################################
# update src_v5.2
# 1. update to delete image using housekeeoing function

def get_uuid() -> str:
	return subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()

def get_hdd_id() -> str:
	serials = subprocess.check_output('wmic diskdrive get Name, SerialNumber').decode().split('\n')[1:]
	for serial in serials:
		if 'DRIVE0' in serial:
			return serial.split('DRIVE0')[-1].strip()

def dongle():
	try:
		with open('dongle.key', 'rb') as dongle_file:
			dongle_key = dongle_file.read()
			#print(f"Read File: {dongle_key}")
	except IOError:
		print("Copyright Software, illegal use is prohibited.")
		sys.exit(0)
	temp = dongle_key.split()
	key = temp[0]
	#print(f"Encrypt Key: {key}")
	encrypted = temp[1]
	#print(f"Encrypted: {encrypted}")
	f = Fernet(key)
	decrypted = f.decrypt(encrypted)
	#print(f"Decrypted: {decrypted}")
	mix_data = decrypted.decode('utf-8')
	data_date = mix_data.split('_')[0]
	data_id = mix_data.split('_')[-1]
	#print(f"Data Date: {data_date}, Data ID: {data_id}")

	if 'nt' in os.name:
		#unique_id = get_uuid() + '-' + get_hdd_id()
		unique_id = get_uuid()
		#print(unique_id)
	else:
		proc = subprocess.Popen('findmnt / -o UUID -n'.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		unique_id, err = proc.communicate()
		#print(unique_id)
		unique_id = unique_id.decode('utf-8')
		unique_id = unique_id.rstrip('\n')
		#print(unique_id)

	if not data_id == unique_id:
		print("Copyright Software, illegal use is prohibited.")
		sys.exit(0)

	try:
		data_date = datetime.strptime(data_date, "%Y-%m-%d-%H-%M-%S-%f")
	except:
		print("Copyright Software, illegal dongle key use is prohibited.")
		sys.exit(0)
	try:
		life_date = data_date.replace(data_date.year + 10)
		#life_date = datetime(2032, 5, 31)
		#print(life_date)
	except:
		print("Copyright Software, illegal dongle key use is prohibited.")
		sys.exit(0)

	today_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")[:-3]
	#print(today_date)
	today = datetime.strptime(today_date, "%Y-%m-%d-%H-%M-%S-%f")
	#print(today)

	if today > life_date:
		print("Outdated Software, illegal use is prohibited.")
		sys.exit(0)

	if os.path.exists('generator.exe'):
		os.remove('generator.exe')
	if os.path.exists('generator'):
		os.remove('generator')
	print("Copyright Software.")

#==================================================
import sys
import os
from datetime import datetime
import subprocess
import uuid
from cryptography.fernet import Fernet
dongle()

import cv2
import serial
import numpy as np
import anpr_r1 as ANPR
import vavc_r0 as VAVC
import threading
import queue
import time
import tkinter as tk
import collections

import json
from configparser import ConfigParser
from csvlogger_v1 import checkDetection, csvLogger, vavcCsvLogger, vavcCsvTracker

import socket
import shutil

import torch
from utils.torch_utils import select_device
from models.experimental import attempt_load
from utils.general import set_logging, check_img_size, non_max_suppression, scale_coords, xyxy2xywh
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
import Jetson.GPIO as GPIO

vehicle_class_name_to_numeric = {		# vehicle classes to alphabetical
	'no_detection': '1',
	'class0_emergencyVehicle': '1',
	'class1_lightVehicle': '1',
	'class2_mediumVehicle': '2',
	'class3_heavyVehicle': '3',
	'class4_taxi': '4',
	'class5_bus': '5',
}


#==================================================
class capThread(threading.Thread):
	def __init__(self, camID, captureName):
		threading.Thread.__init__(self)
		self.camID = camID
		self.captureName = captureName
	def run(self):
		print(f"\nCAMERA Start {self.camID}.")
		capCapture(self.camID, self.captureName)

class showThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print(f"\nDISPLAY Start Preview.")
		showPreview()

class OBListenerThread(threading.Thread):
	def __init__(self, vehicle_data_queue):
		threading.Thread.__init__(self)
		self.vehicle_data_queue = vehicle_data_queue
	def run(self):
		print(f"\nOB Listener Start.")
		OBlistener(self.vehicle_data_queue)

#--------------------------------------------------
def capCapture(camID, captureName):
	global progRUN, progStop, pause
	global filename0, detectFlag0, NoSignalCam0
	progStop = False
	pause = False

	# local variable
	cam0STOP = False
	n_cam = [0]
	NoSignalCam0 = False

	while not cam0STOP:

		if (datetime.now().strftime("%H%M") == "1009"):
			try:
				path = '/media/xavier/VAVC_KESAS_2'
				if os.path.exists(path):
					housekeeping_dir(path)
			except:
				sys.exit('[Path Error] : Check directory path on function housekeeping.\n')
		
			
		
		
		
		if progStop:
			cam0STOP = True
			progRUN = False
			break

		if os.path.isdir(captureName):  # video directory
			if camID==cam_ID0:
				if(n_cam[0]==len(os.listdir(captureName))):
					time.sleep(0.01)
					continue
				filename0 = os.listdir(captureName)[n_cam[0]]
				if not os.path.splitext(filename0)[-1].lower() in vid_formats:
					n_cam[0] += 1
					time.sleep(0.01)
					continue
				full_filename = os.path.join(captureName, filename0)
				n_cam[0] += 1
		elif os.path.isfile(captureName):  # video file
			if camID==cam_ID0:
				filename0 = captureName
				if not os.path.splitext(filename0)[-1].lower() in vid_formats:
					cam0STOP = True
					break
				full_filename = os.path.abspath(filename0)
		else:  # webcam
			if camID==cam_ID0:
				filename0 = captureName
				full_filename = filename0

		print(f"CAMERA Starting: {camID}, {full_filename}.")
		try:
			#cap = cv2.VideoCapture(full_filename)
			cap = cv2.VideoCapture(eval(full_filename) if full_filename.isnumeric() else full_filename)
		except cv2.error as e:
			print("ERROR: Input Source cannot open, {e}.")
			if camID==cam_ID0:
				cam0STOP = True
		width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
		height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
		if width<w_min or height<h_min:  # check cam input frame size correct
			#print("ERROR: Video Resolution below 640x480.")
			fps = int(cap.get(cv2.CAP_PROP_FPS))
			if fps == 0:
				#print("ERROR: frame/second = 0")
				if camID==cam_ID0 and NoSignalCam0==False:
					NoSignalCam0 = True
					print(f"Camera [{camID}] No Signal: {NoSignalCam0}")
					'''
					# send email notice
					email_subject = 'ANPR Camera Status'
					email_body = f'ANPR Camera no signal, {camID}.'
					email_text = """From: %s\nTo: %s\nSubject: %s\n\n%s\n""" % (email_from, ', '.join(email_to), email_subject, email_body)
					#print(f"text={email_text}")
					try:
						smtp_server = smtplib.SMTP_SSL(smtp_host, smtp_port)
						smtp_server.ehlo()
						smtp_server.login(email_from, email_password)
						smtp_server.sendmail(email_from, email_to, email_text)
						smtp_server.close()
						print("email sent successfully!")
					except Exception as ex:
						print("email not send, something went wrong …", ex)
					'''
					'''
					# send whatsapp (need web whatsapp)
					try:
						pywhatkit.sendwhatmsg_instantly("+60135801934", email_body, 15, True, 4)
						#pywhatkit.sendwhatmsg_to_group_instantly("Delloyd - kita² jer", email_body, 15, True, 4) # cannot work
						print("whatsapp sent successfully!")
					except Exception as ex:
						print("whatsapp not send, something went wrong …", ex)
					'''
				continue
		scaleRatio = min(w_std/width, h_std/height)
		if camID==cam_ID0:
			NoSignalCam0 = False

		timeStart = time.time() #init
		while cap.isOpened():
			#--------------------------------------------------
			if os.path.isfile(full_filename):
				if((time.time() - timeStart) < 0.04): #25fps
					time.sleep(0.001)
					continue
				timeStart = time.time()
			#--------------------------------------------------
			if not pause:
				try:
					rval, capF = cap.read()
				except:
					print(f"ERROR: Frame Read error: {camID}.")
					break
			if rval:
				if not pause:
					if camID==cam_ID0:
						prev_capF0 = capF
				else:
					if camID==cam_ID0:
						capF = prev_capF0
				capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
				h_capF, w_capF = capF.shape[:2]
				top = bottom = int(abs(h_std - h_capF) / 2)
				left = right = int(abs(w_std - w_capF) / 2)
				capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border

				if camID==cam_ID0:
					'''					
					if not input_buf0.empty():
						input_buf0.get()
					input_buf0.put(capF)  # for preview
					'''

					if detectFlag0 is False:
						if not detect_buf0.empty():
							detect_buf0.get()
						detect_buf0.put(capF)  # for detect
						detectFlag0 = True

				if progStop:
					cam0STOP = True
					progRUN = False
					break

			else:
				print(f"Frame Read End: {camID}, {full_filename}.")
				break

			time.sleep(0.01)
			#print("\x1b[2K", end="\r", flush=True)  # erase line
			#print(f"{camID} capture", end="\r", flush=True)

		print(f"CAMERA release: {camID}, {full_filename}.")
		cap.release()

	print(f"\nActive threads (cam): {threading.activeCount()}.")
	progRUN = False

#--------------------------------------------------
def weights_detectionUpdate(device, existing_weights_detection):
	global weights_detection, model_detection
	print("==================================================")
	# Load model plate detection
	weights_detection = ''
	file_detection = [x for x in sorted(os.listdir(lpd_path)) if x.endswith('02.pt')]  # sort available model 02.pt
	for x in file_detection:
		weights_detection = os.path.join(lpd_path, x)  # use up to date model
		if weights_detection is not existing_weights_detection:
			try:
				model_detection = attempt_load(weights_detection, map_location=device)  # load FP32 model
			except:
				print(f"[Error] License Plate Detection model file: {weights_detection}")
				weights_detection = ''
	if weights_detection == '':
		print("[Error] Cannot find suitable License Plate Detection model file.")
		sys.exit(0)
	print(f"[Model] License Plate Detection model file: {weights_detection}")
	return weights_detection

#--------------------------------------------------
def weights_recognizeUpdate(device, existing_weights_recognize):
	global weights_recognize, model_recognize
	print("==================================================")
	# Load model plate recognize
	weights_recognize = ''
	file_recognize = [x for x in sorted(os.listdir(cr_path)) if x.endswith('01.pt')]  # sort available model 01.pt
	for x in file_recognize:
		weights_recognize = os.path.join(cr_path, x)  # use up to date model
		if weights_recognize is not existing_weights_recognize:
			try:
				model_recognize = attempt_load(weights_recognize, map_location=device)  # load FP32 model
			except:
				print(f"[Error] Character Recognition model file: {weights_recognize}")
				weights_recognize = ''
	if weights_recognize == '':
		print("[Error] Cannot find suitable Character Recognition model file.")
		sys.exit(0)
	print(f"[Model] Character Recognize model file: {weights_recognize}")
	return weights_recognize

#--------------------------------------------------
def weights_vavcUpdate(device, existing_weights_vavc):
	global weights_vavc, model_vavc
	print("==================================================")
	# Load model video analytic vehicle classification (vavc)
	weights_vavc = ''
	file_vavc = [x for x in sorted(os.listdir(vavc_path)) if x.endswith('03.pt')]  # sort available model 03.pt
	for x in file_vavc:
		weights_vavc = os.path.join(vavc_path, x)  # use up to date model
		if weights_vavc is not existing_weights_vavc:
			try:
				model_vavc = attempt_load(weights_vavc, map_location=device)  # load FP32 model
			except:
				print(f"[Error] Video Analytic Vehicle Classification model file: {weights_vavc}")
				weights_vavc = ''
	if weights_vavc == '':
		print("[Error] Cannot find suitable Video Analytic Vehicle Classification model file.")
		sys.exit(0)
	print(f"[Model] Video Analytic Vehicle Classification model file: {weights_vavc}")
	return weights_vavc

#--------------------------------------------------
def showPreview():

	print(f"PREVIEW Starting...")
	global progStop, pause
	progStop = False
	pause = False
	global flagROI, flagPoint, detection_ROI, imgMouse
	global existing_weights_detection, existing_weights_recognize, existing_weights_vavc
	global camDisp0

	# local variable
	setPreview = False
	plateFlag0 = False
	font = cv2.FONT_HERSHEY_SIMPLEX
	fontScale = 0.6
	cv2.namedWindow('PREVIEW')
	cv2.moveWindow('PREVIEW', 0, 0)
	setROI0 = False
	window = 0
	if window == 0:
		imgPreview = np.zeros((int(h_std/windowScale), int(w_std/windowScale), 3), dtype=np.uint8)
	if window == 1:
		imgPreview = np.zeros((int(h_std/windowScale*2), int(w_std/windowScale), 3), dtype=np.uint8)
	if window == 2:
		imgPreview = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
	imgMouse = np.zeros((h_std, w_std, 3), dtype=np.uint8)
	modelUpdateFlag = False
	detected_plate0 = ''
	previous_plate0 = ''

	config = ConfigParser()
	if os.path.isfile('./config.ini'):
		print(f"{__file__}  READ FILE: config.ini.")
		config.read('./config.ini')
	else:
		if os.path.isfile('./setting.ini'):
			print(f"{__file__}  READ FILE: setting.ini.")
			config.read('./setting.ini')
		else:
			print("ERROR: config.ini or setting.ini file not found.")
			sys.exit(0)
	camDisp0 = config.getboolean('src_input','input_disp0')
	print(f"camDisp0: {camDisp0}.")

	while True:
		#--------------------------------------------------
		# plate cam0
		plate_box_img0 = None
		if not plate_buf0.empty():
			cam_ID, input_img, plate_box_img0, input_conf, detected_plate0, rfid_plate0, va_class0, tc_class0, time_rfid0, time_start0, time_end0, dt = plate_buf0.get().copy()
			if (cam_ID is not '') and (previous_plate0 is not detected_plate0):
				previous_plate0 = detected_plate0
				#dt = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]
				#print(f"Date: {dt}")
				# save detection image
				
				input_name = os.path.join(full_path0, '%s.' %dt + cam_ID + '.01.' + detected_plate0 + '.jpg')
				cv2.imwrite(input_name, input_img)
				plate_box_name = os.path.join(crop_path0, '%s.' %dt + cam_ID + '.02.' + detected_plate0 + '.jpg')
				cv2.imwrite(plate_box_name, plate_box_img0)

				# save log
				csvLogger(cam_ID, input_mode, log_path0, tc_class0, va_class0, str(1), rfid_plate0, detected_plate0, input_conf, input_name, time_rfid0, time_start0, time_end0)

		#--------------------------------------------------
		'''		
		if not input_buf0.empty() and camDisp0==True:
			try:
				imgP = input_buf0.get().copy()
			except:
				print("input_buf0 timeout")
			if setROI0:
				imgSetROI = cv2.addWeighted(imgP.copy(), 1, imgMouse, 1, 0)
				cv2.putText(imgSetROI, 'CAMERA: ' + cam_ID0, (10,50), font, 1.5, (0,255,0), 2, cv2.LINE_AA)
				cv2.imshow('SetROI', imgSetROI)
				#cv2.moveWindow('SetROI', 20, 20)
			if imgP is not None:
				cv2.putText(imgP, 'CAMERA: ' + cam_ID0, (10,50), font, 1.5, (0,255,0), 2, cv2.LINE_AA)
				imgP = cv2.resize(imgP, (int(imgP.shape[1]/windowScale),int(imgP.shape[0]/windowScale)))
				imgPreview[:int(imgP.shape[0]), :int(imgP.shape[1]), :3] = imgP.copy()
				setPreview = True
		'''

		#--------------------------------------------------
		if window == 0:
			if not preview_buf0.empty() and camDisp0==True:
				imgP = preview_buf0.get().copy()

				if setROI0:
					imgSetROI = cv2.addWeighted(imgP.copy(), 1, imgMouse, 1, 0)
					cv2.putText(imgSetROI, 'CAMERA: ' + cam_ID0, (10,50), font, 1.5, (0,255,0), 2, cv2.LINE_AA)
					cv2.imshow('SetROI', imgSetROI)
					#cv2.moveWindow('SetROI', 20, 20)

				if imgP is not None:
					if anpr_vavc0 == 'ANPR':
						cv2.putText(imgP, 'DETECT: ' + cam_ID0, (10,50), font, 1.5, (0,255,0), 2, cv2.LINE_AA)
						cv2.putText(imgP, 'PLATE NUMBER: ' + detected_plate0, (128,int(imgP.shape[0])-32), font, 1.5, (255,255,255), 2, cv2.LINE_AA)
						[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[0], np.int32).copy()
						if x3<x2 and x4<=x1:
							polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x4, y4]], np.int32)
						elif x3>=x2 and x4>x1:
							polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x1, y2]], np.int32)
						elif x3>=x2 and x4<=x1:
							polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x4, y4]], np.int32)
						elif x3<x2 and x4>x1:
							polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x1, y2]], np.int32)
						cv2.polylines(imgP, [polygon], isClosed=True, color=(0,255,0), thickness=2)
					imgP = cv2.resize(imgP, (int(imgP.shape[1]/windowScale),int(imgP.shape[0]/windowScale)))
					imgPreview[:int(imgP.shape[0]), :int(imgP.shape[1]), :3] = imgP.copy()
					setPreview = True

		#--------------------------------------------------
		'''
		if window > 1:
			if plate_box_img0 is not None and detected_plate0 is not '' and camDisp0==True:
				imgP = plate_box_img0
				if imgP.shape[0] > (h_std/windowScale/2) or imgP.shape[1] > (w_std/windowScale):
					imgP = cv2.resize(imgP, (int(imgP.shape[1]/2),int(imgP.shape[0]/2)))
				h_imgP, w_imgP = imgP.shape[:2]
				top = bottom = int(abs((h_std/windowScale/2) - h_imgP) / 2)
				left = right = int(abs((w_std/windowScale) - w_imgP) / 2)
				imgP = cv2.copyMakeBorder(imgP, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0,0,0))  # add black border
				imgPreview[int(h_std/windowScale*2)+(padding*2):int(h_std/windowScale*2)+(padding*2)+int(imgP.shape[0]), :int(imgP.shape[1]), :3] = imgP.copy()
				setPreview = True
				plateOff_t0 = time.time()
				plateFlag0 = True
			if plateFlag0 and ((plateOff_t0+3) < time.time()):
				imgP = np.zeros((int(h_std/windowScale/2), int(w_std/windowScale), 3), dtype=np.uint8)
				imgPreview[int(h_std/windowScale*2)+(padding*2):int(h_std/windowScale*2)+(padding*2)+int(imgP.shape[0]), :int(imgP.shape[1]), :3] = imgP.copy()
				setPreview = True
				plateFlag0 = False
				detected_plate0 = ''
		'''

		if setPreview is True:
			cv2.imshow('PREVIEW', imgPreview)
			setPreview = False

		key = cv2.waitKey(1)
		#--------------------------------------------------
		if (key & 0xFF) == ord('1'):
			setROI0 = not setROI0
			if setROI0:
				flagROI = 1
				cv2.namedWindow('SetROI')
				imgMouse[:] = 0
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[0], np.int32).copy()
				if x3 < x2 and x4 <= x1:
					polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x4, y4]], np.int32)
				elif x3 >= x2 and x4 > x1:
					polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x1, y2]], np.int32)
				elif x3 >= x2 and x4 <= x1:
					polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x4, y4]], np.int32)
				elif x3 < x2 and x4 > x1:
					polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x1, y2]], np.int32)
				cv2.polylines(imgMouse, [polygon], isClosed=True, color=(0,255,0), thickness=2)
				cv2.rectangle(imgMouse, (x1,y1), (x2,y2), color=(0,255,0), thickness=2)
				cv2.rectangle(imgMouse, (x4,y4), (x3,y3), color=(0,255,0), thickness=2)
				cv2.circle(imgMouse, (x1,y1), 5, color=(0,0,255), thickness=-1)
				cv2.circle(imgMouse, (x2,y2), 5, color=(0,0,255), thickness=-1)
				cv2.circle(imgMouse, (x3,y3), 5, color=(0,0,255), thickness=-1)
				cv2.circle(imgMouse, (x4,y4), 5, color=(0,0,255), thickness=-1)
				textctr1 = int((cv2.getTextSize(f"({str(x1)},{str(y1)})", font, fontScale, thickness=2)[0][0])/2)
				textctr2 = int((cv2.getTextSize(f"({str(x2)},{str(y2)})", font, fontScale, thickness=2)[0][0])/2)
				textctr3 = int((cv2.getTextSize(f"({str(x3)},{str(y3)})", font, fontScale, thickness=2)[0][0])/2)
				textctr4 = int((cv2.getTextSize(f"({str(x4)},{str(y4)})", font, fontScale, thickness=2)[0][0])/2)
				cv2.putText(imgMouse, f"({x1},{y1})", (x1-textctr1,y1-10), font, fontScale, color=(0,0,255), thickness=2)
				cv2.putText(imgMouse, f"({x2},{y2})", (x2-textctr2,y2-10), font, fontScale, color=(0,0,255), thickness=2)
				cv2.putText(imgMouse, f"({x3},{y3})", (x3-textctr3,y3-10), font, fontScale, color=(0,0,255), thickness=2)
				cv2.putText(imgMouse, f"({x4},{y4})", (x4-textctr4,y4-10), font, fontScale, color=(0,0,255), thickness=2)
				cv2.setMouseCallback('SetROI', mouse)
			else:
				flagROI = 0
				cv2.destroyWindow('SetROI')
		#--------------------------------------------------
		if (key & 0xFF) == ord('s'):
			if flagROI == 1:
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[0], np.int32)
				text = f"[[{x1},{y1}], [{x2},{y2}], [{x3},{y3}], [{x4},{y4}]]"
				config.set('roi', 'ROI_input0', text)
				with open('config.ini', 'w') as configfile:
					config.write(configfile)
				config.read('./config.ini')
				cv2.putText(imgMouse, f"DETECTION ROI SAVED", (10,100), font, 1.5, color=(255,255,255), thickness=2)
				#print("0 SAVE", detection_ROI[0])
			if flagROI == 2:
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[1], np.int32)
				text = f"[[{x1},{y1}], [{x2},{y2}], [{x3},{y3}], [{x4},{y4}]]"
				config.set('roi', 'ROI_input1', text)
				with open('config.ini', 'w') as configfile:
					config.write(configfile)
				config.read('./config.ini')
				cv2.putText(imgMouse, f"DETECTION ROI SAVED", (10,100), font, 1.5, color=(255,255,255), thickness=2)
				#print("1 SAVE", detection_ROI[1])
		#--------------------------------------------------
		if (key & 0xFF) == ord(' '):
			pause = not pause
		#--------------------------------------------------
		if (key & 0xFF) == ord('w'):
			if window < 2:
				window += 1
			else:
				window = 0
			if window==0:
				imgPreview = np.zeros((int(h_std/windowScale), int(w_std/windowScale), 3), dtype=np.uint8)
			if window==1:
				imgPreview = np.zeros((int(h_std/windowScale*2)+padding, int(w_std/windowScale), 3), dtype=np.uint8)
			if window==2:
				imgPreview = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
		#--------------------------------------------------
		if (datetime.now().strftime("%H%M") == "0305"):
			modelUpdateFlag = False
		if ((key & 0xFF) == ord('m')) or ((datetime.now().strftime("%H%M") == "0300") and (modelUpdateFlag == False)):
			modelUpdateFlag = True
			new_weights_detection = weights_detectionUpdate(device, existing_weights_detection)
			if new_weights_detection is not existing_weights_detection:
				existing_weights_detection = new_weights_detection
				print("Loaded new model (detection).")
			else:
				print("No new model (detection).")
			new_weights_recognize = weights_recognizeUpdate(device, existing_weights_recognize)
			if new_weights_recognize is not existing_weights_recognize:
				existing_weights_recognize = new_weights_recognize
				print("Loaded new model (recognite).")
			else:
				print("No new model (recognite).")
			new_weights_vavc = weights_vavcUpdate(device, existing_weights_vavc)
			if new_weights_vavc is not existing_weights_vavc:
				existing_weights_vavc = new_weights_vavc
				print("Loaded new model (vavc).")
			else:
				print("No new model (vavc).")
		#--------------------------------------------------
		if (key & 0xFF) == ord('q'):
			progStop = True
			break

		#print("\x1b[2K", end="\r", flush=True)  # erase line
		#print("disp running", end="\r", flush=True)

	cv2.destroyWindow('PREVIEW')
	print(f"\nActive threads (preview): {threading.activeCount()}.")

#--------------------------------------------------
def mouse(event, x, y, flags, param):
	global flagROI, flagPoint, detection_ROI, imgMouse
	global mx1, my1, mx2, my2, mx3, my3, mx4, my4

	font = cv2.FONT_HERSHEY_SIMPLEX
	fontScale = 0.6
	if event == cv2.EVENT_LBUTTONDOWN:
		if flagROI == 1:
			[[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]] = np.array(detection_ROI[0], np.int32).copy()
			#print("0 DOWN", [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]])
		elif flagROI == 2:
			[[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]] = np.array(detection_ROI[1], np.int32).copy()
			#print("1 DOWN", [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]])
		if (x in range(mx1-10, mx1+10)) and (y in range(my1-10, my1+10)):
			flagPoint = 1
			if x < mx2:	mx1 = x
			else:		mx1 = mx2-1
			if y < my2:	my1 = y
			else:		my1 = my2-1
		elif (x in range(mx2-10, mx2+10)) and (y in range(my2-10, my2+10)):
			flagPoint = 2
			if x > mx1:	mx2 = x
			else:		mx2 = mx1+1
			if y > my1:	my2 = y
			else:		my2 = my1+1
		elif (x in range(mx3-10, mx3+10)) and (y in range(my3-10, my3+10)):
			flagPoint = 3
			if x > mx4:	mx3 = x
			else:		mx3 = mx4+1
			if y > my4:	my3 = y
			else:		my3 = my4+1
		elif (x in range(mx4-10, mx4+10)) and (y in range(my4-10, my4+10)):
			flagPoint = 4
			if x < mx3:	mx4 = x
			else:		mx4 = mx3-1
			if y < my3:	my4 = y
			else:		my4 = my3-1
		imgMouse[:] = 0
		if mx3 < mx2 and mx4 <= mx1:
			polygon = np.array([[mx1, my1], [mx2, my1], [mx2, my2], [mx3, my3], [mx4, my3], [mx4, my4]], np.int32)
		elif mx3 >= mx2 and mx4 > mx1:
			polygon = np.array([[mx1, my1], [mx2, my1], [mx3, my4], [mx3, my3], [mx4, my3], [mx1, my2]], np.int32)
		elif mx3 >= mx2 and mx4 <= mx1:
			polygon = np.array([[mx1, my1], [mx2, my1], [mx3, my4], [mx3, my3], [mx4, my3], [mx4, my4]], np.int32)
		elif mx3 < mx2 and mx4 > mx1:
			polygon = np.array([[mx1, my1], [mx2, my1], [mx2, my2], [mx3, my3], [mx4, my3], [mx1, my2]], np.int32)
		cv2.polylines(imgMouse, [polygon], isClosed=True, color=(0,255,0), thickness=2)
		cv2.rectangle(imgMouse, (mx1,my1), (mx2,my2), color=(0,255,0), thickness=2)
		cv2.rectangle(imgMouse, (mx4,my4), (mx3,my3), color=(0,255,0), thickness=2)
		cv2.circle(imgMouse, (mx1,my1), 5, color=(0,0,255), thickness=-1)
		cv2.circle(imgMouse, (mx2,my2), 5, color=(0,0,255), thickness=-1)
		cv2.circle(imgMouse, (mx3,my3), 5, color=(0,0,255), thickness=-1)
		cv2.circle(imgMouse, (mx4,my4), 5, color=(0,0,255), thickness=-1)
		textctr1 = int((cv2.getTextSize(f"({str(mx1)},{str(my1)})", font, fontScale, thickness=2)[0][0])/2)
		textctr2 = int((cv2.getTextSize(f"({str(mx2)},{str(my2)})", font, fontScale, thickness=2)[0][0])/2)
		textctr3 = int((cv2.getTextSize(f"({str(mx3)},{str(my3)})", font, fontScale, thickness=2)[0][0])/2)
		textctr4 = int((cv2.getTextSize(f"({str(mx4)},{str(my4)})", font, fontScale, thickness=2)[0][0])/2)
		cv2.putText(imgMouse, f"({mx1},{my1})", (mx1-textctr1,my1-10), font, fontScale, color=(0,0,255), thickness=2)
		cv2.putText(imgMouse, f"({mx2},{my2})", (mx2-textctr2,my2-10), font, fontScale, color=(0,0,255), thickness=2)
		cv2.putText(imgMouse, f"({mx3},{my3})", (mx3-textctr3,my3-10), font, fontScale, color=(0,0,255), thickness=2)
		cv2.putText(imgMouse, f"({mx4},{my4})", (mx4-textctr4,my4-10), font, fontScale, color=(0,0,255), thickness=2)

	elif event == cv2.EVENT_MOUSEMOVE and flags == 1:
		if flagPoint == 1:
			if x < mx2:	mx1 = x
			else:		mx1 = mx2-1
			if y < my2:	my1 = y
			else:		my1 = my2-1
		elif flagPoint == 2:
			if x > mx1:	mx2 = x
			else:		mx2 = mx1+1
			if y > my1:	my2 = y
			else:		my2 = my1+1
		elif flagPoint == 3:
			if x > mx4:	mx3 = x
			else:		mx3 = mx4+1
			if y > my4:	my3 = y
			else:		my3 = my4+1
		elif flagPoint == 4:
			if x < mx3:	mx4 = x
			else:		mx4 = mx3-1
			if y < my3:	my4 = y
			else:		my4 = my3-1
		imgMouse[:] = 0
		if mx3 < mx2 and mx4 <= mx1:
			polygon = np.array([[mx1, my1], [mx2, my1], [mx2, my2], [mx3, my3], [mx4, my3], [mx4, my4]], np.int32)
		elif mx3 >= mx2 and mx4 > mx1:
			polygon = np.array([[mx1, my1], [mx2, my1], [mx3, my4], [mx3, my3], [mx4, my3], [mx1, my2]], np.int32)
		elif mx3 >= mx2 and mx4 <= mx1:
			polygon = np.array([[mx1, my1], [mx2, my1], [mx3, my4], [mx3, my3], [mx4, my3], [mx4, my4]], np.int32)
		elif mx3 < mx2 and mx4 > mx1:
			polygon = np.array([[mx1, my1], [mx2, my1], [mx2, my2], [mx3, my3], [mx4, my3], [mx1, my2]], np.int32)
		cv2.polylines(imgMouse, [polygon], isClosed=True, color=(0,255,0), thickness=2)
		cv2.rectangle(imgMouse, (mx1,my1), (mx2,my2), color=(0,255,0), thickness=2)
		cv2.rectangle(imgMouse, (mx4,my4), (mx3,my3), color=(0,255,0), thickness=2)
		cv2.circle(imgMouse, (mx1,my1), 5, color=(0,0,255), thickness=-1)
		cv2.circle(imgMouse, (mx2,my2), 5, color=(0,0,255), thickness=-1)
		cv2.circle(imgMouse, (mx3,my3), 5, color=(0,0,255), thickness=-1)
		cv2.circle(imgMouse, (mx4,my4), 5, color=(0,0,255), thickness=-1)
		textctr1 = int((cv2.getTextSize(f"({str(mx1)},{str(my1)})", font, fontScale, thickness=2)[0][0])/2)
		textctr2 = int((cv2.getTextSize(f"({str(mx2)},{str(my2)})", font, fontScale, thickness=2)[0][0])/2)
		textctr3 = int((cv2.getTextSize(f"({str(mx3)},{str(my3)})", font, fontScale, thickness=2)[0][0])/2)
		textctr4 = int((cv2.getTextSize(f"({str(mx4)},{str(my4)})", font, fontScale, thickness=2)[0][0])/2)
		cv2.putText(imgMouse, f"({mx1},{my1})", (mx1-textctr1,my1-10), font, fontScale, color=(0,0,255), thickness=2)
		cv2.putText(imgMouse, f"({mx2},{my2})", (mx2-textctr2,my2-10), font, fontScale, color=(0,0,255), thickness=2)
		cv2.putText(imgMouse, f"({mx3},{my3})", (mx3-textctr3,my3-10), font, fontScale, color=(0,0,255), thickness=2)
		cv2.putText(imgMouse, f"({mx4},{my4})", (mx4-textctr4,my4-10), font, fontScale, color=(0,0,255), thickness=2)

	elif event == cv2.EVENT_LBUTTONUP:
		if flagPoint == 1:
			if x < mx2:	mx1 = x
			else:		mx1 = mx2-1
			if y < my2:	my1 = y
			else:		my1 = my2-1
		elif flagPoint == 2:
			if x > mx1:	mx2 = x
			else:		mx2 = mx1+1
			if y > my1:	my2 = y
			else:		my2 = my1+1
		elif flagPoint == 3:
			if x > mx4:	mx3 = x
			else:		mx3 = mx4+1
			if y > my4:	my3 = y
			else:		my3 = my4+1
		elif flagPoint == 4:
			if x < mx3:	mx4 = x
			else:		mx4 = mx3-1
			if y < my3:	my4 = y
			else:		my4 = my3-1
		imgMouse[:] = 0
		if mx3 < mx2 and mx4 <= mx1:
			polygon = np.array([[mx1, my1], [mx2, my1], [mx2, my2], [mx3, my3], [mx4, my3], [mx4, my4]], np.int32)
		elif mx3 >= mx2 and mx4 > mx1:
			polygon = np.array([[mx1, my1], [mx2, my1], [mx3, my4], [mx3, my3], [mx4, my3], [mx1, my2]], np.int32)
		elif mx3 >= mx2 and mx4 <= mx1:
			polygon = np.array([[mx1, my1], [mx2, my1], [mx3, my4], [mx3, my3], [mx4, my3], [mx4, my4]], np.int32)
		elif mx3 < mx2 and mx4 > mx1:
			polygon = np.array([[mx1, my1], [mx2, my1], [mx2, my2], [mx3, my3], [mx4, my3], [mx1, my2]], np.int32)
		cv2.polylines(imgMouse, [polygon], isClosed=True, color=(0,255,0), thickness=2)
		cv2.rectangle(imgMouse, (mx1,my1), (mx2,my2), color=(0,255,0), thickness=2)
		cv2.rectangle(imgMouse, (mx4,my4), (mx3,my3), color=(0,255,0), thickness=2)
		cv2.circle(imgMouse, (mx1,my1), 5, color=(0,0,255), thickness=-1)
		cv2.circle(imgMouse, (mx2,my2), 5, color=(0,0,255), thickness=-1)
		cv2.circle(imgMouse, (mx3,my3), 5, color=(0,0,255), thickness=-1)
		cv2.circle(imgMouse, (mx4,my4), 5, color=(0,0,255), thickness=-1)
		textctr1 = int((cv2.getTextSize(f"({str(mx1)},{str(my1)})", font, fontScale, thickness=2)[0][0])/2)
		textctr2 = int((cv2.getTextSize(f"({str(mx2)},{str(my2)})", font, fontScale, thickness=2)[0][0])/2)
		textctr3 = int((cv2.getTextSize(f"({str(mx3)},{str(my3)})", font, fontScale, thickness=2)[0][0])/2)
		textctr4 = int((cv2.getTextSize(f"({str(mx4)},{str(my4)})", font, fontScale, thickness=2)[0][0])/2)
		cv2.putText(imgMouse, f"({mx1},{my1})", (mx1-textctr1,my1-10), font, fontScale, color=(0,0,255), thickness=2)
		cv2.putText(imgMouse, f"({mx2},{my2})", (mx2-textctr2,my2-10), font, fontScale, color=(0,0,255), thickness=2)
		cv2.putText(imgMouse, f"({mx3},{my3})", (mx3-textctr3,my3-10), font, fontScale, color=(0,0,255), thickness=2)
		cv2.putText(imgMouse, f"({mx4},{my4})", (mx4-textctr4,my4-10), font, fontScale, color=(0,0,255), thickness=2)

		flagPoint = 0
		if flagROI == 1:
			detection_ROI[0] = [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]].copy()
			#print("0 UP", detection_ROI[0])
		elif flagROI == 2:
			detection_ROI[1] = [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]].copy()
			#print("1 UP", detection_ROI[1])

#--------------------------------------------------
def pathUpdate():
	global today_date, cr_path, lpd_path, vavc_path
	global full_path0, crop_path0, log_path0, vavc_dataset_path, vavc_log_path
	today_date = datetime.now().strftime("%Y%m%d")
	print(f"Program Directory Initialize... {today_date}")
	curr_path = os.path.dirname(os.path.realpath(__file__))
	cr_path = os.path.join(curr_path, 'trained_models', 'cr')
	lpd_path = os.path.join(curr_path, 'trained_models', 'lpd')
	vavc_path = os.path.join(curr_path, 'trained_models', 'vavc')
	if not os.path.isdir(cr_path) or not os.path.isdir(lpd_path) or not os.path.isdir(vavc_path):
		print("Error: models directory don't exist")
		sys.exit(0)

	anpr_path = os.path.join(curr_path, 'image')
	if not os.path.isdir(anpr_path):
		os.makedirs(anpr_path, exist_ok=True)

	#--------------------------------------------------
	full_path0 = os.path.join(anpr_path, 'full')
	if not os.path.isdir(full_path0):
		os.makedirs(full_path0, exist_ok=True)

	crop_path0 = os.path.join(anpr_path, 'crop')
	if not os.path.isdir(crop_path0):
		os.makedirs(crop_path0, exist_ok=True)

	log_path0 = os.path.join(curr_path, 'log')
	if not os.path.isdir(log_path0):
		os.makedirs(log_path0, exist_ok=True)

	if not os.path.isdir(vavc_dataset_path):
		os.makedirs(vavc_dataset_path, exist_ok=True)

	print("Din amier",os.path.dirname(vavc_dataset_path))

	folder_date = time.strftime("%d-%m-%Y")
	if os.path.basename(vavc_dataset_path) != folder_date:
		vavc_dataset_path = os.path.dirname(vavc_dataset_path)+"/"+folder_date
		# vavc_dataset_path = vavc_dataset_path + "/" + folder_date
		os.makedirs(vavc_dataset_path, exist_ok=True)
		config.set("host_setup", "vavc_dataset_folder", str(vavc_dataset_path))
		with open('config.ini', 'w') as configfile:
			config.write(configfile)

	
	vavc_log_path = os.path.dirname(vavc_dataset_path)+"/"+"log"
	if not os.path.isdir(vavc_log_path):
		os.makedirs(vavc_log_path, exist_ok=True)
	
	return

# Generate the xml files
def createXmlLabelFile(image_name):
	
	tree = Element('annotation')
	file_loc_split = os.path.split(image_name)

	child = SubElement(tree, 'folder')
	child.text = ''

	child = SubElement(tree, 'filename')
	child.text = file_loc_split[1]  # image name

	child = SubElement(tree, 'path')
	child.text = image_name

	child = SubElement(tree, 'source')
	child_2 = SubElement(child, 'database')
	child_2.text = 'Unknown'

	child = SubElement(tree, 'size')
	child_2 = SubElement(child, 'width')
	child_2.text = str(1280)
	child_2 = SubElement(child, 'height')
	child_2.text = str(720)
	child_2 = SubElement(child, 'depth')
	child_2.text = str(3)

	child = SubElement(tree, 'segmented')
	child.text = str(0)
	return tree


def writeXml(tree, file_name):
	ET.ElementTree(tree).write(file_name)


def addLabel(tree, bbox, class_label):
	boundingBox = bbox[:4]

	object = SubElement(tree, 'object')

	name = SubElement(object, 'name')
	name.text = class_label

	pose = SubElement(object, 'pose')
	pose.text = '0'

	difficult = SubElement(object, 'difficult')
	difficult.text = '0'

	bndBox = SubElement(object, 'bndbox')

	xmin = SubElement(bndBox, 'xmin')
	xmin.text = str(int(bbox[0]))

	ymin = SubElement(bndBox, 'ymin')
	ymin.text = str(int(bbox[1]))

	xmax = SubElement(bndBox, 'xmax')
	xmax.text = str(int(bbox[2]))

	ymax = SubElement(bndBox, 'ymax')
	ymax.text = str(int(bbox[3]))


def OBlistener(vehicle_data_queue):
	global send_to_serial, prev_ob_sensor, prev_loop_sensor, vavc_log_path

	## !!! set default prev_ob_sensor, prev_loop_sensor in main()
	## default signal 

	curr_ob_sensor = 0
	curr_loop_sensor = 0

	# to track ob/loop state changes into tracking log file
	prev_ob_state = 0
	prev_loop_state = 0
	curr_ob_state = 0
	curr_loop_state = 0

	# Pin Definitions
	Ob_signal = 40  
	Loop_signal = 35 
	
	# xavier gpio setup
	GPIO.setmode(GPIO.BOARD) 
	GPIO.setup(Ob_signal, GPIO.IN) 
	GPIO.setup(Loop_signal, GPIO.IN)   

	while input_mode == 'plaza_toll':

		## read signal from xavier
		curr_ob_sensor = GPIO.input(Ob_signal)
		curr_loop_sensor = GPIO.input(Loop_signal)
		curr_ob_state, curr_loop_state = curr_ob_sensor, curr_loop_sensor
			
		## tracking sensor OB/Loop state changes
		if (int(prev_ob_state) == 0 and int(curr_ob_state) == 1):
			prev_ob_state = curr_ob_state

			timeStamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
			vavcCsvTracker(timeStamp, vavc_log_path, 'OB : state ON trigger', '', '')
			print('OB on')
		
		if (int(prev_loop_state) == 0 and int(curr_loop_state) == 1):
			prev_loop_state = curr_loop_sensor

			timeStamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
			vavcCsvTracker(timeStamp, vavc_log_path, 'Loop : state ON trigger', '', '')
			print('Loop on')

		if (int(prev_ob_state) == 1 and int(curr_ob_state) == 0):
			prev_ob_state = curr_ob_state

			timeStamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
			vavcCsvTracker(timeStamp, vavc_log_path, 'OB : state OFF trigger', '', '')
			print('OB off')			

		if (int(prev_loop_state) == 1 and int(curr_loop_state) == 0):
			prev_loop_state = curr_loop_sensor
			print('Loop off')

			timeStamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
			vavcCsvTracker(timeStamp, vavc_log_path, 'Loop : state OFF trigger', '', '')



		## when changes from LOW to HIGH
		if (int(prev_ob_sensor) == 0 and int(curr_ob_sensor) == 1) and (int(prev_loop_sensor) == 0 and int(curr_loop_sensor) == 1):	# (no car -> has car) # vehicle entered
			print('vehicle entered\n')
			prev_ob_sensor = curr_ob_sensor
			prev_loop_sensor = curr_loop_sensor
			
			timeStamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
			vavcCsvTracker(timeStamp, vavc_log_path, 'Vehicle enter', '', '')


		## save only when vehicle exit
		## when changes from HIGH to LOW
		if (int(prev_ob_sensor) == 1 and int(curr_ob_sensor) == 0) and (int(prev_loop_sensor) == 1 and int(curr_loop_sensor) == 0):	# (no car -> has car) # vehicle entered
			print('vehicle exit\n')
			prev_ob_sensor = curr_ob_sensor
			prev_loop_sensor = curr_loop_sensor

			try:
				if not vehicle_data_queue.empty():
					vehicle_data = vehicle_data_queue.get()	
					va_class = vehicle_data[0]
					detected_single_wheel = vehicle_data[1]
					detected_double_wheel = vehicle_data[2]

					single_wheel = len(detected_single_wheel)
					double_wheel = len(detected_double_wheel)

					axle_data = single_wheel + double_wheel
					tire_data = (single_wheel*2) + (double_wheel*4) 

				else:
					print('No detection')

					va_class = '1'
					axle_data = '2'
					tire_data = '4'
	
			except:
				print('Exception')

				va_class = '1'
				axle_data = '2'
				tire_data = '4'
	
			avc_data, ipc_data = vaSendData(str(va_class), str(axle_data), str(tire_data))	
			timeStamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]

			vavcCsvTracker(timeStamp, vavc_log_path, 'Vehicle exit', avc_data, str(va_class))
			vavcCsvTracker(timeStamp, vavc_log_path, 'IPC Response', ipc_data, '')
			
			
			ack = b'\x06'		
			nak = b'\x15'		## check : which IPC data send fro NAK

			error_counter = 0
			if len(ipc_data) == 0:
		
				while error_counter < 3:
					print(f'No response from IPC, sending data again [{error_counter}]')
					vavcCsvTracker('', vavc_log_path, '', '', '')
					vavcCsvTracker('', vavc_log_path, 'No response', '', '')

					avc_data, ipc_data = vaSendData(str(va_class), str(axle_data), str(tire_data))
					error_counter = error_counter + 1

					timeStamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
					vavcCsvTracker(timeStamp, vavc_log_path, 'Send again', avc_data, str(va_class))
					vavcCsvTracker(timeStamp, vavc_log_path, 'IPC Response', ipc_data, '')


					if len(ipc_data) > 0:
						break

			if len(ipc_data) > 0 and ipc_data[1] == nak:    # check NAK index from IPC

				while error_counter < 3:
					print(f'NAK sent by IPC, sending data again [{error_counter}]')
					vavcCsvTracker('', vavc_log_path, '', '', '')
					vavcCsvTracker('', vavc_log_path, 'NAK response', '', '')

					avc_data, ipc_data = vaSendData(str(va_class), str(axle_data), str(tire_data))
					error_counter = error_counter + 1

					timeStamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
					vavcCsvTracker(timeStamp, vavc_log_path, 'Send again', avc_data, str(va_class))
					vavcCsvTracker(timeStamp, vavc_log_path, 'IPC Response', ipc_data, '')


					if ipc_data[1] != nak:	
						break


			print('Vehicle class : ', va_class, '\n')
			print("=====================================================")
			send_to_serial = False

		if progRUN is False:
			break


def saveDataset(va_data_to_xml, raw_frame):
	global image_label_num

	vavc_datetime = datetime.now()
	image_label_num = vavc_datetime.strftime("%Y%m%d_T%H%M%S-%f")[:-3]
	image_ext = '.jpg'
	xml_ext = '.xml'

	# save the xml label file
	_image_name = os.path.join(str(image_label_num) + image_ext)
	image_name = os.path.join(vavc_dataset_path, _image_name)
		
	cv2.imwrite(image_name, raw_frame)

	# save the xml label file
	va_class_label = va_data_to_xml[0]
	current_va_class_bbox = va_data_to_xml[1]
	detected_single_wheel = va_data_to_xml[2]
	detected_double_wheel = va_data_to_xml[3]
	detected_license_plate = va_data_to_xml[4]
	detected_license_plate_taxi = va_data_to_xml[5]

	tree = createXmlLabelFile(image_name)
	
	addLabel(tree, current_va_class_bbox, class_label=va_class_label)	# va_class
	
	for i in range(len(detected_single_wheel)):
		addLabel(tree, detected_single_wheel[i], class_label='singleWheel')	# single_wheel

	for i in range(len(detected_double_wheel)):
		addLabel(tree, detected_double_wheel[i], class_label='doubleWheel')	# double_wheel

	for i in range(len(detected_license_plate)):
		addLabel(tree, detected_license_plate[i], class_label='license_plate')	# license_plate

	for i in range(len(detected_license_plate_taxi)):
		addLabel(tree, detected_license_plate_taxi[i], class_label='license_plate_taxi')	# license_plate_taxi

	xml_name = os.path.join(vavc_dataset_path, str(image_label_num) + xml_ext)

	writeXml(tree, xml_name)

	return _image_name, vavc_datetime

#-------------------------------------------------------------------------------------------------------------------
#housekeeping for archieve folder

def housekeeping_dir(folder_path):
	
	all_dirs = os.listdir(folder_path)
	date_dirs = []
	for dir_name in all_dirs:
		try:
			datetime.datetime.strptime(dir_name, '%d-%m-%Y')
			date_dirs.append(dir_name)
		except ValueError:
			pass
	print('date_dirs:', len(date_dirs))
	if len(date_dirs) > 60:             # maintain image for 2 months
		sorted_dirs = sorted(date_dirs)
		index_to_delete = min(5, len(sorted_dirs)) - 1
		if index_to_delete >= 0:
			oldest_dirs = sorted_dirs[:index_to_delete+1]
			for dir_name in oldest_dirs:
				dir_path = os.path.join(folder_path, dir_name)
				try:
					# Get a list of all files and directories inside the directory
					dir_contents = os.listdir(dir_path)
					for item in dir_contents:
						item_path = os.path.join(dir_path, item)
						if os.path.isdir(item_path):
							# Recursively delete any subdirectories
							os.system(f'rm -r "{item_path}"')
						else:
							# Delete any files
							os.remove(item_path)
					# Delete the directory itself
					os.rmdir(dir_path)
					print(f"Directory {dir_path} deleted.")
				except OSError as e:
					print(f"Error deleting directory {dir_path}: {e}")
		else:
			print("No directories to delete.")
	else:
		print(f'No deletion. Directory is only have {len(date_dirs)}')


#==================================================
if __name__ == "__main__":
#--------------------------------------------------
	print("==================================================")

	#input_buf0 = queue.Queue()
	detect_buf0 = queue.Queue()
	detectFlag0 = False
	preview_buf0 = queue.Queue()
	crop_buf0 = queue.Queue()
	plate_buf0 = queue.Queue()
	vehicle_data_queue = queue.Queue()
	anpr_queue0 = collections.deque([], 5)
	anpr_data0 = []
	plate_buf_list0 = []
	prev_ob_sensor = 0
	prev_loop_sensor = 0
	
	#####
	curr_payment_data = []
	#####

	# constant variable
	img_formats = ['.bmp', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.dng']
	vid_formats = ['.mov', '.avi', '.mp4', '.mpg', '.mpeg', '.m4v', '.wmv', '.mkv']
	w_std = 1280  # standard frame size to optimize calculate time taken (torch=640, stride=32)
	h_std = 768
	w_min = 640
	h_min = 480
	padding = 5  # preview padding
	root = tk.Tk()
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	root.destroy()
	print(f"screen_width={screen_width}, screen_height={screen_height}")
	windowScale = 2.5

	# variable
	progRUN = True
	today_date = ''
	maxthread = 0
	detection_ROI = []
	dt = ''
	mx1 = 0; my1 = 0; mx2 = 0; my2 = 0; mx3 = 0; my3 = 0; mx4 = 0; my4 = 0
	flagPoint = 0
	flagROI = 0
	email_to = []

#--------------------------------------------------
	config = ConfigParser()
	if os.path.isfile('./config.ini'):
		print(f"{__file__}  READ FILE: config.ini.")
		config.read('./config.ini')
	else:
		if os.path.isfile('./setting.ini'):
			print(f"{__file__}  READ FILE: setting.ini.")
			config.read('./setting.ini')
		else:
			print("ERROR: config.ini or setting.ini file not found.")
			sys.exit(0)

	# Load host setup
	host_IP = config.get('host_setup', 'host_IP')
	if host_IP=='local':
		host_IP = socket.gethostbyname_ex(socket.gethostname() + ".local")[-1][-1]
	host_port = config.getint('host_setup', 'host_port')
	print(f"[Host Setup] IP: {host_IP},  Port: {host_port}.")
	vavc_dataset_path = config.get('host_setup', 'vavc_dataset_folder')

	# Load input mode
	input_mode = config.get('src_mode', 'input_mode')
	
	if input_mode == 'plaza_toll':
		from RS232_comm_v4 import src as vaSendData


	# Load camera id
	# for image
	cam_ID = config.get('src_id', 'input_id')
	src_fullpath = config.get('src_input','input_src')
	print(f"[Image Source] CAM_ID: {cam_ID},  Link: {src_fullpath}.")
	# for video0
	cam_ID0 = config.get('src_id', 'input_id0')
	src_fullpath0 = config.get('src_input','input_src0')
	anpr0_enable = config.getboolean('src_input','input_anpr0')
	anpr_vavc0 = config.get('src_input','input_anpr_vavc0')
	print(f"[Camera Source] CAM_ID0: {cam_ID0},  Link: {src_fullpath0},  ANPR Enable: {anpr0_enable}, ANPR/VAVC: {anpr_vavc0}.")


	# Load detection ROI
	# for video0
	acceptable_bounding_box_area = [235, 150, 2000, 1508]
	saved_bbox_value = config.get('roi','vavc_save_dataset')

	detection_ROI.append(json.loads(config.get('roi', 'ROI_input0')))
	print(f"[CAM_ID0 ROI] polygon: {detection_ROI[0]}.")
	imgROI0 = np.zeros((h_std, w_std, 1), dtype=np.uint8)
	[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[0], np.int32).copy()
	if x1>=x2 or x4>=x1 or y2>=y3 or y1>=y4:
		print("ERROR: setting.ini [roi] ROI_Input0 [[x1,y1], [x2,y3], [x3,y3], [x4,y4]] condition x2>x1, x3>x4, y3>y2 and y4>y1.")
	if x3<x2 and x4<=x1:
		polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x4, y4]], np.int32).copy()
	elif x3>=x2 and x4>x1:
		polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x1, y2]], np.int32).copy()
	elif x3>=x2 and x4<=x1:
		polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x4, y4]], np.int32).copy()
	elif x3<x2 and x4>x1:
		polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x1, y2]], np.int32).copy()
	cv2.fillPoly(imgROI0, [polygon], color=255)

	# Directory
	pathUpdate()
	# Load weight model
	set_logging()
	device = select_device('0')
	#device = select_device('cpu')
	half = device.type != 'cpu'  # half precision only supported on CUDA
	# Load model plate detection
	existing_weights_detection = ''
	existing_weights_detection = weights_detectionUpdate(device, existing_weights_detection)
	# Load model plate recognize
	existing_weights_recognize = ''
	existing_weights_recognize = weights_recognizeUpdate(device, existing_weights_recognize)
	# Load model video analytic vehicle classification
	existing_weights_vavc = ''
	existing_weights_vavc = weights_vavcUpdate(device, existing_weights_vavc)

	print('==================================================')
	print("Video Detection Start.")
	capThread0 = capThread(cam_ID0, src_fullpath0)
	showThread = showThread()
	OBListenerThread0 = OBListenerThread(vehicle_data_queue)

	print(f"Active threads: {threading.activeCount()}.")
	print('Thread start.')
	capThread0.start()
	showThread.start()
	OBListenerThread0.start()
	print(f"Active threads: {threading.activeCount()}.")

	anprCount0 = 0
	anprCapture0 = False
	recogniteFlag0 = False
	dataset_saved = False	# flag, save to dataset.. 
	send_to_serial = False
	RUN = True
	while RUN:
		if today_date != datetime.now().strftime("%Y%m%d"):
			pathUpdate()

		if maxthread < threading.activeCount():
			maxthread = threading.activeCount()
		if progRUN is False:
			print("Thread stop.")
			capThread0.join()
			showThread.join()
			OBListenerThread0.join()
			print(f"Active threads (main): {threading.activeCount()}.")
			RUN = False
			break
		time.sleep(0.001)

		#--------------------------------------------------
		if detectFlag0 is True:

			detection_t0 = time.time()
			det_t0 = datetime.now().strftime('%H:%M:%S.%f')[:-3]
			detect_img0 = detect_buf0.get().copy()
			detect_img0raw = detect_img0.copy()

			if anpr_vavc0 == 'VAVC':
				#t_start = time.time()
				crop_img0, current_prediction, current_va_class_bbox, detected_single_wheel, detected_double_wheel, detected_license_plate, detected_license_plate_taxi = VAVC.vehicleDetection(model_vavc, half, device, detect_img0, acceptable_bounding_box_area) 
				#t_end = time.time()
				#print(f'Time VAVC : {t_end-t_start}')

				if current_va_class_bbox is not None:
					crop_img0 = cv2.line(crop_img0, (current_va_class_bbox[0], 0), (current_va_class_bbox[0], 720), (0,0,255), 2)

				crop_img0 = cv2.line(crop_img0, (int(saved_bbox_value), 0), (int(saved_bbox_value), 720), (0,255,0), 2)

				plate_conf0 = ''
				#detected_frame0, predicted_vehicle_data0, crop_img0, plate_conf0 = VAVC.vehicleDetection(model_vavc, half, device, detect_img0, imgROI0)
				#print(f'detected_vehicle_class: {detected_vehicle_class}')
				

				if dataset_saved is False and send_to_serial is False:	# if dataset not yet saved, save dataset and raise flag (preventing for always, non-stop save)
					if (current_prediction is not "no_detection"):	
						if current_va_class_bbox[0] < int(saved_bbox_value):
				
							va_data_to_xml = []			# append data needed by xml
							va_data_to_xml.append(current_prediction)
							va_data_to_xml.append(current_va_class_bbox)
							va_data_to_xml.append(detected_single_wheel)
							va_data_to_xml.append(detected_double_wheel)
							va_data_to_xml.append(detected_license_plate)
							va_data_to_xml.append(detected_license_plate_taxi)


							vavc_image_name, vavc_datetime = saveDataset(va_data_to_xml, detect_img0raw)
							dataset_saved = True
							print('Dataset saved')
							vavc_datetime = vavc_datetime.strftime("%d-%m-%y.T%H:%M:%S.%f")[:-3]
							va_class = vehicle_class_name_to_numeric[current_prediction]
							vavcCsvLogger(vavc_datetime, cam_ID, vavc_log_path, va_class, vavc_image_name)

							timeStamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
							vavcCsvTracker('', vavc_log_path, '', '', '')
							vavcCsvTracker(timeStamp, vavc_log_path, 'Dataset saved (Vehicle at payment)', '', '')
	
							if input_mode == 'plaza_toll':
								va_data_to_serial = []			# append all data needed by RS232
								va_data_to_serial.append(va_class)
								va_data_to_serial.append(detected_single_wheel)
								va_data_to_serial.append(detected_double_wheel)

								#print('va_class : ', va_class, '\n')
								print('Detecteed : ', va_class, '\n')			
								if not vehicle_data_queue.empty():		# update vehicle_data_queue 
									vehicle_data_queue.get()
									vehicle_data_queue.put_nowait(va_data_to_serial)
								else:
									vehicle_data_queue.put_nowait(va_data_to_serial)

								send_to_serial = True
							

				if dataset_saved is True and current_va_class_bbox is not None and (current_va_class_bbox[0] > int(saved_bbox_value)):
					dataset_saved = False
			else:
				crop_img0, plate_conf0 = ANPR.runPlateDetection(model_detection, half, device, detect_img0, imgROI0)

			if not preview_buf0.empty():
				preview_buf0.get()
			preview_buf0.put(detect_img0)

			if not crop_buf0.empty():
				crop_buf0.get()
			crop_buf0.put([cam_ID0, detect_img0raw, crop_img0, plate_conf0])

			detectFlag0 = False
			recogniteFlag0 = True

	
	print("==================================================")
	print("Program END.")
	cv2.destroyAllWindows()
	print(f"Final Active threads (main): {threading.activeCount()}.")

#==================================================
# END
