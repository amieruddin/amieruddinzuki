#==================================================
#===== MAIN PROGRAM - main
# main8v? anpr_r? csvlogger_r? vavc_r?
#==================================================

#==================================================
#===== yolov5 reference 
# https://github.com/ultralytics/yolov5
# Python>=3.8.0 is required with all requirements.txt installed including PyTorch>=1.12:
#==================================================

#==================================================
#===== Install CUDA 11.6 Toolkit to Windows10/Linux
#https://developer.nvidia.com/cuda-11-6-1-download-archive
#==================================================

#==================================================
#!!!!! Install yolov5 with TensorRT need to refer install.txt
#!!!!! model file .pt need to use export to convert it to .engine
#!!!!! yaml data file in folder Data
#==================================================

#==================================================
#===== Uninstall all packages (if required)
#pip freeze > packages.txt && pip uninstall -y -r packages.txt && del packages.txt
#pip cache purge
#===== Conda environment: pip install torch, torchvision with cuda 11.6
#pip install torch==1.12.1+cu116 torchvision==0.13.1+cu116 --extra-index-url https://download.pytorch.org/whl/cu116
#===== Verify install ok
#python
#import torch
#torch.cuda.is_available()
#===== Install packages refer to the file requirement.txt
# modify requirements.txt on line below to add +cu116
#-- torch>=1.7.0+cu116
#-- torchvision>=0.8.1+cu116
#-- opencv-python>=4.1.2 downgrade to opencv-python>=4.1.0.25 (linux only)
#pip install -r requirements.txt
#===== Install addition packages
#pip install openpyxl flask waitress
#pip install tk
#pip install pywhatkit
#pip install cryptography
#pip install pyinstaller
#==================================================
#===== build anpr1.exe (windows)
#pyinstaller --name anpr1 --onedir --icon=anpr.ico main1v6t4.py
#===== build anpr1 (linux)
#pyinstaller --name anpr1 --onedir main1v6t4.py
#===== copy folder [dist/anpr1, trained_models, utils] to new folder, copy file [setting.ini / config.ini] to new folder, rename [utils/torch_utils.py to utils/torch_utils.pyc]
#===== build generator
#pyinstaller --onefile generator.py
#===== copy generator(.exe) to new folder
#===== new folder as Master can copy to other PC (with requirements installed) and generate license key before run
#===== generator(.exe) to create dongle.key in new folder on the run-PC)
#==================================================

#==================================================
# HISTORY
#==================================================
# 1. image standard size 1280x768 for yolov5 (accepted camera input size 640x480)
#===== 20/9/2021
# 1. modify to 2 cameras
# 2. threading on capture x2, preview x1, flask x1
# 3. add flask
# 4. modify datalogger
#===== 6/10/2021
# 1. input mode none, basename error
# 2. open log anpr write error
#===== 7/10/2021
# 1. modify to 1 cam
# 2. arrange flow of flask on request, responce, datalogger format
# 3. save image to unrecognize if conf<0.8 and pass ROI
#===== 1/11/2021
# 1. restructure program
#===== 8/11/2021
# 1. model renew without stop program
# 2. filename requirement
#===== 22/11/2021
# 1. request to change 2 request OB and RFID/TnG, need restructure due to time very short
#===== 22/11/2021
# 1. 2 cameras
#===== 3/12/2021
# 1. 4 cameras
#===== 28/12/2021
# 1. add camera status
# 2. add model update
# 3. change image id
# 4. change directory structure
# 5. add response va/status (image id, trained model)
# 6. modify sensor 1=OB 0=payment
# 7. change ABC1234 to ''
# 8. enable/disable anpr vavc
# 9. camera failure alert (email)
# 10. 2nd request (0=payment) to send previous data (1=OB)
# 11. dongle key
# 12. software life
# 13. exe/linux distribute
#===== 28/2/2022
# 1. 8 cameras
#===== 10/3/2022
# 1. car move-in/out saturation
#===== 11/8/2022
# 1. 100fps
# 2. increase speed
# 3. tensorRT
#==================================================
# PENDING
#==================================================
# 1. trained models protection
#==================================================

#==================================================
#main8 v7.5		-	4/11/2022
# 1. for LPT - lane Quatriz/tngo
# - i.	  detection based on ROI --> result and img need to save in temporary memory
# - ii.   sensor 0 @ payment get reseult based on detection --> save image, clear memory
# - iii.  sensor 2 --> clear memory
# 2. update list of vanity plate in anpr_r2.pt & anpr_r2.engine



CAMERA_FPS = 50 #30
PROCESS_FPS = 30 #240
SKIP_DET = False
DROP_FRAME = True
PRINT_DROP_FRAME = False
DEBUG_PRINT_FRAME_COUNT = False
ENABLE_DEBUG_PRINT = False
ENABLE_PRINT_INFERENCE = True
SHOW_PREVIEW_SLEEP = 0.04  # manual calculate: 50fps
DATA_YAML = './data/lpd_delloyd.yaml'
DATA_YAML_CR = './data/cr_delloyd.yaml'
DATA_YAML_plate_grading = './data/plate_grading_delloyd.yaml'
TSRT = True  # use TensorRT (.engine)

PRINT_TIME = False
PRINT_DETECTION_PLATE_MODE_OFFLINE = True
PRINT_CONFIDENCE = False

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

def hash_md5():
	md5 = 0
	if os.path.exists('__file__'):
		with open(__file__, 'rb') as f:
			hashmd5 = hashlib.md5()
			for chunk in iter(lambda: f.read(4096), b''):
				hashmd5.update(chunk)
			md5 = hashmd5.hexdigest()
			print(f"Copyright Software. {__file__}-{md5}")
	elif os.path.exists(sys.argv[0]):
		with open(sys.argv[0], 'rb') as f:
			hashmd5 = hashlib.md5()
			for chunk in iter(lambda: f.read(4096), b''):
				hashmd5.update(chunk)
			md5 = hashmd5.hexdigest()
			print(f"Copyright Software. {sys.argv[0]}-{md5}")
	elif os.path.exists(sys.executable):
		with open(sys.executable, 'rb') as f:
			hashmd5 = hashlib.md5()
			for chunk in iter(lambda: f.read(4096), b''):
				hashmd5.update(chunk)
			md5 = hashmd5.hexdigest()
			print(f"Copyright Software. {sys.executable}-{md5}")
	else:
		print(f"Copyright Software, filename/checksum error.")
		sys.exit(0)

#==================================================
from base64 import encode
from email.encoders import encode_base64
import sys
import os
from datetime import datetime, date
import subprocess
import uuid
from cryptography.fernet import Fernet
dongle()
import hashlib
hash_md5()

import cv2
import numpy as np
if(TSRT):
	import anpr_r2_engine as ANPR
	print("ANPR use model .engine")
else:
	import anpr_r2_pt as ANPR
	print("ANPR use model .pt")
import vavc_r1 as VAVC
import threading
import queue
import time
import tkinter as tk
import collections

import json
from configparser import ConfigParser
from csvlogger_r1 import checkDetection, csvLogger

import socket
from flask import Flask, request, jsonify
import requests
from waitress import serve
import smtplib
#import pywhatkit

import torch
import pandas as pd
from utils.torch_utils import select_device, time_sync
from models.experimental import attempt_load
from utils.general import set_logging, check_img_size, non_max_suppression, scale_coords, xyxy2xywh
from numpy import random
from utils.plots import Annotator

import tensorrt as trt  # https://developer.nvidia.com/nvidia-tensorrt-download
from models.common import YoloTRT
from collections import OrderedDict, namedtuple

#for based32
from numpy import chararray, int64

#for vavc save xml
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
import shutil
import csv

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

#--------------------------------------------------
def capCapture(camID, captureName):
	global progRUN, progStop, pause
	global filename0, detectFlag0, NoSignalCam0
	global filename1, detectFlag1, NoSignalCam1
	global filename2, detectFlag2, NoSignalCam2
	global filename3, detectFlag3, NoSignalCam3
	global filename4, detectFlag4, NoSignalCam4
	global filename5, detectFlag5, NoSignalCam5
	global filename6, detectFlag6, NoSignalCam6
	global filename7, detectFlag7, NoSignalCam7
	global cameraFPS
	progStop = False
	pause = False

	# local variable
	cam0STOP = False
	cam1STOP = False
	cam2STOP = False
	cam3STOP = False
	cam4STOP = False
	cam5STOP = False
	cam6STOP = False
	cam7STOP = False
	n_cam = [0, 0, 0, 0, 0, 0, 0, 0]
	NoSignalCam0 = False
	NoSignalCam1 = False
	NoSignalCam2 = False
	NoSignalCam3 = False
	NoSignalCam4 = False
	NoSignalCam5 = False
	NoSignalCam6 = False
	NoSignalCam7 = False

	fps_frequency = 1/cameraFPS
	thread_sleep = fps_frequency/2
	drop_frame = cameraFPS/PROCESS_FPS
	if(drop_frame < 0):
		drop_frame = 0
	frameCount = drop_frame + 1
	print(f"Camera [{camID}] frame rate:{fps_frequency:.3f}s, thread sleep:{thread_sleep:.3f}s")
	print(f"drop frame count: {drop_frame}")

	while not cam0STOP and not cam1STOP and not cam2STOP and not cam3STOP and not cam4STOP and not cam5STOP and not cam6STOP and not cam7STOP:

		if progStop:
			cam0STOP = True
			cam1STOP = True
			cam2STOP = True
			cam3STOP = True
			cam4STOP = True
			cam5STOP = True
			cam6STOP = True
			cam7STOP = True
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
			if camID==cam_ID1:
				if(n_cam[1]==len(os.listdir(captureName))):
					time.sleep(0.01)
					continue
				filename1 = os.listdir(captureName)[n_cam[1]]
				if not os.path.splitext(filename1)[-1].lower() in vid_formats:
					n_cam[1] += 1
					time.sleep(0.01)
					continue
				full_filename = os.path.join(captureName, filename1)
				n_cam[1] += 1
			if camID==cam_ID2:
				if(n_cam[2]==len(os.listdir(captureName))):
					time.sleep(0.01)
					continue
				filename2 = os.listdir(captureName)[n_cam[2]]
				if not os.path.splitext(filename2)[-1].lower() in vid_formats:
					n_cam[2] += 1
					time.sleep(0.01)
					continue
				full_filename = os.path.join(captureName, filename2)
				n_cam[2] += 1
			if camID==cam_ID3:
				if(n_cam[3]==len(os.listdir(captureName))):
					time.sleep(0.01)
					continue
				filename3 = os.listdir(captureName)[n_cam[3]]
				if not os.path.splitext(filename3)[-1].lower() in vid_formats:
					n_cam[3] += 1
					time.sleep(0.01)
					continue
				full_filename = os.path.join(captureName, filename3)
				n_cam[3] += 1
			if camID==cam_ID4:
				if(n_cam[4]==len(os.listdir(captureName))):
					time.sleep(0.01)
					continue
				filename4 = os.listdir(captureName)[n_cam[4]]
				if not os.path.splitext(filename4)[-1].lower() in vid_formats:
					n_cam[4] += 1
					time.sleep(0.01)
					continue
				full_filename = os.path.join(captureName, filename4)
				n_cam[4] += 1
			if camID==cam_ID5:
				if(n_cam[5]==len(os.listdir(captureName))):
					time.sleep(0.01)
					continue
				filename5 = os.listdir(captureName)[n_cam[5]]
				if not os.path.splitext(filename5)[-1].lower() in vid_formats:
					n_cam[5] += 1
					time.sleep(0.01)
					continue
				full_filename = os.path.join(captureName, filename5)
				n_cam[5] += 1
			if camID==cam_ID6:
				if(n_cam[6]==len(os.listdir(captureName))):
					time.sleep(0.01)
					continue
				filename6 = os.listdir(captureName)[n_cam[6]]
				if not os.path.splitext(filename6)[-1].lower() in vid_formats:
					n_cam[6] += 1
					time.sleep(0.01)
					continue
				full_filename = os.path.join(captureName, filename6)
				n_cam[6] += 1
			if camID==cam_ID7:
				if(n_cam[7]==len(os.listdir(captureName))):
					time.sleep(0.01)
					continue
				filename7 = os.listdir(captureName)[n_cam[7]]
				if not os.path.splitext(filename7)[-1].lower() in vid_formats:
					n_cam[7] += 1
					time.sleep(0.01)
					continue
				full_filename = os.path.join(captureName, filename7)
				n_cam[7] += 1
		elif os.path.isfile(captureName):  # video file
			if camID==cam_ID0:
				filename0 = captureName
				if not os.path.splitext(filename0)[-1].lower() in vid_formats:
					cam0STOP = True
					break
				full_filename = os.path.abspath(filename0)
			if camID==cam_ID1:
				filename1 = captureName
				if not os.path.splitext(filename1)[-1].lower() in vid_formats:
					cam1STOP = True
					break
				full_filename = os.path.abspath(filename1)
			if camID==cam_ID2:
				filename2 = captureName
				if not os.path.splitext(filename2)[-1].lower() in vid_formats:
					cam2STOP = True
					break
				full_filename = os.path.abspath(filename2)
			if camID==cam_ID3:
				filename3 = captureName
				if not os.path.splitext(filename3)[-1].lower() in vid_formats:
					cam3STOP = True
					break
				full_filename = os.path.abspath(filename3)
			if camID==cam_ID4:
				filename4 = captureName
				if not os.path.splitext(filename4)[-1].lower() in vid_formats:
					cam4STOP = True
					break
				full_filename = os.path.abspath(filename4)
			if camID==cam_ID5:
				filename5 = captureName
				if not os.path.splitext(filename5)[-1].lower() in vid_formats:
					cam5STOP = True
					break
				full_filename = os.path.abspath(filename5)
			if camID==cam_ID6:
				filename6 = captureName
				if not os.path.splitext(filename6)[-1].lower() in vid_formats:
					cam6STOP = True
					break
				full_filename = os.path.abspath(filename6)
			if camID==cam_ID7:
				filename7 = captureName
				if not os.path.splitext(filename7)[-1].lower() in vid_formats:
					cam7STOP = True
					break
				full_filename = os.path.abspath(filename7)
		else:  # webcam
			if camID==cam_ID0:
				filename0 = captureName
				full_filename = filename0
			if camID==cam_ID1:
				filename1 = captureName
				full_filename = filename1
			if camID==cam_ID2:
				filename2 = captureName
				full_filename = filename2
			if camID==cam_ID3:
				filename3 = captureName
				full_filename = filename3
			if camID==cam_ID4:
				filename4 = captureName
				full_filename = filename4
			if camID==cam_ID5:
				filename5 = captureName
				full_filename = filename5
			if camID==cam_ID6:
				filename6 = captureName
				full_filename = filename6
			if camID==cam_ID7:
				filename7 = captureName
				full_filename = filename7

		#print(f"CAMERA Starting: {camID}, {full_filename}.")
		try:
			#cap = cv2.VideoCapture(full_filename)
			cap = cv2.VideoCapture(eval(full_filename) if full_filename.isnumeric() else full_filename)
		except cv2.error as e:
			print("ERROR: Input Source cannot open, {e}.")
			if camID==cam_ID0:
				cam0STOP = True
			if camID==cam_ID1:
				cam1STOP = True
			if camID==cam_ID2:
				cam2STOP = True
			if camID==cam_ID3:
				cam3STOP = True
			if camID==cam_ID4:
				cam4STOP = True
			if camID==cam_ID5:
				cam5STOP = True
			if camID==cam_ID6:
				cam6STOP = True
			if camID==cam_ID7:
				cam7STOP = True
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
				if camID==cam_ID1 and NoSignalCam1==False:
					NoSignalCam1 = True
					print(f"Camera [{camID}] No Signal: {NoSignalCam1}")
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
				if camID==cam_ID2 and NoSignalCam2==False:
					NoSignalCam2 = True
					print(f"Camera [{camID}] No Signal: {NoSignalCam2}")
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
				if camID==cam_ID3 and NoSignalCam3==False:
					NoSignalCam3 = True
					print(f"Camera [{camID}] No Signal: {NoSignalCam3}")
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
				if camID==cam_ID4 and NoSignalCam4==False:
					NoSignalCam4 = True
					print(f"Camera [{camID}] No Signal: {NoSignalCam4}")
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
				if camID==cam_ID5 and NoSignalCam5==False:
					NoSignalCam5 = True
					print(f"Camera [{camID}] No Signal: {NoSignalCam5}")
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
				if camID==cam_ID6 and NoSignalCam6==False:
					NoSignalCam6 = True
					print(f"Camera [{camID}] No Signal: {NoSignalCam6}")
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
				if camID==cam_ID7 and NoSignalCam7==False:
					NoSignalCam7 = True
					print(f"Camera [{camID}] No Signal: {NoSignalCam7}")
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
		if camID==cam_ID1:
			NoSignalCam1 = False
		if camID==cam_ID2:
			NoSignalCam2 = False
		if camID==cam_ID3:
			NoSignalCam3 = False
		if camID==cam_ID4:
			NoSignalCam4 = False
		if camID==cam_ID5:
			NoSignalCam5 = False
		if camID==cam_ID6:
			NoSignalCam6 = False
		if camID==cam_ID7:
			NoSignalCam7 = False

		timeStart = time.time() #init
		frame_count=0
		while cap.isOpened():
			if(ENABLE_DEBUG_PRINT):
				capture_t0 = time.time()
				cap_t0 = datetime.now().strftime('%H:%M:%S.%f')[:-3]
			#--------------------------------------------------
			if os.path.isfile(full_filename):
				if((time.time() - timeStart) < fps_frequency):
					time.sleep(thread_sleep)
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
					if camID==cam_ID1:
						prev_capF1 = capF
					if camID==cam_ID2:
						prev_capF2 = capF
					if camID==cam_ID3:
						prev_capF3 = capF
					if camID==cam_ID4:
						prev_capF4 = capF
					if camID==cam_ID5:
						prev_capF5 = capF
					if camID==cam_ID6:
						prev_capF6 = capF
					if camID==cam_ID7:
						prev_capF7 = capF
				else:
					if camID==cam_ID0:
						capF = prev_capF0
					if camID==cam_ID1:
						capF = prev_capF1
					if camID==cam_ID2:
						capF = prev_capF2
					if camID==cam_ID3:
						capF = prev_capF3
					if camID==cam_ID4:
						capF = prev_capF4
					if camID==cam_ID5:
						capF = prev_capF5
					if camID==cam_ID6:
						capF = prev_capF6
					if camID==cam_ID7:
						capF = prev_capF7

				if(DEBUG_PRINT_FRAME_COUNT):
					frame_count = frame_count + 1
					if(frame_count%100 == 0):
						print(f"CH:{camID}: FrameCount:{frame_count}, \tTime: {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")

				if(DROP_FRAME == True):
					if(frameCount < drop_frame):
						frameCount = frameCount + 1
						if(PRINT_DROP_FRAME):
							print(f"Dropping frame: {frameCount}")
						continue;
					else:
						frameCount = 0
			
				if(ENABLE_DEBUG_PRINT):
					capture_t1 = time.time()

				if (0):
					capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
					h_capF, w_capF = capF.shape[:2]
					top = bottom = int(abs(h_std - h_capF) / 2)
					left = right = int(abs(w_std - w_capF) / 2)
					capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border

				flag_resize=0
				if camID==cam_ID0:
#					if not input_buf0.empty():
#						input_buf0.get()
#					input_buf0.put(capF)  # for preview
					if input_buf0.empty():
						capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
						h_capF, w_capF = capF.shape[:2]
						top = bottom = int(abs(h_std - h_capF) / 2)
						left = right = int(abs(w_std - w_capF) / 2)
						capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						input_buf0.put(capF)  # for preview
						flag_resize=1
