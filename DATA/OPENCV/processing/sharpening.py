import cv2
import numpy as np
from ..dip import DIP
from ..basic import load, save, imshow

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
    # basic_sharpener = Basic('*lena.jpg')
    # basic_sharpener.view('x', 'diff()', 'y', n=3)
    # imshow(basic_sharpener.y)

    # TEST 1
    from ..callback.pselect import PSelect
    basic = Basic(
        DIP_SPATH='/home/alihejrati/Documents/Dataset/fundus - RetinaLessions/retinal-lesions-v20191227/images_896x896/*.jpg',
        DIP_SPATH_HEAD=3,
        DIP_DPATH='*/RetinaLessions',
        DIP_DF_DPATH='*/RetinaLessions.csv',
        # DIP_VIEW=dict(query=['x', 'y'], s=.5, n=3, imshow_flag=True, save_flag=True),
        DIP_CALLBACK=PSelect,
        DIP_CALLBACK_ARGS=dict(N=2, F=['X', 'Y'], P=['OD', 'FOV'])
    )
    print(basic.df)