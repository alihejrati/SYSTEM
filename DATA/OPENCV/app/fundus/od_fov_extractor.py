if __name__ == '__main__':
    from . import ROOT_DIR
    from ...dip import DIP
    from ...callback.pselect import PSelect
    DIP(
        SPATH='/home/alihejrati/Documents/Dataset/fundus - RetinaLessions/retinal-lesions-v20191227/images_896x896/*.jpg',
        # SPATH_HEAD=3,
        DF_DPATH=f'{ROOT_DIR}/export/RetinaLessions.csv',
        # VIEW=dict(query=['x', 'y'], n=2, imshow=False, save=True),
        CALLBACK=PSelect,
        CALLBACK_ARGS=dict(N=2, F=['X', 'Y'], P=['OD', 'FOV'])
    )