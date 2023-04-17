from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np
import time
import xml.etree.ElementTree as ET
import shutil
import glob
import random
import time
import os


src = '/home/delloyd/11.data_collection/emblem'
dst = '/home/delloyd/11.data_collection/emblem/augmented/'

if not os.path.exists(dst):
    os.makedirs(dst)


def augmentation(image, xml_dir, result_dir, filename):
    #brightness
    for brightness in range(-50, 51):
        bright_img = image.point(lambda x: x + brightness)
        bright_img.save(f'{result_dir}img1_bright_{brightness}_{filename}.jpg')

        xml_name = os.path.splitext(os.path.basename(xml_dir))[0]
        new_xml_name = f'{result_dir}img1_bright_{brightness}_{filename}.xml'
        shutil.copy(xml_dir, new_xml_name)


    # blurring
    for blur in np.arange(0, 1, 0.1):
        blurred_img = image.filter(ImageFilter.GaussianBlur(blur))
        blurred_img.save(f'{result_dir}img1_blur_{blur:.1f}_{filename}.jpg')

        xml_name = os.path.splitext(os.path.basename(xml_dir))[0]
        new_xml_name = f'{result_dir}img1_blur_{blur:.1f}_{filename}.xml'
        shutil.copy(xml_dir, new_xml_name)


    # contrast
    contrast_factor = 0.5
    img_contrasted = ImageEnhance.Contrast(image).enhance(contrast_factor)
    for contrast in np.arange(0, 2, 0.1):
        filename = f"result/img1_contrast_{contrast}.jpg"
        contrasted_adjusted_img = ImageOps.autocontrast(img_contrasted, cutoff=contrast)
        contrasted_adjusted_img.save(f'{result_dir}img1_contrast_{contrast:.1f}_{filename}.jpg')

        xml_name = os.path.splitext(os.path.basename(xml_dir))[0]
        new_xml_name = f'{result_dir}img1_contrast_{contrast:.1f}_{filename}.xml'
        shutil.copy(xml_dir, new_xml_name)

    #hue
    for hue_percent in range(-40, 41):
        hue_img = ImageEnhance.Color(image).enhance(1 + hue_percent/100)
        hue_img.save(f'{result_dir}img1_hue_{hue_percent}_{filename}.jpg')

        xml_name = os.path.splitext(os.path.basename(xml_dir))[0]
        new_xml_name = f'{result_dir}img1_hue_{hue_percent}_{filename}.xml'
        shutil.copy(xml_dir, new_xml_name)

    #saturation
    for saturation_percent in range(-50, 51):
        saturation_img = ImageEnhance.Color(image).enhance(1 + saturation_percent/100)
        saturation_img.save(f'{result_dir}img1_saturation_{saturation_percent}_{filename}.jpg')

        xml_name = os.path.splitext(os.path.basename(xml_dir))[0]
        new_xml_name = f'{result_dir}img1_saturation_{saturation_percent}_{filename}.xml'
        shutil.copy(xml_dir, new_xml_name)

    #exposure
    for exposure_percent in range(-30, 31):
        exposure_img = ImageEnhance.Brightness(image).enhance(1 + exposure_percent/100)
        exposure_img.save(f'{result_dir}img1_exposure_{exposure_percent}_{filename}.jpg')

        xml_name = os.path.splitext(os.path.basename(xml_dir))[0]
        new_xml_name = f'{result_dir}img1_exposure_{exposure_percent}_{filename}.xml'
        shutil.copy(xml_dir, new_xml_name)






if __name__ == '__main__':




    for files in os.listdir(src):

        try:
            if files.endswith('.jpg'):
                xml = src + '/' + os.path.splitext(files)[0] + '.xml'
                img = src + '/' + files
                filename = files
                image = Image.open(img)
                augmentation(image, xml, dst, filename)
        except:
            continue
        time.sleep(0.001)
