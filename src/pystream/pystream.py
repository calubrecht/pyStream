from functools import reduce


class Stream:
    def __init__(self, streamable):
        self.streamable = streamable

    def __iter__(self):
        return self.streamable

    def map(self, mappedFunc):
        newStreamable = map(mappedFunc, self.streamable)
        return Stream(newStreamable)

    def filter(self, filterFunc):
        newStreamable = filter(filterFunc, self.streamable)
        return Stream(newStreamable)

    def reduce(self, reduceFunc):
        return reduce(reduceFunc, self.streamable)
