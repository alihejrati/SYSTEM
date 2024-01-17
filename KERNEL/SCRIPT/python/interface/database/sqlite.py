# https://github.com/coleifer/peewee

from . import SQL
from peewee import *

class SQLite(SQL):
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

if __name__ == '__main__':
    db = SQLite()
    db.create_tables({
        'tblA': {
            'name': {'type': 'CharField', 'params': {'unique': True}},
            'age': 'IntegerField',
            'score': {'type': 'FloatField', 'params': {'unique': True}},
        }
    })
    db.tables['tblA'].create(name='mmd222', age=13, score=2.461)
    db.tables['tblA'].create(name='ali222', age=26, score=210)