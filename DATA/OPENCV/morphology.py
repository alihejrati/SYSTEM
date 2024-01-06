import numpy as np
from .basic import load, imshow
from KERNEL.SCRIPT.python.classes.basic import PYBASE
from skimage.morphology import convex_hull_image

class Morphology(PYBASE):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass

    def convex_hull(self, img):
        return (convex_hull_image(img).astype(np.uint8) * 255).astype(np.uint8)

if __name__ == '__main__':
    m = Morphology()
    imshow(m.convex_hull(255 - load('*templ.png')))