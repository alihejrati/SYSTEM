# TODO fold, unfold, sethook 
# NOTE: x.shape=anything!    
# NOTE: xv.shape=(d,)        
# NOTE: x1d.shape=(B,d)      
# NOTE: x2d.shape=(B,h,w)    
# NOTE: x3d.shape=(B,ch,h,w) 

import os, sys

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch

def fold3d(x, gp=None):
    """
        x is x3d
        gp is grid patch size
    """
    B, ch, h, w = x.shape
    gp = gp if gp else int(ch ** .5)
    return x.view(B, gp, gp, 1, h, w).permute(0, 3, 1, 4, 2, 5).contiguous().view(B, 1, gp*h, gp*w) 

if __name__ == '__main__':
    pass # unit test