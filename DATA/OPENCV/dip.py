import cv2
import numpy as np
from .geometry import resize
from .basic import load, save, imshow
from KERNEL.PYTHON.classes.basic import PYBASE

class DIP(PYBASE):
    def __init__(self, x, **kwargs):
        super().__init__(**kwargs)
        self.x = x
        self.__start()

    def __start(self):
        """
            self.kwargs # OPTIONAL
                -> DIP_POINTS: dict of points like => {'OD_X': 457, 'OD_Y': 400, 'FOV_X': 457, 'FOV_Y': 497}
                -> DIP_POINTS_NAME: list of point names like => ['OD', 'FOV'] 
                -> DIP_POINTS_FEATURE_NAME: list of point feature names like => ['X', 'Y']
        """
        if isinstance(self.x, str):
            self.x = load(self.x)
        
        if self.kwargs.get('run_processing_flag', True): # OPTIONAL
            self.y = self.processing()
        
    def processing(self):
        return self.x

    def diff(self):
        return cv2.subtract(self.x, self.y)
    
    def view(self, *query, n=-1, s=1):
        if len(query) == 0:
            query = ['x', 'y']
        
        n = int((len(query) ** .5) if n == -1 else n)
        assert n>=1

        grid = []
        Grid = None
        for idxq, q in enumerate(query):
            if q.endswith('()'):
                image = getattr(self, q[:-2])()
            else:
                image = getattr(self, q)

            if s != 1: # OPTIONAL
                image = resize(image, s=s)

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

        return imshow(Grid) # TODO make it grid

if __name__ == '__main__':
    # TEST 0
    DIP('*lena.jpg').view('x', 'diff()', 'y', s=.5, n=3)
    DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.5) # n <- int(sqrt(5))
    DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.5, n=9)
    DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.5, n=3)
    DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.5, n=4)
    DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.3, n=1)