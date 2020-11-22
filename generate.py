#!/usr/bin/python3.8

import sys
import argparse
from enum import Enum

from countryboundary import CountryBoundary
from randombasic import RandomPointRect
from randomcity import RandomPointCity

class GenerationMode(Enum):
  RANDOM = 0 # randomly generated locations
  URBAN = 1  # locations are generated close to large cities
  MIXED = 2  # a mix of random and urban

  @classmethod
  def fromString(cls, strValue):
    for c in cls:
      if c.name.lower() == strValue:
        return c
    raise ValueError

# helper when more than one type of generator is needed, e.g. mixed mode
class GeneratorPool:
  def __init__(self):
    self.pool = []
    self.current = 0

  def add(self, generator):
    self.pool.append(generator)

  def getNext(self):
    nextGenerator = self.pool[self.current]
    self.current = (self.current + 1) % len(self.pool)
    return nextGenerator; 

  def empty(self):
    return len(self.pool) == 0


def main():

  # parsing configuration
  parser = argparse.ArgumentParser()
  parser.add_argument("-n", "--numberOfPoints", type=int, required=True, help="number of points to generate")
  parser.add_argument("-f", "--boundaryFile", type=str, required=True, help="country boundary coordinates")
  parser.add_argument("-c", "--citiesFile", type=str, help="list of cities with coordinates, population and densities")

  # generating info for the mode argument
  modeChoices = [c.name.lower() for c in GenerationMode]
  parser.add_argument("-m", "--mode", type=str, required=True,
    choices=modeChoices, help="mode of generation: urban vs random vs mixed")

  args = parser.parse_args() 

  csvFile = args.boundaryFile
  countToGenerate = args.numberOfPoints

  print("Generating %d point(s) in a country defined by '%s' coordinates" % (countToGenerate, csvFile))

  # making up the country boundary
  boundary = CountryBoundary(csvFile)


  # choosing the mode and making generators
  generatorPool = GeneratorPool()

  mode = GenerationMode.fromString(args.mode)

  if mode == GenerationMode.RANDOM or mode == GenerationMode.MIXED:
    boundingBox = boundary.getBoundingBox()
    generatorPool.add(RandomPointRect(boundingBox[0], boundingBox[1]))

  if mode == GenerationMode.URBAN or mode == GenerationMode.MIXED:
    if not args.citiesFile:
      sys.exit("Cannot proceed with URBAN mode. Missing cities definitions argument.")
    generatorPool.add(RandomPointCity(args.citiesFile))

  if generatorPool.empty():
      sys.exit("Failed to configure random location generators. Check arguments.")

  # generating random datapoints
  randomWithinCountry = []

  count = 0
  while count < countToGenerate:
    # picking next generator
    generator = generatorPool.getNext()
    # picking next random point
    point = generator.pickRandom()
    if boundary.inside(point): 
      randomWithinCountry.append(point)
      count += 1

  for p in randomWithinCountry:
    print('%f,%f' % (p.x, p.y))




if __name__ == "__main__":
  main()

