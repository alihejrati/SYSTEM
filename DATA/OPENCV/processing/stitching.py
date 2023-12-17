import cv2
import numpy as np
from ..dip import DIP
from ..basic import imshow

class Stitching(DIP):
    """https://www.aiismath.com/pages/c_08_features/sift_nb/"""
    def processing(self):
        imageStitcher = cv2.Stitcher_create()
        status, stitched_img = imageStitcher.stitch(self.x)
        return stitched_img

if __name__ == '__main__':
    # TEST
    Stitching(
        '*/panaroma/a1.jpg',
        '*/panaroma/a2.jpg',
        VIEW=dict(query=['y'], s=1, n=3, imshow=True),
    )