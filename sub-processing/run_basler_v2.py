'''

export LD_LIBRARY_PATH=/home/delloyd/anaconda3/envs/inspecto/lib

'''


import cv2
import os
import sys
from pypylon import pylon
import random
import pyautogui


def save_img(image):
	save_path = './img'
	# if not os.path.exists(save_path):
	# 	os.makedirs(save_path)
	random_num = random.randint(0,1000)
	img_name = os.path.join(save_path, f'mirror_{random_num}.jpg')
	cv2.imwrite(img_name, image)
	print('img save : ', img_name)
        
def getParameter():     #get device parameter
    print("Camera Model : ", camera.GetDeviceInfo().GetModelName())
    print('\nImage Format Control')
    print(f'Offset X : {camera.OffsetX.GetValue()}\nOffset Y : {camera.OffsetY.GetValue()}')
    print(f'Width : {camera.Width.GetValue()}\nHeight : {camera.Height.GetValue()}')

    print('\nAcquisition Control')
    print('Shutter Mode : ', camera.ShutterMode.GetValue())
    print('Exposure Auto : ', camera.ExposureAuto.GetValue())
    print('Exposure Mode : ', camera.ExposureMode.GetValue())
    # print('Acquistion Frame Rate : ', camera.AcquisitionFrameRate.GetValue())
    print(f'Result Frame Rate :  {int(camera.ResultingFrameRate.GetValue())}')

def setParameter():
    print("\nSet parameter")
    
    camera.PixelFormat.SetValue('Mono8')
    camera.ExposureAuto.SetValue('Off')
    camera.ExposureTime.SetValue(33100.0)
    #camera.Gain.SetValue(1.0)  # Set gain to 1.0


     

# Connect to the first available camera
# pylon.pylonInitialize()
try:
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    

    
    camera.Open()
except Exception as e:
    print(f'{e}')
    sys.exit(0)


getParameter()
#setParameter()



# Set camera parameters
# camera.ExposureTime.SetValue(5000)  # Set exposure time to 5 ms
camera.ExposureAuto.SetValue("Continuous")


# Create format converter
converter = pylon.ImageFormatConverter()
# Specify the output pixel format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed

# Start grabbing images
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

# Create an OpenCV window
frame_width = camera.Width.GetValue()
frame_height = camera.Height.GetValue()
cv2.namedWindow("Inspecto", cv2.WINDOW_NORMAL)
width, height= pyautogui.size()
print(f'Screen resolution WxH : {width}x{height}' )
cv2.resizeWindow("Inspecto", width, height)

# Process images
while camera.IsGrabbing():
    # Wait for a new image to be ready
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    # Convert image to OpenCV format
    converted_image = converter.Convert(grabResult)
    image = converted_image.GetArray()

    # # Apply a basic color correction to adjust brightness and contrast
    # alpha = 2.0
    # beta = 50
    # image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    # Do something with the color image, e.g. display it
    cv2.imshow('Inspecto', image)
    cv2.waitKey(1)

    # Release the grab result to free up memory
    grabResult.Release()

    # print('Resulting FPS : ',int(camera.ResultingFrameRate.GetValue()))

    if cv2.waitKey(1) & 0xff == ord('s'):
        save_img(image)
    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop grabbing images and release the camera
camera.StopGrabbing()
camera.Close()
