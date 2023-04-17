import os
import shutil
import time
import xml.etree.ElementTree as ET


def filter_vavc_class_to_multifolder(src):
    
    for files in sorted(os.listdir(src)):
        if files.endswith('xml'):

            tree = ET.parse(os.path.join(src, files))
            root = tree.getroot()

            for obj in root.findall('object'):
                class_name = obj.find('name').text


                if class_name is None:
                    continue

                elif class_name == 'class1_lightVehicle':
                    try:
                        xml_src = os.path.join(src,files)
                        xml_dst = os.path.join('./class1', files)
                        shutil.move(xml_src, xml_dst)

                        jpg_file = os.path.splitext(files)[0] + '.jpg'
                        jpg_src = os.path.join(src, jpg_file)
                        jpg_dst = os.path.join('./class1', jpg_file)
                        shutil.move(jpg_src, jpg_dst)

                        print('move class1_lightVehicle')
                        break
                    except:
                        continue

                elif class_name == 'class2_mediumVehicle':
                    try:
                        xml_src = os.path.join(src,files)
                        xml_dst = os.path.join('./class2', files)
                        shutil.move(xml_src, xml_dst)

                        jpg_file = os.path.splitext(files)[0] + '.jpg'
                        jpg_src = os.path.join(src, jpg_file)
                        jpg_dst = os.path.join('./class2', jpg_file)
                        shutil.move(jpg_src, jpg_dst)

                        print('move class2_mediumVehicle')
                        break
                    except:
                        continue

                elif class_name == 'class3_heavyVehicle':
                    try:
                        xml_src = os.path.join(src,files)
                        xml_dst = os.path.join('./class3', files)
                        shutil.move(xml_src, xml_dst)

                        jpg_file = os.path.splitext(files)[0] + '.jpg'
                        jpg_src = os.path.join(src, jpg_file)
                        jpg_dst = os.path.join('./class3', jpg_file)
                        shutil.move(jpg_src, jpg_dst)

                        print('move class2_heavyVehicle')
                        break
                    except:
                        continue

                elif class_name == 'class4_taxi':
                    try:
                        xml_src = os.path.join(src,files)
                        xml_dst = os.path.join('./class4', files)
                        shutil.move(xml_src, xml_dst)

                        jpg_file = os.path.splitext(files)[0] + '.jpg'
                        jpg_src = os.path.join(src, jpg_file)
                        jpg_dst = os.path.join('./class4', jpg_file)
                        shutil.move(jpg_src, jpg_dst)

                        print('move class4_taxi')
                        break
                    except:
                        continue

                elif class_name == 'class5_bus':
                    try:
                        xml_src = os.path.join(src,files)
                        xml_dst = os.path.join('./class5', files)
                        shutil.move(xml_src, xml_dst)

                        jpg_file = os.path.splitext(files)[0] + '.jpg'
                        jpg_src = os.path.join(src, jpg_file)
                        jpg_dst = os.path.join('./class5', jpg_file)
                        shutil.move(jpg_src, jpg_dst)

                        print('move class5_bus')
                        break
                    except:
                        continue

                elif class_name == 'class_moto':
                    try:
                        xml_src = os.path.join(src,files)
                        xml_dst = os.path.join('./class_moto', files)
                        shutil.move(xml_src, xml_dst)

                        jpg_file = os.path.splitext(files)[0] + '.jpg'
                        jpg_src = os.path.join(src, jpg_file)
                        jpg_dst = os.path.join('./class_moto', jpg_file)
                        shutil.move(jpg_src, jpg_dst)

                        print('move class_moto')
                        break
                    except:
                        continue
                    
        time.sleep(0.001)
                    




if __name__ == '__main__':


    src = '/home/delloyd/3.MLFF/data_collection_temerloh/backup'

    #make classes directory
    class_dir = ['./class1', './class2', './class3', './class4', './class5', './class_moto']
    for directory in class_dir:
        if not os.path.exists(directory):
            os.makedirs(directory)


    filter_vavc_class_to_multifolder(src)