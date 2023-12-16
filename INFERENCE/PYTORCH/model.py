from KERNEL.PYTHON.classes.basic import PYBASE

class PTModel(PYBASE):
    """pytorch model"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass

class PLModel(PYBASE):
    """pytorch lightning model"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass