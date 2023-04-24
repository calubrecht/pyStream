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
    '''
    Stream class wrapping an iterable and providing map, filter, etc. functions that return further Stream objects.
    '''
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
        '''
        Call the built-in map function on the wrapped iterable with the give function and return a new Stream
        :param mapped_func: function to apply with the map function
        :return: Stream object wrapping the result of map
        '''
        new_streamable = map(mapped_func, self.streamable)
        return Stream(new_streamable)

    def filter(self, filter_func: Callable) -> 'Stream':
        '''
        Call the built-in filter function on the wrapped iterable with the give function and return a new Stream
        :param filter_func: function to apply with the filter function
        :return: Stream object wrapping the result of filter
        '''
        new_streamable = filter(filter_func, self.streamable)
        return Stream(new_streamable)

    def zip(self, *other_streams: Iterable) -> 'Stream':
        '''
        Call the built-in zip function on the wrapper iterable and all other supplied streams/iteraables and return a new Stream
        :param other_streams: Stream objects or Iterables to zip with this Stream
        :return: Stream object wrapping the result of zip
        '''
        for stream in other_streams:
            if not isinstance(stream, Iterable):
                raise TypeError("Input " + str(stream) + " is not an Iterable")
        streamables = [self.streamable, ] + list(Stream(other_streams).map(lambda s: to_stream(s)))
        new_streamable = zip(*streamables)
        return Stream(new_streamable)

    @terminal_method
    def group(self, key_func: Callable) -> dict:
        '''
        Call the itertools.group_by function on the wrapper iterable with the supplied key_func and return a dict
        mapping keys to list of values and closes the stream
        :param key_func: Function to determine key to group by
        :return: dict of key to list of values
        '''
        grouped = {}
        for k, g in groupby(self.streamable, key_func):
            grouped[k] = list(g)
        return grouped

    @terminal_method
    def first(self):
        '''
        :return: Returns the first element of the stream (or None if stream is empty) and closes the stream
        '''
        try:
          return next(iter(self.streamable))
        except   StopIteration:
          return None

    @terminal_method
    def reduce(self, reduce_func: Callable):
        '''
        Performs the functools.reduce operation on the Stream with the given reduce function and closes the stream
        :param reduce_func: Function to apply reduce with
        :return: Result of reduce operation
        '''
        return reduce(reduce_func, self.streamable)

    def close(self):
        '''
        End the stream. Willl return no further values
        '''
        self.streamable = []


def to_stream(streamable: Iterable) -> Stream:
    '''
    Ensure that the output is a Stream by wrapping it if necessar
    :param streamable: an Iterable to return or wrap
    :return: The streamable input if a Stream, or a new Stream wrapping the input if not
    '''
    if isinstance(streamable, Stream):
        return streamable
    return Stream(streamable)


def zip_streams(*streams: Iterable) -> Stream:
    '''
    Apply zip function to a series of iterables and return a Stream object
    :param streams: Streams or iterables to zip
    :return: Stream object wrapping the return value of the zip function
    '''
    if len(streams) == 0:
        return Stream([])
    for s in streams:
        if not isinstance(s, Iterable):
            raise TypeError("Input <" + str(s) + "> is not an iterable")
    if len(streams) == 1:
        return to_stream(streams[0])
    return to_stream(streams[0]).zip(*streams[1:])
