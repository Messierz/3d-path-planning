__author__ = 'messierz'

import sys
import pygame
import time
import pprint
import math
import numpy as np

class Point3D(object):
    def __init__(self, x = 0, y = 0, z = 0, point = None):
        if point is None:
            self.x = x
            self.y = y
            self.z = z
        else:
            self.x = point[0]
            self.y = point[1]
            self.z = point[2]

    def __repr__(self):
        return "(%i, %i, %i)" %(self.x, self.y, self.z)

    def Distance(self, point):
        return (self.x - point.x) * (self.x - point.x) + \
               (self.y - point.y) * (self.y - point.y) + \
               (self.z - point.z) * (self.z - point.z)

    def Equal(self, point):
        return (self.x == point.x) and (self.y == point.y) and (self.z == point.z)

    def Neighbors(self, boundX, boundY, boundZ):
        neighbors = []
        for i in xrange(-1, 2):
            for j in xrange(-1, 2):
                for k in xrange(-1, 2):
                    if (self.z + i >= 0) and (self.z + i < boundZ) and \
                       (self.y + j >= 0) and (self.y + j < boundY) and \
                       (self.x + k >= 0) and (self.x + k < boundX) and \
                       not ((i == 0) and (j == 0) and (k == 0)) :
                        neighbors.append(Point3D(x = self.x + k, y = self.y + j, z = self.z + i))
        return neighbors

    def IsExistedIn(self, list):
        isExist = False
        for item in list:
            isExist = isExist or self.Equal(item)
        return isExist

    def _IsExistedIn(self, list):
        isExist = False
        for item in list:
            isExist = isExist or ((self.x == item.x) and (self.y == item.y) and (self.z < item.z))
        return isExist
