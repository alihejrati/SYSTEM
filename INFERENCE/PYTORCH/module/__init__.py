from .. import Grad
from KERNEL.SCRIPT.python.classes.basic import PYBASE

from ... import Metrics # dynamic import...

class Module(PYBASE):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        self.Grad = Grad()
        self.metrics = Metrics()
        # self.data