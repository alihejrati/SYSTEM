from . import DataSet

class Categorical(DataSet):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.__start()

    def __start(self):
        pass