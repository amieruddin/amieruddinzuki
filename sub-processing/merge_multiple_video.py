from moviepy.editor import VideoFileClip, concatenate_videoclips 
import cv2


clip1 = VideoFileClip("/home/delloyd/9.coding/merge video/vantage/penang1.avi")
clip3 = VideoFileClip("/home/delloyd/9.coding/merge video/vantage/penang2.avi")
clip2 = VideoFileClip("/home/delloyd/9.coding/merge video/vantage/penang3.avi")
clip4 = VideoFileClip("/home/delloyd/9.coding/merge video/vantage/penang4.avi")
clip5 = VideoFileClip("/home/delloyd/9.coding/merge video/vantage/penang5.avi")






final_clip = concatenate_videoclips([clip1,clip2,clip3,clip4,clip5]) 
final_clip.write_videofile("/home/delloyd/8.source/mlff-penang-jksb.mp4") 


'''
def using_opencv(video_files):

    # Create the video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify the codec
    width = int(cv2.VideoCapture(video_files[0]).get(cv2.CAP_PROP_FRAME_WIDTH))  # Get the width of the first video
    height = int(cv2.VideoCapture(video_files[0]).get(cv2.CAP_PROP_FRAME_HEIGHT))  # Get the height of the first video
    fps = int(cv2.VideoCapture(video_files[0]).get(cv2.CAP_PROP_FPS))  # Get the fps of the first video
    out = cv2.VideoWriter("combined_video.mp4", fourcc, fps, (width, height))

    # Loop through each video file
    for video_file in video_files:
        cap = cv2.VideoCapture(video_file)  # Create a video capture object
        
        while True:
            ret, frame = cap.read()  # Read the next frame from the video
            
            if not ret:  # If no frame was returned, break out of the loop
                break
            
            out.write(frame)  # Write the frame to the output video
            
        cap.release()  # Release the video capture object
        
    out.release()  # Release the video writer object

    print('Done')


if __name__ == '__main__':

    video_files = [clip1,clip2,clip3,clip4,clip5,clip6,clip7,clip8,clip9,clip10,clip11,clip12,clip13,clip14]
    using_opencv(video_files)'''
