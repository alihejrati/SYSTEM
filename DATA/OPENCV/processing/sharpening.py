import cv2
import numpy as np
from ..dip import DIP
from ..basic import imshow

class Basic(DIP):
    def processing(self):
        img = self.x
        kernel_sharpening = np.array([
            [-1,    -1,     -1], 
            [-1,     9,     -1], 
            [-1,    -1,     -1]
        ])
        return cv2.filter2D(img, -1, kernel_sharpening)

if __name__ == '__main__':
    # TEST 0) testcase example
    basic_sharpener = Basic('*lena.jpg')
    basic_sharpener.view('x', 'diff()', 'y', n=3)
    basic_sharpener.view('y', s=2)
    imshow(basic_sharpener.y)

    # TEST 1) dataloader example
    Basic(
        SPATH='/home/alihejrati/Documents/Dataset/fundus - RetinaLessions/retinal-lesions-v20191227/images_896x896/*.jpg',
        SPATH_HEAD=3,
        DPATH='*/RetinaLessions',
        VIEW=dict(query=['x', 'diff()', 'y'], s=.5, n=3, imshow=False, save=True),
    )