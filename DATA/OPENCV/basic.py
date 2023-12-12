#NOTE: file extension is an algorithm for saving/serializing and loading/deserializing digital signal on disk.

# 1. Windows bitmap (bmp, dib)
# The BMP file format, also known as bitmap image file or device independent bitmap (DIB), is a raster graphics image file format used to store bitmap digital images, independently of the display device. It is capable of storing two-dimensional digital images both monochrome and color, in various color depths, and optionally with data compression, alpha channels, and color profiles.

# 2. Netpbm – Portable image formats (pbm, pgm, ppm)
# Netpbm is an open-source package of graphics programs and a programming library. Several graphics formats are used and defined by the Netpbm project. The portable pixmap format (PPM), the portable graymap format (PGM) and the portable bitmap format (PBM) are image file formats designed to be easily exchanged between platforms.

#  3. Sun Raster (sr, ras)
# Sun Raster was a raster graphics file format used on SunOS by Sun Microsystems. The format was mainly used in research papers.

# 4. JPEG (jpeg, jpg, jpe)
# JPEG is a raster image file format that’s used to store images that have been compressed to store a lot of information into a small file. 

# 5. JPEG 2000 (jp2)
# JPEG 2000 (JP2) is an image compression standard and coding system. It is a discrete wavelet transform (DWT) based compression standard that could be adapted for motion imaging video compression with the Motion JPEG 2000 extension. A standard uses wavelet based compression techniques, offering a high level of scalability and accessibility. In other words JPEG 2000 compresses images with fewer artifacts than a regular JPEG.

# 6. TIFF files (tiff, tif)
# It is an adaptable file format for handling images and data within a single file.

# 7. Portable network graphics (png)
# It is a raster-graphics file-format that supports lossless data compression. A PNG was developed as an improved, non-patented replacement for Graphics Interchange Format (GIF).

#NOTE: opencv image cordinate 2D system, begins with upper-left (0,0) as origin, and for each pixel use (x=col,y=row).
#NOTE: *numpy image cordinate 2D system, begins with upper-left (0,0) as origin, and for each pixel use (x=row,y=col).

#NOTE: all functions in opencv consider color image as BGR order, whereas matplotlib consider color image as RGB order.

# NOTE: normally dtype=np.float64 is deafult data type for numpy array.

# NOTE: variable names should be like this: (549, 969, 3) -> (h,w,ch)

import os
import cv2
import numpy as np
from ..IO import fs
from time import sleep
from threading import Thread
import matplotlib.pyplot as plt
from multiprocessing import Process
from KERNEL.PYTHON.classes.handler import Handler
from KERNEL.PYTHON.functions.coding import random_string

try:
    # For Google Colab we use the cv2_imshow() function
    from google.colab.patches import cv2_imshow # TODO test this on colab and check callback setting in this case.
except Exception as e:
    def cv2_imshow(img, winname, callback=None, handler=None):
        cv2.imshow(winname, img)
        if callback:
            callback.sethook(winname, handler, img)
        cv2.waitKey(0)

def save(fpath: str, img):
    if fpath.startswith('*'): # NOTE: index path
        fpath = fs.path('@opencv', 'export', fpath[1:], makedirs=True)
    else:
        fpath = fs.path(fpath, f_back=1, makedirs=True)

    return cv2.imwrite(fpath, img)

def load(fpath: str, mode='color'):
    """Loading our image with a cv2.imread() function, this function loads the image in BGR order"""
    if mode == 'color':
        mode = cv2.IMREAD_COLOR # There’s also another option for loading a color image: we can just put the number 1 instead cv2.IMREAD_COLOR and we will obtain the same output.
    elif mode == 'gray':
        mode = cv2.IMREAD_GRAYSCALE # The value that’s needed for loading a grayscale image is cv2.IMREAD_GRAYSCALE, or we can just put the number 0 instead as an argument.
    else:
        assert False
    
    if fpath.startswith('*'): # NOTE: index path
        fpath = fs.path('@opencv', 'import', fpath[1:])
    else:
        fpath = fs.path(fpath, f_back=1)
    
    img = cv2.imread(fpath, mode)
    return img

def split(img):
    """We can split the our image into 3 three channels (b, g, r) for normal color image, otherwise this functin split image into their channells."""
    return cv2.split(img) # return 3 channells: b, g, r seperaitly, if img was a normal color image; otherwise img splits to their own channells and those channells seperaily will return.

def convert_color(img, mode='bgr2rgb'):
    """
        Example:
            b, g, r = split(img) # img is a normal color image loaded by cv2.
            rgb_version_img = cv2.merge([r, g, b])
            * This tequnice can be used for any multi channell image.
    """
    if mode == 'bgr2rgb':
        mode = cv2.COLOR_BGR2RGB
    else:
        assert False
    return cv2.cvtColor(img, mode)

def imshow(img, mode='cv2', **kwargs):
    if mode == 'cv2':
        callback = kwargs.get('callback', None)
        winname = str(kwargs.get('winname', None) or 'image')
        if callback:
            h = Handler()
            def handler():
                h.send()
            proc = Process(target=cv2_imshow, args=(img, winname, callback, handler))
            proc.start()
            h.pause()
            proc.terminate()
            return callback.state
        else:
            cv2_imshow(img, winname)
            cv2.destroyWindow(winname)
    elif mode == 'plt':
        plt.imshow(convert_color(img))
        plt.axis('off')
        plt.show()
    else:
        assert False

def events():
    for i in dir(cv2):
        if 'EVENT' in i:
            print(f'-> {i}')

if __name__ == '__main__':
    # TEST 0
    # events()

    # TEST 1
    imshow(load('*lena.jpg'))