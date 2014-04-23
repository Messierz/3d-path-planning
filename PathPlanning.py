__author__ = 'Bonus'

import sys
import pygame
import time
import pprint
import math
import numpy as np
from Point3D import *
from Obstacle import *
from BresenhamLine3D import *

class PathPlanning(object):
    def __init__(self, start, goal, boundX, boundY, boundZ, obstacle):
        self.start = start
        self.goal = goal
        self.boundX = boundX
        self.boundY = boundY
        self.boundZ = boundZ
        self.obstacle = obstacle
        self.result = []

    def Solve(self):
        self.AStar_Algorithm()
        if not self.result:
            return None
        return self.PostSmoothingPath()


    def Lowest_F_Score(self):
        if len(self.openSet) > 1:
            index = 0
            min = self.f[self.openSet[0].z, self.openSet[0].y, self.openSet[0].x]
            for i in xrange(len(self.openSet)):
                if self.f[self.openSet[i].z, self.openSet[i].y, self.openSet[i].x] < min:
                    index = i
                    min = self.f[self.openSet[i].z, self.openSet[i].y, self.openSet[i].x]
            return index
        else:
            return 0

    def Reconstruct_Path(self, current):
        if current.Equal(self.start):
            self.result.append(current)
            return self.result
        else:
            self.result = self.Reconstruct_Path(self.parent[current.z][current.y][current.x])
            self.result.append(current)
            return self.result

    def AStar_Algorithm(self):
        self.closeSet = []
        self.openSet = []
        self.parent = [[[Point3D(0, 0, 0) for k in xrange(self.boundX)] for j in xrange(self.boundY)] for i in xrange(self.boundZ)]
        h = np.zeros((self.boundZ, self.boundY, self.boundX))
        g = np.zeros((self.boundZ, self.boundY, self.boundX))
        self.f = np.zeros((self.boundZ, self.boundY, self.boundX))
        for i in xrange(self.boundZ):
            for j in xrange(self.boundY):
                for k in xrange(self.boundX):
                    h[i, j, k] = self.goal.Distance(Point3D(point = (k, j, i)))

        current = self.start
        self.openSet.append(current)
        self.f[current.z, current.y, current.x] = float(math.sqrt(h[current.z, current.y, current.x]))
        while len(self.openSet) > 0:
            index = self.Lowest_F_Score()
            current = self.openSet[index]
            if current.Equal(self.goal):
                return self.Reconstruct_Path(self.goal)

            self.closeSet.append(current)
            del self.openSet[index]
            neighbors = current.Neighbors(self.boundX, self.boundY, self.boundZ)
            for neighbor in neighbors:
                if not self.obstacle:
                    if neighbor.IsExistedIn(self.closeSet):
                        continue
                else:
                    if neighbor.IsExistedIn(self.closeSet) or neighbor._IsExistedIn(self.obstacle):
                        continue
                tentativeGScore = g[current.z, current.y, current.x] + current.Distance(neighbor)
                x = neighbor.x
                y = neighbor.y
                z = neighbor.z
                if not neighbor.IsExistedIn(self.openSet):
                    g[z, y, x] = sys.maxint
                    self.openSet.append(neighbor)
                if tentativeGScore < g[z, y, x]:
                    g[z, y, x] = tentativeGScore
                    self.f[z, y, x] = float(math.sqrt(g[z, y, x])) + float(math.sqrt(h[z, y, x]))
                    self.parent[z][y][x] = current
        return None

    def PostSmoothingPath(self):
        psPath = []
        psPath.append(self.result[0])
        if not self.obstacle:
            psPath.append(self.result[len(self.result) - 1])
            return psPath
        k = 0
        for i in xrange(1, len(self.result) - 1):
            if not BresenhamLine3D(psPath[k], self.result[i]).LineOfSight(self.obstacle):
                k += 1
                psPath.append(self.result[i])
        psPath.append(self.result[i])
        self.result = psPath
        return psPath

start_time = time.clock()
start = Point3D(x = 0, y = 0, z = 0)
img = cv2.imread('input.png')
goal = Point3D(x = 82, y = 60, z = 50)
# img = cv2.imread('input_.png')
# goal = Point3D(x = 138, y = 160, z = 50)
# img = cv2.imread('input__.png')
# goal = Point3D(x = 350, y = 222, z = 40)
obstacle = Obstacle(img, 100).GenerateObstacleList()
# p = Point3D(50, 40, 30)
# print p._IsExistedIn(obstacle)
print time.clock() - start_time

boundX = img.shape[1]
boundY = img.shape[0]
boundZ = 100
p = PathPlanning(start, goal, boundX, boundY, boundZ, obstacle)
result = p.Solve()
print time.clock() - start_time
if result:
    for i in xrange(len(result) - 1):
        cv2.line(img, (result[i].x, result[i].y), (result[i+1].x, result[i+1].y), (0, 0, 255), 1)
    cv2.imshow('result', img)
pprint.pprint(result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# p = BresenhamLine3D(Point3D(0, 0, 0), Point3D(5, 5, 5))
# pprint.pprint(p.GetAllPoint())
# print(p.LineOfSight([Point3D(3,3,3)]))

# start = Point3D(0, 0, 0)
# goal = Point3D(5, 6, 7)
# result = PathPlanning(start, goal, 8, 8, 8, None).Solve()
# print result




