from KERNEL.PYTHON.classes.basic import PYBASE

class CallBack(PYBASE):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass