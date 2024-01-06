def decorator(func, **memory):
    def inner(*args, **kwargs):
        kwargs['memory'] = memory
        return func(*args, **kwargs, memory=memory)
    return inner
