import cv2
import os
import threading


src = '/home/delloyd/8.source/video/mlff-topview-50Meter.mp4'
dst = 'extract'

def extract_frames(start_frame, end_frame, video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    count = start_frame
    while count < end_frame:
        ret, frame = cap.read()
        if ret == False:
            break
        file_name = os.path.join(output_path, f"mlff_{count}.jpg")
        cv2.imwrite(file_name, frame)
        count += 15 #skip every fps
        print('img : ', img_count)
        cap.set(cv2.CAP_PROP_POS_FRAMES, count)
    cap.release()

def extract_with_count(video_path, output_path, num_threads=4):
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    except OSError:
        print('Error: Creating directory of data')
    
    cap = cv2.VideoCapture(video_path)
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    thread_list = []
    frames_per_thread = num_frames // num_threads

    for i in range(num_threads):
        start_frame = i * frames_per_thread
        end_frame = start_frame + frames_per_thread
        if i == num_threads - 1:
            end_frame = num_frames
        t = threading.Thread(target=extract_frames, args=(start_frame, end_frame, video_path, output_path))
        thread_list.append(t)
    
    print('Thread use : ', len(thread_list))
    
    for t in thread_list:
        t.start()
    
    for t in thread_list:
        t.join()

if __name__ == '__main__':
    extract_with_count(src, dst, num_threads=4)


