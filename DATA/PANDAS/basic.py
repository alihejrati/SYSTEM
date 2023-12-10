import numpy as np
import pandas as pd
from ..IO import fs

def create(data, **kwargs):
    """
        https://www.geeksforgeeks.org/different-ways-to-create-pandas-dataframe/
        data: 
            -> dict of colList
            -> list of rowDict
            -> list of rowList ; arg=>columns=[...]
            -> zip(colList) ; arg=>columns=[...]
    """
    df = pd.DataFrame(data, **kwargs.get('df', dict()))
    return df 

def save(fpath: str, df, **kwargs):
    if fpath.startswith('*'): # NOTE: index path
        fpath = fs.path('@pandas', 'export', fpath[1:], makedirs=True)
    else:
        fpath = fs.path(fpath, f_back=1, makedirs=True)

    ext = fs.ospsplit(fpath)[1].split('.')[-1]

    if ext == 'csv':
        return df.to_csv(fpath, **kwargs.get('csv', dict(sep=',', encoding='utf-8', index=False))) # OPTIONAL
    else:
        assert False
    

def load(fpath: str, **kwargs):
    if fpath.startswith('*'): # NOTE: index path
        fpath = fs.path('@pandas', 'import', fpath[1:])
    else:
        fpath = fs.path(fpath, f_back=1)
    
    ext = fs.ospsplit(fpath)[1].split('.')[-1]
    
    if ext == 'csv':
        df = pd.read_csv(fpath, **kwargs.get('csv', dict())) # OPTIONAL
    elif ext == 'xlsx':
        df = pd.read_excel(fpath, **kwargs.get('excel', dict())) # OPTIONAL
    else:
        assert False
    
    return df
