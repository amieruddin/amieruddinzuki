from PIL import Image
import os
import xml.etree.ElementTree as ET
import time




src = './test_data'
dst = './result'

if not os.path.exists(dst):
    os.makedirs(dst, exist_ok=True)

count = 0
for filename in sorted(os.listdir(src)):

    if filename.endswith('.jpg'):


    


        img_path = os.path.join(src, filename)
        xml_path = os.path.join(src, os.path.splitext(filename)[0] + '.xml')
        # print(img_name)

        img = Image.open(img_path)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        #mirror image
        img_mirrored = img.transpose(method=Image.FLIP_LEFT_RIGHT)


        # update xml file
        for obj in root.findall('object'):
            bbox = obj.find('bndbox')
            width = int(root.find('size').find('width').text)
            xmin = int(bbox.find('xmin').text)
            xmax = int(bbox.find('xmax').text)
            bbox.find('xmin').text = str(width - xmax)
            bbox.find('xmax').text = str(width - xmin)

        #save mirror image
        img_mirrored.save(dst + '/' + 'mirror_' + filename)
        tree.write(dst + '/' + 'mirror_' + os.path.splitext(filename)[0] + '.xml')

        count += 1
        time.sleep(0.001)

print("---------------------------- Done --------------------------")
print(f'Total : {count}')