#					if detectFlag0 is False:
#						if not detect_buf0.empty():
#							detect_buf0.get()
#						detect_buf0.put(capF)  # for detect
					if (len(detect_buf0) == 0):
						if not flag_resize:
							capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
							h_capF, w_capF = capF.shape[:2]
							top = bottom = int(abs(h_std - h_capF) / 2)
							left = right = int(abs(w_std - w_capF) / 2)
							capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						#resize for detection
						if(TSRT):
							# stride = max(int(model_detection.stride), stride=32)  # model stride=32
							stride = 32
						else:
							stride = 32  # model stride=32
						imgsz = [640, 640]
						imgsz = check_img_size(imgsz, s=stride)  # check image size
						capF_resize = ANPR.letterbox(capF, imgsz, stride=stride, auto=False)[0]            #0.0004 - 0.0006
						capF_resize = capF_resize[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
						capF_resize = np.ascontiguousarray(capF_resize)
						## testing code
						capF_resize = torch.from_numpy(capF_resize)
						capF_resize = capF_resize.half() if half else capF_resize.float()  # uint8 to fp16/32
						capF_resize = capF_resize.to(device)
						capF_resize /= 255.0  # 0~255 to 0.0~1.0
						if capF_resize.ndimension() == 3:
							capF_resize = capF_resize.unsqueeze(0)
						detect_buf0.appendleft(capF_resize)  # for detect
						detect_buf0.appendleft(capF)  # for detect
						detectFlag0 = True

				flag_resize=0
				if camID==cam_ID1:
#					if not input_buf1.empty():
#						input_buf1.get()
#					input_buf1.put(capF)  # for preview
					if input_buf1.empty():
						capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
						h_capF, w_capF = capF.shape[:2]
						top = bottom = int(abs(h_std - h_capF) / 2)
						left = right = int(abs(w_std - w_capF) / 2)
						capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						input_buf1.put(capF)  # for preview
						flag_resize=1
#					if detectFlag1 is False:
#						if not detect_buf1.empty():
#							detect_buf1.get()
#						detect_buf1.put(capF)  # for detect
					if (len(detect_buf1) == 0):
						if not flag_resize:
							capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
							h_capF, w_capF = capF.shape[:2]
							top = bottom = int(abs(h_std - h_capF) / 2)
							left = right = int(abs(w_std - w_capF) / 2)
							capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						#resize for detection
						if(TSRT):
							# stride = max(int(model_detection.stride), 32)  # model stride=32
							stride = 32
						else:
							stride = 32  # model stride=32
						imgsz = [640, 640]
						imgsz = check_img_size(imgsz, s=stride)  # check image size
						capF_resize = ANPR.letterbox(capF, imgsz, stride=stride, auto=False)[0]            #0.0004 - 0.0006
						capF_resize = capF_resize[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
						capF_resize = np.ascontiguousarray(capF_resize)
						## testing code
						capF_resize = torch.from_numpy(capF_resize)
						capF_resize = capF_resize.half() if half else capF_resize.float()  # uint8 to fp16/32
						capF_resize = capF_resize.to(device)
						capF_resize /= 255.0  # 0~255 to 0.0~1.0
						if capF_resize.ndimension() == 3:
							capF_resize = capF_resize.unsqueeze(0)
						detect_buf1.appendleft(capF_resize)  # for detect
						detect_buf1.appendleft(capF)  # for detect
						detectFlag1 = True

				flag_resize=0
				if camID==cam_ID2:
#					if not input_buf2.empty():
#						input_buf2.get()
#					input_buf2.put(capF)  # for preview
					if input_buf2.empty():
						capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
						h_capF, w_capF = capF.shape[:2]
						top = bottom = int(abs(h_std - h_capF) / 2)
						left = right = int(abs(w_std - w_capF) / 2)
						capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						input_buf2.put(capF)  # for preview
						flag_resize=1
#					if detectFlag2 is False:
#						if not detect_buf2.empty():
#							detect_buf2.get()
#						detect_buf2.put(capF)  # for detect
					if (len(detect_buf2) == 0):
						if not flag_resize:
							capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
							h_capF, w_capF = capF.shape[:2]
							top = bottom = int(abs(h_std - h_capF) / 2)
							left = right = int(abs(w_std - w_capF) / 2)
							capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						#resize for detection
						if(TSRT):
							# stride = max(int(model_detection.stride), 32)  # model stride=32
							stride = 32
						else:
							stride = 32  # model stride=32
						imgsz = [640, 640]
						imgsz = check_img_size(imgsz, s=stride)  # check image size
						capF_resize = ANPR.letterbox(capF, imgsz, stride=stride, auto=False)[0]            #0.0004 - 0.0006
						capF_resize = capF_resize[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
						capF_resize = np.ascontiguousarray(capF_resize)
						## testing code
						capF_resize = torch.from_numpy(capF_resize)
						capF_resize = capF_resize.half() if half else capF_resize.float()  # uint8 to fp16/32
						capF_resize = capF_resize.to(device)
						capF_resize /= 255.0  # 0~255 to 0.0~1.0
						if capF_resize.ndimension() == 3:
							capF_resize = capF_resize.unsqueeze(0)
						detect_buf2.appendleft(capF_resize)  # for detect
						detect_buf2.appendleft(capF)  # for detect
						detectFlag2 = True

				flag_resize=0
				if camID==cam_ID3:
#					if not input_buf3.empty():
#						input_buf3.get()
#					input_buf3.put(capF)  # for preview
					if input_buf3.empty():
						capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
						h_capF, w_capF = capF.shape[:2]
						top = bottom = int(abs(h_std - h_capF) / 2)
						left = right = int(abs(w_std - w_capF) / 2)
						capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						input_buf3.put(capF)  # for preview
						flag_resize=1
#					if detectFlag3 is False:
#						if not detect_buf3.empty():
#							detect_buf3.get()
#						detect_buf3.put(capF)  # for detect
					if (len(detect_buf3) == 0):
						if not flag_resize:
							capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
							h_capF, w_capF = capF.shape[:2]
							top = bottom = int(abs(h_std - h_capF) / 2)
							left = right = int(abs(w_std - w_capF) / 2)
							capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						#resize for detection
						if(TSRT):
							# stride = max(int(model_detection.stride), 32)  # model stride=32
							stride = 32
						else:
							stride = 32  # model stride=32
						imgsz = [640, 640]
						imgsz = check_img_size(imgsz, s=stride)  # check image size
						capF_resize = ANPR.letterbox(capF, imgsz, stride=stride, auto=False)[0]            #0.0004 - 0.0006
						capF_resize = capF_resize[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
						capF_resize = np.ascontiguousarray(capF_resize)
						## testing code
						capF_resize = torch.from_numpy(capF_resize)
						capF_resize = capF_resize.half() if half else capF_resize.float()  # uint8 to fp16/32
						capF_resize = capF_resize.to(device)
						capF_resize /= 255.0  # 0~255 to 0.0~1.0
						if capF_resize.ndimension() == 3:
							capF_resize = capF_resize.unsqueeze(0)
						detect_buf3.appendleft(capF_resize)  # for detect
						detect_buf3.appendleft(capF)  # for detect
						detectFlag3 = True

				flag_resize=0
				if camID==cam_ID4:
#					if not input_buf4.empty():
#						input_buf4.get()
#					input_buf4.put(capF)  # for preview
					if input_buf4.empty():
						capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
						h_capF, w_capF = capF.shape[:2]
						top = bottom = int(abs(h_std - h_capF) / 2)
						left = right = int(abs(w_std - w_capF) / 2)
						capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						input_buf4.put(capF)  # for preview
						flag_resize=1
#					if detectFlag4 is False:
#						if not detect_buf4.empty():
#							detect_buf4.get()
#						detect_buf4.put(capF)  # for detect
					if (len(detect_buf4) == 0):
						if not flag_resize:
							capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
							h_capF, w_capF = capF.shape[:2]
							top = bottom = int(abs(h_std - h_capF) / 2)
							left = right = int(abs(w_std - w_capF) / 2)
							capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						#resize for detection
						if(TSRT):
							# stride = max(int(model_detection.stride), 32)  # model stride=32
							stride = 32
						else:
							stride = 32  # model stride=32
						imgsz = [640, 640]
						imgsz = check_img_size(imgsz, s=stride)  # check image size
						capF_resize = ANPR.letterbox(capF, imgsz, stride=stride, auto=False)[0]            #0.0004 - 0.0006
						capF_resize = capF_resize[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
						capF_resize = np.ascontiguousarray(capF_resize)
						## testing code
						capF_resize = torch.from_numpy(capF_resize)
						capF_resize = capF_resize.half() if half else capF_resize.float()  # uint8 to fp16/32
						capF_resize = capF_resize.to(device)
						capF_resize /= 255.0  # 0~255 to 0.0~1.0
						if capF_resize.ndimension() == 3:
							capF_resize = capF_resize.unsqueeze(0)
						detect_buf4.appendleft(capF_resize)  # for detect
						detect_buf4.appendleft(capF)  # for detect
						detectFlag4 = True

				flag_resize=0
				if camID==cam_ID5:
#					if not input_buf5.empty():
#						input_buf5.get()
#					input_buf5.put(capF)  # for preview
					if input_buf5.empty():
						capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
						h_capF, w_capF = capF.shape[:2]
						top = bottom = int(abs(h_std - h_capF) / 2)
						left = right = int(abs(w_std - w_capF) / 2)
						capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						input_buf5.put(capF)  # for preview
						flag_resize=1
#					if detectFlag5 is False:
#						if not detect_buf5.empty():
#							detect_buf5.get()
#						detect_buf5.put(capF)  # for detect
					if (len(detect_buf5) == 0):
						if not flag_resize:
							capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
							h_capF, w_capF = capF.shape[:2]
							top = bottom = int(abs(h_std - h_capF) / 2)
							left = right = int(abs(w_std - w_capF) / 2)
							capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						#resize for detection
						if(TSRT):
							# stride = max(int(model_detection.stride), 32)  # model stride=32
							stride = 32
						else:
							stride = 32  # model stride=32
						imgsz = [640, 640]
						imgsz = check_img_size(imgsz, s=stride)  # check image size
						capF_resize = ANPR.letterbox(capF, imgsz, stride=stride, auto=False)[0]            #0.0004 - 0.0006
						capF_resize = capF_resize[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
						capF_resize = np.ascontiguousarray(capF_resize)
						## testing code
						capF_resize = torch.from_numpy(capF_resize)
						capF_resize = capF_resize.half() if half else capF_resize.float()  # uint8 to fp16/32
						capF_resize = capF_resize.to(device)
						capF_resize /= 255.0  # 0~255 to 0.0~1.0
						if capF_resize.ndimension() == 3:
							capF_resize = capF_resize.unsqueeze(0)
						detect_buf5.appendleft(capF_resize)  # for detect
						detect_buf5.appendleft(capF)  # for detect
						detectFlag5 = True

				flag_resize=0
				if camID==cam_ID6:
#					if not input_buf6.empty():
#						input_buf6.get()
#					input_buf6.put(capF)  # for preview
					if input_buf6.empty():
						capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
						h_capF, w_capF = capF.shape[:2]
						top = bottom = int(abs(h_std - h_capF) / 2)
						left = right = int(abs(w_std - w_capF) / 2)
						capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						input_buf6.put(capF)  # for preview
						flag_resize=1
#					if detectFlag6 is False:
#						if not detect_buf6.empty():
#							detect_buf6.get()
#						detect_buf6.put(capF)  # for detect
					if (len(detect_buf6) == 0):
						if not flag_resize:
							capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
							h_capF, w_capF = capF.shape[:2]
							top = bottom = int(abs(h_std - h_capF) / 2)
							left = right = int(abs(w_std - w_capF) / 2)
							capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						#resize for detection
						if(TSRT):
							# stride = max(int(model_detection.stride), 32)  # model stride=32
							stride = 32
						else:
							stride = 32  # model stride=32
						imgsz = [640, 640]
						imgsz = check_img_size(imgsz, s=stride)  # check image size
						capF_resize = ANPR.letterbox(capF, imgsz, stride=stride, auto=False)[0]            #0.0004 - 0.0006
						capF_resize = capF_resize[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
						capF_resize = np.ascontiguousarray(capF_resize)
						## testing code
						capF_resize = torch.from_numpy(capF_resize)
						capF_resize = capF_resize.half() if half else capF_resize.float()  # uint8 to fp16/32
						capF_resize = capF_resize.to(device)
						capF_resize /= 255.0  # 0~255 to 0.0~1.0
						if capF_resize.ndimension() == 3:
							capF_resize = capF_resize.unsqueeze(0)
						detect_buf6.appendleft(capF_resize)  # for detect
						detect_buf6.appendleft(capF)  # for detect
						detectFlag6 = True

				flag_resize=0
				if camID==cam_ID7:
#					if not input_buf7.empty():
#						input_buf7.get()
#					input_buf7.put(capF)  # for preview
					if input_buf7.empty():
						capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
						h_capF, w_capF = capF.shape[:2]
						top = bottom = int(abs(h_std - h_capF) / 2)
						left = right = int(abs(w_std - w_capF) / 2)
						capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						input_buf7.put(capF)  # for preview
						flag_resize=1
#					if detectFlag7 is False:
#						if not detect_buf7.empty():
#							detect_buf7.get()
#						detect_buf7.put(capF)  # for detect
					if (len(detect_buf7) == 0):
						if not flag_resize:
							capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
							h_capF, w_capF = capF.shape[:2]
							top = bottom = int(abs(h_std - h_capF) / 2)
							left = right = int(abs(w_std - w_capF) / 2)
							capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border
						#resize for detection
						if(TSRT):
							# stride = max(int(model_detection.stride), 32)  # model stride=32
							stride = 32
						else:
							stride = 32  # model stride=32
						imgsz = [640, 640]
						imgsz = check_img_size(imgsz, s=stride)  # check image size
						capF_resize = ANPR.letterbox(capF, imgsz, stride=stride, auto=False)[0]            #0.0004 - 0.0006
						capF_resize = capF_resize[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
						capF_resize = np.ascontiguousarray(capF_resize)
						## testing code
						capF_resize = torch.from_numpy(capF_resize)
						capF_resize = capF_resize.half() if half else capF_resize.float()  # uint8 to fp16/32
						capF_resize = capF_resize.to(device)
						capF_resize /= 255.0  # 0~255 to 0.0~1.0
						if capF_resize.ndimension() == 3:
							capF_resize = capF_resize.unsqueeze(0)
						detect_buf7.appendleft(capF_resize)  # for detect
						detect_buf7.appendleft(capF)  # for detect
						detectFlag7 = True

				if(ENABLE_DEBUG_PRINT):
					print(f"cam_ID:{camID}, StartTime:{cap_t0}, EndTime:{datetime.now().strftime('%H:%M:%S.%f')[:-3]}, CapTime:{(capture_t1 - capture_t0):.4f}, CycleTime:{(time.time() - capture_t0):.4f}", end="  ")
					print(f"\n")

				if progStop:
					cam0STOP = True
					cam1STOP = True
					cam2STOP = True
					cam3STOP = True
					cam4STOP = True
					cam5STOP = True
					cam6STOP = True
					cam7STOP = True
					progRUN = False
					break

			else:
				print(f"Frame Read End: {camID}, {full_filename}.")
				break

#			time.sleep(0.01)
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
	file_detection = [x for x in sorted(os.listdir(lpd_path), reverse=True) if x.endswith('02.pt')]  # sort available model 02.pt
	for x in file_detection:
		weights_detection = os.path.join(lpd_path, x)  # use up to date model
		if weights_detection is not existing_weights_detection:
			try:
#				model_detection = attempt_load(weights_detection, map_location=device)  # load FP32 model
				model_detection = attempt_load(weights_detection, device)  # load FP32 model
			except:
				print(f"[Error] License Plate Detection model file: {weights_detection}")
				weights_detection = ''
	if weights_detection == '':
		print("[Error] Cannot find suitable License Plate Detection model file.")
		sys.exit(0)
	print(f"[Model] License Plate Detection model file: {weights_detection}")
	print(f"model class names: {model_detection.module.names if hasattr(model_detection, 'module') else model_detection.names}")  # get class names
	model_detection.half() if half else model_detection.float()
	return weights_detection

def weights_detectionUpdateTRT(device, existing_weights_detection, data_path):
	global weights_detection, model_detection
	print("==================================================")
	# Load model plate detection
	weights_detection = ''
	file_detection = [x for x in sorted(os.listdir(lpd_path), reverse=True) if x.endswith('.02.engine')]  # sort available model 02.engine
	for x in file_detection:
		weights_detection = os.path.join(lpd_path, x)  # use up to date model
		if weights_detection is not existing_weights_detection:
			dnn = False
			data = data_path
			try:
				model_detection = YoloTRT(weights_detection, device=device, dnn=dnn, data=data, fp16=half)
			except:
				print(f"[Error] License Plate Detection model file: {weights_detection}")
				weights_detection = ''
	if weights_detection == '':
		print("[Error] Cannot find suitable License Plate Detection model file.")
		sys.exit(0)
	print(f"[Model] License Plate Detection model file: {weights_detection}")
	print(f"model class names: {model_detection.module.names if hasattr(model_detection, 'module') else model_detection.names}")  # get class names
	model_detection.half() if half else model_detection.float()
	return weights_detection

#--------------------------------------------------
def weights_recognizeUpdate(device, existing_weights_recognize):
	global weights_recognize, model_recognize
	print("==================================================")
	# Load model plate recognize
	weights_recognize = ''
	file_recognize = [x for x in sorted(os.listdir(cr_path), reverse=True) if x.endswith('01.pt')]  # sort available model 01.pt
	for x in file_recognize:
		weights_recognize = os.path.join(cr_path, x)  # use up to date model
		if weights_recognize is not existing_weights_recognize:
			try:
#				model_recognize = attempt_load(weights_recognize, map_location=device)  # load FP32 model
				model_recognize = attempt_load(weights_recognize, device)  # load FP32 model
			except:
				print(f"[Error] Character Recognition model file: {weights_recognize}")
				weights_recognize = ''
	if weights_recognize == '':
		print("[Error] Cannot find suitable Character Recognition model file.")
		sys.exit(0)
	print(f"[Model] Character Recognize model file: {weights_recognize}")
	print(f"model class names: {model_recognize.module.names if hasattr(model_recognize, 'module') else model_recognize.names}")  # get class names
	model_recognize.half() if half else model_recognize.float()
	return weights_recognize

def weights_recognizeUpdateTRT(device, existing_weights_recognize, data_path):
	global weights_recognize, model_recognize
	print("==================================================")
	# Load model plate recognize
	weights_recognize = ''
	file_recognize = [x for x in sorted(os.listdir(cr_path), reverse=True) if x.endswith('.01.engine')]  # sort available model 01.engine
	for x in file_recognize:
		print(f"detectionUpdate file name: {x}")
		weights_recognize = os.path.join(cr_path, x)  # use up to date model
		if weights_recognize is not existing_weights_recognize:
			dnn = False
			data = data_path
			try:
				model_recognize = YoloTRT(weights_recognize, device=device, dnn=dnn, data=data, fp16=half)
			except:
				print(f"[Error] Character Recognition model file: {weights_recognize}")
				weights_recognize = ''
	if weights_recognize == '':
		print("[Error] Cannot find suitable Character Recognition model file.")
		sys.exit(0)
	print(f"[Model] Character Recognize model file: {weights_recognize}")
	print(f"model class names: {model_recognize.module.names if hasattr(model_recognize, 'module') else model_recognize.names}")  # get class names
	model_recognize.half() if half else model_recognize.float()
	return weights_recognize

#--------------------------------------------------
def weights_vavcUpdate(device, existing_weights_vavc):
	global weights_vavc, model_vavc
	print("==================================================")
	# Load model video analytic vehicle classification (vavc)
	weights_vavc = ''
	file_vavc = [x for x in sorted(os.listdir(vavc_path), reverse=True) if x.endswith('03.pt')]  # sort available model 03.pt
	for x in file_vavc:
		weights_vavc = os.path.join(vavc_path, x)  # use up to date model
		if weights_vavc is not existing_weights_vavc:
			try:
#				model_vavc = attempt_load(weights_vavc, map_location=device)  # load FP32 model
				model_vavc = attempt_load(weights_vavc, device)  # load FP32 model
			except:
				print(f"[Error] Video Analytic Vehicle Classification model file: {weights_vavc}")
				weights_vavc = ''
	if weights_vavc == '':
		print("[Error] Cannot find suitable Video Analytic Vehicle Classification model file.")
		sys.exit(0)
	print(f"[Model] Video Analytic Vehicle Classification model file: {weights_vavc}")
	print(f"model class names: {model_vavc.module.names if hasattr(model_vavc, 'module') else model_vavc.names}")  # get class names
	model_vavc.half() if half else model_vavc.float()
	return weights_vavc


def weights_plate_gradingUpdateTRT(device, existing_weights_plate_grading, data_path):
	global weights_plate_grading, model_plate_grading
	print("==================================================")
	# Load model plate recognize
	weights_plate_grading = ''
	file_plate_grading = [x for x in sorted(os.listdir(cr_path), reverse=True) if x.endswith('.01.engine')]  # sort available model 01.engine
	for x in file_plate_grading:
		print(f"detectionUpdate file name: {x}")
		weights_plate_grading = os.path.join(cr_path, x)  # use up to date model
		if weights_plate_grading is not existing_weights_plate_grading:
			dnn = False
			data = data_path
			try:
				model_plate_grading = YoloTRT(weights_plate_grading, device=device, dnn=dnn, data=data, fp16=half)
			except:
				print(f"[Error] Character Recognition model file: {weights_plate_grading}")
				weights_plate_grading = ''
	if weights_plate_grading == '':
		print("[Error] Cannot find suitable Character Recognition model file.")
		sys.exit(0)
	print(f"[Model] Character plate_grading model file: {weights_plate_grading}")
	print(f"model class names: {model_plate_grading.module.names if hasattr(model_plate_grading, 'module') else model_plate_grading.names}")  # get class names
	model_plate_grading.half() if half else model_plate_grading.float()
	return weights_plate_grading






#--------------------------------------------------
def showPreview():

	print(f"PREVIEW Starting...")
	global progStop, pause
	progStop = False
	pause = False
	global flagROI, flagPoint, detection_ROI, imgMouse
	global existing_weights_detection, existing_weights_recognize, existing_weights_vavc
	global camDisp0, camDisp1, camDisp2, camDisp3, camDisp4, camDisp5, camDisp6, camDisp7

	# local variable
	setPreview = False
	plateFlag0 = False
	plateFlag1 = False
	plateFlag2 = False
	plateFlag3 = False
	plateFlag4 = False
	plateFlag5 = False
	plateFlag6 = False
	plateFlag7 = False
	font = cv2.FONT_HERSHEY_SIMPLEX
	fontScale = 0.6
	cv2.namedWindow('PREVIEW')
	cv2.moveWindow('PREVIEW', 0, 0)
	setROI0 = False
	setROI1 = False
	setROI2 = False
	setROI3 = False
	setROI4 = False
	setROI5 = False
	setROI6 = False
	setROI7 = False
	window = 2
	if window == 0:
		#imgPreview = np.zeros((int(h_std/windowScale), int(w_std/windowScale*4)+(padding*3), 3), dtype=np.uint8)
		imgPreview = np.zeros((int(h_std/windowScale*5)+(padding*5), int(w_std/windowScale*4)+(padding*3), 3), dtype=np.uint8)
	if window == 1:
		#imgPreview = np.zeros((int(h_std/windowScale*2)+padding, int(w_std/windowScale*4)+(padding*3), 3), dtype=np.uint8)
		imgPreview = np.zeros((int(h_std/windowScale*5)+(padding*5), int(w_std/windowScale*4)+(padding*3), 3), dtype=np.uint8)
	if window == 2:
		#imgPreview = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale*4)+(padding*3), 3), dtype=np.uint8)
		imgPreview = np.zeros((int(h_std/windowScale*5)+(padding*5), int(w_std/windowScale*4)+(padding*3), 3), dtype=np.uint8)
	imgMouse = np.zeros((h_std, w_std, 3), dtype=np.uint8)
	modelUpdateFlag = False
	detected_plate0 = ''
	detected_plate1 = ''
	detected_plate2 = ''
	detected_plate3 = ''
	detected_plate4 = ''
	detected_plate5 = ''
	detected_plate6 = ''
	detected_plate7 = ''
	previous_plate0 = ''
	previous_plate1 = ''
	previous_plate2 = ''
	previous_plate3 = ''
	previous_plate4 = ''
	previous_plate5 = ''
	previous_plate6 = ''
	previous_plate7 = ''

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
	camDisp1 = config.getboolean('src_input','input_disp1')
	print(f"camDisp1: {camDisp1}.")
	camDisp2 = config.getboolean('src_input','input_disp2')
	print(f"camDisp2: {camDisp2}.")
	camDisp3 = config.getboolean('src_input','input_disp3')
	print(f"camDisp3: {camDisp3}.")
	camDisp4 = config.getboolean('src_input','input_disp4')
	print(f"camDisp4: {camDisp4}.")
	camDisp5 = config.getboolean('src_input','input_disp5')
	print(f"camDisp5: {camDisp5}.")
	camDisp6 = config.getboolean('src_input','input_disp6')
	print(f"camDisp6: {camDisp6}.")
	camDisp7 = config.getboolean('src_input','input_disp7')
	print(f"camDisp7: {camDisp7}.")

	while True:
		time.sleep(SHOW_PREVIEW_SLEEP)
		#--------------------------------------------------
		# plate cam0
		plate_box_img0 = None
		if not plate_buf0.empty():
			cam_ID, input_img, plate_box_img0, input_conf, detected_plate0, rfid_plate0, va_class0, tc_class0, time_rfid0, time_start0, time_end0, dt = plate_buf0.get().copy()
			if (cam_ID != '') and (previous_plate0 is not detected_plate0):
				previous_plate0 = detected_plate0
				#dt = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]
				#print(f"Date: {dt}")
				# save detection image
				if isinstance(input_conf, str):
					input_name = os.path.join(full_path0, '%s.' %dt + cam_ID + '.01.jpg')
					cv2.imwrite(input_name, input_img)
				else:

					if toll_input == "offline":
						input_name = os.path.join(full_path0, '%s.' %dt + cam_ID + '.01.' + detected_plate0 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path0, '%s.' %dt + cam_ID + '.02.' + detected_plate0 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img0)
	
					elif toll_input == "KLK":
						input_name = os.path.join(full_path0, '%s.' %dt_base32 + cam_ID + '.01.' + detected_plate0 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path0, '%s.' %dt_base32 + cam_ID + '.02.' + detected_plate0 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img0)

					elif toll_input == "LPT":

						#decode dt base32 to bas10
						dt_base32 = decode_base32(dt,32)
						dt_base32 = datetime.strptime(str(dt_base32), "%y%m%d%H%M%S%f")
						dt_base32 = dt_base32.strftime("%Y%m%d.%H%M%S.%f")[:-3]

						# debug - get new date time if date time is empty
						if dt_base32 == " ":
							tracking_date = datetime.now().strftime("%Y%m%d")
							tracking_datetime_empty = os.path.join(log_path0,tracking_date + '_cam0_tracking_datetime_empty.txt')
							with open(tracking_datetime_empty, 'a+') as track_file:
								track_file.write(f"Date time: empty\t| Image ID: {dt}\t| cam_ID: {cam_ID}\t|  detected_plate: {detected_plate0}\t| \n")
							print(f"{dt_base32}{dt}.{cam_ID}.01.{detected_plate0}.jpg")
							dt_base32 = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]

						input_name = os.path.join(full_path0 , '%s.' %dt_base32 + dt + "." + cam_ID + '.01.' + detected_plate0 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path0 , '%s.' %dt_base32 + dt + "." + cam_ID + '.02.' + detected_plate0 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img0)

					

				# save log
				csvLogger(cam_ID, input_mode0, log_path0, tc_class0, va_class0, str(1), rfid_plate0, detected_plate0, input_conf, input_name, time_rfid0, time_start0, time_end0)

		#--------------------------------------------------
		# plate cam1
		plate_box_img1 = None
		if not plate_buf1.empty():
			cam_ID, input_img, plate_box_img1, input_conf, detected_plate1, rfid_plate1, va_class1, tc_class1, time_rfid1, time_start1, time_end1, dt = plate_buf1.get().copy()
			if (cam_ID != '') and (previous_plate1 is not detected_plate1):
				previous_plate1 = detected_plate1
				#dt = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]
				#print(f"Date: {dt}")
				# save detection image
				if isinstance(input_conf, str):
					input_name = os.path.join(full_path1, '%s.' %dt + cam_ID + '.01.jpg')
					cv2.imwrite(input_name, input_img)
				else:

					if toll_input == "offline":
						input_name = os.path.join(full_path1, '%s.' %dt + cam_ID + '.01.' + detected_plate1 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path1, '%s.' %dt + cam_ID + '.02.' + detected_plate1 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img1)
	
					elif toll_input == "KLK":
						input_name = os.path.join(full_path1, '%s.' %dt_base32 + cam_ID + '.01.' + detected_plate1 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path1, '%s.' %dt_base32 + cam_ID + '.02.' + detected_plate1 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img1)

					elif toll_input == "LPT":

						#decode dt base32 to bas10
						dt_base32 = decode_base32(dt,32)
						dt_base32 = datetime.strptime(str(dt_base32), "%y%m%d%H%M%S%f")
						dt_base32 = dt_base32.strftime("%Y%m%d.%H%M%S.%f")[:-3]

						# debug - get new date time if date time is empty
						if dt_base32 == " ":
							tracking_date = datetime.now().strftime("%Y%m%d")
							tracking_datetime_empty = os.path.join(log_path1,tracking_date + '_cam1_tracking_datetime_empty.txt')
							with open(tracking_datetime_empty, 'a+') as track_file:
								track_file.write(f"Date time: empty\t| Image ID: {dt}\t| cam_ID: {cam_ID}\t|  detected_plate: {detected_plate1}\t| \n")
							print(f"{dt_base32}{dt}.{cam_ID}.01.{detected_plate1}.jpg")
							dt_base32 = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]

						input_name = os.path.join(full_path1 , '%s.' %dt_base32 + dt + "." + cam_ID + '.01.' + detected_plate1 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path1 , '%s.' %dt_base32 + dt + "." + cam_ID + '.02.' + detected_plate1 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img1) 
				# save log
				csvLogger(cam_ID, input_mode1, log_path1, tc_class1, va_class1, str(1), rfid_plate1, detected_plate1, input_conf, input_name, time_rfid1, time_start1, time_end1)

		#--------------------------------------------------
		# plate cam2
		plate_box_img2 = None
		if not plate_buf2.empty():
			cam_ID, input_img, plate_box_img2, input_conf, detected_plate2, rfid_plate2, va_class2, tc_class2, time_rfid2, time_start2, time_end2, dt = plate_buf2.get().copy()
			if (cam_ID != '') and (previous_plate2 is not detected_plate2):
				previous_plate2 = detected_plate2
				#dt = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]
				#print(f"Date: {dt}")
				# save detection image
				if isinstance(input_conf, str):
					input_name = os.path.join(full_path2, '%s.' %dt + cam_ID + '.01.jpg')
					cv2.imwrite(input_name, input_img)
				else:

					if toll_input == "offline":
						input_name = os.path.join(full_path2, '%s.' %dt + cam_ID + '.01.' + detected_plate2 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path2, '%s.' %dt + cam_ID + '.02.' + detected_plate2 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img2)
	
					elif toll_input == "KLK":
						input_name = os.path.join(full_path2, '%s.' %dt_base32 + cam_ID + '.01.' + detected_plate2 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path2, '%s.' %dt_base32 + cam_ID + '.02.' + detected_plate2 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img2)

					elif toll_input == "LPT":

						#decode dt base32 to bas10
						dt_base32 = decode_base32(dt,32)
						dt_base32 = datetime.strptime(str(dt_base32), "%y%m%d%H%M%S%f")
						dt_base32 = dt_base32.strftime("%Y%m%d.%H%M%S.%f")[:-3]

						# debug - get new date time if date time is empty
						if dt_base32 == " ":
							tracking_date = datetime.now().strftime("%Y%m%d")
							tracking_datetime_empty = os.path.join(log_path2,tracking_date + '_cam2_tracking_datetime_empty.txt')
							with open(tracking_datetime_empty, 'a+') as track_file:
								track_file.write(f"Date time: empty\t| Image ID: {dt}\t| cam_ID: {cam_ID}\t|  detected_plate: {detected_plate2}\t| \n")
							print(f"{dt_base32}{dt}.{cam_ID}.01.{detected_plate2}.jpg")
							dt_base32 = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]

						input_name = os.path.join(full_path2 , '%s.' %dt_base32 + dt + "." + cam_ID + '.01.' + detected_plate2 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path2 , '%s.' %dt_base32 + dt + "." + cam_ID + '.02.' + detected_plate2 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img2)
				# save log
				csvLogger(cam_ID, input_mode2, log_path2, tc_class2, va_class2, str(1), rfid_plate2, detected_plate2, input_conf, input_name, time_rfid2, time_start2, time_end2)

		#--------------------------------------------------
		# plate cam3
		plate_box_img3 = None
		if not plate_buf3.empty():
			cam_ID, input_img, plate_box_img3, input_conf, detected_plate3, rfid_plate3, va_class3, tc_class3, time_rfid3, time_start3, time_end3, dt = plate_buf3.get().copy()
			if (cam_ID != '') and (previous_plate3 is not detected_plate3):
				previous_plate3 = detected_plate3
				#dt = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]
				#print(f"Date: {dt}")
				# save detection image
				if isinstance(input_conf, str):
					input_name = os.path.join(full_path3, '%s.' %dt + cam_ID + '.01.jpg')
					cv2.imwrite(input_name, input_img)
				else:

					if toll_input == "offline":
						input_name = os.path.join(full_path3, '%s.' %dt + cam_ID + '.01.' + detected_plate3 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path3, '%s.' %dt + cam_ID + '.02.' + detected_plate3 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img3)
	
					elif toll_input == "KLK":
						input_name = os.path.join(full_path3, '%s.' %dt_base32 + cam_ID + '.01.' + detected_plate3 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path3, '%s.' %dt_base32 + cam_ID + '.02.' + detected_plate3 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img3)

					elif toll_input == "LPT":

						#decode dt base32 to bas10
						dt_base32 = decode_base32(dt,32)
						dt_base32 = datetime.strptime(str(dt_base32), "%y%m%d%H%M%S%f")
						dt_base32 = dt_base32.strftime("%Y%m%d.%H%M%S.%f")[:-3]

						# debug - get new date time if date time is empty
						if dt_base32 == " ":
							tracking_date = datetime.now().strftime("%Y%m%d")
							tracking_datetime_empty = os.path.join(log_path3,tracking_date + '_cam3_tracking_datetime_empty.txt')
							with open(tracking_datetime_empty, 'a+') as track_file:
								track_file.write(f"Date time: empty\t| Image ID: {dt}\t| cam_ID: {cam_ID}\t|  detected_plate: {detected_plate3}\t| \n")
							print(f"{dt_base32}{dt}.{cam_ID}.01.{detected_plate3}.jpg")
							dt_base32 = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]

						input_name = os.path.join(full_path3 , '%s.' %dt_base32 + dt + "." + cam_ID + '.01.' + detected_plate3 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path3 , '%s.' %dt_base32 + dt + "." + cam_ID + '.02.' + detected_plate3 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img3)
				# save log
				csvLogger(cam_ID, input_mode3, log_path3, tc_class3, va_class3, str(1), rfid_plate3, detected_plate3, input_conf, input_name, time_rfid3, time_start3, time_end3)

		#--------------------------------------------------
		# plate cam4
		plate_box_img4 = None
		if not plate_buf4.empty():
			cam_ID, input_img, plate_box_img4, input_conf, detected_plate4, rfid_plate4, va_class4, tc_class4, time_rfid4, time_start4, time_end4, dt = plate_buf4.get().copy()
			if (cam_ID != '') and (previous_plate4 is not detected_plate4):
				previous_plate4 = detected_plate4
				#dt = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]
				#print(f"Date: {dt}")
				# save detection image
				if isinstance(input_conf, str):
					input_name = os.path.join(full_path4, '%s.' %dt + cam_ID + '.01.jpg')
					cv2.imwrite(input_name, input_img)
				else:

					if toll_input == "offline":
						input_name = os.path.join(full_path4, '%s.' %dt + cam_ID + '.01.' + detected_plate4 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path4, '%s.' %dt + cam_ID + '.02.' + detected_plate4 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img4)
	
					elif toll_input == "KLK":
						input_name = os.path.join(full_path4, '%s.' %dt_base32 + cam_ID + '.01.' + detected_plate4 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path4, '%s.' %dt_base32 + cam_ID + '.02.' + detected_plate4 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img4)

					elif toll_input == "LPT":

						#decode dt base32 to bas10
						dt_base32 = decode_base32(dt,32)
						dt_base32 = datetime.strptime(str(dt_base32), "%y%m%d%H%M%S%f")
						dt_base32 = dt_base32.strftime("%Y%m%d.%H%M%S.%f")[:-3]

						# debug - get new date time if date time is empty
						if dt_base32 == " ":
							tracking_date = datetime.now().strftime("%Y%m%d")
							tracking_datetime_empty = os.path.join(log_path4,tracking_date + '_cam4_tracking_datetime_empty.txt')
							with open(tracking_datetime_empty, 'a+') as track_file:
								track_file.write(f"Date time: empty\t| Image ID: {dt}\t| cam_ID: {cam_ID}\t|  detected_plate: {detected_plate4}\t| \n")
							print(f"{dt_base32}{dt}.{cam_ID}.01.{detected_plate4}.jpg")
							dt_base32 = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]

						input_name = os.path.join(full_path4 , '%s.' %dt_base32 + dt + "." + cam_ID + '.01.' + detected_plate4 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path4 , '%s.' %dt_base32 + dt + "." + cam_ID + '.02.' + detected_plate4 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img4)
				# save log
				csvLogger(cam_ID, input_mode4, log_path4, tc_class4, va_class4, str(1), rfid_plate4, detected_plate4, input_conf, input_name, time_rfid4, time_start4, time_end4)

		#--------------------------------------------------
		# plate cam5
		plate_box_img5 = None
		if not plate_buf5.empty():
			cam_ID, input_img, plate_box_img5, input_conf, detected_plate5, rfid_plate5, va_class5, tc_class5, time_rfid5, time_start5, time_end5, dt = plate_buf5.get().copy()
			if (cam_ID != '') and (previous_plate5 is not detected_plate5):
				previous_plate5 = detected_plate5
				#dt = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]
				#print(f"Date: {dt}")
				# save detection image
				if isinstance(input_conf, str):
					input_name = os.path.join(full_path5, '%s.' %dt + cam_ID + '.01.jpg')
					cv2.imwrite(input_name, input_img)
				else:

					if toll_input == "offline":
						input_name = os.path.join(full_path5, '%s.' %dt + cam_ID + '.01.' + detected_plate5 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path5, '%s.' %dt + cam_ID + '.02.' + detected_plate5 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img5)
	
					elif toll_input == "KLK":
						input_name = os.path.join(full_path0, '%s.' %dt_base32 + cam_ID + '.01.' + detected_plate5 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path5, '%s.' %dt_base32 + cam_ID + '.02.' + detected_plate5 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img5)

					elif toll_input == "LPT":

						#decode dt base32 to bas10
						dt_base32 = decode_base32(dt,32)
						dt_base32 = datetime.strptime(str(dt_base32), "%y%m%d%H%M%S%f")
						dt_base32 = dt_base32.strftime("%Y%m%d.%H%M%S.%f")[:-3]

						# debug - get new date time if date time is empty
						if dt_base32 == " ":
							tracking_date = datetime.now().strftime("%Y%m%d")
							tracking_datetime_empty = os.path.join(log_path5,tracking_date + '_cam5_tracking_datetime_empty.txt')
							with open(tracking_datetime_empty, 'a+') as track_file:
								track_file.write(f"Date time: empty\t| Image ID: {dt}\t| cam_ID: {cam_ID}\t|  detected_plate: {detected_plate5}\t| \n")
							print(f"{dt_base32}{dt}.{cam_ID}.01.{detected_plate5}.jpg")
							dt_base32 = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]

						input_name = os.path.join(full_path5 , '%s.' %dt_base32 + dt + "." + cam_ID + '.01.' + detected_plate5 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path5 , '%s.' %dt_base32 + dt + "." + cam_ID + '.02.' + detected_plate5 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img5) 
				# save log
				csvLogger(cam_ID, input_mode5, log_path5, tc_class5, va_class5, str(1), rfid_plate5, detected_plate5, input_conf, input_name, time_rfid5, time_start5, time_end5)

		#--------------------------------------------------
		# plate cam6
		plate_box_img6 = None
		if not plate_buf6.empty():
			cam_ID, input_img, plate_box_img6, input_conf, detected_plate6, rfid_plate6, va_class6, tc_class6, time_rfid6, time_start6, time_end6, dt = plate_buf6.get().copy()
			if (cam_ID != '') and (previous_plate6 is not detected_plate6):
				previous_plate6 = detected_plate6
				#dt = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]
				#print(f"Date: {dt}")
				# save detection image
				if isinstance(input_conf, str):
					input_name = os.path.join(full_path6, '%s.' %dt + cam_ID + '.01.jpg')
					cv2.imwrite(input_name, input_img)
				else:

					if toll_input == "offline":
						input_name = os.path.join(full_path6, '%s.' %dt + cam_ID + '.01.' + detected_plate6 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path6, '%s.' %dt + cam_ID + '.02.' + detected_plate6 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img6)
	
					elif toll_input == "KLK":
						input_name = os.path.join(full_path6, '%s.' %dt_base32 + cam_ID + '.01.' + detected_plate6 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path6, '%s.' %dt_base32 + cam_ID + '.02.' + detected_plate6 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img6)

					elif toll_input == "LPT":

						#decode dt base32 to bas10
						dt_base32 = decode_base32(dt,32)
						dt_base32 = datetime.strptime(str(dt_base32), "%y%m%d%H%M%S%f")
						dt_base32 = dt_base32.strftime("%Y%m%d.%H%M%S.%f")[:-3]

						# debug - get new date time if date time is empty
						if dt_base32 == " ":
							tracking_date = datetime.now().strftime("%Y%m%d")
							tracking_datetime_empty = os.path.join(log_path6,tracking_date + '_cam6_tracking_datetime_empty.txt')
							with open(tracking_datetime_empty, 'a+') as track_file:
								track_file.write(f"Date time: empty\t| Image ID: {dt}\t| cam_ID: {cam_ID}\t|  detected_plate: {detected_plate6}\t| \n")
							print(f"{dt_base32}{dt}.{cam_ID}.01.{detected_plate6}.jpg")
							dt_base32 = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]

						input_name = os.path.join(full_path6 , '%s.' %dt_base32 + dt + "." + cam_ID + '.01.' + detected_plate6 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path6 , '%s.' %dt_base32 + dt + "." + cam_ID + '.02.' + detected_plate6 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img6)
				# save log
				csvLogger(cam_ID, input_mode6, log_path6, tc_class6, va_class6, str(1), rfid_plate6, detected_plate6, input_conf, input_name, time_rfid6, time_start6, time_end6)

		#--------------------------------------------------
		# plate cam7
		plate_box_img7 = None
		if not plate_buf7.empty():
			cam_ID, input_img, plate_box_img7, input_conf, detected_plate7, rfid_plate7, va_class7, tc_class7, time_rfid7, time_start7, time_end7, dt = plate_buf7.get().copy()
			if (cam_ID != '') and (previous_plate7 is not detected_plate7):
				previous_plate7 = detected_plate7
				#dt = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]
				#print(f"Date: {dt}")
				# save detection image
				if isinstance(input_conf, str):
					input_name = os.path.join(full_path7, '%s.' %dt + cam_ID + '.01.jpg')
					cv2.imwrite(input_name, input_img)
				else:

					if toll_input == "offline":
						input_name = os.path.join(full_path7, '%s.' %dt + cam_ID + '.01.' + detected_plate7 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path7, '%s.' %dt + cam_ID + '.02.' + detected_plate7 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img7)
	
					elif toll_input == "KLK":
						input_name = os.path.join(full_path1, '%s.' %dt_base32 + cam_ID + '.01.' + detected_plate7 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path7, '%s.' %dt_base32 + cam_ID + '.02.' + detected_plate7 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img7)

					elif toll_input == "LPT":

						#decode dt base32 to bas10
						dt_base32 = decode_base32(dt,32)
						dt_base32 = datetime.strptime(str(dt_base32), "%y%m%d%H%M%S%f")
						dt_base32 = dt_base32.strftime("%Y%m%d.%H%M%S.%f")[:-3]

						# debug - get new date time if date time is empty
						if dt_base32 == " ":
							tracking_date = datetime.now().strftime("%Y%m%d")
							tracking_datetime_empty = os.path.join(log_path7,tracking_date + '_cam7_tracking_datetime_empty.txt')
							with open(tracking_datetime_empty, 'a+') as track_file:
								track_file.write(f"Date time: empty\t| Image ID: {dt}\t| cam_ID: {cam_ID}\t|  detected_plate: {detected_plate7}\t| \n")
							print(f"{dt_base32}{dt}.{cam_ID}.01.{detected_plate7}.jpg")
							dt_base32 = datetime.now().strftime("%Y%m%d.%H%M%S.%f")[:-3]

						input_name = os.path.join(full_path7 , '%s.' %dt_base32 + dt + "." + cam_ID + '.01.' + detected_plate7 + '.jpg')
						cv2.imwrite(input_name, input_img)
						plate_box_name = os.path.join(crop_path7 , '%s.' %dt_base32 + dt + "." + cam_ID + '.02.' + detected_plate7 + '.jpg')
						cv2.imwrite(plate_box_name, plate_box_img7)
				# save log
				csvLogger(cam_ID, input_mode7, log_path7, tc_class7, va_class7, str(1), rfid_plate7, detected_plate7, input_conf, input_name, time_rfid7, time_start7, time_end7)

		#--------------------------------------------------
		if not input_buf0.empty() and camDisp0==True:
			try:
				imgP = input_buf0.get().copy()
			except:
				print("input_buf0 timeout")
			if setROI0:
				imgSetROI = cv2.addWeighted(imgP.copy(), 1, imgMouse, 1, 0)
				cv2.putText(imgSetROI, 'CAMERA: ' + cam_ID0, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.imshow('SetROI', imgSetROI)
				#cv2.moveWindow('SetROI', 20, 20)
			if imgP is not None:
				cv2.putText(imgP, 'CAMERA: ' + cam_ID0, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.putText(imgP, 'LANE   : ' + lane_type0, (10,112), font, 2, (0,255,0), 4, cv2.LINE_AA)
				imgP = cv2.resize(imgP, (int(imgP.shape[1]/windowScale),int(imgP.shape[0]/windowScale)))
				imgPreview[:int(imgP.shape[0]), :int(imgP.shape[1]), :3] = imgP.copy()
				setPreview = True

		if not input_buf1.empty() and camDisp1==True:
			try:
				imgP = input_buf1.get().copy()
			except:
				print("input_buf1 timeout")
			if setROI1:
				imgSetROI = cv2.addWeighted(imgP.copy(), 1, imgMouse, 1, 0)
				cv2.putText(imgSetROI, 'CAMERA: ' + cam_ID1, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.imshow('SetROI', imgSetROI)
				#cv2.moveWindow('SetROI', 20, 20)
			if imgP is not None:
				cv2.putText(imgP, 'CAMERA: ' + cam_ID1, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.putText(imgP, 'LANE   : ' + lane_type1, (10,112), font, 2, (0,255,0), 4, cv2.LINE_AA)
				imgP = cv2.resize(imgP, (int(imgP.shape[1]/windowScale),int(imgP.shape[0]/windowScale)))
				imgPreview[:int(imgP.shape[0]), int(imgP.shape[1])+padding:int(imgP.shape[1]*2)+padding, :3] = imgP.copy()
				setPreview = True

		if not input_buf2.empty() and camDisp2==True:
			try:
				imgP = input_buf2.get().copy()
			except:
				print("input_buf2 timeout")
			if setROI2:
				imgSetROI = cv2.addWeighted(imgP.copy(), 1, imgMouse, 1, 0)
				cv2.putText(imgSetROI, 'CAMERA: ' + cam_ID2, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.imshow('SetROI', imgSetROI)
				#cv2.moveWindow('SetROI', 20, 20)
			if imgP is not None:
				cv2.putText(imgP, 'CAMERA: ' + cam_ID2, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.putText(imgP, 'LANE   : ' + lane_type2, (10,112), font, 2, (0,255,0), 4, cv2.LINE_AA)
				imgP = cv2.resize(imgP, (int(imgP.shape[1]/windowScale),int(imgP.shape[0]/windowScale)))
				imgPreview[:int(imgP.shape[0]), int(imgP.shape[1]*2)+(padding*2):int(imgP.shape[1]*3)+(padding*2), :3] = imgP.copy()
				setPreview = True

		if not input_buf3.empty() and camDisp3==True:
			try:
				imgP = input_buf3.get().copy()
			except:
				print("input_buf3 timeout")
			if setROI3:
				imgSetROI = cv2.addWeighted(imgP.copy(), 1, imgMouse, 1, 0)
				cv2.putText(imgSetROI, 'CAMERA: ' + cam_ID3, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.imshow('SetROI', imgSetROI)
				#cv2.moveWindow('SetROI', 20, 20)
			if imgP is not None:
				cv2.putText(imgP, 'CAMERA: ' + cam_ID3, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.putText(imgP, 'LANE   : ' + lane_type3, (10,112), font, 2, (0,255,0), 4, cv2.LINE_AA)
				imgP = cv2.resize(imgP, (int(imgP.shape[1]/windowScale),int(imgP.shape[0]/windowScale)))
				imgPreview[:int(imgP.shape[0]), int(imgP.shape[1]*3)+(padding*3):int(imgP.shape[1]*4)+(padding*3), :3] = imgP.copy()
				setPreview = True

		if not input_buf4.empty() and camDisp4==True:
			try:
				imgP = input_buf4.get().copy()
			except:
				print("input_buf4 timeout")
			if setROI4:
				imgSetROI = cv2.addWeighted(imgP.copy(), 1, imgMouse, 1, 0)
				cv2.putText(imgSetROI, 'CAMERA: ' + cam_ID4, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.imshow('SetROI', imgSetROI)
				#cv2.moveWindow('SetROI', 20, 20)
			if imgP is not None:
				cv2.putText(imgP, 'CAMERA: ' + cam_ID4, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.putText(imgP, 'LANE   : ' + lane_type4, (10,112), font, 2, (0,255,0), 4, cv2.LINE_AA)
				imgP = cv2.resize(imgP, (int(imgP.shape[1]/windowScale),int(imgP.shape[0]/windowScale)))
				imgPreview[int(imgP.shape[0]*2.5)+(padding*3):int(imgP.shape[0]*3.5)+(padding*3), :int(imgP.shape[1]), :3] = imgP.copy()
				setPreview = True

		if not input_buf5.empty() and camDisp5==True:
			try:
				imgP = input_buf5.get().copy()
			except:
				print("input_buf5 timeout")
			if setROI5:
				imgSetROI = cv2.addWeighted(imgP.copy(), 1, imgMouse, 1, 0)
				cv2.putText(imgSetROI, 'CAMERA: ' + cam_ID5, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.imshow('SetROI', imgSetROI)
				#cv2.moveWindow('SetROI', 20, 20)
			if imgP is not None:
				cv2.putText(imgP, 'CAMERA: ' + cam_ID5, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.putText(imgP, 'LANE   : ' + lane_type5, (10,112), font, 2, (0,255,0), 4, cv2.LINE_AA)
				imgP = cv2.resize(imgP, (int(imgP.shape[1]/windowScale),int(imgP.shape[0]/windowScale)))
				imgPreview[int(imgP.shape[0]*2.5)+(padding*3):int(imgP.shape[0]*3.5)+(padding*3), int(imgP.shape[1])+padding:int(imgP.shape[1]*2)+padding, :3] = imgP.copy()
				setPreview = True

		if not input_buf6.empty() and camDisp6==True:
			try:
				imgP = input_buf6.get().copy()
			except:
				print("input_buf6 timeout")
			if setROI6:
				imgSetROI = cv2.addWeighted(imgP.copy(), 1, imgMouse, 1, 0)
				cv2.putText(imgSetROI, 'CAMERA: ' + cam_ID6, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.imshow('SetROI', imgSetROI)
				#cv2.moveWindow('SetROI', 20, 20)
			if imgP is not None:
				cv2.putText(imgP, 'CAMERA: ' + cam_ID6, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.putText(imgP, 'LANE   : ' + lane_type6, (10,112), font, 2, (0,255,0), 4, cv2.LINE_AA)
				imgP = cv2.resize(imgP, (int(imgP.shape[1]/windowScale),int(imgP.shape[0]/windowScale)))
				imgPreview[int(imgP.shape[0]*2.5)+(padding*3):int(imgP.shape[0]*3.5)+(padding*3), int(imgP.shape[1]*2)+(padding*2):int(imgP.shape[1]*3)+(padding*2), :3] = imgP.copy()
				setPreview = True

		if not input_buf7.empty() and camDisp7==True:
			try:
				imgP = input_buf7.get().copy()
			except:
				print("input_buf7 timeout")
			if setROI7:
				imgSetROI = cv2.addWeighted(imgP.copy(), 1, imgMouse, 1, 0)
				cv2.putText(imgSetROI, 'CAMERA: ' + cam_ID7, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.imshow('SetROI', imgSetROI)
				#cv2.moveWindow('SetROI', 20, 20)
			if imgP is not None:
				cv2.putText(imgP, 'CAMERA: ' + cam_ID7, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.putText(imgP, 'LANE   : ' + lane_type7, (10,112), font, 2, (0,255,0), 4, cv2.LINE_AA)
				imgP = cv2.resize(imgP, (int(imgP.shape[1]/windowScale),int(imgP.shape[0]/windowScale)))
				imgPreview[int(imgP.shape[0]*2.5)+(padding*3):int(imgP.shape[0]*3.5)+(padding*3), int(imgP.shape[1]*3)+(padding*3):int(imgP.shape[1]*4)+(padding*3), :3] = imgP.copy()
				setPreview = True

		#--------------------------------------------------
		if window > 0:
			if not preview_buf0.empty() and camDisp0==True:
				imgP = preview_buf0.get().copy()
				if imgP is not None:
					cv2.putText(imgP, 'DETECT: ' + cam_ID0, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
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
					imgPreview[int(imgP.shape[0])+padding:int(imgP.shape[0]*2)+padding, :int(imgP.shape[1]), :3] = imgP.copy()
					setPreview = True

			if not preview_buf1.empty() and camDisp1==True:
				imgP = preview_buf1.get().copy()
				if imgP is not None:
					cv2.putText(imgP, 'DETECT: ' + cam_ID1, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
					cv2.putText(imgP, 'PLATE NUMBER: ' + detected_plate1, (128,int(imgP.shape[0])-32), font, 1.5, (255,255,255), 2, cv2.LINE_AA)
					[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[1], np.int32).copy()
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
					imgPreview[int(imgP.shape[0])+padding:int(imgP.shape[0]*2)+padding, int(imgP.shape[1])+padding:int(imgP.shape[1]*2)+padding, :3] = imgP.copy()
					setPreview = True

			if not preview_buf2.empty() and camDisp2==True:
				imgP = preview_buf2.get().copy()
				if imgP is not None:
					cv2.putText(imgP, 'DETECT: ' + cam_ID2, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
					cv2.putText(imgP, 'PLATE NUMBER: ' + detected_plate2, (128,int(imgP.shape[0])-32), font, 1.5, (255,255,255), 2, cv2.LINE_AA)
					[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[2], np.int32).copy()
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
					imgPreview[int(imgP.shape[0])+padding:int(imgP.shape[0]*2)+padding, int(imgP.shape[1]*2)+(padding*2):int(imgP.shape[1]*3)+(padding*2), :3] = imgP.copy()
					setPreview = True

			if not preview_buf3.empty() and camDisp3==True:
				imgP = preview_buf3.get().copy()
				if imgP is not None:
					cv2.putText(imgP, 'DETECT: ' + cam_ID3, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
					cv2.putText(imgP, 'PLATE NUMBER: ' + detected_plate3, (128,int(imgP.shape[0])-32), font, 1.5, (255,255,255), 2, cv2.LINE_AA)
					[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[3], np.int32).copy()
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
					imgPreview[int(imgP.shape[0])+padding:int(imgP.shape[0]*2)+padding, int(imgP.shape[1]*3)+(padding*3):int(imgP.shape[1]*4)+(padding*3), :3] = imgP.copy()
					setPreview = True

			if not preview_buf4.empty() and camDisp4==True:
				imgP = preview_buf4.get().copy()
				if imgP is not None:
					cv2.putText(imgP, 'DETECT: ' + cam_ID4, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
					cv2.putText(imgP, 'PLATE NUMBER: ' + detected_plate4, (128,int(imgP.shape[0])-32), font, 1.5, (255,255,255), 2, cv2.LINE_AA)
					[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[4], np.int32).copy()
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
					imgPreview[int(imgP.shape[0]*3.5)+(padding*4):int(imgP.shape[0]*4.5)+(padding*4), :int(imgP.shape[1]), :3] = imgP.copy()
					setPreview = True

			if not preview_buf5.empty() and camDisp5==True:
				imgP = preview_buf5.get().copy()
				if imgP is not None:
					cv2.putText(imgP, 'DETECT: ' + cam_ID5, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
					cv2.putText(imgP, 'PLATE NUMBER: ' + detected_plate5, (128,int(imgP.shape[0])-32), font, 1.5, (255,255,255), 2, cv2.LINE_AA)
					[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[5], np.int32).copy()
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
					imgPreview[int(imgP.shape[0]*3.5)+(padding*4):int(imgP.shape[0]*4.5)+(padding*4), int(imgP.shape[1])+padding:int(imgP.shape[1]*2)+padding, :3] = imgP.copy()
					setPreview = True

			if not preview_buf6.empty() and camDisp6==True:
				imgP = preview_buf6.get().copy()
				if imgP is not None:
					cv2.putText(imgP, 'DETECT: ' + cam_ID6, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
					cv2.putText(imgP, 'PLATE NUMBER: ' + detected_plate6, (128,int(imgP.shape[0])-32), font, 1.5, (255,255,255), 2, cv2.LINE_AA)
					[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[6], np.int32).copy()
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
					imgPreview[int(imgP.shape[0]*3.5)+(padding*4):int(imgP.shape[0]*4.5)+(padding*4), int(imgP.shape[1]*2)+(padding*2):int(imgP.shape[1]*3)+(padding*2), :3] = imgP.copy()
					setPreview = True

			if not preview_buf7.empty() and camDisp7==True:
				imgP = preview_buf7.get().copy()
				if imgP is not None:
					cv2.putText(imgP, 'DETECT: ' + cam_ID7, (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
					cv2.putText(imgP, 'PLATE NUMBER: ' + detected_plate7, (128,int(imgP.shape[0])-32), font, 1.5, (255,255,255), 2, cv2.LINE_AA)
					[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[7], np.int32).copy()
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
					imgPreview[int(imgP.shape[0]*3.5)+(padding*4):int(imgP.shape[0]*4.5)+(padding*4), int(imgP.shape[1]*3)+(padding*3):int(imgP.shape[1]*4)+(padding*3), :3] = imgP.copy()
					setPreview = True

		#--------------------------------------------------
		if window > 1:
			if plate_box_img0 is not None and detected_plate0 != '' and camDisp0==True:
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

			if plate_box_img1 is not None and detected_plate1 != '' and camDisp1==True:
				imgP = plate_box_img1
				if imgP.shape[0] > (h_std/windowScale/2) or imgP.shape[1] > (w_std/windowScale):
					imgP = cv2.resize(imgP, (int(imgP.shape[1]/2),int(imgP.shape[0]/2)))
				h_imgP, w_imgP = imgP.shape[:2]
				top = bottom = int(abs((h_std/windowScale/2) - h_imgP) / 2)
				left = right = int(abs((w_std/windowScale) - w_imgP) / 2)
				imgP = cv2.copyMakeBorder(imgP, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0,0,0))  # add black border
				imgPreview[int(h_std/windowScale*2)+(padding*2):int(h_std/windowScale*2)+(padding*2)+int(imgP.shape[0]), int(imgP.shape[1])+padding:int(imgP.shape[1]*2)+padding, :3] = imgP.copy()
				setPreview = True
				plateOff_t1 = time.time()
				plateFlag1 = True
			if plateFlag1 and ((plateOff_t1+3) < time.time()):
				imgP = np.zeros((int(h_std/windowScale/2), int(w_std/windowScale), 3), dtype=np.uint8)
				imgPreview[int(h_std/windowScale*2)+(padding*2):int(h_std/windowScale*2)+(padding*2)+int(imgP.shape[0]), int(imgP.shape[1])+padding:int(imgP.shape[1]*2)+padding, :3] = imgP.copy()
				setPreview = True
				plateFlag1 = False
				detected_plate1 = ''

			if plate_box_img2 is not None and detected_plate2 != '' and camDisp2==True:
				imgP = plate_box_img2
				if imgP.shape[0] > (h_std/windowScale/2) or imgP.shape[1] > (w_std/windowScale):
					imgP = cv2.resize(imgP, (int(imgP.shape[1]/2),int(imgP.shape[0]/2)))
				h_imgP, w_imgP = imgP.shape[:2]
				top = bottom = int(abs((h_std/windowScale/2) - h_imgP) / 2)
				left = right = int(abs((w_std/windowScale) - w_imgP) / 2)
				imgP = cv2.copyMakeBorder(imgP, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0,0,0))  # add black border
				imgPreview[int(h_std/windowScale*2)+(padding*2):int(h_std/windowScale*2)+(padding*2)+int(imgP.shape[0]), int(imgP.shape[1]*2)+(padding*2):int(imgP.shape[1]*3)+(padding*2), :3] = imgP.copy()
				setPreview = True
				plateOff_t2 = time.time()
				plateFlag2 = True
			if plateFlag2 and ((plateOff_t2+3) < time.time()):
				imgP = np.zeros((int(h_std/windowScale/2), int(w_std/windowScale), 3), dtype=np.uint8)
				imgPreview[int(h_std/windowScale*2)+(padding*2):int(h_std/windowScale*2)+(padding*2)+int(imgP.shape[0]), int(imgP.shape[1]*2)+(padding*2):int(imgP.shape[1]*3)+(padding*2), :3] = imgP.copy()
				setPreview = True
				plateFlag2 = False
				detected_plate2 = ''

			if plate_box_img3 is not None and detected_plate3 != '' and camDisp3==True:
				imgP = plate_box_img3
				if imgP.shape[0] > (h_std/windowScale/2) or imgP.shape[1] > (w_std/windowScale):
					imgP = cv2.resize(imgP, (int(imgP.shape[1]/2),int(imgP.shape[0]/2)))
				h_imgP, w_imgP = imgP.shape[:2]
				top = bottom = int(abs((h_std/windowScale/2) - h_imgP) / 2)
				left = right = int(abs((w_std/windowScale) - w_imgP) / 2)
				imgP = cv2.copyMakeBorder(imgP, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0,0,0))  # add black border
				imgPreview[int(h_std/windowScale*2)+(padding*2):int(h_std/windowScale*2)+(padding*2)+int(imgP.shape[0]), int(imgP.shape[1]*3)+(padding*3):int(imgP.shape[1]*4)+(padding*3), :3] = imgP.copy()
				setPreview = True
				plateOff_t3 = time.time()
				plateFlag3 = True
			if plateFlag3 and ((plateOff_t3+3) < time.time()):
				imgP = np.zeros((int(h_std/windowScale/2), int(w_std/windowScale), 3), dtype=np.uint8)
				imgPreview[int(h_std/windowScale*2)+(padding*2):int(h_std/windowScale*2)+(padding*2)+int(imgP.shape[0]), int(imgP.shape[1]*3)+(padding*3):int(imgP.shape[1]*4)+(padding*3), :3] = imgP.copy()
				setPreview = True
				plateFlag3 = False
				detected_plate3 = ''

			if plate_box_img4 is not None and detected_plate4 != '' and camDisp4==True:
				imgP = plate_box_img4
				if imgP.shape[0] > (h_std/windowScale/2) or imgP.shape[1] > (w_std/windowScale):
					imgP = cv2.resize(imgP, (int(imgP.shape[1]/2),int(imgP.shape[0]/2)))
				h_imgP, w_imgP = imgP.shape[:2]
				top = bottom = int(abs((h_std/windowScale/2) - h_imgP) / 2)
				left = right = int(abs((w_std/windowScale) - w_imgP) / 2)
				imgP = cv2.copyMakeBorder(imgP, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0,0,0))  # add black border
				imgPreview[int(h_std/windowScale*4.5)+(padding*5):int(h_std/windowScale*4.5)+(padding*5)+int(imgP.shape[0]), :int(imgP.shape[1]), :3] = imgP.copy()
				setPreview = True
				plateOff_t4 = time.time()
				plateFlag4 = True
			if plateFlag4 and ((plateOff_t4+3) < time.time()):
				imgP = np.zeros((int(h_std/windowScale/2), int(w_std/windowScale), 3), dtype=np.uint8)
				imgPreview[int(h_std/windowScale*4.5)+(padding*5):int(h_std/windowScale*4.5)+(padding*5)+int(imgP.shape[0]), :int(imgP.shape[1]), :3] = imgP.copy()
				setPreview = True
				plateFlag4 = False
				detected_plate4 = ''

			if plate_box_img5 is not None and detected_plate5 != '' and camDisp5==True:
				imgP = plate_box_img5
				if imgP.shape[0] > (h_std/windowScale/2) or imgP.shape[1] > (w_std/windowScale):
					imgP = cv2.resize(imgP, (int(imgP.shape[1]/2),int(imgP.shape[0]/2)))
				h_imgP, w_imgP = imgP.shape[:2]
				top = bottom = int(abs((h_std/windowScale/2) - h_imgP) / 2)
				left = right = int(abs((w_std/windowScale) - w_imgP) / 2)
				imgP = cv2.copyMakeBorder(imgP, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0,0,0))  # add black border
				imgPreview[int(h_std/windowScale*4.5)+(padding*5):int(h_std/windowScale*4.5)+(padding*5)+int(imgP.shape[0]), int(imgP.shape[1])+padding:int(imgP.shape[1]*2)+padding, :3] = imgP.copy()
				setPreview = True
				plateOff_t5 = time.time()
				plateFlag5 = True
			if plateFlag5 and ((plateOff_t5+3) < time.time()):
				imgP = np.zeros((int(h_std/windowScale/2), int(w_std/windowScale), 3), dtype=np.uint8)
				imgPreview[int(h_std/windowScale*4.5)+(padding*5):int(h_std/windowScale*4.5)+(padding*5)+int(imgP.shape[0]), int(imgP.shape[1])+padding:int(imgP.shape[1]*2)+padding, :3] = imgP.copy()
				setPreview = True
				plateFlag5 = False
				detected_plate5 = ''

			if plate_box_img6 is not None and detected_plate6 != '' and camDisp6==True:
				imgP = plate_box_img6
				if imgP.shape[0] > (h_std/windowScale/2) or imgP.shape[1] > (w_std/windowScale):
					imgP = cv2.resize(imgP, (int(imgP.shape[1]/2),int(imgP.shape[0]/2)))
				h_imgP, w_imgP = imgP.shape[:2]
				top = bottom = int(abs((h_std/windowScale/2) - h_imgP) / 2)
				left = right = int(abs((w_std/windowScale) - w_imgP) / 2)
				imgP = cv2.copyMakeBorder(imgP, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0,0,0))  # add black border
				imgPreview[int(h_std/windowScale*4.5)+(padding*5):int(h_std/windowScale*4.5)+(padding*5)+int(imgP.shape[0]), int(imgP.shape[1]*2)+(padding*2):int(imgP.shape[1]*3)+(padding*2), :3] = imgP.copy()
				setPreview = True
				plateOff_t6 = time.time()
				plateFlag6 = True
			if plateFlag6 and ((plateOff_t6+3) < time.time()):
				imgP = np.zeros((int(h_std/windowScale/2), int(w_std/windowScale), 3), dtype=np.uint8)
				imgPreview[int(h_std/windowScale*4.5)+(padding*5):int(h_std/windowScale*4.5)+(padding*5)+int(imgP.shape[0]), int(imgP.shape[1]*2)+(padding*2):int(imgP.shape[1]*3)+(padding*2), :3] = imgP.copy()
				setPreview = True
				plateFlag6 = False
				detected_plate6 = ''

			if plate_box_img7 is not None and detected_plate7 != '' and camDisp7==True:
				imgP = plate_box_img7
				if imgP.shape[0] > (h_std/windowScale/2) or imgP.shape[1] > (w_std/windowScale):
					imgP = cv2.resize(imgP, (int(imgP.shape[1]/2),int(imgP.shape[0]/2)))
				h_imgP, w_imgP = imgP.shape[:2]
				top = bottom = int(abs((h_std/windowScale/2) - h_imgP) / 2)
				left = right = int(abs((w_std/windowScale) - w_imgP) / 2)
				imgP = cv2.copyMakeBorder(imgP, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0,0,0))  # add black border
				imgPreview[int(h_std/windowScale*4.5)+(padding*5):int(h_std/windowScale*4.5)+(padding*5)+int(imgP.shape[0]), int(imgP.shape[1]*3)+(padding*3):int(imgP.shape[1]*4)+(padding*3), :3] = imgP.copy()
				setPreview = True
				plateOff_t7 = time.time()
				plateFlag7 = True
			if plateFlag7 and ((plateOff_t7+3) < time.time()):
				imgP = np.zeros((int(h_std/windowScale/2), int(w_std/windowScale), 3), dtype=np.uint8)
				imgPreview[int(h_std/windowScale*4.5)+(padding*5):int(h_std/windowScale*4.5)+(padding*5)+int(imgP.shape[0]), int(imgP.shape[1]*3)+(padding*3):int(imgP.shape[1]*4)+(padding*3), :3] = imgP.copy()
				setPreview = True
				plateFlag7 = False
				detected_plate7 = ''

		key = cv2.waitKey(1)
		#--------------------------------------------------
		if (key & 0xFF) == ord('!'):
			imgP = np.zeros((int(h_std/windowScale), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 0:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 1:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			imgPreview[:int(h_std/windowScale*2.5)+(padding*2), :int(imgP.shape[1]), :3] = imgP.copy()
			camDisp0 = not camDisp0
		if (key & 0xFF) == ord('@'):
			imgP = np.zeros((int(h_std/windowScale), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 0:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 1:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			imgPreview[:int(h_std/windowScale*2.5)+(padding*2), int(imgP.shape[1])+padding:int(imgP.shape[1]*2)+padding, :3] = imgP.copy()
			camDisp1 = not camDisp1
		if (key & 0xFF) == ord('#'):
			imgP = np.zeros((int(h_std/windowScale), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 0:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 1:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			imgPreview[:int(h_std/windowScale*2.5)+(padding*2), int(imgP.shape[1]*2)+(padding*2):int(imgP.shape[1]*3)+(padding*2), :3] = imgP.copy()
			camDisp2 = not camDisp2
		if (key & 0xFF) == ord('$'):
			imgP = np.zeros((int(h_std/windowScale), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 0:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 1:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			imgPreview[:int(h_std/windowScale*2.5)+(padding*2), int(imgP.shape[1]*3)+(padding*3):int(imgP.shape[1]*4)+(padding*3), :3] = imgP.copy()
			camDisp3 = not camDisp3
		if (key & 0xFF) == ord('%'):
			imgP = np.zeros((int(h_std/windowScale), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 0:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 1:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			imgPreview[int(h_std/windowScale*2.5)+(padding*3):int(h_std/windowScale*5)+(padding*5), :int(imgP.shape[1]), :3] = imgP.copy()
			camDisp4 = not camDisp4
		if (key & 0xFF) == ord('^'):
			imgP = np.zeros((int(h_std/windowScale), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 0:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 1:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			imgPreview[int(h_std/windowScale*2.5)+(padding*3):int(h_std/windowScale*5)+(padding*5), int(imgP.shape[1])+padding:int(imgP.shape[1]*2)+padding, :3] = imgP.copy()
			camDisp5 = not camDisp5
		if (key & 0xFF) == ord('&'):
			imgP = np.zeros((int(h_std/windowScale), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 0:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 1:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			imgPreview[int(h_std/windowScale*2.5)+(padding*3):int(h_std/windowScale*5)+(padding*5), int(imgP.shape[1]*2)+(padding*2):int(imgP.shape[1]*3)+(padding*2), :3] = imgP.copy()
			camDisp6 = not camDisp6
		if (key & 0xFF) == ord('*'):
			imgP = np.zeros((int(h_std/windowScale), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 0:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			if window > 1:
				imgP = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale), 3), dtype=np.uint8)
			imgPreview[int(h_std/windowScale*2.5)+(padding*3):int(h_std/windowScale*5)+(padding*5), int(imgP.shape[1]*3)+(padding*3):int(imgP.shape[1]*4)+(padding*3), :3] = imgP.copy()
			camDisp7 = not camDisp7

		if setPreview is True:
			cv2.imshow('PREVIEW', imgPreview)
			setPreview = False

		#--------------------------------------------------
		if (key & 0xFF) == ord('1'):
			setROI0 = not setROI0
			setROI1 = False
			setROI2 = False
			setROI3 = False
			setROI4 = False
			setROI5 = False
			setROI6 = False
			setROI7 = False
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
		if (key & 0xFF) == ord('2'):
			setROI1 = not setROI1
			setROI0 = False
			setROI2 = False
			setROI3 = False
			setROI4 = False
			setROI5 = False
			setROI6 = False
			setROI7 = False
			if setROI1:
				flagROI = 2
				cv2.namedWindow('SetROI')
				imgMouse[:] = 0
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[1], np.int32).copy()
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
		if (key & 0xFF) == ord('3'):
			setROI2 = not setROI2
			setROI0 = False
			setROI1 = False
			setROI3 = False
			setROI4 = False
			setROI5 = False
			setROI6 = False
			setROI7 = False
			if setROI2:
				flagROI = 3
				cv2.namedWindow('SetROI')
				imgMouse[:] = 0
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[2], np.int32).copy()
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
		if (key & 0xFF) == ord('4'):
			setROI3 = not setROI3
			setROI0 = False
			setROI1 = False
			setROI2 = False
			setROI4 = False
			setROI5 = False
			setROI6 = False
			setROI7 = False
			if setROI3:
				flagROI = 4
				cv2.namedWindow('SetROI')
				imgMouse[:] = 0
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[3], np.int32).copy()
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
		if (key & 0xFF) == ord('5'):
			setROI4 = not setROI4
			setROI0 = False
			setROI1 = False
			setROI2 = False
			setROI3 = False
			setROI5 = False
			setROI6 = False
			setROI7 = False
			if setROI4:
				flagROI = 5
				cv2.namedWindow('SetROI')
				imgMouse[:] = 0
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[4], np.int32).copy()
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
		if (key & 0xFF) == ord('6'):
			setROI5 = not setROI5
			setROI0 = False
			setROI1 = False
			setROI2 = False
			setROI3 = False
			setROI4 = False
			setROI6 = False
			setROI7 = False
			if setROI5:
				flagROI = 6
				cv2.namedWindow('SetROI')
				imgMouse[:] = 0
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[5], np.int32).copy()
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
		if (key & 0xFF) == ord('7'):
			setROI6 = not setROI6
			setROI0 = False
			setROI1 = False
			setROI2 = False
			setROI3 = False
			setROI4 = False
			setROI5 = False
			setROI7 = False
			if setROI6:
				flagROI = 7
				cv2.namedWindow('SetROI')
				imgMouse[:] = 0
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[6], np.int32).copy()
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
		if (key & 0xFF) == ord('8'):
			setROI7 = not setROI7
			setROI0 = False
			setROI1 = False
			setROI2 = False
			setROI3 = False
			setROI4 = False
			setROI5 = False
			setROI6 = False
			if setROI7:
				flagROI = 8
				cv2.namedWindow('SetROI')
				imgMouse[:] = 0
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[7], np.int32).copy()
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
			if flagROI == 3:
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[2], np.int32)
				text = f"[[{x1},{y1}], [{x2},{y2}], [{x3},{y3}], [{x4},{y4}]]"
				config.set('roi', 'ROI_input2', text)
				with open('config.ini', 'w') as configfile:
					config.write(configfile)
				config.read('./config.ini')
				cv2.putText(imgMouse, f"DETECTION ROI SAVED", (10,100), font, 1.5, color=(255,255,255), thickness=2)
				#print("2 SAVE", detection_ROI[2])
			if flagROI == 4:
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[3], np.int32)
				text = f"[[{x1},{y1}], [{x2},{y2}], [{x3},{y3}], [{x4},{y4}]]"
				config.set('roi', 'ROI_input3', text)
				with open('config.ini', 'w') as configfile:
					config.write(configfile)
				config.read('./config.ini')
				cv2.putText(imgMouse, f"DETECTION ROI SAVED", (10,100), font, 1.5, color=(255,255,255), thickness=2)
				#print("3 SAVE", detection_ROI[3])
			if flagROI == 5:
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[5], np.int32)
				text = f"[[{x1},{y1}], [{x2},{y2}], [{x3},{y3}], [{x4},{y4}]]"
				config.set('roi', 'ROI_input4', text)
				with open('config.ini', 'w') as configfile:
					config.write(configfile)
				config.read('./config.ini')
				cv2.putText(imgMouse, f"DETECTION ROI SAVED", (10,100), font, 1.5, color=(255,255,255), thickness=2)
				#print("4 SAVE", detection_ROI[4])
			if flagROI == 6:
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[6], np.int32)
				text = f"[[{x1},{y1}], [{x2},{y2}], [{x3},{y3}], [{x4},{y4}]]"
				config.set('roi', 'ROI_input5', text)
				with open('config.ini', 'w') as configfile:
					config.write(configfile)
				config.read('./config.ini')
				cv2.putText(imgMouse, f"DETECTION ROI SAVED", (10,100), font, 1.5, color=(255,255,255), thickness=2)
				#print("5 SAVE", detection_ROI[5])
			if flagROI == 7:
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[7], np.int32)
				text = f"[[{x1},{y1}], [{x2},{y2}], [{x3},{y3}], [{x4},{y4}]]"
				config.set('roi', 'ROI_input6', text)
				with open('config.ini', 'w') as configfile:
					config.write(configfile)
				config.read('./config.ini')
				cv2.putText(imgMouse, f"DETECTION ROI SAVED", (10,100), font, 1.5, color=(255,255,255), thickness=2)
				#print("6 SAVE", detection_ROI[6])
			if flagROI == 8:
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[8], np.int32)
				text = f"[[{x1},{y1}], [{x2},{y2}], [{x3},{y3}], [{x4},{y4}]]"
				config.set('roi', 'ROI_input7', text)
				with open('config.ini', 'w') as configfile:
					config.write(configfile)
				config.read('./config.ini')
				cv2.putText(imgMouse, f"DETECTION ROI SAVED", (10,100), font, 1.5, color=(255,255,255), thickness=2)
				#print("7 SAVE", detection_ROI[7])
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
				#imgPreview = np.zeros((int(h_std/windowScale), int(w_std/windowScale*4)+(padding*3), 3), dtype=np.uint8)
				imgPreview = np.zeros((int(h_std/windowScale*5)+(padding*5), int(w_std/windowScale*4)+(padding*3), 3), dtype=np.uint8)
			if window==1:
				#imgPreview = np.zeros((int(h_std/windowScale*2)+padding, int(w_std/windowScale*4)+(padding*3), 3), dtype=np.uint8)
				imgPreview = np.zeros((int(h_std/windowScale*5)+(padding*5), int(w_std/windowScale*4)+(padding*3), 3), dtype=np.uint8)
			if window==2:
				#imgPreview = np.zeros((int(h_std/windowScale*2.5)+(padding*2), int(w_std/windowScale*4)+(padding*3), 3), dtype=np.uint8)
				imgPreview = np.zeros((int(h_std/windowScale*5)+(padding*5), int(w_std/windowScale*4)+(padding*3), 3), dtype=np.uint8)
		#--------------------------------------------------
		'''
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
			'''
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
		elif flagROI == 3:
			[[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]] = np.array(detection_ROI[2], np.int32).copy()
			#print("1 DOWN", [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]])
		elif flagROI == 4:
			[[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]] = np.array(detection_ROI[3], np.int32).copy()
			#print("1 DOWN", [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]])
		elif flagROI == 5:
			[[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]] = np.array(detection_ROI[4], np.int32).copy()
			#print("1 DOWN", [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]])
		elif flagROI == 6:
			[[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]] = np.array(detection_ROI[5], np.int32).copy()
			#print("1 DOWN", [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]])
		elif flagROI == 7:
			[[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]] = np.array(detection_ROI[6], np.int32).copy()
			#print("1 DOWN", [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]])
		elif flagROI == 8:
			[[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]] = np.array(detection_ROI[7], np.int32).copy()
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
		elif flagROI == 3:
			detection_ROI[2] = [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]].copy()
			#print("2 UP", detection_ROI[2])
		elif flagROI == 4:
			detection_ROI[3] = [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]].copy()
			#print("3 UP", detection_ROI[3])
		elif flagROI == 5:
			detection_ROI[4] = [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]].copy()
			#print("4 UP", detection_ROI[4])
		elif flagROI == 6:
			detection_ROI[5] = [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]].copy()
			#print("5 UP", detection_ROI[5])
		elif flagROI == 7:
			detection_ROI[6] = [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]].copy()
			#print("6 UP", detection_ROI[6])
		elif flagROI == 8:
			detection_ROI[7] = [[mx1, my1], [mx2, my2], [mx3, my3], [mx4, my4]].copy()
			#print("7 UP", detection_ROI[7])

#--------------------------------------------------
def pathUpdate():
	global today_date, cr_path, lpd_path, vavc_path, plate_grading_path
	global full_path0, crop_path0, log_path0, xml_path0
	global full_path1, crop_path1, log_path1, xml_path1
	global full_path2, crop_path2, log_path2, xml_path2
	global full_path3, crop_path3, log_path3, xml_path3
	global full_path4, crop_path4, log_path4, xml_path4
	global full_path5, crop_path5, log_path5, xml_path5
	global full_path6, crop_path6, log_path6, xml_path6
	global full_path7, crop_path7, log_path7, xml_path7
	today_date = datetime.now().strftime("%Y%m%d")
	print(f"Program Directory Initialize... {today_date}")
	curr_path = os.path.dirname(os.path.realpath(__file__))
	cr_path = os.path.join(curr_path, 'trained_models', 'cr')
	lpd_path = os.path.join(curr_path, 'trained_models', 'lpd')
	vavc_path = os.path.join(curr_path, 'trained_models', 'vavc')
	plate_grading_path = os.path.join(curr_path, 'trained_models', 'plate_grading')
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

	xml_path0 = os.path.join(anpr_path, 'xml')
	if not os.path.isdir(xml_path0):
		os.makedirs(xml_path0, exist_ok=True)

	log_path0 = os.path.join(curr_path, 'log')
	if not os.path.isdir(log_path0):
		os.makedirs(log_path0, exist_ok=True)

	#--------------------------------------------------
	full_path1 = os.path.join(anpr_path, 'full')
	if not os.path.isdir(full_path1):
		os.makedirs(full_path1, exist_ok=True)

	crop_path1 = os.path.join(anpr_path, 'crop')
	if not os.path.isdir(crop_path1):
		os.makedirs(crop_path1, exist_ok=True)

	log_path1 = os.path.join(curr_path, 'log')
	if not os.path.isdir(log_path1):
		os.makedirs(log_path1, exist_ok=True)

	#--------------------------------------------------
	full_path2 = os.path.join(anpr_path, 'full')
	if not os.path.isdir(full_path2):
		os.makedirs(full_path2, exist_ok=True)

	crop_path2 = os.path.join(anpr_path, 'crop')
	if not os.path.isdir(crop_path2):
		os.makedirs(crop_path2, exist_ok=True)

	log_path2 = os.path.join(curr_path, 'log')
	if not os.path.isdir(log_path2):
		os.makedirs(log_path2, exist_ok=True)

	#--------------------------------------------------
	full_path3 = os.path.join(anpr_path, 'full')
	if not os.path.isdir(full_path3):
		os.makedirs(full_path3, exist_ok=True)

	crop_path3 = os.path.join(anpr_path, 'crop')
	if not os.path.isdir(crop_path3):
		os.makedirs(crop_path3, exist_ok=True)

	log_path3 = os.path.join(curr_path, 'log')
	if not os.path.isdir(log_path3):
		os.makedirs(log_path3, exist_ok=True)

	#--------------------------------------------------
	full_path4 = os.path.join(anpr_path, 'full')
	if not os.path.isdir(full_path4):
		os.makedirs(full_path4, exist_ok=True)

	crop_path4 = os.path.join(anpr_path, 'crop')
	if not os.path.isdir(crop_path4):
		os.makedirs(crop_path4, exist_ok=True)

	log_path4 = os.path.join(curr_path, 'log')
	if not os.path.isdir(log_path4):
		os.makedirs(log_path4, exist_ok=True)

	#--------------------------------------------------
	full_path5 = os.path.join(anpr_path, 'full')
	if not os.path.isdir(full_path5):
		os.makedirs(full_path5, exist_ok=True)

	crop_path5 = os.path.join(anpr_path, 'crop')
	if not os.path.isdir(crop_path5):
		os.makedirs(crop_path5, exist_ok=True)

	log_path5 = os.path.join(curr_path, 'log')
	if not os.path.isdir(log_path5):
		os.makedirs(log_path5, exist_ok=True)

	#--------------------------------------------------
	full_path6 = os.path.join(anpr_path, 'full')
	if not os.path.isdir(full_path6):
		os.makedirs(full_path6, exist_ok=True)

	crop_path6 = os.path.join(anpr_path, 'crop')
	if not os.path.isdir(crop_path6):
		os.makedirs(crop_path6, exist_ok=True)

	log_path6 = os.path.join(curr_path, 'log')
	if not os.path.isdir(log_path6):
		os.makedirs(log_path6, exist_ok=True)

	#--------------------------------------------------
	full_path7 = os.path.join(anpr_path, 'full')
	if not os.path.isdir(full_path7):
		os.makedirs(full_path7, exist_ok=True)

	crop_path7 = os.path.join(anpr_path, 'crop')
	if not os.path.isdir(crop_path7):
		os.makedirs(crop_path7, exist_ok=True)

	log_path7 = os.path.join(curr_path, 'log')
	if not os.path.isdir(log_path7):
		os.makedirs(log_path7, exist_ok=True)

	return

#--------------------------------------------------
def flaskFunc():
	app = Flask(__name__)
	app.debug = True

	def flaskStart():
		print("serveThread Starting...")
		#global serveThread
		#lock = threading.Lock()
		#with lock:
		try:
			serveThread = threading.Thread(target=serve, args=(app, ), kwargs={'host': host_IP, 'port': host_port, 'threads': 16})
			serveThread.daemon = True
			serveThread.start()
			#flaskThread = threading.Thread(target=lambda: app.run(host=host_IP, port=host_port, debug=True, use_reloader=False)).start()
		except:
			print("ERROR: Host IP and Port setting is not valid.")
			return

	def flaskShutdown():
		from win32api import GenerateConsoleCtrlEvent
		CTRL_C_EVENT = 0
		GenerateConsoleCtrlEvent(CTRL_C_EVENT, 0)

	def getMicrosecTimestamp():
		timestamp = datetime.now().strftime("%H:%M:%S.%f")
		return timestamp[:-3]

	@app.route('/', methods=['GET'])
	def home():
		return	f"<h1>Toll class programming API</h1> \
				<p>A prototype API for getting toll vehicle class.</p>"

	@app.route('/va/status', methods=['GET', 'POST'])
	def info():
		# response structure
		response = {
			'response': {
				'header': {
					'plaza': '',
					'lane': '',
					'timestamp': '',
				},
				'body': {
					'camera': '',
					'cr_model': '',
					'lpd_model': '',
					'vavc_model': '',
				}
			}
		}

		if request.method == 'POST':
			_time0 = time.time()

			time_start = getMicrosecTimestamp()
			print("\n")
			print("POST REQUEST:")
			content = request.get_json()
			#print(content)
			# request structure
			content_header = content['request']['header']
			plaza_loc = content_header['plaza']
			lane_loc = content_header['lane']
			time_rfid = content_header['timestamp']
			#print(f"[Request Header]")
			print(f"plaza: {plaza_loc}, lane: {lane_loc}, request_time: {time_rfid}")

			response['response']['header']['plaza'] = plaza_loc
			response['response']['header']['lane'] = lane_loc
			response['response']['header']['timestamp'] = time_rfid
			response['response']['body']['cr_model'] = os.path.basename(weights_recognize)
			response['response']['body']['lpd_model'] = os.path.basename(weights_detection)
			response['response']['body']['vavc_model'] = os.path.basename(weights_vavc)
			if NoSignalCam0:
				StatusCam = f"{cam_ID0} No Signal"
			else:
				StatusCam = f"{cam_ID0} Streaming"
			if NoSignalCam1:
				StatusCam = f"{cam_ID1} No Signal"
			else:
				StatusCam = f"{cam_ID1} Streaming"
			if NoSignalCam2:
				StatusCam = f"{cam_ID2} No Signal"
			else:
				StatusCam = f"{cam_ID2} Streaming"
			if NoSignalCam3:
				StatusCam = f"{cam_ID3} No Signal"
			else:
				StatusCam = f"{cam_ID3} Streaming"
			if NoSignalCam4:
				StatusCam = f"{cam_ID4} No Signal"
			else:
				StatusCam = f"{cam_ID4} Streaming"
			if NoSignalCam5:
				StatusCam = f"{cam_ID5} No Signal"
			else:
				StatusCam = f"{cam_ID5} Streaming"
			if NoSignalCam6:
				StatusCam = f"{cam_ID6} No Signal"
			else:
				StatusCam = f"{cam_ID6} Streaming"
			if NoSignalCam7:
				StatusCam = f"{cam_ID7} No Signal"
			else:
				StatusCam = f"{cam_ID7} Streaming"
			response['response']['body']['camera'] = StatusCam
			print("POST RESPONSE:")
			#print(response)
			#print(f"[Response Body]")
			print(f"cr model: {os.path.basename(weights_recognize)},")
			print(f"lpd model: {os.path.basename(weights_detection)},")
			print(f"vavc model: {os.path.basename(weights_vavc)},")
			print(f"camera: {StatusCam}")
		return jsonify(response)



#convert timestamp from base10 to base32
digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
bitsInLong = 64
def encode_base32 (dec,radix):    
	if(radix<2 or radix > len(digits)):
		raise Exception("radix should be in between 2 & 36")

	index = bitsInLong -1
	currentNumber:int = abs(dec)
	charArray = chararray(bitsInLong)
	result = ""
	while int(currentNumber) > 0 :              
		rem:int = int(currentNumber % radix) 
		charArray[index] =  digits[int(rem)]
		currentNumber = currentNumber / radix
		index -= 1 

	parts:chararray = charArray[index+1:bitsInLong:1]

	for x in parts: 
		if isinstance(x,str):
			result = result + x 
		else:
			result = result + x.decode('utf-8')

	return result

def decode_base32(encoded,radix):
	result = 0
	multiplier = 1
	if(radix<2 or radix > len(digits)):
		raise Exception("radix shoud be in between 2 & 36")
	
	if not encoded:
		return result

	encoded = encoded.upper()
	r_encoded = encoded[len(encoded):1:-1]

	index = 0
	for x in reversed(encoded):
		if x == 0 or x == '-':
			result = -result
			break

		num = digits.index(x)
		if num == -1:
			return result
			break

		result += num * multiplier
		multiplier *= radix
	return result






#### For VAVC - start ####
# Generate the xml files
def createXmlLabelFile(image_name, w, h):
	
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
	child_2.text = str(w)
	child_2 = SubElement(child, 'height')
	child_2.text = str(h)
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
	# xmin.text = str(bbox[0]).split('.')[1][:2]
	# xmin.text = str(bbox[0])

	ymin = SubElement(bndBox, 'ymin')
	ymin.text = str(int(bbox[1]))

	xmax = SubElement(bndBox, 'xmax')
	xmax.text = str(int(bbox[2]))

	ymax = SubElement(bndBox, 'ymax')
	ymax.text = str(int(bbox[3]))

def saveDataset_ANPR(letter_to_xml, crop_img, w, h):
	global image_label_num

	img_h, img_w, channels = crop_img.shape

	tree = createXmlLabelFile('low.jpg', img_w, img_h)

	for i, data in enumerate(letter_to_xml):
		bbox = data[1]
		# print(data[0], bbox)
	
		addLabel(tree, bbox, class_label=data[0])	# va_class
	

	xml_name = 'low.xml'
	cv2.imwrite('low.jpg', crop_img)

	writeXml(tree, xml_name)

def saveData_VAVC(h, w, img, det_bbox, det_clss, filename, src_fullpath):

	tree = createXmlLabelFile(filename + '.jpg', w, h)
	for bbox, clss in zip(det_bbox, det_clss):
		addLabel(tree, bbox, class_label=clss)	# va_class

	xml_name = src_fullpath + '/' + filename + '.xml'
	# cv2.imwrite(src_fullpath + '/' + filename + '.jpg', img)
	print('xml : ',xml_name)
	print('jpg : ',src_fullpath + '/' + filename + '.jpg')
	writeXml(tree, xml_name)

#### For VAVC - end ####

#==================================================
if __name__ == "__main__":
#--------------------------------------------------
	print("==================================================")

	input_buf0 = queue.Queue()
	input_buf1 = queue.Queue()
	input_buf2 = queue.Queue()
	input_buf3 = queue.Queue()
	input_buf4 = queue.Queue()
	input_buf5 = queue.Queue()
	input_buf6 = queue.Queue()
	input_buf7 = queue.Queue()
#	detect_buf0 = queue.Queue()
#	detect_buf1 = queue.Queue()
#	detect_buf2 = queue.Queue()
#	detect_buf3 = queue.Queue()
#	detect_buf4 = queue.Queue()
#	detect_buf5 = queue.Queue()
#	detect_buf6 = queue.Queue()
#	detect_buf7 = queue.Queue()
	detect_buf0 = collections.deque([])
	detect_buf1 = collections.deque([])
	detect_buf2 = collections.deque([])
	detect_buf3 = collections.deque([])
	detect_buf4 = collections.deque([])
	detect_buf5 = collections.deque([])
	detect_buf6 = collections.deque([])
	detect_buf7 = collections.deque([])
	detectFlag0 = False
	detectFlag1 = False
	detectFlag2 = False
	detectFlag3 = False
	detectFlag4 = False
	detectFlag5 = False
	detectFlag6 = False
	detectFlag7 = False
	preview_buf0 = queue.Queue()
	preview_buf1 = queue.Queue()
	preview_buf2 = queue.Queue()
	preview_buf3 = queue.Queue()
	preview_buf4 = queue.Queue()
	preview_buf5 = queue.Queue()
	preview_buf6 = queue.Queue()
	preview_buf7 = queue.Queue()
	crop_buf0 = queue.Queue()
	crop_buf1 = queue.Queue()
	crop_buf2 = queue.Queue()
	crop_buf3 = queue.Queue()
	crop_buf4 = queue.Queue()
	crop_buf5 = queue.Queue()
	crop_buf6 = queue.Queue()
	crop_buf7 = queue.Queue()
	plate_buf0 = queue.Queue()
	plate_buf1 = queue.Queue()
	plate_buf2 = queue.Queue()
	plate_buf3 = queue.Queue()
	plate_buf4 = queue.Queue()
	plate_buf5 = queue.Queue()
	plate_buf6 = queue.Queue()
	plate_buf7 = queue.Queue()
	anpr_queue0 = collections.deque([], 5)
	anpr_queue1 = collections.deque([], 5)
	anpr_queue2 = collections.deque([], 5)
	anpr_queue3 = collections.deque([], 5)
	anpr_queue4 = collections.deque([], 5)
	anpr_queue5 = collections.deque([], 5)
	anpr_queue6 = collections.deque([], 5)
	anpr_queue7 = collections.deque([], 5)
	anpr_data0 = []
	anpr_data1 = []
	anpr_data2 = []
	anpr_data3 = []
	anpr_data4 = []
	anpr_data5 = []
	anpr_data6 = []
	anpr_data7 = []
	plate_buf_list0 = []
	plate_buf_list1 = []
	plate_buf_list2 = []
	plate_buf_list3 = []
	plate_buf_list4 = []
	plate_buf_list5 = []
	plate_buf_list6 = []
	plate_buf_list7 = []
	curr_payment_data0 = []
	curr_payment_data1 = []
	curr_payment_data2 = []
	curr_payment_data3 = []
	curr_payment_data4 = []
	curr_payment_data5 = []
	curr_payment_data6 = []
	curr_payment_data7 = []
	curr_anpr0 = ''	# init curr_anpr0
	curr_anpr1 = ''	# init curr_anpr1
	curr_anpr2 = ''	# init curr_anpr2
	curr_anpr3 = ''	# init curr_anpr3
	curr_anpr4 = ''	# init curr_anpr4
	curr_anpr5 = ''	# init curr_anpr5
	curr_anpr6 = ''	# init curr_anpr6
	curr_anpr7 = ''	# init curr_anpr7
	prev_rfid0 = ''	# init prev_rfid0
	prev_rfid1 = ''	# init prev_rfid1
	prev_rfid2 = ''	# init prev_rfid2
	prev_rfid3 = ''	# init prev_rfid3
	prev_rfid4 = ''	# init prev_rfid4
	prev_rfid5 = ''	# init prev_rfid5
	prev_rfid6 = ''	# init prev_rfid6
	prev_rfid7 = ''	# init prev_rfid7

	prev_plateQ_0 = ''
	prev_plateQ_1 = ''
	prev_plateQ_2 = ''
	prev_plateQ_3 = ''
	prev_plateQ_4 = ''
	prev_plateQ_5 = ''
	prev_plateQ_6 = ''
	prev_plateQ_7 = ''

	prev_plateT_0 = ''
	prev_plateT_1 = ''
	prev_plateT_2 = ''
	prev_plateT_3 = ''
	prev_plateT_4 = ''
	prev_plateT_5 = ''
	prev_plateT_6 = ''
	prev_plateT_7 = ''

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
	#windowScale = 2.5
	windowScale = 4

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
	cameraFPS = CAMERA_FPS
	AvgTime = 0.0

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

	#Load toll input
	toll_input = config.get('toll', 'toll_input')

	# Load input mode
	input_type = config.get('src', 'input_type')
	input_mode = config.get('src_mode', 'input_mode')
	input_mode0 = config.get('src_mode', 'input_mode0')
	input_mode1 = config.get('src_mode', 'input_mode1')
	input_mode2 = config.get('src_mode', 'input_mode2')
	input_mode3 = config.get('src_mode', 'input_mode3')
	input_mode4 = config.get('src_mode', 'input_mode4')
	input_mode5 = config.get('src_mode', 'input_mode5')
	input_mode6 = config.get('src_mode', 'input_mode6')
	input_mode7 = config.get('src_mode', 'input_mode7')
	print(f"[Input] Type: {input_type} \nInput mode0: {input_mode0} \nInput mode1: {input_mode1} \nInput mode2: {input_mode2} \nInput mode3: {input_mode3} \nInput mode4: {input_mode4} \nInput mode5: {input_mode5} \nInput mode6: {input_mode6} \nInput mode7: {input_mode7}.")

	#Load lane type
	lane_type0 = config.get('lane_type', 'lane_type0')
	lane_type1 = config.get('lane_type', 'lane_type1')
	lane_type2 = config.get('lane_type', 'lane_type2')
	lane_type3 = config.get('lane_type', 'lane_type3')
	lane_type4 = config.get('lane_type', 'lane_type4')
	lane_type5 = config.get('lane_type', 'lane_type5')
	lane_type6 = config.get('lane_type', 'lane_type6')
	lane_type7 = config.get('lane_type', 'lane_type7')


	#ADQT API - data send to adqt service
	ADQT_API = "http://" + str(host_IP) + ":" + str(host_port) + "/api/anpr/trigger"

	# Load camera id
	# for image
	cam_ID = config.get('src_id', 'input_id')
	src_fullpath = config.get('src_input','input_src')
	print(f"[Image Source] CAM_ID: {cam_ID},  Link: {src_fullpath}.")
	# for video0
	cam_ID0 = config.get('src_id', 'input_id0')
	src_fullpath0 = config.get('src_input','input_src0')
	anpr0_enable = config.getboolean('src_input','input_anpr0')
	input_vavc0 = config.get('src_input','input_vavc0')
	print(f"[Camera Source] CAM_ID0: {cam_ID0},  Link: {src_fullpath0},  ANPR Enable: {anpr0_enable}, ANPR/VAVC: {input_vavc0}.")
	# for video1
	cam_ID1 = config.get('src_id', 'input_id1')
	src_fullpath1 = config.get('src_input','input_src1')
	anpr1_enable = config.getboolean('src_input','input_anpr1')
	input_vavc1 = config.get('src_input','input_vavc1')
	print(f"[Camera Source] CAM_ID1: {cam_ID1},  Link: {src_fullpath1},  ANPR Enable: {anpr1_enable}, ANPR/VAVC: {input_vavc1}.")
	# for video2
	cam_ID2 = config.get('src_id', 'input_id2')
	src_fullpath2 = config.get('src_input','input_src2')
	anpr2_enable = config.getboolean('src_input','input_anpr2')
	input_vavc2 = config.get('src_input','input_vavc2')
	print(f"[Camera Source] CAM_ID2: {cam_ID2},  Link: {src_fullpath2},  ANPR Enable: {anpr2_enable}, ANPR/VAVC: {input_vavc2}.")
	# for video3
	cam_ID3 = config.get('src_id', 'input_id3')
	src_fullpath3 = config.get('src_input','input_src3')
	anpr3_enable = config.getboolean('src_input','input_anpr3')
	input_vavc3 = config.get('src_input','input_vavc3')
	print(f"[Camera Source] CAM_ID3: {cam_ID3},  Link: {src_fullpath3},  ANPR Enable: {anpr3_enable}, ANPR/VAVC: {input_vavc3}.")
	# for video4
	cam_ID4 = config.get('src_id', 'input_id4')
	src_fullpath4 = config.get('src_input','input_src4')
	anpr4_enable = config.getboolean('src_input','input_anpr4')
	input_vavc4 = config.get('src_input','input_vavc4')
	print(f"[Camera Source] CAM_ID4: {cam_ID4},  Link: {src_fullpath4},  ANPR Enable: {anpr4_enable}, ANPR/VAVC: {input_vavc4}.")
	# for video5
	cam_ID5 = config.get('src_id', 'input_id5')
	src_fullpath5 = config.get('src_input','input_src5')
	anpr5_enable = config.getboolean('src_input','input_anpr5')
	input_vavc5 = config.get('src_input','input_vavc5')
	print(f"[Camera Source] CAM_ID5: {cam_ID5},  Link: {src_fullpath5},  ANPR Enable: {anpr5_enable}, ANPR/VAVC: {input_vavc5}.")
	# for video6
	cam_ID6 = config.get('src_id', 'input_id6')
	src_fullpath6 = config.get('src_input','input_src6')
	anpr6_enable = config.getboolean('src_input','input_anpr6')
	input_vavc6 = config.get('src_input','input_vavc6')
	print(f"[Camera Source] CAM_ID6: {cam_ID6},  Link: {src_fullpath6},  ANPR Enable: {anpr6_enable}, ANPR/VAVC: {input_vavc6}.")
	# for video7
	cam_ID7 = config.get('src_id', 'input_id7')
	src_fullpath7 = config.get('src_input','input_src7')
	anpr7_enable = config.getboolean('src_input','input_anpr7')
	input_vavc7 = config.get('src_input','input_vavc7')
	print(f"[Camera Source] CAM_ID7: {cam_ID7},  Link: {src_fullpath7},  ANPR Enable: {anpr7_enable}, ANPR/VAVC: {input_vavc7}.")

	# Load detection ROI
	# for video0
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
	# for video1
	detection_ROI.append(json.loads(config.get('roi', 'ROI_input1')))
	print(f"[CAM_ID1 ROI] polygon: {detection_ROI[1]}.")
	imgROI1 = np.zeros((h_std, w_std, 1), dtype=np.uint8)
	[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[1], np.int32).copy()
	if x1>=x2 or x4>=x1 or y2>=y3 or y1>=y4:
		print("ERROR: setting.ini [roi] ROI_Input1 [[x1,y1], [x2,y3], [x3,y3], [x4,y4]] condition x2>x1, x3>x4, y3>y2 and y4>y1.")
	if x3<x2 and x4<=x1:
		polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x4, y4]], np.int32).copy()
	elif x3>=x2 and x4>x1:
		polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x1, y2]], np.int32).copy()
	elif x3>=x2 and x4<=x1:
		polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x4, y4]], np.int32).copy()
	elif x3<x2 and x4>x1:
		polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x1, y2]], np.int32).copy()
	cv2.fillPoly(imgROI1, [polygon], color=255)
	# for video2
	detection_ROI.append(json.loads(config.get('roi', 'ROI_input2')))
	print(f"[CAM_ID2 ROI] polygon: {detection_ROI[2]}.")
	imgROI2 = np.zeros((h_std, w_std, 1), dtype=np.uint8)
	[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[2], np.int32).copy()
	if x1>=x2 or x4>=x1 or y2>=y3 or y1>=y4:
		print("ERROR: setting.ini [roi] ROI_Input2 [[x1,y1], [x2,y3], [x3,y3], [x4,y4]] condition x2>x1, x3>x4, y3>y2 and y4>y1.")
	if x3<x2 and x4<=x1:
		polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x4, y4]], np.int32).copy()
	elif x3>=x2 and x4>x1:
		polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x1, y2]], np.int32).copy()
	elif x3>=x2 and x4<=x1:
		polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x4, y4]], np.int32).copy()
	elif x3<x2 and x4>x1:
		polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x1, y2]], np.int32).copy()
	cv2.fillPoly(imgROI2, [polygon], color=255)
	# for video3
	detection_ROI.append(json.loads(config.get('roi', 'ROI_input3')))
	print(f"[CAM_ID3 ROI] polygon: {detection_ROI[3]}.")
	imgROI3 = np.zeros((h_std, w_std, 1), dtype=np.uint8)
	[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[3], np.int32).copy()
	if x1>=x2 or x4>=x1 or y2>=y3 or y1>=y4:
		print("ERROR: setting.ini [roi] ROI_Input3 [[x1,y1], [x2,y3], [x3,y3], [x4,y4]] condition x2>x1, x3>x4, y3>y2 and y4>y1.")
	if x3<x2 and x4<=x1:
		polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x4, y4]], np.int32).copy()
	elif x3>=x2 and x4>x1:
		polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x1, y2]], np.int32).copy()
	elif x3>=x2 and x4<=x1:
		polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x4, y4]], np.int32).copy()
	elif x3<x2 and x4>x1:
		polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x1, y2]], np.int32).copy()
	cv2.fillPoly(imgROI3, [polygon], color=255)
	# for video4
	detection_ROI.append(json.loads(config.get('roi', 'ROI_input4')))
	print(f"[CAM_ID4 ROI] polygon: {detection_ROI[4]}.")
	imgROI4 = np.zeros((h_std, w_std, 1), dtype=np.uint8)
	[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[4], np.int32).copy()
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
	cv2.fillPoly(imgROI4, [polygon], color=255)
	# for video5
	detection_ROI.append(json.loads(config.get('roi', 'ROI_input5')))
	print(f"[CAM_ID5 ROI] polygon: {detection_ROI[5]}.")
	imgROI5 = np.zeros((h_std, w_std, 1), dtype=np.uint8)
	[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[5], np.int32).copy()
	if x1>=x2 or x4>=x1 or y2>=y3 or y1>=y4:
		print("ERROR: setting.ini [roi] ROI_Input1 [[x1,y1], [x2,y3], [x3,y3], [x4,y4]] condition x2>x1, x3>x4, y3>y2 and y4>y1.")
	if x3<x2 and x4<=x1:
		polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x4, y4]], np.int32).copy()
	elif x3>=x2 and x4>x1:
		polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x1, y2]], np.int32).copy()
	elif x3>=x2 and x4<=x1:
		polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x4, y4]], np.int32).copy()
	elif x3<x2 and x4>x1:
		polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x1, y2]], np.int32).copy()
	cv2.fillPoly(imgROI5, [polygon], color=255)
	# for video6
	detection_ROI.append(json.loads(config.get('roi', 'ROI_input6')))
	print(f"[CAM_ID6 ROI] polygon: {detection_ROI[6]}.")
	imgROI6 = np.zeros((h_std, w_std, 1), dtype=np.uint8)
	[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[6], np.int32).copy()
	if x1>=x2 or x4>=x1 or y2>=y3 or y1>=y4:
		print("ERROR: setting.ini [roi] ROI_Input2 [[x1,y1], [x2,y3], [x3,y3], [x4,y4]] condition x2>x1, x3>x4, y3>y2 and y4>y1.")
	if x3<x2 and x4<=x1:
		polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x4, y4]], np.int32).copy()
	elif x3>=x2 and x4>x1:
		polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x1, y2]], np.int32).copy()
	elif x3>=x2 and x4<=x1:
		polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x4, y4]], np.int32).copy()
	elif x3<x2 and x4>x1:
		polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x1, y2]], np.int32).copy()
	cv2.fillPoly(imgROI6, [polygon], color=255)
	# for video7
	detection_ROI.append(json.loads(config.get('roi', 'ROI_input7')))
	print(f"[CAM_ID7 ROI] polygon: {detection_ROI[7]}.")
	imgROI7 = np.zeros((h_std, w_std, 1), dtype=np.uint8)
	[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[7], np.int32).copy()
	if x1>=x2 or x4>=x1 or y2>=y3 or y1>=y4:
		print("ERROR: setting.ini [roi] ROI_Input3 [[x1,y1], [x2,y3], [x3,y3], [x4,y4]] condition x2>x1, x3>x4, y3>y2 and y4>y1.")
	if x3<x2 and x4<=x1:
		polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x4, y4]], np.int32).copy()
	elif x3>=x2 and x4>x1:
		polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x1, y2]], np.int32).copy()
	elif x3>=x2 and x4<=x1:
		polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x4, y4]], np.int32).copy()
	elif x3<x2 and x4>x1:
		polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x1, y2]], np.int32).copy()
	cv2.fillPoly(imgROI7, [polygon], color=255)
	'''
	# Load email
	smtp_host = config.get('email', 'smtp_host')
	smtp_port = int(config.getint('email', 'smtp_port'))
	email_from = config.get('email', 'email_from')
	email_password = config.get('email', 'email_password')
	email_to = eval(config.get('email', 'email_to'))
	#print(f"smtp={smtp_host}, port={smtp_port}")
	#print(f"from={email_from}, pw={email_password}")
	#print(f"to={', '.join(email_to)}")
	'''

	# Directory
	pathUpdate()
	# Load weight model
	set_logging()
	'''
	device = select_device('0')
	#device = select_device('cpu')
	half = device.type != 'cpu'  # half precision only supported on CUDA
	'''
	device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
	print(f'device = {device}')
	if not device == 'cpu':
		print(f'current_device = {torch.cuda.current_device()}')
		device_count = torch.cuda.device_count()
		print(f'device_count = {device_count}')
		for i in range(device_count):
			p = torch.cuda.get_device_properties(i)
			print(f'CUDA:{i} ({p.name}, version={p.major}.{p.minor}, {p.total_memory / 1024 ** 2:.0f}MB, multi_processor_count={p.multi_processor_count})')
		if torch.backends.cudnn.is_available():
			torch.backends.cudnn.benchmark = True  # benchmark multiple convolution algorithms and select the fastest
			print(f'cudnn_enable={torch.backends.cudnn.enabled}, cudnn_version={torch.backends.cudnn.version()}, cudnn_benchmark={torch.backends.cudnn.benchmark}')
	half = device.type != 'cpu'  # half precision only supported on CUDA
	print(f'half (use "cuda"=float16 if True else "cpu"=float32) = {half}')

	# Load model plate detection
	existing_weights_detection = ''
	if(TSRT):
		existing_weights_detection = weights_detectionUpdateTRT(device, existing_weights_detection, DATA_YAML)
	else:
		existing_weights_detection = weights_detectionUpdate(device, existing_weights_detection)
	# Load model plate recognize
	existing_weights_recognize = ''
	if(TSRT):
		existing_weights_recognize = weights_recognizeUpdateTRT(device, existing_weights_recognize, DATA_YAML_CR)
	else:
		existing_weights_recognize = weights_recognizeUpdate(device, existing_weights_recognize)
	# Load model video analytic vehicle classification
	existing_weights_vavc = ''
	existing_weights_vavc = weights_vavcUpdate(device, existing_weights_vavc)


	# Load model plate plate_grading
	existing_weights_plate_grading = ''
	if(TSRT):
		existing_weights_plate_grading = weights_plate_gradingUpdateTRT(device, existing_weights_plate_grading, DATA_YAML_plate_grading)
	else:
		existing_weights_plate_grading = weights_plate_gradingUpdate(device, existing_weights_plate_grading)


