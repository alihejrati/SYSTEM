from KERNEL.PYTHON.classes.basic import PYBASE

class PLCB1(PYBASE):
    """pytorch lightning callback1"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass