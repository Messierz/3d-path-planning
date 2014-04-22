__author__ = 'messierz'

import sys
import cv2
import pprint
import numpy as np
from Point3D import *

class Obstacle():
    def __init__(self, image, maxHeight):
        self.image = image
        self.maxHeight = maxHeight
        self.obstacle = []

    def GenerateObstacleList(self):
        for i in xrange(self.image.shape[0]):
            for j in xrange(self.image.shape[1]):
                if self.image[i, j, 0] < self.maxHeight:
                    self.obstacle.append(Point3D(j, i, self.maxHeight - self.image[i, j, 0]))
        return self.obstacle
