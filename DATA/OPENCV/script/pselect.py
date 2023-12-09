import cv2
from ...IO import fs
from ..callback import CallBack 
from ...PANDAS.basic import create
from ..basic import load, save, imshow

class CB(CallBack):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        self.n = 0
        self.N = int(self.kwargs.get('N', 1))
        self.fname = str(self.kwargs.get('fname'))
        self.state = []

    def CB_EVENT_LBUTTONDOWN(self, **kwargs):
        if self.n < self.N:
            self.n += 1
            self.state.append([kwargs['x'], kwargs['y']])
            print(self.fname, kwargs['x'], kwargs['y'])

        if self.n >= self.N:
            print('######', self.state)
            self.winclose()

def pselect(srcdir, N):
    for fpath in fs.ls(srcdir):
        cb = CB(
            N=N,
            fname=fs.ospsplit(fpath)[1]
        )
        state = imshow(load(fpath), callback=cb)
        print(state)
        print(cb.state)

if __name__ == '__main__':
    pselect(
        '/home/alihejrati/Documents/Dataset/fundus - RetinaLessions/retinal-lesions-v20191227/images_896x896/*.jpg',
        N=2
    )