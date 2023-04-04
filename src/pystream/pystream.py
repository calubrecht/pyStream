from functools import reduce
from itertools import groupby

def terminalMethod(func):
    def wrapper(*args):
        streamObj = args[0]
        res = func(*args)
        streamObj.close()
        return res
    return wrapper

class Stream:
    def __init__(self, streamable):
        self.streamable = streamable
        self.iter = None

    def __iter__(self):
        if not self.iter:
          self.iter = iter(self.streamable)
        return self.iter

    def __next__(self):
        if not self.iter:
          self.iter = iter(self.streamable)
        return next(self.iter)

    def map(self, mappedFunc):
        newStreamable = map(mappedFunc, self.streamable)
        return Stream(newStreamable)

    def filter(self, filterFunc):
        newStreamable = filter(filterFunc, self.streamable)
        return Stream(newStreamable)

    @terminalMethod
    def group(self, keyFunc):
        grouped = {}
        for k,g in groupby(self.streamable, keyFunc):
            grouped[k] = list(g)
        return grouped

    @terminalMethod
    def first(self):
        return next(self.streamable)

    @terminalMethod
    def reduce(self, reduceFunc):
        return reduce(reduceFunc, self.streamable)

    def close(self):
        self.streamable = []
