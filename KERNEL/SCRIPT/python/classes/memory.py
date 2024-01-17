from .basic import PYBASE

class Memory(PYBASE):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        self.memory = dict()

    def log(self, tag: str, logdict, **kwargs):
        """assuming that each `mv` is a scaller value!! if you dont this mind you can freely change this function such that compatability also exist:)"""
        for mk, mv in logdict.items():
            try:
                self.memory[tag][mk].append(mv)
            except Exception as e:
                self.memory[tag] = self.memory.get(tag, dict())
                self.memory[tag][mk] = self.memory[tag].get(mk, [])
                self.memory[tag][mk].append(mv)
