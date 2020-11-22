import csv
import math
import random
import bisect

from enum import Enum
from point import Point

class CSVSchema(Enum):
   NAME       = 0
   LATITUDE   = 1
   LONGITUDE  = 2
   POPULATION = 3
   DENSITY    = 4


# generic city class
class City:
  def __init__(self, name, lat, lng, population, density):
    self.name = name
    self.lat = lat
    self.lng = lng
    self.population = population
    self.density = density

  def __repr__(self):
    return "%s: %f, %f %d" % (self.name, self.lat, self.lng, self.population, self.density)


# given city chooses a random location around it
def randomOffsetFromCityCenter(city):
  density = city.density
  population = city.population
  area = population / density # square km

  # assuming cities are round :)
  cityRadius = math.sqrt(area/math.pi) * 1000 # in meters
  
  # choosing random direction and offset
  randomDirection = 2 * math.pi * random.random()
  
  # using normal distribution around 0 with standard deviation equals radius
  # we need half normal (no negative values)
  randomOffset = -1
  while randomOffset < 0:
    randomOffset = random.gauss(0, cityRadius)

  # computing new latitude and longitude for the random offset
  # http://www.movable-type.co.uk/scripts/latlong.html
  angDistance = randomOffset / 6371000
  bearing = randomDirection

  oldLat = math.radians(city.lat)
  oldLng = math.radians(city.lng)

  lat = math.asin(math.sin(oldLat) * math.cos(angDistance) +
      math.cos(oldLat) * math.sin(angDistance) * math.cos(bearing))

  lng = oldLng + math.atan2(math.sin(bearing) * math.sin(angDistance) * math.cos(oldLat),
      math.cos(angDistance) - math.sin(oldLat) * math.sin(lat))

  return Point(math.degrees(lat), math.degrees(lng))


class RandomPointCity:
  # helps simulate choosing random points 'biased/weighted' toward the
  # popular city ceters

  # list of all cities
  cities = []

  # population of the cities is used as a weight during random selection
  # we are maintaining two elements:
  #  - the total sum (total population) (range for random number picking)
  #  - lookup table with running accumulated sum
  # cities and running sum arrays are expected to coplement each other in lookup

  # overall range to choose a random number from
  randomRange = 0 

  # array that we will binary search to find the index of the city
  runningSum = [] 

  def __init__(self, citiesCSV):
    
    with open(citiesCSV) as citiesWithPopulation:
      citiesReader = csv.reader(citiesWithPopulation)
      for cityData in citiesReader:
        name = cityData[CSVSchema.NAME.value]
        lat = float(cityData[CSVSchema.LATITUDE.value])
        lng = float(cityData[CSVSchema.LONGITUDE.value])
        population = int(cityData[CSVSchema.POPULATION.value])
        density = float(cityData[CSVSchema.DENSITY.value])

        city = City(name, lat, lng, population, density)
        self.cities.append(city)

    # sorting the cities by population
    def populationKey(c):
       return c.population
    self.cities.sort(key = populationKey)

    # preparing random lookup structures
    for c in self.cities:
      self.randomRange += c.population
      self.runningSum.append(self.randomRange)


  def pickRandom(self):
    randomValueInRange = int(self.randomRange * random.random())
    randomCityIndex = bisect.bisect_right(self.runningSum, randomValueInRange)

    randomCity = self.cities[randomCityIndex]

    return randomOffsetFromCityCenter(randomCity)


