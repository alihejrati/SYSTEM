# NOTE: https://datahacker.rs/003-how-to-resize-translate-flip-and-rotate-an-image-with-opencv/
# In geometry, an affine transformation (Latin affinis – “connected with”) 
# is a function that maps an arbitrary connected space onto itself while preserving 
# the dimension of any affine sub-spaces. 
# So, in simple words, it maps points to points, lines to lines or planes to planes, 
# while preserving the ratio of the lengths of parallel line segments. 
# Since picture is a connected collection of pixels (points) affine transformation 
# represents a segment of digital image processing.

import cv2
import numpy as np
from KERNEL.SCRIPT.python.classes.basic import PYBASE
from DATA.OPENCV.basic import load, save, imshow


class Geometry(PYBASE):
    """
        The height of the image is stored at the index 0. 
        The width of the image is stored at index 1. 
        The number of channels in the image is stored at index 2
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass

    def affine(self, img, M, **kwargs):
        """M is affine_matrix."""
        h, w = img.shape[:2]
        return cv2.warpAffine(img, np.float32(M), (w, h))

    def translation(self, img, tx=0, ty=0, **kwargs):
        """
            Example: tx=100, ty=-50
            Negative values of tx will shift the image to the left
            Positive values will shift the image to the right
            Negative values of ty will shift the image up
            Positive values will shift the image down
        """
        M = np.float32([
            [1, 0, tx],
            [0, 1, ty],
        ])
        if kwargs.get('return_M', False): # OPTIONAL
            return M
        return self.affine(img, M)

    def rotation(self, img, theta=0, **kwargs):
        """
            Example: theta=60, s=1
            if theta is positive, our output image will rotate counterclockwise(<-). Similarly, 
            if theta is negative the image will rotate clockwise(->).
            * s = 1 -> rotated image will have the same dimensions. 
            * s = 2 -> rotated image will have the doubled in size.
        """
        h, w = img.shape[:2]
        scale = float(kwargs.get('scale', 1)) # OPTIONAL
        center = list(kwargs.get('center', (w // 2, h // 2)))
        center[0] = int(center[0])
        center[1] = int(center[1])
        M = cv2.getRotationMatrix2D(center, theta, scale)
        if kwargs.get('return_M', False): # OPTIONAL
            return M
        return self.affine(img, M)

    def ROT(self, img, **kwargs):
        """
            params: theta, tx, ty
        """
        R = self.rotation(img, **kwargs, return_M=True) # its also done scale transform with `scale` param as well.
        T = self.translation(img, **kwargs, return_M=True)
        T[:, :-1] = 0
        M = R + T
        return self.affine(img, M)

    def flip(self, img, mode='both', **kwargs):
        """
            A value 1 indicates that we are going to flip our image around the y-axis (horizontal flipping). 
            On the other hand, a value 0 indicates that we are going to flip the image around the
            x-axis (vertical flipping). 
            If we want to flip the image around both axes, we will use a negative value (e.g. -1).
        """
        if mode == 'both' or mode == 'vh' or mode == 'hv':
            mode = -1
        elif mode == 'v' or mode == 'vertical':
            mode = 0
        elif mode == 'h' or mode == 'horizontal':
            mode = 1
        else:
            assert False
        return cv2.flip(img, mode)

    def resize(self, img, **kwargs):
        H, W = img.shape[:2] # NOTE: name ordering is a rule!
        h = int(kwargs.get('h', -1))   # OPTIONAL
        w = int(kwargs.get('w', -1))   # OPTIONAL
        s = float(kwargs.get('s', -1)) # OPTIONAL
        
        if s != -1 and s != 1:
            h = -1
            w = int(W * s)

        aspect_ratio = True
        if w != -1 and h != -1:
            aspect_ratio = False

        if aspect_ratio:
            if w != -1:
                ratio = float(w) / W
                h = int(H * ratio)
            elif h != -1:
                ratio = float(h) / H
                w = int(W * ratio)
            else:
                assert False, 'At least one of w or h, or both of them, must be provided.'
        return cv2.resize(img, (w, h))



if __name__ == '__main__':
    # TEST 1) resize
    geometry = Geometry()
    imshow(geometry.resize(load('*lena.jpg'), s=1.2))
    
    # got_img_h128w256 = geometry.resize(got_img, w=256, h=128)
    # got_img_h256w128 = geometry.resize(got_img, w=128, h=256)
    # got_img_w400 = geometry.resize(got_img, w=400)
    # got_img_h300 = geometry.resize(got_img, h=300)
    # print(got_img.shape, got_img_w400.shape, got_img_h300.shape, got_img_h128w256.shape, got_img_h256w128.shape)
    # save('./export/geometry/got.jpg', got_img)
    # save('./export/geometry/got_img_h128w256.jpg', got_img_h128w256)
    # save('./export/geometry/got_img_h256w128.jpg', got_img_h256w128)
    # save('./export/geometry/got_img_w400.jpg', got_img_w400)
    # save('./export/geometry/got_img_h300.jpg', got_img_h300)

    # TEST 2) affine:translation & rotation & ROT
    save('./export/geometry/got_ROTt10r100u50.jpg', geometry.ROT(load('./import/got.png'), theta=10, tx=100, ty=-50))
    save('./export/geometry/got_translated_r100d50.jpg', geometry.translation(load('./import/got.png'), 100, 50))
    save('./export/geometry/got_translated_r100u50.jpg', geometry.translation(load('./import/got.png'), 100, -50))
    save('./export/geometry/got_rotated_t30.jpg', geometry.rotation(load('./import/got.png'), 30))
    save('./export/geometry/got_rotated_t360.jpg', geometry.rotation(load('./import/got.png'), 360))
    save('./export/geometry/got_rotated_t370.jpg', geometry.rotation(load('./import/got.png'), 370))
    save('./export/geometry/got_rotated_t-10.jpg', geometry.rotation(load('./import/got.png'), -10))

    # TEST 3) flip
    save('./export/geometry/got_flip_vh.jpg', geometry.flip(load('./import/got.png'), 'vh'))
    save('./export/geometry/got_flip_h.jpg', geometry.flip(load('./import/got.png'), 'h'))
    save('./export/geometry/got_flip_v.jpg', geometry.flip(load('./import/got.png'), 'v'))
    pass