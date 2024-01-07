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