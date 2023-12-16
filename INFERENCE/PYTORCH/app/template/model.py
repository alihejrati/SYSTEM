from ...model import PLModel

class Model(PLModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass