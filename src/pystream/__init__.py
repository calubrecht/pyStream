'''
A module to create a Stream object which can be used to chain together map, filter, etc. calls in a manner similar
to java 8 streams.

A stream can be created from any iterable (list, tuple, the result of a map function call), like so

l = (1, 2, 3)
Stream(l).filter(filterFunc).map(mapFunc)
'''


from .pystream import Stream
from .pystream import zip_streams
from .pystream import to_stream
