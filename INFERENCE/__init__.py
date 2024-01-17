import re
from KERNEL.SCRIPT.python.classes.memory import Memory
from KERNEL.SCRIPT.python.interface.database.sqlite import SQLite

class Points(Memory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        self.points = self.memory
    
    def save(self):
        pass

class Metrics(Memory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        self.R = dict()
        self.reductions = dict()
        self.metrics = self.memory

    def logger(self, tag: str, **kwargs):
        """this function shoud be overwrite in each child class"""
        print(self.reductions)
    
    def save(self, tag: str, **kwargs):
        for MK, mv in self.memory.get(tag, dict()).items():
            mk, mr = (MK + ':reduction_mean').split(':')[:2]
            mrv = getattr(self, mr)(tag, mk, mv)
            if mrv is None:
                continue
            try:
                self.reductions[tag][mk] = mrv
            except Exception as e:
                self.reductions[tag] = self.reductions.get(tag, dict())
                self.reductions[tag][mk] = mrv
        
        self.logger(tag, **kwargs)

        self.R[tag] = self.reductions[tag]
        self.memory[tag] = dict()
        self.reductions[tag] = dict()

        return self.R[tag]

    def inference(self, tag: str, regexp: str, **kwargs):
        R = kwargs.get('R', self.R[tag]) # OPTIONAL
        reduction = kwargs.get('reduction', 'reduction_mean') # OPTIONAL

        RV = []
        pattern = re.compile(regexp)
        for rk, rv in R.items():
            if pattern.match(rk):
                RV.append(rv)
        return getattr(self, reduction)(tag, None, RV)

    def reduction_sum(self, tag: str, mk: str, mv):
        return sum(mv)
    
    def reduction_mean(self, tag: str, mk: str, mv):
        return sum(mv) / len(mv)
    
    def reduction_ignore(self, tag: str, mk: str, mv):
        return None
    
    def reduction_accuracy(self, tag: str, mk: str, mv):
        globalname, localname = mk.split('/')
        subname = '{}/{}'.format(globalname, localname.replace('ACC', ''))
        TP = sum(self.memory[tag][f'{subname}TP:reduction_ignore'])
        TN = sum(self.memory[tag][f'{subname}TN:reduction_ignore'])
        FP = sum(self.memory[tag][f'{subname}FP:reduction_ignore'])
        FN = sum(self.memory[tag][f'{subname}FN:reduction_ignore'])
        return (TP + TN) / (TP + TN + FP + FN)


class SQLiteLogger(Metrics):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        self.sqlite = SQLite(db=self.kwargs['db'])

    def logger(self, tag: str, **kwargs):
        try:
            self.sqlite.tables[tag].create(**self.reductions[tag])
        except Exception as e:
            if self.sqlite.tables.get(tag, None) is None:
                self.sqlite.create_tables({
                    tag: dict((mk, dict(type='FloatField', params=dict())) for mk, mv in self.reductions[tag].items())
                    # TODO currently only we assume each field is FloatField and have no params for FloatField class, you can extend types later...
                })
                self.sqlite.tables[tag].create(**self.reductions[tag])
            else:
                raise e
            
