from ..IO import fs
from tqdm import tqdm
from .basic import create, load, save
from ..NUMPY.mathematics import Mathematics
from ..NUMPY.basic import load as npload
from KERNEL.PYTHON.classes.basic import PYBASE

class DSP(PYBASE):
    """Digital Signal Processing"""
    
    def __init__(self, *x, **kwargs):
        super().__init__(**kwargs)
        self.x = list(x)
        self.__start()

    def __start(self):
        """
            self.kwargs # OPTIONAL
                -> RUN: bool value for controling of executable proccessing function.
                -> VIEW: contains view params for run it automatically,
                -> FPATH: dst file path => save view
                -> FNAME: src/dst file name => save  view
                -> DPATH: dst directory path => save view
                -> SPATH: src directory path => loading a multiple inputs. # NOTE: dataloader handler
                -> POINTS: `dict` of points like => {'OD_X': 457, 'OD_Y': 400, 'FOV_X': 457, 'FOV_Y': 497}
                -> POINTS_NAME: list of point names like => ['OD', 'FOV'] 
                -> POINTS_FEATURE_NAME: list of point feature names like => ['X', 'Y']
                -> DF_DPATH: `dst` path for saving data likes: ID,POINTS,... as dataframe # NOTE: dataloader handler
                -> DF_SPATH: # TODO
        """
        SPATH = self.kwargs.get('SPATH', False) # OPTIONAL: use it only for make dataloader handler not for testcase signal handler.
        DF_SPATH = self.kwargs.get('DF_SPATH', False) # TODO!!!!!!!!!!!!
        SPATH_HEAD = int(self.kwargs.get('SPATH_HEAD', -1)) # OPTIONAL: use it only for make dataloader handler not for testcase signal handler.
        if SPATH: # NOTE: dataloader handler.
            data = []
            for idx_fpath, fpath in enumerate(tqdm(fs.ls(SPATH))):
                fname = fs.ospsplit(fpath)[1]
                self.kwargs['FNAME'] = fname
                self.kwargs['SPATH'] = False
                self.kwargs['DF_SPATH'] = False
                self.kwargs['SPATH_HEAD'] = -1
                self.kwargs['_SPATH'] = SPATH
                self.kwargs['_DF_SPATH'] = DF_SPATH
                self.kwargs['_SPATH_HEAD'] = SPATH_HEAD
                
                obj = self.__class__(fpath, **self.kwargs)
                data.append(dict(
                    ID=fname, 
                    **obj.kwargs.get('POINTS', dict()) # feature points
                ))
                if idx_fpath == SPATH_HEAD - 1:
                    break
            self.df = create(data)
            DF_DPATH = self.kwargs.get('DF_DPATH', None) # OPTIONAL
            if DF_DPATH:
                save(DF_DPATH, self.df)
            return

        # NOTE: testcase signal handler.
        self.mathematics = Mathematics()

        self.p = float(self.kwargs.get('p', 1)) # PROBABILITY
        
        self.Nx = len(self.x)
        for idx, xi in enumerate(self.x):
            if isinstance(xi, str):
                self.x[idx] = self.loader(xi)
            setattr(self, f'x{idx}', self.x[idx])
        if self.Nx == 0:
            self.x = None
        elif self.Nx == 1:
            self.x = self.x0
        else:
            # self.x = None
            pass
        
        self.signal()

        if self.kwargs.get('RUN', True): # OPTIONAL
            self.x = self.preprocessing()
            self.y = self.processing()
            self.y = self.postprocessing()
            self.y = self.type_cast()
        
        VIEW = self.kwargs.get('VIEW', None)
        if VIEW:
            query = VIEW['query']
            self.view(*query, **VIEW)

    def loader(self, fpath):
        return npload(fpath, **self.kwargs.get('LOADER', dict())) # OPTIONAL

    def signal(self):
        pass

    def preprocessing(self):
        return self.x
    
    def processing(self):
        return self.x

    def postprocessing(self):
        return self.y

    def type_cast(self):
        return self.y

    def view(self, *query, n=-1, s=1, **kwargs): # TODO
        if len(query) == 0:
            query = ['x', 'y']
        
        n = int((len(query) ** .5) if n == -1 else n) # number of signals in each row in grid view.
        assert n>=1



if __name__ == '__main__':
    dsp = DSP()