from functools import reduce
from itertools import groupby
from collections.abc import Iterable
from typing import Callable


def terminal_method(func):
    def wrapper(*args):
        stream_obj = args[0]
        res = func(*args)
        stream_obj.close()
        return res

    return wrapper


class Stream:
    def __init__(self, streamable: Iterable):
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

    def map(self, mapped_func: Callable) -> 'Stream':
        new_streamable = map(mapped_func, self.streamable)
        return Stream(new_streamable)

    def filter(self, filter_func: Callable) -> 'Stream':
        new_streamable = filter(filter_func, self.streamable)
        return Stream(new_streamable)

    def zip(self, *other_streams: Iterable) -> 'Stream':
        for stream in other_streams:
            if not isinstance(stream, Iterable):
                raise TypeError("Input " + str(stream) + " is not an Iterable")
        streamables = [self.streamable, ] + list(Stream(other_streams).map(lambda s: to_stream(s)))
        new_streamable = zip(*streamables)
        return Stream(new_streamable)

    @terminal_method
    def group(self, key_func: Callable) -> dict:
        grouped = {}
        for k, g in groupby(self.streamable, key_func):
            grouped[k] = list(g)
        return grouped

    @terminal_method
    def first(self):
        return next(iter(self.streamable))

    @terminal_method
    def reduce(self, reduce_func: Callable):
        return reduce(reduce_func, self.streamable)

    def close(self):
        self.streamable = []


def to_stream(streamable: Iterable) -> Stream:
    if isinstance(streamable, Stream):
        return streamable
    return Stream(streamable)


def zip_streams(*streams: Iterable) -> Stream:
    if len(streams) == 0:
        return Stream([])
    for s in streams:
        if not isinstance(s, Iterable):
            raise TypeError("Input <" + str(s) + "> is not an iterable")
    if len(streams) == 1:
        return to_stream(streams[0])
    return to_stream(streams[0]).zip(*streams[1:])
