# TODO fold, unfold, sethook 
# NOTE: x.shape=anything!    
# NOTE: xv.shape=(d,)        
# NOTE: x1d.shape=(B,d)      
# NOTE: x2d.shape=(B,h,w)    
# NOTE: x3d.shape=(B,ch,h,w) 

# NOTE: my point of view to tensor directory is functional not object oriented!

import torch
from torch.nn import functional as F