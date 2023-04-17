
import os
from queue import Empty
import sys
from traceback import print_tb
import cv2
import csv
import time
import shutil
import re

from configparser import ConfigParser

ANPR = True
VAVC = False

config = ConfigParser()
config.read('./setting.ini')
src_path = config.get('setup', 'src_path')
# folder_basename = os.path.dirname(src_path)
folder_basename = src_path


print(folder_basename)

failed_img_path = os.path.join(folder_basename, os.path.basename(os.path.normpath(src_path)) + '_tracking')

anpr_folder = os.path.join(folder_basename, "ANPR")
false_anpr = os.path.join(anpr_folder, "0")
true_anpr = os.path.join(anpr_folder, "1")
special_plate = os.path.join(anpr_folder, "special_plate")
if not os.path.isdir(anpr_folder):
    os.mkdir(anpr_folder)
if not os.path.isdir(true_anpr):
    os.mkdir(true_anpr)
if not os.path.isdir(false_anpr):
    os.mkdir(false_anpr)
if not os.path.isdir(special_plate):
    os.mkdir(special_plate)

vavc_folder = os.path.join(folder_basename, "VAVC")
true_vavc = os.path.join(vavc_folder, "1")
false_vavc = os.path.join(vavc_folder, "0")
if not os.path.isdir(vavc_folder):
        os.mkdir(vavc_folder)
if not os.path.isdir(true_vavc):
        os.mkdir(true_vavc)
if not os.path.isdir(false_vavc):
        os.mkdir(false_vavc)

broken_folder = os.path.join(folder_basename, "broken")
if not os.path.isdir(broken_folder):
    os.mkdir(broken_folder)



# log_file = os.path.join(folder_basename, os.path.basename(os.path.normpath(src_path)) + '_log.csv')
# tracking_counter = os.path.join(folder_basename, os.path.basename(os.path.normpath(src_path)) + '_tracking.txt')

log_file = os.path.join(failed_img_path, '_log.csv')
tracking_counter = os.path.join(failed_img_path,'_tracking.txt')




def csvLogger(img_name, ANPR, VAVC):
    if ANPR == "9" and VAVC == "9":
        broken = "broken img"
    else:
        broken = ""

    if not os.path.isfile(log_file):
        with open(log_file, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['FILENAME', 'ANPR', 'VAVC', 'BROKEN'])

    with open(log_file, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([img_name, ANPR, VAVC, broken])


def src():
    filelist = os.listdir(src_path)
    counter = 0
    is_start_from_tracking = False

    if not os.path.isdir(failed_img_path):
        os.mkdir(failed_img_path)

    if not os.path.exists(tracking_counter):             # if tracking not existed
        with open(tracking_counter, 'w') as track_file:
            track_file.write('0')
    else:
        print('Tracking existed')
        with open(tracking_counter, 'r') as track_file:
            _start_counter = track_file.read()
            start_counter = int(_start_counter)
        is_start_from_tracking = True

    for filename in sorted(filelist):
        if filename.endswith(".jpg"):

            counter = counter + 1

            if is_start_from_tracking is True:
                if counter < start_counter:
                    continue
                else:
                    is_start_from_tracking = False

            with open(tracking_counter, 'w') as track_file:
                track_file.write(str(counter))

            detected_anpr = filename.split('.')
            detected_anpr = detected_anpr[7]
            # print(detected_anpr)


            detected_vavc = filename.split('_')
            # print(detected_vavc)
            detected_vavc = detected_vavc[1]
            # print(detected_vavc)

            winname='DISPLAY'
            img_fullpath = os.path.join(src_path, filename)
            img = cv2.imread(img_fullpath)
            img = cv2.resize(img,(1000,600))
            cv2.rectangle(img, (350, (img.shape[0]-90)),(750,600), (0,0,0), -1)
            cv2.putText(img, "ANPR : " + detected_anpr.rsplit('_')[0], (400, (img.shape[0]-50)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)    # (50, (img.shape[0]-50)) or ((img.shape[1]-300), (img.shape[0]-50))
            # cv2.putText(img, "VAVC : " + detected_vavc, (400, (img.shape[0]-10)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.namedWindow(winname)
            cv2.moveWindow(winname, 10, 50)
            cv2.imshow(winname, img)

            time.sleep(0.3)
            cv2.waitKey(15)
            # qkey = cv2.waitKey(0) & 0b11111111
            # if qkey == ord('q'):
            #     sys.exit()
            

            while True:

                if ANPR is True:
                    print("---------------------")
                    ANPR_input = input("ANPR : ")
                    if ANPR_input == "q":
                        print("\n[ Press Q ] Exit program...\n")
                        sys.exit()

                    elif ANPR_input == "0":
                        img_dst = os.path.join(false_anpr, filename)
                        shutil.copy(img_fullpath, img_dst)
                    elif ANPR_input == "1":
                        img_dst = os.path.join(true_anpr, filename)
                        shutil.copy(img_fullpath, img_dst)
                    elif ANPR_input == "9":         #broken image
                        img_dst = os.path.join(broken_folder, filename)
                        shutil.copy(img_fullpath, img_dst)
                        print("ANPR Broken")
                    elif ANPR_input == "7":
                        vanity = re.sub(r'[^a-zA-Z]', '', detected_anpr)
                        print("special_plate : ", vanity)
                        img_dst = os.path.join(special_plate, filename)
                        shutil.copy(img_fullpath, img_dst)
                    else:
                        print("--- invalid input ---")
                        print("--- re-enter again ---")
                        continue

                    if VAVC is False:
                        VAVC_input=''


                if VAVC is True:
                    VAVC_input = input("VAVC : ")
                    if VAVC_input == "q":
                        print("\n[ Press Q ] Exit program...\n")
                        sys.exit()

                    
                    elif VAVC_input == "0":
                        img_dst = os.path.join(false_vavc, filename)
                        shutil.copy(img_fullpath, img_dst)
                    elif VAVC_input == "1":
                        img_dst = os.path.join(true_vavc, filename)
                        shutil.copy(img_fullpath, img_dst)
                    elif VAVC_input == "9":
                        print("VAVC broken")

                    else:
                        print("--- invalid input ---")
                        print("--- re-enter again ---")
                        continue
                
                
            
                csvLogger(filename, ANPR_input, VAVC_input)
                break

            

    print(f'--DONE---\n')
    print(f'Total image : {counter}')
    cv2.destroyWindow('DISPLAY')
    cv2.destroyAllWindows()


if __name__ == '__main__':
    
    src()
