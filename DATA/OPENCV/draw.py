import cv2
from .basic import load, save, imshow
from KERNEL.PYTHON.classes.basic import PYBASE

class Draw(PYBASE):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass
    
    def hex2vec(self, hex, mode='bgr'):
        h = hex.lstrip('#')
        rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        if mode == 'rgb':
            return rgb
        elif mode == 'bgr':
            return tuple([rgb[2], rgb[1], rgb[0]])
        else:
            assert False

    def line(self, img, p1, p2, **kwargs):
        kwargs['thickness'] = kwargs.get('thickness', 2)
        kwargs['color'] = kwargs.get('color', (255, 255, 255))
        if isinstance(kwargs['color'], str):
            kwargs['color'] = self.hex2vec(kwargs['color'])
        cv2.line(img, p1, p2, **kwargs)
    
    def circle(self, img, center, radius=10, **kwargs):
        # kwargs['lineType'] = kwargs.get('lineType', 0)
        kwargs['thickness'] = kwargs.get('thickness', 2)
        kwargs['color'] = kwargs.get('color', (255, 255, 255))
        if isinstance(kwargs['color'], str):
            kwargs['color'] = self.hex2vec(kwargs['color'])
        cv2.circle(img, center, radius, **kwargs)

if __name__ == '__main__':
    # TEST 0
    img = load('*/lena.jpg')
    draw = Draw()
    draw.line(img, (0,0), img.shape[:2], color='#7e1be0')
    draw.circle(img, [img.shape[0]//2, img.shape[1]//2], 160, color='#c7c718')
    imshow(img)