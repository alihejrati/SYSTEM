from KERNEL.PYTHON.classes.basic import PYBASE

class PTData(PYBASE):
    """pytorch dataloader/dataset"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass

class PLData(PYBASE):
    """pytorch lightning dataloader/dataset"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass