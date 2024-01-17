# https://github.com/coleifer/peewee

import datetime
from peewee import *
from KERNEL.SCRIPT.python.classes.basic import PYBASE

class SQL(PYBASE):
    def __init__(self, db: str = None, **kwargs):
        super().__init__(**kwargs)
        self.db_path = db or '@HOME/database/SQLite/test.db'
        if not self.db_path.endswith('.db'):
            self.db_path = self.db_path + '.db'
        self.db_path = self.fspath(self.db_path, makedirs=True)
        self.__start()

    def __start(self):
        self.db = SqliteDatabase(self.db_path)
        self.db.connect()
        self.orm = self.ORM()
        self.tables = dict()

    def create_tables(self, tables):
        for tn, tc in tables.items(): # tn: table name, tc: table columns informations
            columns = dict() # table columns instancess
            for cn, _cv in tc.items(): # cn: column name, cv: column value
                if isinstance(_cv, str):
                    cv = dict(type=_cv, params=dict())
                else:
                    cv = _cv
                columns[cn] = eval(cv['type'])(**cv.get('params', dict()))
            
            self.tables[tn] = type(
                tn,
                (self.orm,),
                {
                    **columns,
                    'timestamp': DateTimeField(default=datetime.datetime.now)
                },
            )
        self.db.create_tables(list(self.tables.values()))
    
    def ORM(self):
        db = self.db
        class BaseModel(Model):
            class Meta:
                database = db
        return BaseModel
    