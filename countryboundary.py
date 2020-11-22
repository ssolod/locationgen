import csv

from enum import Enum

from point import Point
from polygon import isInside

class CSVSchema(Enum):
  LAT  = 0
  LONG = 1
  
class CountryBoundary:

  def __init__(self, csvBoundaryPath):
    self.boundaryPoints = []
    # reading boundary definition
    with open(csvBoundaryPath) as countryBoundary:
      boundaryReader = csv.reader(countryBoundary)
      for point in boundaryReader:
        x = float(point[CSVSchema.LAT.value])
        y = float(point[CSVSchema.LONG.value])
        self.boundaryPoints.append(Point(x,y))

  def __str__(self):
    return str(self.boundaryPoints)

  def getBoundingBox(self):
    lattitudes = [p.x for p in self.boundaryPoints]
    longitudes = [p.y for p in self.boundaryPoints]
    start = Point(min(lattitudes), min(longitudes))
    end = Point(max(lattitudes), max(longitudes))
    return start, end 

  def inside(self, point):
    return isInside(self.boundaryPoints, point)

