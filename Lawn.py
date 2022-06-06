from shapely.geometry import Point, Polygon
import numpy as np
class Lawn:
    def __init__(self):
        self.lawnCoordinates = list()
        self.lawnPolygon = False

    def containsCoordinate(self, coordinates):
        if not self.lawnPolygon:
            print("BAD NO LAWN DEFINED")
            return False
        return Point(coordinates[0], coordinates[1]).within(self.lawnPolygon)
    def defineBoundaries(self, a, b, c, d):
        self.lawnCoordinates = []
        self.lawnCoordinates.append(a)
        self.lawnCoordinates.append(b)
        self.lawnCoordinates.append(c)
        self.lawnCoordinates.append(d)
        self.lawnPolygon = Polygon(self.lawnCoordinates)
    def getPlotableBoundaryCoordinates(self):
        return np.array(self.lawnCoordinates, np.int32)
    def filterForCoordinatesOnLawn(self, coordinates):
        return [x for x in coordinates if self.containsCoordinate(x)]
