import rawpy
import time
import os
from datetime import datetime
from PIL import Image

raw_ext_format = ['cr2', 'crw', 'dng', 'nef', 'rw2', 'arw']
now = datetime.now()
current_time = now.strftime('%H%M')

src = './images'
dst = './images/result'

for files in sorted(os.listdir(src)):
    start_time = time.time()
    if (os.path.splitext(files)[1][1:].lower()) in raw_ext_format:
        files_path = os.path.join(src, files)
        with rawpy.imread(files_path) as raw_img:

            rgb = raw_img.postprocess()
            # # get info 
            # size = rgb.size
            # pixel = rgb.dtype
            # width, height = raw_img.sizes.raw_width, raw_img.sizes.raw_height
            # print(f"Size: {size}\nPixel: {pixel}\nWidth: {width}\nHeight: {height}")

            jpg_img = Image.fromarray(rgb)
            jpg_img = jpg_img.resize((1280, 768))
            jpg_img.save(os.path.join(dst, os.path.splitext(files)[0] +'.jpg'))

    print(files, '--- %.3f seconds ---' % (time.time() - start_time))