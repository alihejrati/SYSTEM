import torch
from .. import Grad
from torch import nn
from KERNEL.SCRIPT.python.classes.basic import PYBASE

class Lerner(PYBASE, nn.Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        self.Grad = Grad()
        # self.m
        # self.pl.device self.device = 'cuda' # dynamic it...

    def example(self):
        x = torch.randint(2,100, (4,4), dtype=torch.float32, requires_grad=True)
        x.register_hook(lambda grad: print('x.grad', grad))
        y = 2*x
        y.register_hook(lambda grad: print('y.grad', grad))
        y.retain_grad()
        z= 3*y
        z.register_hook(lambda grad: grad)
        z.register_hook(lambda grad: print('z.grad2', grad))

        z.retain_grad()
        h = 4*z
        h.register_hook(lambda grad: print('h.grad', grad))
        h.retain_grad()
        h.backward(torch.ones_like(h))