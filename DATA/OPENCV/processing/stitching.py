import cv2
import numpy as np
from ..dip import DIP
from ..basic import imshow

class Stitching(DIP):
    def processing(self):
        imshow(self.x0)
        imshow(self.x1)

if __name__ == '__main__':
    # TEST
    Stitching(
        '*/panaroma/c1.jpg',
        '*/panaroma/c2.jpg',
        VIEW=dict(query=['x0', 'x1'], s=.5, n=3, imshow=True),
    )