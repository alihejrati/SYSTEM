import cv2
import numpy as np
from ..IO import fs
from .geometry import resize
from .basic import load, save, imshow
from KERNEL.PYTHON.classes.basic import PYBASE
from ..PANDAS.basic import create as dfcreate, save as dfsave

class DIP(PYBASE):
    def __init__(self, x=None, **kwargs):
        super().__init__(**kwargs)
        self.x = x
        self.__start()

    def __start(self):
        """
            self.kwargs # OPTIONAL
                -> DIP_VIEW: contains view params for run it automatically,
                -> DIP_FPATH: dst file path => save view
                -> DIP_FNAME: src/dst file name => save  view
                -> DIP_DPATH: dst directory path => save view
                -> DIP_SPATH: src directory path => loading a multiple inputs. # NOTE: dataloader handler
                -> DIP_POINTS: `dict` of points like => {'OD_X': 457, 'OD_Y': 400, 'FOV_X': 457, 'FOV_Y': 497}
                -> DIP_POINTS_NAME: list of point names like => ['OD', 'FOV'] 
                -> DIP_POINTS_FEATURE_NAME: list of point feature names like => ['X', 'Y']
                -> DIP_CALLBACK: default values is None, it gonna be set on img from testcase img handler. # NOTE: self.view() has its own callback param from its kwargs variable, and it ganna be set on Grid image, if imshow operation was active.
                -> DIP_CALLBACK_ARGS: args passed to DIP_CALLBACK if DIP_CALLBACK was exist.
                -> DIP_DF_DPATH: `dst` path for saving data likes: ID,DIP_POINTS,... as dataframe # NOTE: dataloader handler
        """
        DIP_SPATH = self.kwargs.get('DIP_SPATH', False) # OPTIONAL: use it only for make dataloader handler not for testcase img handler.
        DIP_SPATH_HEAD = int(self.kwargs.get('DIP_SPATH_HEAD', -1)) # OPTIONAL: use it only for make dataloader handler not for testcase img handler.
        if DIP_SPATH: # NOTE: dataloader handler.
            data = []
            for idx_fpath, fpath in enumerate(fs.ls(DIP_SPATH)):
                fname = fs.ospsplit(fpath)[1]
                self.kwargs['DIP_FNAME'] = fname
                self.kwargs['DIP_SPATH'] = False
                self.kwargs['DIP_SPATH_HEAD'] = -1
                dip_obj = self.__class__(fpath, **self.kwargs)
                data.append(dict(
                    ID=fname, 
                    **dip_obj.kwargs.get('DIP_POINTS', dict())
                ))
                if idx_fpath == DIP_SPATH_HEAD - 1:
                    break
            self.df = dfcreate(data)
            DIP_DF_DPATH = self.kwargs.get('DIP_DF_DPATH', None) # OPTIONAL
            if DIP_DF_DPATH:
                dfsave(DIP_DF_DPATH, self.df)
            return

        
        # NOTE: testcase img handler.
        if isinstance(self.x, str):
            self.x = load(self.x)
        
        DIP_CALLBACK = self.kwargs.get('DIP_CALLBACK', None) # OPTIONAL
        if DIP_CALLBACK:
            dip_callback = DIP_CALLBACK(**self.kwargs.get('DIP_CALLBACK_ARGS', dict())) # OPTIONAL
            cb_state = imshow(self.x, winname=self.kwargs.get('DIP_FNAME', None), callback=dip_callback)
            dip_cb_state_handler = dip_callback.dip_state_handler(cb_state)
            self.kwargs['DIP_POINTS'] = self.kwargs.get('DIP_POINTS', dict())
            for cbs_k, cbs_v in dip_cb_state_handler.items():
                self.kwargs['DIP_POINTS'][cbs_k] = cbs_v

        if self.kwargs.get('run_processing_flag', True): # OPTIONAL
            self.y = self.processing()
        
        if self.kwargs.get('DIP_VIEW', None):
            query = self.kwargs['DIP_VIEW']['query']
            self.view(*query, **self.kwargs['DIP_VIEW'])

    def processing(self):
        return self.x

    def diff(self):
        return cv2.subtract(self.x, self.y)
    
    def view(self, *query, n=-1, s=1, **kwargs):
        if len(query) == 0:
            query = ['x', 'y']
        
        n = int((len(query) ** .5) if n == -1 else n) # number of image in each row in grid view.
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
        
        self.Grid = Grid
        if kwargs.get('save_flag', False): # OPTIONAL
            save(self.kwargs.get('DIP_FPATH', fs.ospjoin(
                self.kwargs.get('DIP_DPATH', '*/DIP'),
                self.kwargs.get('DIP_FNAME', 'example.png')
            )), self.Grid)
        if kwargs.get('imshow_flag', True): # OPTIONAL
            return imshow(Grid, callback=kwargs.get('callback', None))

if __name__ == '__main__':
    # BUG: there is no bug, but if you run test0 and test1 togetere there is a little bug, you can check it later.

    # TEST 0) testcase example
    # DIP('*lena.jpg').view('x', 'diff()', 'y', s=.5, n=3)
    # DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.5) # n <- int(sqrt(5))
    # DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.5, n=9)
    # DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.5, n=3, save_flag=True)
    # DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.5, n=4)
    # DIP('*lena.jpg').view('x', 'x', 'x', 'x', 'y', s=.3, n=1)

    # TEST 1) dataloader example
    from .callback.pselect import PSelect
    DIP(
        DIP_SPATH='/home/alihejrati/Documents/Dataset/fundus - RetinaLessions/retinal-lesions-v20191227/images_896x896/*.jpg',
        DIP_SPATH_HEAD=3,
        DIP_DPATH='*/RetinaLessions',
        DIP_DF_DPATH='*/RetinaLessions.csv',
        DIP_VIEW=dict(query=['x', 'diff()', 'y'], s=.5, n=3, imshow_flag=False, save_flag=True),
        DIP_CALLBACK=PSelect,
        DIP_CALLBACK_ARGS=dict(N=2, F=['X', 'Y'], P=['OD', 'FOV'])
    )