from ...IO import fs
from ..callback import CallBack 
from ..basic import load, save, imshow
from ...PANDAS.basic import \
    save as dfsave, \
    create as dfcreate

class PSelect(CallBack):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        flag = bool(self.kwargs.get('flag', False))
        if flag: # slave call
            self.n = 0
            self.N = int(self.kwargs.get('N'))
        else: # master call
            self.run()

    def run(self):
        """
            N: number of points
            P: name of each point # OPTIONAL
            F: name of each feature # OPTIONAL
        """
        head = int(self.kwargs.get('head', -1))
        srcdir = str(self.kwargs.get('srcdir'))
        N = int(self.kwargs.get('N', 1))
        P = list(self.kwargs.get('P', [f'P{i+1}' for i in range(N)]))
        dfpath = str(self.kwargs.get('dfpath', '*opencv_script_pselect.csv'))
        
        assert len(P) == N

        data = []
        
        for idxf, fpath in enumerate(fs.ls(srcdir)):
            img = load(fpath)
            state = imshow(img, callback=self.__class__(N=N, flag=True))
            fname = fs.ospsplit(fpath)[1]
            dfrow = dict()
            for idxp, p in enumerate(state):
                F = list(self.kwargs.get('F', range(len(p)))) # OPTIONAL
                assert len(F) == len(p)
                for idxpi, pi in enumerate(p):
                    dfrow[f'{P[idxp]}_{F[idxpi]}'] = pi
            
            dip = self.kwargs.get('dip', None)
            if dip is not None:
                dip_obj = dip(img, DIP_POINTS=dfrow, DIP_POINTS_NAME=P, DIP_POINTS_FEATURE_NAME=F)
                dfrow = dict(**dip_obj.kwargs.get('DIP_POINTS', dict()))

            dfrow = dict(ID=fname, **dfrow)

            data.append(dfrow)
            
            if idxf == head - 1:
                break
        
        dfsave(dfpath, dfcreate(data))

    def CB_EVENT_LBUTTONDOWN(self, **kwargs):
        """
            # NOTE: you can overwrite this function for new inherited PSelect class, i.e. for extracting other features than x,y.
        """
        if self.n < self.N:
            self.n += 1
            self.state.append([kwargs['x'], kwargs['y']]) # NOTE: overwritable candidate => feature extraction

        if self.n >= self.N:
            self.winclose()
    
if __name__ == '__main__':
    from .processing.sharpening import Basic
    PSelect(
        head=3,
        srcdir='/home/alihejrati/Documents/Dataset/fundus - RetinaLessions/retinal-lesions-v20191227/images_896x896/*.jpg',
        dfpath='*/RetinaLessions.csv',
        dip=Basic,
        N=2,
        F=['X', 'Y'],
        P=['OD', 'FOV'],
    )