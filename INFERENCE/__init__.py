from KERNEL.SCRIPT.python.classes.basic import PYBASE
from KERNEL.SCRIPT.python.interface.database.sqlite import SQLite

class Metrics(PYBASE):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__start()

    def __start(self):
        self.metrics = dict()
        self.reductions = dict()

    def logger(self, tag: str, **kwargs):
        """this shoud be overwrite in each Logger class"""
        print(self.reductions[tag])

    def log(self, tag: str, logdict, **kwargs):
        """assuming that each `mv` is a scaller value!! if you dont this mind you can freely change this function such that compatability also exist:)"""
        for mk, mv in logdict.items():
            try:
                self.metrics[tag][mk].append(mv)
            except Exception as e:
                self.metrics[tag] = self.metrics.get(tag, dict())
                self.metrics[tag][mk] = self.metrics[tag].get(mk, [])
                self.metrics[tag][mk].append(mv)

    def save(self, tag: str, **kwargs):
        for MK, mv in self.metrics.get(tag, dict()).items():
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

        self.metrics[tag] = dict()
        self.reductions[tag] = dict()

    def reduction_sum(self, tag: str, mk: str, mv):
        return sum(mv)
    
    def reduction_mean(self, tag: str, mk: str, mv):
        return sum(mv) / len(mv)
    
    def reduction_ignore(self, tag: str, mk: str, mv):
        return None
    
    def reduction_accuracy(self, tag: str, mk: str, mv):
        globalname, localname = mk.split('/')
        subname = '{}/{}'.format(globalname, localname.replace('ACC', ''))
        TP = sum(self.metrics[tag][f'{subname}TP'])
        TN = sum(self.metrics[tag][f'{subname}TN'])
        FP = sum(self.metrics[tag][f'{subname}FP'])
        FN = sum(self.metrics[tag][f'{subname}FN'])
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
            
