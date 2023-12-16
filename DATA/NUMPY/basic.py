import numpy as np
from ..IO import fs

def load(fpath: str,):
    if fpath.startswith('*'): # NOTE: index path
        fpath = fs.path('@numpy', 'import', fpath[1:])
    else:
        fpath = fs.path(fpath, f_back=1)
    
    sig = np.load(fpath)
    return sig

if __name__ == '__main__':
    pass # unit test