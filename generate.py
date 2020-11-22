#!/usr/bin/python3.8

import argparse
import random
import csv
from enum import Enum

from polygon import Point, isInside
from randompoint import randomPoint

class CoordType(Enum):
  LAT  = 0
  LONG = 1
  
class CountryBoundary:

  def __init__(self, csvBoundaryPath):
    self.boundaryPoints = []
    # reading boundary definition
    with open(csvBoundaryPath) as countryBoundary:
      boundaryReader = csv.reader(countryBoundary)
      for point in boundaryReader:
        x = float(point[CoordType.LAT.value])
        y = float(point[CoordType.LONG.value])
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


# generates a random point in a given rectangle
def randomPoint(rectTopLeft, rectBottomRight):
  xRange = rectBottomRight.x - rectTopLeft.x
  yRange = rectBottomRight.y - rectTopLeft.y

  xRandom = rectTopLeft.x + xRange * random.random()
  yRandom = rectTopLeft.y + yRange * random.random()

  return Point(xRandom, yRandom)


def main():

  # parsing configuration
  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--count", type=int, required=True, help="number of points to generate")
  parser.add_argument("-f", "--file", type=str, required=True, help="country boundary coordinates")
  args = parser.parse_args() 

  csvFile = args.file
  countToGenerate = args.count

  print("Generating %d point(s) in a country defined by '%s' coordinates" % (countToGenerate, csvFile))

  # making up the country boundary
  boundary = CountryBoundary(csvFile)

  boundingBox = boundary.getBoundingBox()

  randomWithinCountry = []

  # generating random datapoints
  count = 0
  while count < countToGenerate:
    point = randomPoint(boundingBox[0], boundingBox[1])
    if boundary.inside(point): 
      randomWithinCountry.append(point)
      count += 1

  for p in randomWithinCountry:
    print('%f,%f' % (p.x, p.y))

if __name__ == "__main__":

  main()

