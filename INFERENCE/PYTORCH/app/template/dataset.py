from ...dataset import PLData

class Data(PLData):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass