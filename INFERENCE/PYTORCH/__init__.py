import torch
from torch import nn
from KERNEL.SCRIPT.python.classes.basic import PYBASE

class Grad(PYBASE):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass

    def dzq_dz_eq1(self, zq, z, w=1):
        """
            transfer gradients from `zq` to `z`  | (zq -> z)
            `zq` and `z` must be the same shape
            (Notic): zq not change in terms of numerically but here we define a drevative path from zq to z such that (dzq/dz = 1)
            Example: 
                zq = dzq_dz_eq1(zq, z)
        """
        return (w * z) + (zq - (w * z)).detach()

    def safe(self, x, cb, w=1, **kwargs):
        xzq = cb(x.detach(), **kwargs)
        zxq = self.dzq_dz_eq1(xzq, x, w=w)
        return zxq