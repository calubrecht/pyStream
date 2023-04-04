import unittest
from src.pystream import Stream

class SimpleData:
  def __init__(self, objName, classification, count):
    self.objName = objName
    self.classification = classification
    self.count = count

class TestPystream(unittest.TestCase):

  def test_chainFilterMap(self):
    data = (SimpleData("Bread", "Food", 23), SimpleData("Corn", "Food", 11), SimpleData("Robot", "Toy", 3))

    mapped = Stream(data).filter(lambda d : d.classification=="Food").map(lambda d : str(d.count) + " " + d.objName + "s")

    mappedList = list(mapped)

    self.assertEqual(2, len(mappedList))
    self.assertEqual("23 Breads", mappedList[0])

  def test_streamFirst(self):
    data = (SimpleData("Bread", "Food", 23), SimpleData("Corn", "Food", 11), SimpleData("Robot", "Toy", 3))

    stream = Stream(data).filter(lambda d : d.classification=="Food")
    firstItem= stream.first()
    self.assertEqual("Bread", firstItem.objName)

    # stream is now finished, should have nothing to return
    with self.assertRaises(StopIteration):
      next(stream)

  def test_groupStream(self):
    data = (SimpleData("Bread", "Food", 23), SimpleData("Corn", "Food", 11), SimpleData("Robot", "Toy", 3))
    groups = Stream(data).group(lambda d: d.classification)

    self.assertEqual(2, len(groups))
    self.assertEqual(2, len(groups["Food"]))
    self.assertEqual(1, len(groups["Toy"]))

