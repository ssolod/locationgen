# *****************************************
#
# mostly taken from 
# https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon/
#
# *****************************************

from enum import Enum

class Point: 
    def __init__(self, x, y): 
        self.x = x 
        self.y = y 

    def __str__(self):
        return "x=%f,y=%f" % (self.x, self.y)

    def __repr__(self):
        return "[%f,%f]" % (self.x, self.y)
      
  
# define orientation between 3 points
class Orientation(Enum):
    COLINEAR = 1          # all points are on the same line
    CLOCKWISE = 2         # points are presented in a clockwise order 
    COUNTERCLOCKWISE = 3  # points are presented in a counter-clockwise order


# Given three colinear points p, q, r, the function checks if  
# point q lies on line segment 'pr'  
def onSegment(p, q, r): 
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))): 
        return True
    return False
  

def getOrientation(p, q, r): 
    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/  
    # for details of below formula.  
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y)) 
    if (val > 0): 
        return Orientation.CLOCKWISE
    elif (val < 0): 
        return Orientation.COUNTERCLOCKWISE
    else: 
        return Orientation.COLINEAR
          

# logic on how this works is outlined here
# https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
def doIntersect(startA,endA,startB,endB): 
    
    # Find the 4 orientations required for  
    # the general and special cases 
    o1 = getOrientation(startA, endA, startB) 
    o2 = getOrientation(startA, endA, endB) 
    o3 = getOrientation(startB, endB, startA) 
    o4 = getOrientation(startB, endB, endA)

    # General case 
    if ((o1 != o2) and (o3 != o4)): 
        return True
  
    # Special Cases 
  
    # {startA,endA} and startB are colinear
    # and startB lies on segment {startA,endA}
    if ((o1 == Orientation.COLINEAR) and onSegment(startA, startB, endA)): 
        return True
  
    # {startA,endA} and endB are colinear
    # and endB lies on segment {startA,endA}
    if ((o2 == Orientation.COLINEAR) and onSegment(startA, endB, endA)): 
        return True
  
    # {startB,endB} and startA are colinear
    # and startA lies on segment {startB,endB}
    if ((o3 == Orientation.COLINEAR) and onSegment(startB, startA, endB)): 
        return True
  
    # {startB,endB} and endA are colinear
    # and endA lies on segment {startB,endB}
    if ((o4 == Orientation.COLINEAR) and onSegment(startB, endA, endB)): 
        return True
  
    # If none of the cases 
    return False


# Returns True if the point p lies inside the polygon
# The logic is to create a line segment from given point to right infinity
# check if number of intersections is odd (means point it inside)
def isInside(polygonPoints, point):

    # There must be at least 3 vertices in polygon
    if len(polygonPoints) < 3:
      return False

    # Create a point for line segment from p to infinite
    LargeX = 1000000
    extreme = Point(LargeX, point.y)

    # Count intersections of the above line with sides of polygon
    count = 0
    for index in range(len(polygonPoints)):
        nextIndex = (index+1) % len(polygonPoints)

        # Check if the line segment from 'point' to 'extreme' intersects
        # with the line segment from 'polygonPoints[index]' to
        # 'polygonPoints[nextIndex]'
        if doIntersect(polygonPoints[index], polygonPoints[nextIndex], point, extreme):
            # If the point 'point' is colinear with line segment 'index-nextIndex',
            # then check if it lies on segment. If it lies, return true,
            # otherwise false
            if getOrientation(polygonPoints[index], point, polygonPoints[nextIndex]) == Orientation.COLINEAR:
               return onSegment(polygonPoints[index], point, polygonPoints[nextIndex])

            count += 1

    # Return true if count is odd
    return count % 2 == 1

