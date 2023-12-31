from . import Module

class Module(Module):
    """pytorch lightning module"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass