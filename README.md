pystream

This is a very simple module designed to allow python map/filter functions to be chained together.

The iterable that would normally be the second argument to map is instead passed as an argument to the Stream
constructor. The Stream constructor then has methods for filter/map that take only the function and return a new
Stream object for further functions to be called.

Usage:

from pystream import Stream

class sec:
    def __init__(self, secType, identifier, maturity):
        self.secType = secType
        self.identifier = identifier
        self.maturity = maturity



inventory = (sec("CORP", "ABCD", "2022"),sec("MMKT", "ABCE", "2083"),sec("MMKT", "ABCF", "2029"),sec("MUNI", "ABCJ", "1995"))

def isLive(s):
    return int(s.maturity) <= 2023

def toString(s):
  return s.maturity + ":" + s.identifier + ":" + s.maturity

def clomp(s1, s2):
    return s1 + "||" + s2

liveItems = Stream(inventory).filter(isLive).map(toString)

print (list(liveItems))
