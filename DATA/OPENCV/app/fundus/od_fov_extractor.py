if __name__ == '__main__':
    from . import ROOT_DIR
    from ...dip import DIP
    from ...callback.pselect import PSelect
    DIP(
        DIP_SPATH='/home/alihejrati/Documents/Dataset/fundus - RetinaLessions/retinal-lesions-v20191227/images_896x896/*.jpg',
        DIP_SPATH_HEAD=3,
        DIP_DF_DPATH=f'{ROOT_DIR}/export/RetinaLessions.csv',
        DIP_CALLBACK=PSelect,
        DIP_CALLBACK_ARGS=dict(N=2, F=['X', 'Y'], P=['OD', 'FOV'])
    )