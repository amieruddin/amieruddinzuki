import os
import glob
import cv2
import sys
import time


#parameter
view_full = True
view_crop = True


print('Preview')

while True:

	#preview full image
	if view_full is True:
		path_full_img =os.getcwd() + '/image/full/'

		if os.path.exists(path_full_img):
			list_full_img = glob.glob(path_full_img + '*.jpg')
			latest_full_img = max(list_full_img, key=os.path.getctime)		#get latest image
			# oldest_full_img = max(list_of_img, key=os.path.getctime)		#get oldest image
			# print(latest_full_img)

			#preview image
			img = cv2.imread(latest_full_img)
			try:
				img_resize = cv2.resize(img, (720, 480))
			except:
				pass
			cv2.imshow('Full', img_resize)
			cv2.waitKey(1)
			
			# time.sleep(0.01)
		else:
			sys.exit('[Error] : Path /image/full not exist')



	#-------------------------------------------------------------------------------------------------

	#preview crop image
	if view_crop is True:
		path_crop_img =os.getcwd() + '/image/crop/'

		if os.path.exists(path_crop_img):
			list_crop_img = glob.glob(path_crop_img + '*.jpg')
			latest_crop_img = max(list_crop_img, key=os.path.getctime)		#get latest image
			# oldest_crop_img = max(list_of_img, key=os.path.getctime)		#get oldest image
			# print(latest_crop_img)
			
			#preview image
			img = cv2.imread(latest_crop_img)
			try:	
				cv2.namedWindow('Crop', cv2.WINDOW_NORMAL)
				cv2.resizeWindow('Crop', 240, 140)
				
				
				img_resize = cv2.resize(img, (240, 140))
			except:
				pass
			cv2.imshow('Crop', img_resize)
			key = cv2.waitKey(1)
			
			# Check if the user pressed 'q' to exit the loop
			if key == ord('q'):
				break
			
			
			# time.sleep(0.01)
		else:
			sys.exit('[Error] : Path /image/crop not exist')

	
	
	
