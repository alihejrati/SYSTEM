import cv2
import numpy as np
from ...dip import DIP
from ...basic import load, save, imshow

class Basic(DIP):
    def processing(self):
        img = self.x
        print(self.kwargs)
        kernel_sharpening = np.array([
            [-1,    -1,     -1], 
            [-1,     9,     -1], 
            [-1,    -1,     -1]
        ])
        return cv2.filter2D(img, -1, kernel_sharpening)

if __name__ == '__main__':
    basic_sharpener = Basic('*lena.jpg')
    basic_sharpener.view('x', 'diff()', 'y', n=3)
    imshow(basic_sharpener.y)