from . import Loss

class AdvLoss(Loss):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.__start()

    def __start(self):
        pass