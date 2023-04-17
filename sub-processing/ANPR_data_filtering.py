from ctypes import py_object
from hashlib import new
import random
import os,glob
import shutil
import random
from turtle import ScrolledCanvas
import xml.etree.ElementTree as ET
import xml.dom.minidom
from xml.dom import minidom
import time

def move_file_to_other_location():

    src = r"F:\data_collection\3.19.7.2022"
    dst = r"F:\data_collection\3.19.7.2022\crop"

    for files in os.listdir(src):
        if files.endswith(".jpg"):
            if files[42:44] == "02":
                old_path = os.path.join(src,files)
                new_path = os.path.join(dst,files)
                print(new_path)

                shutil.move(old_path,new_path)

    print("-- DONE --")
                    

def sort_img_by_date():

    src_path = r"F:\data_collection\3.19.7.2022\full"

    for filename in sorted(os.listdir(src_path)):
        if filename.endswith(".jpg"):
            
            img_fullpath = os.path.join(src_path, filename)
            date = filename.split(".") #get date from filename
            print(date)
            d = date[0][8:10]
            m = date[0][5:7]
            y = date[0][0:4]
            
            date = d + "-" + m + "-" + y
            print(date)
            
            date_path = os.path.join(src_path, date)
            if not os.path.isdir(date_path):
                os.mkdir(date_path)
            
            dst_path = os.path.join(date_path,filename)
            shutil.move(img_fullpath, dst_path)
            
    print("--- DONE ---")

def sort_img_by_lane_ID():
    src = r"F:\data_collection\3.19.7.2022\full\13-07-2022"
    dst = r"F:\data_collection\3.19.7.2022\crop"
    count = 0

    for files in os.listdir(src):
        if files.endswith(".jpg"):
            files_split = files.split(".")
            if files_split[4] == "02": #lane ID = 02
                count+=1
                old_path = os.path.join(src,files)
                new_path = os.path.join(dst, files)
                shutil.move(old_path,new_path)
                print(count, ":",files)
            else:
                print("There is no file ID=02")
    
    print("--DONE--")


def get_crop_img_based_on_false_img():

    src = r"F:\data_collection\3.19.7.2022\full\01-07-2022"
    dst = r"F:\data_collection\3.19.7.2022\dst"

def rename_filename():
    src = r"F:\data_collection\3.19.7.2022\to label"
    randm = random.randint(0,999999)
    randm = str(randm)

    count=1
    for files in os.listdir(src):
        
        old_name = os.path.join(src, files)
        new_name = os.path.join(src, "double_line_"+str(count).zfill(6)+".jpg")
        print(new_name)
        print(old_name)
        os.rename(old_name, new_name)
        
        
        count+=1
    

def rename_dataset_based_on_classes_in_xml():
    src = r"C:\Users\PC\Desktop\special_plate_single_line\read xml"

    plate = ["MALAYSIA", "PATRIOT", "PUTRAJAYA", "BAMBEE"]
    for files in os.listdir(src):
        if files.endswith(".xml"):
            tree = ET.parse(os.path.join(src, files))
            root = tree.getroot()

            if root.find("object")[0].text in plate: # get object class
                vanity = root.find("object")[0].text
                print(src, "vanity", vanity, "001")

    
def rename_xml_same_as_jpg():
    count=0
    
    src = r"D:\1.0_TRAINING\3.VAVC\3.4_August\ready to train\train\test"

    for files in os.listdir(src):
        zero = str(count).zfill(6)
        if files.endswith(".jpg"):
            jpg = files
            jpg_old = os.path.join(src, jpg)
            jpg_name = os.path.join(src, "class5_" + zero + ".jpg")
            print(jpg_name)
            os.rename(jpg_old, jpg_name)
            
        if files.endswith(".xml"):
            xml = files
            xml_old = os.path.join(src, xml)
            xml_name = os.path.join(src, "class5_" + zero + ".xml")
            print(xml_name)
            os.rename(xml_old, xml_name)
            count+=1
            continue
        
        
def calculate_all_files_in_a_directory():
    src = r"D:\1.0_TRAINING\3.VAVC\3.4_August\z.combine\train"

    count=0
    for dirname, dirs, files in os.walk(src):
        for filename in files:
            filename_without_extension, extension = os.path.splitext(filename)
            if extension == ".jpg":
                count+=1
    print(count)

def filter_img_to_multi_folder_based_on_xml():
    src= "/media/delloyd/Transcend/Training_database/3.MLFF_top_view/need to label/classes/class2"
    dst = '/media/delloyd/Transcend/Training_database/3.MLFF_top_view/need to label/newfolder'

    #create class file if not exist
    if not os.path.exists(dst+'/class1'):
        os.makedirs(dst+'/class1')
    if not os.path.exists(dst+'/class2'):
        os.makedirs(dst+'/class2')
    if not os.path.exists(dst+'/class3'):
        os.makedirs(dst+'/class3')
    if not os.path.exists(dst+'/class4'):
        os.makedirs(dst+'/class4')
    if not os.path.exists(dst+'/class5'):
        os.makedirs(dst+'/class5')
    if not os.path.exists(dst+'/class_moto'):
        os.makedirs(dst+'/class_moto')



    classes = ["class1_lightVehicle","class2_mediumVehicle", "class3_heavyVehicle", "class4_taxi", "class5_bus", "class_motocycle"]
    temp_char = []
    count = 0

    for files in os.listdir(src):
        temp_char = []
        if files.endswith(".xml"):
            tree = ET.parse(os.path.join(src, files))
            root = tree.getroot()

            for obj_detected in root.iter('object'):
                for class_object in obj_detected.iter('name'):
                    # if class_object.text in classes:
                        # print(class_object.text)

                    # print('class_object.text', class_object.text, '\n')
                    temp_char.append(class_object.text)
                    # print('temp_char' , ''.join(temp_char[:4]))


                    xml_old_path = os.path.join(src, files)
                    # xml_new_path = os.path.join(src + '/' + 'copy', files)

                    img_name = os.path.splitext(xml_old_path)[0]
                    img_name = os.path.basename(img_name)
                    img_old_path = os.path.join(src, img_name + '.jpg')
                    # img_new_path = os.path.join(src + '/' + 'copy', img_name + '.jpg')

                    if class_object.text == 'class1_lightVehicle':
                        xml_new_path = os.path.join(dst + '/' + 'class1', files)
                        img_new_path = os.path.join(dst + '/' + 'class1', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                            print('class1_lightVehicle')
                        except:
                            pass

                    elif class_object.text == 'class2_mediumVehicle':
                        xml_new_path = os.path.join(dst + '/' + 'class2', files)
                        img_new_path = os.path.join(dst + '/' + 'class2', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                            print('class2_mediumVehicle')
                        except:
                            pass

                    elif class_object.text == 'class3_heavyVehicle':# or class_object.text == 'PATR10T':
                        xml_new_path = os.path.join(dst + '/' + 'class3', files)
                        img_new_path = os.path.join(dst + '/' + 'class3', img_name + '.jpg')
                        try:
                            pass
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                            print('class3_heavyVehicle')
                        except:
                            pass

                    elif class_object.text == 'class4_taxi':
                        xml_new_path = os.path.join(dst + '/' + 'class4', files)
                        img_new_path = os.path.join(dst + '/' + 'class4', img_name + '.jpg')
                        try:
                            pass
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                            print('class4_taxi')
                        except:
                            pass

                    elif class_object.text == 'class5_bus':
                        xml_new_path = os.path.join(dst + '/' + 'class5', files)
                        img_new_path = os.path.join(dst + '/' + 'class5', img_name + '.jpg')
                        try:
                            pass
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                            print('class5_bus')
                        except:
                            pass

                    elif ''.join(temp_char[:4]) == 'huhahuha':
                        xml_new_path = os.path.join(dst + '/' + 'class5', files)
                        img_new_path = os.path.join(dst + '/' + 'class5', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                           
                        except:
                            pass

                    elif ''.join(temp_char[:3]) == 'VIP' :
                        xml_new_path = os.path.join(dst + '/' + 'VIP', files)
                        img_new_path = os.path.join(dst + '/' + 'VIP', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass


                    elif ''.join(temp_char[:4]) == 'NAAM' :
                        xml_new_path = os.path.join(dst + '/' + 'NAAM', files)
                        img_new_path = os.path.join(dst + '/' + 'NAAM', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:2]) == '1Q' :
                        xml_new_path = os.path.join(dst + '/' + '1Q', files)
                        img_new_path = os.path.join(dst + '/' + '1Q', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:2]) == 'IQ' :
                        xml_new_path = os.path.join(dst + '/' + 'IQ', files)
                        img_new_path = os.path.join(dst + '/' + 'IQ', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:4]) == 'IIUM' :
                        xml_new_path = os.path.join(dst + '/' + 'IIUM', files)
                        img_new_path = os.path.join(dst + '/' + 'IIUM', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:4]) == '11UM' :
                        xml_new_path = os.path.join(dst + '/' + '11UM', files)
                        img_new_path = os.path.join(dst + '/' + '11UM', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:4]) == 'UITM' :
                        xml_new_path = os.path.join(dst + '/' + 'UITM', files)
                        img_new_path = os.path.join(dst + '/' + 'UITM', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass
                    
                    elif ''.join(temp_char[:4]) == 'U1TM' :
                        xml_new_path = os.path.join(dst + '/' + 'U1TM', files)
                        img_new_path = os.path.join(dst + '/' + 'U1TM', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:9]) == 'XXV1ASEAN' :
                        xml_new_path = os.path.join(dst + '/' + 'XXV1ASEAN', files)
                        img_new_path = os.path.join(dst + '/' + 'XXV1ASEAN', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:7]) == 'X111NAM' :
                        xml_new_path = os.path.join(dst + '/' + 'X111NAM', files)
                        img_new_path = os.path.join(dst + '/' + 'X111NAM', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:4]) == 'X01C' :
                        xml_new_path = os.path.join(dst + '/' + 'X01C', files)
                        img_new_path = os.path.join(dst + '/' + 'X01C', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:7]) == 'PER0DUA' :
                        xml_new_path = os.path.join(dst + '/' + 'PER0DUA', files)
                        img_new_path = os.path.join(dst + '/' + 'PER0DUA', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:6]) == 'PR0T0N' :
                        xml_new_path = os.path.join(dst + '/' + 'PR0T0N', files)
                        img_new_path = os.path.join(dst + '/' + 'PR0T0N', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass
                    
                    elif ''.join(temp_char[:3]) == 'GIM' :
                        xml_new_path = os.path.join(dst + '/' + 'GIM', files)
                        img_new_path = os.path.join(dst + '/' + 'GIM', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass
                    
                    elif ''.join(temp_char[:3]) == 'G1M' :
                        xml_new_path = os.path.join(dst + '/' + 'G1M', files)
                        img_new_path = os.path.join(dst + '/' + 'G1M', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:5]) == 'RIMAU' :
                        xml_new_path = os.path.join(dst + '/' + 'RIMAU', files)
                        img_new_path = os.path.join(dst + '/' + 'RIMAU', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:5]) == 'R1MAU' :
                        xml_new_path = os.path.join(dst + '/' + 'R1MAU', files)
                        img_new_path = os.path.join(dst + '/' + 'R1MAU', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:4]) == 'NBOS' :
                        xml_new_path = os.path.join(dst + '/' + 'NBOS', files)
                        img_new_path = os.path.join(dst + '/' + 'NBOS', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:4]) == 'NB0S' :
                        xml_new_path = os.path.join(dst + '/' + 'NB0S', files)
                        img_new_path = os.path.join(dst + '/' + 'NB0S', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:6]) == 'UNIMAS' :
                        xml_new_path = os.path.join(dst + '/' + 'UNIMAS', files)
                        img_new_path = os.path.join(dst + '/' + 'UNIMAS', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:6]) == 'UN1MAS' :
                        xml_new_path = os.path.join(dst + '/' + 'UN1MAS', files)
                        img_new_path = os.path.join(dst + '/' + 'UN1MAS', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:5]) == 'SUKOM' :
                        xml_new_path = os.path.join(dst + '/' + 'SUKOM', files)
                        img_new_path = os.path.join(dst + '/' + 'SUKOM', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:5]) == 'SUK0M' :
                        xml_new_path = os.path.join(dst + '/' + 'SUK0M', files)
                        img_new_path = os.path.join(dst + '/' + 'SUK0M', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:7]) == 'PERFECT' :
                        xml_new_path = os.path.join(dst + '/' + 'PERFECT', files)
                        img_new_path = os.path.join(dst + '/' + 'PERFECT', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:5]) == 'LOTUS' :
                        xml_new_path = os.path.join(dst + '/' + 'LOTUS', files)
                        img_new_path = os.path.join(dst + '/' + 'LOTUS', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:5]) == 'L0TUS' :
                        xml_new_path = os.path.join(dst + '/' + 'L0TUS', files)
                        img_new_path = os.path.join(dst + '/' + 'L0TUS', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

                    elif ''.join(temp_char[:4]) == 'L1M0' :
                        xml_new_path = os.path.join(dst + '/' + 'L1M0', files)
                        img_new_path = os.path.join(dst + '/' + 'L1M0', img_name + '.jpg')
                        try:
                            shutil.move(xml_old_path, xml_new_path)
                            shutil.move(img_old_path, img_new_path)
                        except:
                            pass

        count += 1
        print(count)
        time.sleep(0.01)

                    


#main
if __name__ == "__main__":
    filter_img_to_multi_folder_based_on_xml()
