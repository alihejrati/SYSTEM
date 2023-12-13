import cv2
import numpy as np
from ....IO import fs
from ...dip import DIP
from ...basic import imshow, load
from ....PANDAS.basic import load as dfload

class FundusROT(DIP):
    def processing(self):
        df = dfload(self.kwargs['_DIP_DF_SPATH'])
        dpath = fs.ospsplit(self.kwargs['_DIP_SPATH'])[0]
        ROW = df[df['ID'] == self.kwargs['DIP_FNAME']].iloc[0]
        # LEFT = self.kwargs['DIP_FNAME'].split('.')[0].split('_')[1].lower() == 'left'
        FOV_X, FOV_Y, OD_X, OD_Y = ROW['FOV_X'], ROW['FOV_Y'], ROW['OD_X'], ROW['OD_Y']
        LEFT = FOV_X < OD_X
        for i in range(len(df)):
            self.X = self.x.copy()
            row = df.iloc[i]
            if row['ID'] == self.kwargs['DIP_FNAME']:
                continue
            q = load(fs.ospjoin(dpath, row['ID']))
            fov_x, fov_y, od_x, od_y = row['FOV_X'], row['FOV_Y'], row['OD_X'], row['OD_Y']
            # left = row['ID'].split('.')[0].split('_')[1].lower() == 'left'
            left = fov_x < od_x
            self.Q = q.copy() # Orginal
            if LEFT != left: # filp horizental
                q = self.geometry.flip(q, 'h')
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
            self.qrot = self.geometry.ROT(self.qrot, tx=tx_err+OD_X-od_x, ty=OD_Y-od_y)
            self.qrot = self.geometry.ROT(self.qrot, theta=alpha, center=[OD_X, OD_Y])
            self.draw.circle(self.qrot, [OD_X, OD_Y], color='#e01b1b')
            self.draw.circle(self.qrot, [FOV_X, FOV_Y], color='#1b70e0')
            # self.xq = self.x / 255 * 
            self.view('X', 'q', 'Q', 
                    'qrot', n=3, imshow=False, save=True, fpath=fs.ospjoin(
                self.kwargs['DIP_DPATH'],
                self.kwargs['DIP_FNAME'].split('.')[0],
                row['ID']
            ))











            # Qimg0 = Qimg.copy()

            # self.draw.line(Qimg, (od_x, od_y), (fov_x, fov_y), color=(0, 255, 0))
            # self.draw.line(Qimg, (od_x, od_y), (FOV_X, FOV_Y), color=(255, 0, 0))
            # self.draw.line(Qimg, (fov_x, fov_y), (FOV_X, FOV_Y), color=(0, 0, 255))
            
            # triangle = self.mathematics.triangle((od_x, od_y), (fov_x, fov_y), (FOV_X, FOV_Y))
            # alpha = triangle['angle']['alpha']
            # alpha = np.sign(fov_y - FOV_Y) * alpha
            # # if LEFT:
            # #     alpha = -1 * alpha
            # print(self.kwargs['DIP_FNAME'], row['ID'], alpha)

            # self.tmp = self.geometry.ROT(Qimg0, theta=alpha, tx=od_x-OD_X, ty=od_y-OD_Y)
            # self.tmp1 = Qimg
            # self.tmp2 = ((Qimg0.copy() / 255 * 0 + self.tmp.copy() / 255 * 1 + img / 255 * 0) * 255).astype(np.uint8)
            # self.draw.circle(self.tmp2, (fov_x, fov_y), 20, color=(0,0,0))
            # self.draw.circle(self.tmp2, (FOV_X, FOV_Y), 20)

            # self.draw.line(self.tmp2, (OD_X, OD_Y), (fov_x, fov_y), color=(0, 255, 0))
            # self.draw.line(self.tmp2, (OD_X, OD_Y), (FOV_X, FOV_Y), color=(255, 0, 0))
            # self.draw.line(self.tmp2, (fov_x, fov_y), (FOV_X, FOV_Y), color=(0, 0, 255))

            

if __name__ == '__main__':
    from . import ROOT_DIR
    FundusROT(
        DIP_SPATH='/home/alihejrati/Documents/Dataset/fundus - RetinaLessions/retinal-lesions-v20191227/images_896x896/*.jpg',
        DIP_SPATH_HEAD=30,
        DIP_DF_SPATH=f'{ROOT_DIR}/export/RetinaLessions.csv',
        DIP_DPATH=f'{ROOT_DIR}/export/RetinaLessions',
        # DIP_VIEW=dict(query=['x', 'y'], n=3, imshow=False, save=True),
    )