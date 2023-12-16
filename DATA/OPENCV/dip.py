import cv2
import numpy as np
from ..IO import fs
from .draw import Draw
from ..PANDAS.dsp import DSP
from .geometry import Geometry
from .morphology import Morphology
from .basic import load, save, imshow

class DIP(DSP):
    """Digital Image Processing"""

    def signal(self):
        self.draw = Draw()
        self.geometry = Geometry()
        self.morphology = Morphology()

        CALLBACK = self.kwargs.get('CALLBACK', None) # OPTIONAL
        if CALLBACK:
            dip_callback = CALLBACK(**self.kwargs.get('CALLBACK_ARGS', dict())) # OPTIONAL
            cb_state = imshow(self.x, winname=self.kwargs.get('FNAME', None), callback=dip_callback)
            dip_cb_state_handler = dip_callback.dip_state_handler(cb_state)
            self.kwargs['POINTS'] = self.kwargs.get('POINTS', dict())
            for cbs_k, cbs_v in dip_cb_state_handler.items():
                self.kwargs['POINTS'][cbs_k] = cbs_v

    def loader(self, fpath):
        return load(fpath, **self.kwargs.get('LOADER', dict())) # OPTIONAL

    def type_cast(self):
        if self.y is not None:
            return self.y.astype(np.uint8)

    def diff(self):
        return cv2.subtract(self.x, self.y)
    
    def view(self, *query, n=-1, s=1, **kwargs): # TODO it shoulde be inherit from DSP, DSP fucus on plotting and this fucus on showing.
        if len(query) == 0:
            query = ['x', 'y']
        
        n = int((len(query) ** .5) if n == -1 else n) # number of images in each row in grid view.
        assert n>=1

        grid = []
        Grid = None
        for idxq, q in enumerate(query):
            if q.endswith('()'):
                image = getattr(self, q[:-2])()
            else:
                image = getattr(self, q)

            if s != 1: # OPTIONAL
                image = self.geometry.resize(image, s=s)

            grid.append(image)

            if (idxq+1) % n == 0:
                if Grid is None:
                    Grid = cv2.hconcat(grid)
                else:
                    Grid = cv2.vconcat([Grid, cv2.hconcat(grid)])
                grid = []
        
        if len(grid) != 0:
            if Grid is None:
                Grid = cv2.hconcat(grid)
            else:
                for i in range(n - len(grid)):
                    grid.append(np.zeros(grid[0].shape, dtype=np.uint8))
                Grid = cv2.vconcat([Grid, cv2.hconcat(grid)])
        
        self.Grid = Grid
        if kwargs.get('save', False): # OPTIONAL
            save(kwargs.get('fpath', self.kwargs.get('FPATH', fs.ospjoin(
                self.kwargs.get('DPATH', '*/DIP'),
                self.kwargs.get('FNAME', 'example.png')
            ))), self.Grid)
        if kwargs.get('imshow', True): # OPTIONAL
            return imshow(Grid, callback=kwargs.get('callback', None))

if __name__ == '__main__':
    # BUG: there is no bug, but if you run test0 and test1 togetere there is a little bug, you can check it later.

    # TEST 0) testcase example
    # DIP('*lena.jpg').view('x', 'diff()', 'y', s=.5, n=3)
    # DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.5) # n <- int(sqrt(5))
    # DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.5, n=9)
    # DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.5, n=3, save=True)
    # DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.5, n=4)
    # DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.3, n=1)

    # TEST 1) dataloader example
    from .callback.pselect import PSelect
    DIP(
        SPATH='/home/alihejrati/Documents/Dataset/fundus - RetinaLessions/retinal-lesions-v20191227/images_896x896/*.jpg',
        SPATH_HEAD=3,
        DPATH='*/RetinaLessions',
        DF_DPATH='*/RetinaLessions.csv',
        VIEW=dict(query=['x', 'diff()', 'y'], s=.5, n=3, imshow=False, save=True),
        CALLBACK=PSelect,
        CALLBACK_ARGS=dict(N=2, F=['X', 'Y'], P=['OD', 'FOV'])
    )