#==================================================

	Analysis_folder = False
	save_xml_ANPR = False
	save_xml_VAVC = True
	plate_grading = False


	if input_type == 'image' and Analysis_folder is True:

		#parameter
		ANPR_ = False
		VAVC_ = False


		#analysis process
									# to check if the plate is good or bad
		analysis_by_confidence_level = False
		move_file_to_confidence_level_folder = False

		# initialize
		not_valid_img = False
		count_less_30 = 0
		count_30_60 = 0
		count_60_65 = 0 
		count_66_70 = 0
		count_71_75 = 0
		count_76_80 = 0
		count_81_85 = 0
		count_86_90 = 0
		count_91_95 = 0
		count_96 = 0

		lowest_character_conflvl = ""
		min_conf_lvl = 0.0
		min_character = "0"

		
		curr_path = os.path.dirname(os.path.realpath(__file__))	#current path
		analysis_path = os.path.join(curr_path, "analysis_conf_level")
		date_path = os.path.join(analysis_path, (date.today()).strftime("%d-%m-%Y"))
		

		print("==================================================")
		print("Image Detection Start.")
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.namedWindow('PREVIEW')
		cv2.moveWindow('PREVIEW', 0, 0)
		file_list = os.listdir(src_fullpath)

		counter = 1
		
		for filename in sorted(file_list):
			filename_split = filename.split('.')
			print(filename_split)
			# if filename.endswith(".jpg") and filename[33:35] == "01":
			if filename.endswith(".jpg"):# and filename_split[4] == "01":
				detected_plate0 = ""

				if today_date != datetime.now().strftime("%Y%m%d"):
					pathUpdate()
				if not os.path.splitext(filename)[-1].lower() in img_formats:
					break
				print("==================================================")
				full_filename = os.path.join(src_fullpath, filename)
				print('counter', full_filename)

				tracking_t0 = time.time()
				capF = cv2.imread(full_filename)
				height, width = capF.shape[:2]
				scaleRatio = min(w_std/width, h_std/height)
				capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
				h_capF, w_capF = capF.shape[:2]
				top = bottom = int(abs(h_std - h_capF) / 2)
				left = right = int(abs(w_std - w_capF) / 2)
				capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border

				img = capF.copy()
				img_resize = capF.copy()

				stride = max(int(model_detection.stride), 32)  # model stride=32
				imgsz = [640, 640]
				imgsz = check_img_size(imgsz, s=stride)  # check image size
				capF_resize = ANPR.letterbox(img_resize, imgsz, stride=stride, auto=False)[0]            #0.0004 - 0.0006
				capF_resize = capF_resize[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
				capF_resize = np.ascontiguousarray(capF_resize)
				## testing code
				capF_resize = torch.from_numpy(capF_resize)
				capF_resize = capF_resize.half() if half else capF_resize.float()  # uint8 to fp16/32
				capF_resize = capF_resize.to(device)
				capF_resize /= 255.0  # 0~255 to 0.0~1.0
				if capF_resize.ndimension() == 3:
					capF_resize = capF_resize.unsqueeze(0)
				

				try:
					# print("filename",filename[33:35])
					# print("do crop")
					crop_img, plate_conf0 = ANPR.runPlateDetection(model_detection, half, device, capF_resize, img, imgROI0)

					try:
						cropped_img = ANPR.correct_skew(crop_img)
						print("Skewing for crop image ...")
					except:
						print("ERROR|EXCEPTION: Skewing error.")
						not_valid_img = True
						print("not_valid_img true ", not_valid_img)
						pass		

					#-----------------------------------------------------------------------------------------------------------------------------
					



						
						



					#-------------------------------------------------------------------------------------------------------------------------------
					if ANPR_ is True:			#do anpr
						
						detected_plate, avg_conf, lowest_character_conflvl, min_conf_lvl, min_character, bbox_l = ANPR.recognize_plate(model_recognize, half, device, cropped_img)  		# recognize plate number
						
						detected_plate0 = detected_plate
						print("\n[Processing] : ")
						print("avg_conf",avg_conf)
						if avg_conf == "":
							avg_conf = 0.0

						print("Plate Detected : ",detected_plate)
						print("lowest_character_conflvl : ", lowest_character_conflvl)
						print("min_conf_lvl : ", min_conf_lvl)
						print("min_character : ", min_character)
						print("\n")
						

					if VAVC_0 is True:			#do VAVC
						detected_frame0, predicted_vehicle_data0, crop_img0, plate_conf0, vavc_conf, vavc_detection_class = VAVC.vehicleDetection(model_vavc, half, device, img, imgROI0)
						print(" vavc_conf : ", vavc_conf)
						if vavc_conf == "":
							vavc_conf = 0.0
						print("vavc_detection_class : ", vavc_detection_class)


				except:
					cropped_img = None
					detected_plate = ''
					avg_conf = 0.0
					# print("Exception : Plate not crop. Image may not clear.")

				#do analysis by confidence level
				# print('lowest_character_conflvl', lowest_character_conflvl)

				if analysis_by_confidence_level is True:
					
					# create folder by confidence level, folder based on confidence level

					
					#1. create root folder
					#2. create date folder
					#3. create conf lvl folder
					 
					
					if not os.path.isdir(analysis_path):
						os.makedirs(analysis_path)
						
					# daily_folder = os.path.join(analysis_path, analysis_path + '/' + (date.today()).strftime("%d-%m-%Y"))
					# print('daily_folder',daily_folder)
					# if not os.path.isdir(daily_folder):
					# 	os.makedirs(daily_folder)

					
					date_path = os.path.join(analysis_path, (date.today()).strftime("%d-%m-%Y"))
					less_30 = os.path.join(date_path, "less_30")
					f_30_60 = os.path.join(date_path, "0.30_0.60")
					f_60_65 = os.path.join(date_path, "0.60_0.65 ")
					f_66_70 = os.path.join(date_path,"0.66_0.70")
					f_71_75 = os.path.join(date_path,"0.71_0.75")
					f_76_80 = os.path.join(date_path,"0.76_0.80")
					f_81_85 = os.path.join(date_path,"0.81_0.85")
					f_86_90 = os.path.join(date_path,"0.86_0.90")
					f_91_95 = os.path.join(date_path,"0.91_0.95")
					f_95 = os.path.join(date_path, "0.96")
					f_broken = os.path.join(date_path, "broken")
					
					
					if not os.path.isdir(date_path):
						os.makedirs(date_path)
					if not os.path.isdir(less_30):
						os.makedirs(less_30)
					if not os.path.isdir(f_30_60):
						os.makedirs(f_30_60)
					if not os.path.isdir(f_60_65):
						os.makedirs(f_60_65)
					if not os.path.isdir(f_66_70):
						os.makedirs(f_66_70)
					if not os.path.isdir(f_71_75):
						os.makedirs(f_71_75)
					if not os.path.isdir(f_76_80):
						os.makedirs(f_76_80)
					if not os.path.isdir(f_81_85):
						os.makedirs(f_81_85)
					if not os.path.isdir(f_86_90):
						os.makedirs(f_86_90)
					if not os.path.isdir(f_91_95):
						os.makedirs(f_91_95)
					if not os.path.isdir(f_95):
						os.makedirs(f_95)
					if not os.path.isdir(f_broken):
						os.makedirs(f_broken)

					
					filename_w_worst_value = str(os.path.splitext(filename)[0]+"_"+lowest_character_conflvl)+".jpg"
					print('filename_w_worst_value', filename_w_worst_value)
					

					if move_file_to_confidence_level_folder is True:		#move file to folder confidence level
						

						
						# for crop in sorted(file_list):
						# 	# print("crop name : ", crop)
						# 	crop_split = crop.split('.')
						# 	# print("crop_split[4]",crop_split[4])
						# 	if crop_split[4] == "02":
						# 		if crop[:32]==filename[:32]:
						# 			# print("crop[32]",crop[:32])
						# 			# print("filename[32]",filename[:32])
						# 			crop_img = crop
						# 			crop_img_w_worst_value = str(os.path.splitext(crop_img)[0]+"_"+lowest_character_conflvl)+".jpg"
						# 		else:
						# 			pass

						# print(f"conf level before formula {min_conf_lvl} type : {type(min_conf_lvl)}")
						int_min_conf_lvl = str(int(min_conf_lvl*100))
						int_min_conf_lvl = int(int_min_conf_lvl.ljust(2,'0'))
						print(f"type : {type(int_min_conf_lvl)}, value : {int_min_conf_lvl}")

						#move to folders
						src_fullpath_filename = os.path.join(src_fullpath,filename)
						src_fullpath_crop = os.path.join(src_fullpath,'crop_img')
						# print("crop_img",crop_img)
						# print("src_fullpath_crop : ",src_fullpath_crop)

						print("\n")

						if int_min_conf_lvl < 30:
							if os.path.exists(src_fullpath_filename):
								shutil.move(src_fullpath_filename, os.path.join(less_30, filename_w_worst_value))
								print(f"Successfull move & rename : \n{less_30}/{filename_w_worst_value}")

							# if os.path.exists(src_fullpath_crop):
							# 	shutil.move(src_fullpath_crop, os.path.join(less_30, crop_img_w_worst_value))
							# 	print(f"{less_30}/{crop_img_w_worst_value}")
							else:
								print("No crop image")
							count_less_30+=1
							

						if int_min_conf_lvl in range(30,61):
							if os.path.exists(src_fullpath_filename):
								shutil.move(src_fullpath_filename, os.path.join(f_30_60, filename_w_worst_value))
								print(f"Successfull move & rename : \n{f_30_60}/{filename_w_worst_value}")

							# if os.path.exists(src_fullpath_crop):
							# 	shutil.move(src_fullpath_crop, os.path.join(f_30_60, crop_img_w_worst_value))
							# 	print(f"{less_30}/{crop_img_w_worst_value}")
							else:
								print("No crop image")
							count_30_60+=1 
							

						if int_min_conf_lvl in range(61,66):
							if os.path.exists(src_fullpath_filename):
								shutil.move(src_fullpath_filename, os.path.join(f_60_65, filename_w_worst_value))
								print(f"Successfull move & rename : \n{f_60_65}/{filename_w_worst_value}")

							# if os.path.exists(src_fullpath_crop):
							# 	shutil.move(src_fullpath_crop, os.path.join(f_60_65, crop_img_w_worst_value))
							# 	print(f"{less_30}/{crop_img_w_worst_value}")
							else:
								print("No crop image")
							count_60_65+=1 
							

						if int_min_conf_lvl in range(66,71):
							if os.path.exists(src_fullpath_filename):
								shutil.move(src_fullpath_filename, os.path.join(f_66_70, filename_w_worst_value))
								print(f"Successfull move & rename : \n{f_66_70}/{filename_w_worst_value}")

							# if os.path.exists(src_fullpath_crop):
							# 	shutil.move(src_fullpath_crop, os.path.join(f_66_70, crop_img_w_worst_value))
							# 	print(f"{less_30}/{crop_img_w_worst_value}")
							else:
								print("No crop image")
							count_66_70+=1
							

						if int_min_conf_lvl in range(71,76):
							if os.path.exists(src_fullpath_filename):
								shutil.move(src_fullpath_filename, os.path.join(f_71_75, filename_w_worst_value))
								print(f"Successfull move & rename : \n{f_71_75}/{filename_w_worst_value}")

							# if os.path.exists(src_fullpath_crop):
							# 	shutil.move(src_fullpath_crop, os.path.join(f_71_75, crop_img_w_worst_value))
							# 	print(f"{less_30}/{crop_img_w_worst_value}")
							else:
								print("No crop image")
							count_71_75+=1
							

						if int_min_conf_lvl in range(76,81):
							if os.path.exists(src_fullpath_filename):
								shutil.move(src_fullpath_filename, os.path.join(f_76_80, filename_w_worst_value))
								print(f"Successfull move & rename : \n{f_76_80}/{filename_w_worst_value}")

							# if os.path.exists(src_fullpath_crop):
							# 	shutil.move(src_fullpath_crop, os.path.join(f_76_80, crop_img_w_worst_value))
							# 	print(f"{less_30}/{crop_img_w_worst_value}")
							else:
								print("No crop image")
							count_76_80+=1
							

						if int_min_conf_lvl in range(81,86):
							if os.path.exists(src_fullpath_filename):
								shutil.move(src_fullpath_filename, os.path.join(f_81_85, filename_w_worst_value))
								print(f"Successfull move & rename : \n{f_81_85}/{filename_w_worst_value}")

							# if os.path.exists(src_fullpath_crop):
							# 	shutil.move(src_fullpath_crop, os.path.join(f_81_85, crop_img_w_worst_value))
							# 	print(f"{less_30}/{crop_img_w_worst_value}")
							else:
								print("No crop image")
							count_81_85+=1
							

						if int_min_conf_lvl in range(86,91):
							print("yes")
							if os.path.exists(src_fullpath_filename):
								shutil.move(src_fullpath_filename, os.path.join(f_86_90, filename_w_worst_value))
								print(f"Successfull move & rename : \n{f_86_90}/{filename_w_worst_value}")

							if os.path.exists(src_fullpath_crop):
								shutil.move(src_fullpath_crop, os.path.join(f_86_90, crop_img_w_worst_value))
								print(f"{less_30}/{crop_img_w_worst_value}")
							else:
								print("No crop image")
							count_86_90+=1
							

						if int_min_conf_lvl in range(91,96):
							if os.path.exists(src_fullpath_filename):
								shutil.move(src_fullpath_filename, os.path.join(f_91_95, filename_w_worst_value))
								print(f"Successfull move & rename : \n{f_91_95}/{filename_w_worst_value}")

							# if os.path.exists(src_fullpath_crop):
							# 	shutil.move(src_fullpath_crop, os.path.join(f_91_95, crop_img_w_worst_value))
							# 	print(f"{less_30}/{crop_img_w_worst_value}")
							else:
								print("No crop image")
							count_91_95+=1
							

						if int_min_conf_lvl >= 96:
							if os.path.exists(src_fullpath_filename):
								shutil.move(src_fullpath_filename, os.path.join(f_95, filename_w_worst_value))
								print(f"Successfull move & rename : \n{f_95}/{filename_w_worst_value}")
		
							# if os.path.exists(src_fullpath_crop):
							# 	shutil.move(src_fullpath_crop, os.path.join(f_95, crop_img_w_worst_value))
							# 	print(f"{less_30}/{crop_img_w_worst_value}")
							else:
								print("No crop image")
							count_96+=1
							
						print("\n")
						# time.sleep(0.01)
				

						

						
						#make csv
						analaysis_log = os.path.join(date_path,"analysis_log.csv")
						# header = 
						data = [filename_w_worst_value,min_character, min_conf_lvl]

						if not os.path.isfile(analaysis_log):
							with open(analaysis_log, mode='w', newline='') as csvfile:
								writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
								
								# writer.writerow(['','',''])
								# writer.writerow(['','',''])
								# writer.writerow(['','',''])
								# writer.writerow(['','',''])
								# writer.writerow(['','',''])
								# writer.writerow(['','',''])
								# writer.writerow(['','',''])
								# writer.writerow(['','',''])
								# writer.writerow(['','',''])
								# writer.writerow(['','',''])
								writer.writerow(["Image", "worst_conf_level", "worst_character"])
								
						savecsv = True
						while savecsv:
							with open(analaysis_log, mode='a', newline='') as csvfile:
								writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
								writer.writerow([filename_w_worst_value, min_conf_lvl,min_character])
							savecsv = False
			
				

				
				cv2.putText(img, f'PLATE NUMBER: {detected_plate0}', (128,int(img.shape[0])-32), font, 1.5, (255,255,255), 2, cv2.LINE_AA)
				# cv2.putText(img, 'PLATE NUMBER: ' + detected_plate, (128,int(img.shape[0])-32), font, 1.5, (255,255,255), 2, cv2.LINE_AA)
				[[x1, y1], [x2, y2], [x3, y3], [x4, y4]] = np.array(detection_ROI[0], np.int32).copy()
				if x3<x2 and x4<=x1:
					polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x4, y4]], np.int32)
				elif x3>=x2 and x4>x1:
					polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x1, y2]], np.int32)
				elif x3>=x2 and x4<=x1:
					polygon = np.array([[x1, y1], [x2, y1], [x3, y4], [x3, y3], [x4, y3], [x4, y4]], np.int32)
				elif x3<x2 and x4>x1:
					polygon = np.array([[x1, y1], [x2, y1], [x2, y2], [x3, y3], [x4, y3], [x1, y2]], np.int32)
				cv2.polylines(img, [polygon], isClosed=True, color=(0,255,0), thickness=2)
				# cv2.imshow('PREVIEW', cv2.resize(img, (int(img.shape[1]/windowScale),int(img.shape[0]/windowScale)))) #ori from dayah
				cv2.imshow('PREVIEW', cv2.resize(img, (800,650)))
				print(f"cam_ID: {cam_ID},  Plate Detection and Recognite Time: {round((time.time() - tracking_t0),3)}")
				
				q_key = cv2.waitKey(100) & 0b11111111 #quit by press Q on keyboard , 0b11111111 suitable represnt Q in 8 bits
				if q_key == ord('q'): 
					sys.exit()

				# end of loop

		counter += 1

		print("count_less_30", count_less_30)
		print("count_30_60", count_30_60)
		print("count_60_65", count_60_65)
		print("count_66_70", count_66_70)
		print("count_71_75", count_71_75)
		print("count_76_80", count_76_80)
		print("count_81_85", count_81_85)
		print("count_86_90", count_86_90)
		print("count_91_95", count_91_95)
		print("count_96", count_96)
		count_all = count_less_30 + count_30_60 + count_60_65 + count_66_70 + count_71_75 + count_76_80 + count_81_85 + count_86_90 + count_91_95 + count_96
		print("Total : ", count_all)

		#take all not remove file in the folder to broken folder



		analaysis_log_count = os.path.join(date_path,"analysis_log_count.csv")
		with open(analaysis_log_count, mode='a', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			writer.writerow(['','','','Conf_level', 'Total_img'])
			writer.writerow(['','','','<0.30',count_less_30])
			writer.writerow(['','','','0.30-0.60',count_30_60])
			writer.writerow(['','','','0.60-0.66',count_60_65])
			writer.writerow(['','','','0.65-0.70',count_66_70])
			writer.writerow(['','','','0.71-0.75',count_71_75])
			writer.writerow(['','','','0.76-0.80',count_76_80])
			writer.writerow(['','','','0.81-0.85',count_81_85])
			writer.writerow(['','','','0.86-0.90',count_86_90])
			writer.writerow(['','','','0.91-0.95',count_91_95])
			writer.writerow(['','','','0.96',count_96])
			writer.writerow(['','','','Total',count_all])






	#---------------------------------------------------------------------------------------------------------------------------------------
	# to save ANPR xml 
	


	if input_type == 'image' and save_xml_ANPR == True :
		print('start save xml')

		curr_path = os.path.dirname(os.path.realpath(__file__))	#current path		

		print("==================================================")
		print("Image Detection Start.")
		font = cv2.FONT_HERSHEY_SIMPLEX
		# cv2.namedWindow('PREVIEW')
		# cv2.moveWindow('PREVIEW', 0, 0)
		file_list = os.listdir(src_fullpath)
		print('here')
		for filename in sorted(file_list):
			
			filename_split = filename.split('.')
			print(filename_split)
			# if filename.endswith(".jpg") and filename[33:35] == "01":
			if filename.endswith(".jpg"):# and filename_split[4] == "01":
				detected_plate0 = ""

				if today_date != datetime.now().strftime("%Y%m%d"):
					pathUpdate()
				if not os.path.splitext(filename)[-1].lower() in img_formats:
					break
				print("==================================================")
				full_filename = os.path.join(src_fullpath, filename)
				print(full_filename)

				tracking_t0 = time.time()
				capF = cv2.imread(full_filename)
				height, width = capF.shape[:2]
				scaleRatio = min(w_std/width, h_std/height)
				capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
				h_capF, w_capF = capF.shape[:2]
				top = bottom = int(abs(h_std - h_capF) / 2)
				left = right = int(abs(w_std - w_capF) / 2)
				capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border

				img = capF.copy()
				img_resize = capF.copy()

				stride = max(int(model_detection.stride), 32)  # model stride=32
				imgsz = [640, 640]
				imgsz = check_img_size(imgsz, s=stride)  # check image size
				capF_resize = ANPR.letterbox(img_resize, imgsz, stride=stride, auto=False)[0]            #0.0004 - 0.0006
				capF_resize = capF_resize[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
				capF_resize = np.ascontiguousarray(capF_resize)
				## testing code
				capF_resize = torch.from_numpy(capF_resize)
				capF_resize = capF_resize.half() if half else capF_resize.float()  # uint8 to fp16/32
				capF_resize = capF_resize.to(device)
				capF_resize /= 255.0  # 0~255 to 0.0~1.0
				if capF_resize.ndimension() == 3:
					capF_resize = capF_resize.unsqueeze(0)
				

				

				crop_img, plate_conf0 = ANPR.runPlateDetection(model_detection, half, device, capF_resize, img, imgROI0)

				detected_plate, avg_conf, lowest_character_conflvl, min_conf_lvl, min_character, bbox_list = ANPR.recognize_plate(model_recognize, half, device, crop_img) 
				print('ele in bbox_list : ', len(bbox_list))
				print('filename', os.path.splitext(filename)[0])

				letter_to_xml = []
				for y, x, w, h, class_, conf, values in bbox_list:
					letter_to_xml.append([class_, values])
				saveDataset_ANPR(letter_to_xml, crop_img, w, h)
					
					

				
				cv2.imshow('PREVIEW',crop_img)
				cv2.waitKey(0)




	#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
	#save vavc xml

	if input_type == 'image' and save_xml_VAVC == True :
		print('start save VAVC xml')

		#get total img in setting 
		import fnmatch
		total_img = len(fnmatch.filter(os.listdir(src_fullpath), '*.jpg'))

		curr_path = os.path.dirname(os.path.realpath(__file__))	#current path		

		print("==================================================")
		print("Image Detection Start.")
		font = cv2.FONT_HERSHEY_SIMPLEX
		# cv2.namedWindow('PREVIEW')
		# cv2.moveWindow('PREVIEW', 0, 0)
		file_list = os.listdir(src_fullpath)
		# print('here')
		img_count = 1
		for filename in sorted(file_list):
			
			filename_split = filename.split('.')
			print(filename_split)
			# if filename.endswith(".jpg") and filename[33:35] == "01":
			if filename.endswith(".jpg"):# and filename_split[4] == "01":
				detected_plate0 = ""

				if today_date != datetime.now().strftime("%Y%m%d"):
					pathUpdate()
				if not os.path.splitext(filename)[-1].lower() in img_formats:
					break
				print("==================================================")
				full_filename = os.path.join(src_fullpath, filename)
				print(full_filename)

				tracking_t0 = time.time()
				capF = cv2.imread(full_filename)
				height, width = capF.shape[:2]
				scaleRatio = min(w_std/width, h_std/height)
				capF = cv2.resize(capF, (int(width*scaleRatio),int(height*scaleRatio)), cv2.INTER_LINEAR)  # resize to stride scale 32 to speed up
				h_capF, w_capF = capF.shape[:2]
				top = bottom = int(abs(h_std - h_capF) / 2)
				left = right = int(abs(w_std - w_capF) / 2)
				capF = cv2.copyMakeBorder(capF, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114,114,114))  # add gray border

				img = capF.copy()
				img_resize = capF.copy()

				stride = max(int(model_detection.stride), 32)  # model stride=32
				imgsz = [640, 640]
				imgsz = check_img_size(imgsz, s=stride)  # check image size
				capF_resize = ANPR.letterbox(img_resize, imgsz, stride=stride, auto=False)[0]            #0.0004 - 0.0006
				capF_resize = capF_resize[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
				capF_resize = np.ascontiguousarray(capF_resize)
				## testing code
				capF_resize = torch.from_numpy(capF_resize)
				capF_resize = capF_resize.half() if half else capF_resize.float()  # uint8 to fp16/32
				capF_resize = capF_resize.to(device)
				capF_resize /= 255.0  # 0~255 to 0.0~1.0
				if capF_resize.ndimension() == 3:
					capF_resize = capF_resize.unsqueeze(0)

				# Convert the list of coordinates to a numpy array
				#if want to see ROI, uncomment
				'''import ast
				roi = config.get('roi','roi_input0')
				roi = ast.literal_eval(roi)
				roi = [list(map(int, item)) for item in roi]

				roi = np.array(roi, dtype=np.int32)
				cv2.polylines(img, [roi], True, (0,0,255), 1)
				
				for point in roi:
					cv2.circle(img, tuple(point),5, (0,255,0), -1)'''



				vavc_frame, predicted_class, crop_img, crop_conf, det_bbox_list, det_cls_list = VAVC.vehicleDetection(model_vavc, half, device, img, imgROI0)
				print('det_bbox_list : ', det_bbox_list)
				print('det_cls_list : ', det_cls_list)



				#save xml
				h, w, channel = img.shape
				filename = os.path.splitext(filename)[0]

				if not any(det_bbox_list) and not any(det_cls_list):
					print('No detection')
				else:
					saveData_VAVC(h, w , img, det_bbox_list, det_cls_list, filename, src_fullpath)
				
					




				cv2.putText(img, str(img_count)+'/'+str(total_img), (10,50), font, 2, (0,255,0), 4, cv2.LINE_AA)
				cv2.imshow('PREVIEW',img)
				cv2.waitKey(50)

				img_count += 1





	if input_type == 'image' and plate_grading == True :
		print('Start plate grading')

		file_list = os.listdir(src_fullpath)

		for filename in sorted(file_list):
			# print(filename)

			stride = max(int(model_detection.stride), 32)  # model stride=32
			imgsz = [640, 640]
			imgsz = check_img_size(imgsz, s=stride)  # check image size
			# capF_resize = ANPR.letterbox(filename, imgsz, stride=stride, auto=False)[0]            #0.0004 - 0.0006
			# capF_resize = capF_resize[:, :, ::-1].transpose(2, 0, 1)  # img[:, :, ::-1] is BGR to RGB, transpose(2, 0, 1) is HWC to CHW
			# capF_resize = np.ascontiguousarray(capF_resize)
			## testing code
			capF_resize = torch.from_numpy(capF_resize)
			capF_resize = capF_resize.half() if half else capF_resize.float()  # uint8 to fp16/32
			capF_resize = capF_resize.to(device)
			capF_resize /= 255.0  # 0~255 to 0.0~1.0
			if capF_resize.ndimension() == 3:
				capF_resize = capF_resize.unsqueeze(0)

			ANPR.plate_grading(model_plate_grading, capF_resize, filename)



















#==================================================
	
	print("==================================================")
	print("Program END.")
	cv2.destroyAllWindows()
	print(f"Final Active threads (main): {threading.activeCount()}.")

#==================================================
# END
