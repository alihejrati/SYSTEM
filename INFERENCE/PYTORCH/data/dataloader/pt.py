from . import DataLoader

class DataLoader(DataLoader):
    """pytorch dataloader/dataset"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        pass