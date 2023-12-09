import pandas as pd
from argparse import Namespace
from dotted_dict import DottedDict # from attrdict import AttrDict # Not work in python 3.10
from types import MethodType, FunctionType



def def_instance_method(Self, fnName: str, fn, **memory):
    fnType = fn.__class__.__name__.lower()
    assert fnType in ['function', 'method'], '`fnType={}` | does not supported currently you must do code for it'.format(fnType)
    assert fn.__code__.co_varnames[0] == 'self', 'we need to have `self` as `first` parameter in parameter list of `fnName={}` for define it as `instance method` of `class={}`'.format(fnName, Self.__class__)
    fn = decorator(fn, **memory)

    if fnType == 'function': # fn is defined `outside` of the class
        setattr(Self, fnName, MethodType(fn, Self))
    elif fnType == 'method': # fn is  defined `inside` of the class
        setattr(Self, fnName, fn)

    return getattr(Self, fnName)

# def ns_add(ns: Namespace, *posargs: Union[Namespace, dict]):
#     pass

def dotdict(d: dict, flag=None):
    flag = bool(True if flag is None else flag)
    if isinstance(d, dict) and flag:
        return DottedDict(d)
    return d

def dict2ns(d: dict):
    if isinstance(d, dict):
        return Namespace(**d)

def make_flatten_dict(d, sep='.'):
    return pd.json_normalize(d, sep=sep).to_dict(orient='records')[0]
