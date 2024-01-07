# NOTE: working with disk(s)

import os, sys
from glob import glob
from os.path import \
    join as ospjoin, \
    isdir as ospisdir, \
    split as ospsplit, \
    dirname as ospdirname,\
    abspath as ospabspath

__MARK_FILE = '.mark'
__LOCAL_DIR = ospsplit(__file__)[0]
__ROOT_DIR = ospjoin(__LOCAL_DIR, '..', '..')
__STRUCTURE = dict()

for i in os.listdir(__ROOT_DIR):
    if ospisdir(i):
        for j in os.listdir(ospjoin(__ROOT_DIR, i)):
            if i.isupper() and j.isupper():
                __STRUCTURE['@' + j] = ospjoin(__ROOT_DIR, i, j)

def ls(*src):
    src = os.sep.join(src)
    res = glob(src)
    return res

def path(*fpath, **kwargs):
    """fpath is a file path not directory path"""
    fpath = os.sep.join(fpath)
    
    if fpath.startswith('*'): # NOTE: index path
        fpath = ospjoin(__STRUCTURE['@IO'], 'import', fpath[1:])
    elif fpath.startswith('@'): # NOTE: index path
        fpath_split = fpath.split(os.sep)
        fpath_split[0] = __STRUCTURE[fpath_split[0].upper()]
        fpath = os.sep.join(fpath_split)


    if fpath.startswith('.'): # NOTE: relative path
        f_back = int(kwargs.get('f_back', 0)) # OPTIONAL: number of intermediate functions respect to source function. value 0 it means source function directly call this function and value 1 it means source function calls 1 intremediate function and that function calls this function. and so on ...
        sys_getframe = sys._getframe()
        for i in range(1 + f_back):
            sys_getframe = sys_getframe.f_back
        fpath = ospjoin(
            ospsplit(ospabspath(sys_getframe.f_code.co_filename))[0], # `Directory path` of a specefic module that indecates relative path.
            fpath # relative path
        )
    

    if kwargs.get('makedirs', False): # OPTIONAL
        os.makedirs(ospsplit(fpath)[0], exist_ok=True)

    # if kwargs.get('mark', False): # OPTIONAL
    #     mark_file = str(kwargs.get('mark_file', __MARK_FILE)) # OPTIONAL
    #     pass

    return fpath
        


if __name__ == '__main__':
    print(path('@opencv', 'import', 'lena.jpg'))