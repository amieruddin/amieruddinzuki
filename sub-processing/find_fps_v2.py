import cv2

# Open the video file
video = cv2.VideoCapture("/home/delloyd/8.source/video/mlff-topview-30Meter.mp4")

# Get the frames per second (fps) of the video
fps = video.get(cv2.CAP_PROP_FPS)

print("Frames per second:", int(fps), 'fps')

# Release the video file
video.release()

