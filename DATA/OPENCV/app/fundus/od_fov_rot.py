import cv2
import numpy as np
from ....IO import fs
from ...dip import DIP
import albumentations as A
from ...basic import imshow, load, save
from ....PANDAS.basic import load as dfload
from tqdm import tqdm

Tclahe = A.Compose([
    A.CLAHE(clip_limit=4.0, tile_grid_size=(8, 8), always_apply=True, p=1),
])

class FundusROT(DIP):
    def lmask(self):
        pure_leasion = np.zeros(self.X.shape)
        qpd, qpf = fs.ospsplit(self.qpath)
        lpaths = fs.ls(fs.ospjoin(qpd, '..', 'lesion_segs_896x896', qpf.replace('.jpg', ''), '*'))
        for lpath in lpaths:
            lesion = load(lpath)
            pure_leasion = pure_leasion + (lesion > 0).astype(np.float32)
        pure_leasion = (np.clip(pure_leasion, 0, 1) * 255).astype(np.uint8)
        self._lmask = pure_leasion
        self.puckets[fs.ospjoin(self.uppath_normal, 'lmask.jpg')] = self._lmask
        self.puckets[fs.ospjoin(self.uppath_clahe, 'lmask.jpg')] = self._lmask

    def lesion(self):
        self.puckets[fs.ospjoin(self.uppath_normal, 'lesion.jpg')] = (self.X - .8 * (1 - (self._lmask / 255)) * self.X).astype(np.uint8)
        self.puckets[fs.ospjoin(self.uppath_clahe, 'lesion.jpg')] = (self.Xclahe - .8 * (1 - (self._lmask / 255)) * self.Xclahe).astype(np.uint8)

    def fundus_mask(self):
        fmask = self.morphology.convex_hull(self.X[:,:,1])
        self.puckets[fs.ospjoin(self.uppath_normal, 'fmask.jpg')] = fmask
        self.puckets[fs.ospjoin(self.uppath_clahe, 'fmask.jpg')] = fmask
    
    def fundus(self):
        self.Xclahe = Tclahe(image=self.X)['image']
        self.puckets[fs.ospjoin(self.uppath_normal, 'fundus.jpg')] = self.X.copy()
        self.puckets[fs.ospjoin(self.uppath_clahe, 'fundus.jpg')] = self.Xclahe

    def cunvexhull(self):
        return
        cvh = self.morphology.convex_hull(self._lmask[:,:,0])
        self.puckets[fs.ospjoin(self.uppath_normal, 'cvh.jpg')] = cvh
        self.puckets[fs.ospjoin(self.uppath_clahe, 'cvh.jpg')] = cvh


    def processing(self):
        df = dfload(self.kwargs['_DIP_DF_SPATH'])
        dpath = fs.ospsplit(self.kwargs['_DIP_SPATH'])[0]
        ROW = df[df['ID'] == self.kwargs['DIP_FNAME']].iloc[0]
        IMG_NAME = self.kwargs['DIP_FNAME'].replace('.jpg', '')
        FOV_X, FOV_Y, OD_X, OD_Y = ROW['FOV_X'], ROW['FOV_Y'], ROW['OD_X'], ROW['OD_Y']
        LEFT = FOV_X < OD_X
        for i in tqdm(range(len(df))):
            self.X = self.x.copy()
            row = df.iloc[i]
            if row['ID'] == self.kwargs['DIP_FNAME']:
                continue
            self.qpath = fs.ospjoin(dpath, row['ID'])
            q = load(self.qpath)
            self.uppath_normal = fs.ospjoin(self.kwargs['DIP_DPATH'], IMG_NAME, row['ID'].replace('.jpg', ''))
            self.uppath_clahe = fs.ospjoin(self.kwargs['DIP_DPATH'], IMG_NAME, row['ID'].replace('.jpg', '') + '_clahe')
            fov_x, fov_y, od_x, od_y = row['FOV_X'], row['FOV_Y'], row['OD_X'], row['OD_Y']
            left = fov_x < od_x
            self.Q = q.copy() # Orginal
            self.X = q.copy()

            self.puckets = dict()
            self.fundus()
            self.lmask()
            self.lesion()
            self.fundus_mask()
            self.cunvexhull()

            if LEFT != left: # filp horizental
                q = self.geometry.flip(q, 'h')
                for puckkey in self.puckets:
                    self.puckets[puckkey] = self.geometry.flip(self.puckets[puckkey], 'h')
                width = q.shape[1]
                od_x = width - od_x - 1
                fov_x = width - fov_x - 1
            self.q = q # usable
            
            # q:od  -> banafsh roshan
            # q:fov -> zard
            self.draw.circle(self.q, [od_x, od_y], color='#b61be0')
            self.draw.circle(self.q, [fov_x, fov_y], color='#e0af1b')
            self.qrot = self.q.copy()
            self.draw.circle(self.q, [OD_X, OD_Y], color='#e01b1b')
            self.draw.circle(self.q, [FOV_X, FOV_Y], color='#1b70e0')
            # X:OD  -> ghermez
            # X:FOV -> abi           
            self.draw.circle(self.X, [OD_X, OD_Y], color='#e01b1b')
            self.draw.circle(self.X, [FOV_X, FOV_Y], color='#1b70e0')
            self.draw.circle(self.X, [od_x, od_y], color='#b61be0')
            self.draw.circle(self.X, [fov_x, fov_y], color='#e0af1b')

            tx_err = 0 # it shoulde be set as zero
            alpha = np.sign(FOV_Y-fov_y) * self.mathematics.triangle([OD_X, OD_Y], [FOV_X, FOV_Y], [fov_x+OD_X-od_x, fov_y+OD_Y-od_y])['angle']['alpha']
            if LEFT == False:
                alpha = -1 * alpha
            
            for puckkey in self.puckets:
                self.puckets[puckkey] = self.geometry.ROT(self.puckets[puckkey], tx=tx_err+OD_X-od_x, ty=OD_Y-od_y)
                self.puckets[puckkey] = self.geometry.ROT(self.puckets[puckkey], theta=alpha, center=[OD_X, OD_Y])
            self.qrot = self.geometry.ROT(self.qrot, tx=tx_err+OD_X-od_x, ty=OD_Y-od_y)
            
            self.qrot_after_translate = self.qrot.copy()
            self.draw.circle(self.qrot_after_translate, [OD_X, OD_Y], color='#e01b1b')
            self.draw.circle(self.qrot_after_translate, [FOV_X, FOV_Y], color='#1b70e0')
            self.draw.line(self.qrot_after_translate, [OD_X, OD_Y], [FOV_X, FOV_Y], color='#34a1eb')
            self.draw.line(self.qrot_after_translate, [OD_X, OD_Y], [fov_x+OD_X-od_x, fov_y+OD_Y-od_y], color='#ebe534')
            self.draw.line(self.qrot_after_translate, [FOV_X, FOV_Y], [fov_x+OD_X-od_x, fov_y+OD_Y-od_y], color='#030303')

            self.qrot = self.geometry.ROT(self.qrot, theta=alpha, center=[OD_X, OD_Y])
            self.draw.circle(self.qrot, [OD_X, OD_Y], color='#e01b1b')
            self.draw.circle(self.qrot, [FOV_X, FOV_Y], color='#1b70e0')

            
            for puckkey, puckval in self.puckets.items():
                save(puckkey, puckval)
            
            # self.view('x', 'q', 'Q', 
            #         'qrot_after_translate', 'qrot', n=3, imshow=False, save=True, fpath=fs.ospjoin(self.uppath_normal, 'example.jpg'))

if __name__ == '__main__':
    from . import ROOT_DIR
    FundusROT(
        DIP_SPATH='/home/alihejrati/Documents/Dataset/fundus - RetinaLessions/retinal-lesions-v20191227/images_896x896/*.jpg',
        DIP_SPATH_HEAD=30,
        DIP_DF_SPATH=f'{ROOT_DIR}/export/RetinaLessions.csv',
        DIP_DPATH=f'{ROOT_DIR}/export/RetinaLessions',
        # DIP_VIEW=dict(query=['x', 'y'], n=3, imshow=False, save=True),
    )