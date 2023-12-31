from KERNEL.PYTHON.classes.basic import PYBASE

class Module(PYBASE):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass