import cv2
import numpy as np
from ....IO import fs
from ...dip import DIP
from ...basic import imshow, load
from ....PANDAS.basic import load as dfload

class FundusROT(DIP):
    def processing(self):
        img = self.x
        df = dfload(self.kwargs['_DIP_DF_SPATH'])
        dpath = fs.ospsplit(self.kwargs['_DIP_SPATH'])[0]
        ROW = df[df['ID'] == self.kwargs['DIP_FNAME']+''].iloc[0]
        LEFT = self.kwargs['DIP_FNAME'].split('.')[0].split('_')[1].lower() == 'left'
        FOV_X, FOV_Y, OD_X, OD_Y = ROW['FOV_X'], ROW['FOV_Y'], ROW['OD_X'], ROW['OD_Y']
        print('--->', FOV_X, FOV_Y, OD_X, OD_Y)
        for i in range(len(df)):
            row = df.iloc[i]
            Qimg = load(fs.ospjoin(dpath, row['ID']))
            fov_x, fov_y, od_x, od_y = row['FOV_X'], row['FOV_Y'], row['OD_X'], row['OD_Y']
            print(fov_x, fov_y, od_x, od_y)
            left = row['ID'].split('.')[0].split('_')[1].lower() == 'left'
            
            if LEFT != left: # filp horizental
                Qimg = self.geometry.flip(Qimg, 'h')
                width = Qimg.shape[1]
                od_x = width - od_x - 1
                fov_x = width - fov_x - 1


            self.draw.line(Qimg, (od_x, od_y), (fov_x, fov_y), color=(0, 255, 0))
            self.draw.line(Qimg, (od_x, od_y), (FOV_X, FOV_Y), color=(255, 0, 0))
            self.draw.line(Qimg, (fov_x, fov_y), (FOV_X, FOV_Y), color=(0, 0, 255))
            
            # self.tmp = self.geometry.ROT(Qimg, theta=0, tx=OD_X-od_x, ty=OD_Y-od_y)
            self.tmp1 = Qimg
            self.view('x', 'tmp1', n=2, imshow=False, save=True, fpath=fs.ospjoin(
                self.kwargs['DIP_DPATH'],
                self.kwargs['DIP_FNAME'].split('.')[0],
                row['ID']
            ))


if __name__ == '__main__':
    from . import ROOT_DIR
    FundusROT(
        DIP_SPATH='/home/alihejrati/Documents/Dataset/fundus - RetinaLessions/retinal-lesions-v20191227/images_896x896/*.jpg',
        DIP_SPATH_HEAD=3,
        DIP_DF_SPATH=f'{ROOT_DIR}/export/RetinaLessions.csv',
        DIP_DPATH=f'{ROOT_DIR}/export/RetinaLessions',
        # DIP_VIEW=dict(query=['x', 'y'], n=3, imshow=False, save=True),
    )