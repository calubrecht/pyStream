import unittest
from src.pystream import Stream
from src.pystream import zipStreams

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

  def test_zip(self):
    data1 = (SimpleData("Bread", "Food", 23), SimpleData("Corn", "Food", 11), SimpleData("Robot", "Toy", 3))
    data2 = (1, 2)

    zipped = list(zipStreams(Stream(data1).filter(lambda d : d.classification == "Food"), Stream(data2)))

    self.assertEqual(2, len(zipped))
    self.assertEqual("Bread", zipped[0][0].objName)
    self.assertEqual(1, zipped[0][1])
    self.assertEqual("Corn", zipped[1][0].objName)
    self.assertEqual(2, zipped[1][1])

  def test_zipFromStreamable(self):
    stream1 = Stream((23, 100, 97))
    stream2 = Stream(("A", "B", "C"))

    zipped = list(stream1.zip(stream2))

    self.assertEqual(3, len(zipped))
    self.assertEqual((23, "A"), zipped[0])
    self.assertEqual((97, "C"), zipped[2])

  def test_zipMoreStreams(self):
    stream1 = Stream((23, 100, 97))
    stream2 = Stream(("A", "B", "C"))
    stream3 = Stream((3, 2, 1))

    zipped = list(zipStreams(stream1, stream2, stream3))

    self.assertEqual(3, len(zipped))
    self.assertEqual((23, "A", 3), zipped[0])
    self.assertEqual((97, "C", 1), zipped[2])
