import random

from point import Point

# generates a random point in a given rectangle
class RandomPointRect:
  def __init__(self, rectTopLeft, rectBottomRight):
    self.topLeft = rectTopLeft
    self.botRight = rectBottomRight

    self.xRange = self.botRight.x - self.topLeft.x
    self.yRange = self.botRight.y - self.topLeft.y

  def pickRandom(self):

    xRandom = self.topLeft.x + self.xRange * random.random()
    yRandom = self.topLeft.y + self.yRange * random.random()
    return Point(xRandom, yRandom)

