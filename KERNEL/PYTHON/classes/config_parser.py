# TODO

import iniherit
from .basic import PYBASE

class ConfigParser(PYBASE):
    config = dict() # share across all instances.

    def __init__(self, name, fpath, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.fpath = fpath
    
    def set_config(self, cfg):
        self.__class__.config[self.name] = cfg 

    def get_config(self, name=None):
        if name is None:
            return self.__class__.config
        return self.__class__.config[name]

class INI_Parser(ConfigParser):
    """https://github.com/cadithealth/iniherit"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.cfg_handler = iniherit.SafeConfigParser()
        self.set_config(self.cfg_handler.read(self.fpath))

if __name__ == '__main__':
    # TEST 0
    print(PYBASE)
    # config = INI_Parser('masterconf', '../import/config_parser/config.ini')
    # ini_parser.get('loggers', 'keys')
    # ini_parser.get('loggers', 'wdef')
    # ini_parser.get('loggers', 'nada')
    pass