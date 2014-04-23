__author__ = 'messierz'

import math
from Point3D import *

class BresenhamLine3D():
    def __init__(self, point1, point2):
        self.x1 = point1.x
        self.y1 = point1.y
        self.z1 = point1.z
        self.x2 = point2.x
        self.y2 = point2.y
        self.z2 = point2.z
        self.pointsInLine = []

    def GetAllPoint(self):
        p = [self.x1, self.y1, self.z1]
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        dz = self.z2 - self.z1
        xInc = -1 if dx < 0 else 1
        yInc = -1 if dy < 0 else 1
        zInc = -1 if dz < 0 else 1
        l = int(math.fabs(dx))
        m = int(math.fabs(dy))
        n = int(math.fabs(dz))
        ax = l << 1
        ay = m << 1
        az = n << 1
        if l >= m and l >= n:
            err1 = ay - l
            err2 = az - l
            for i in xrange(l):
                self.pointsInLine.append(Point3D(p[0], p[1], p[2]))
                if err1 > 0:
                    p[1] += yInc
                    err1 -= ax
                if err2 > 0:
                    p[2] += zInc
                    err2 -= ax
                err1 += ay
                err2 += az
                p[0] += xInc

        elif m >= l and m >= n:
            err1 = ax - m
            err2 = az - m
            for i in xrange(m):
                self.pointsInLine.append(Point3D(p[0], p[1], p[2]))
                if err1 > 0:
                    p[0] += xInc
                    err1 -= ay
                if err2 > 0:
                    p[2] += zInc
                    err2 -= ay
                err1 += ax
                err2 += az
                p[1] += yInc

        else:
            err1 = ax - n
            err2 = ay - n
            for i in xrange(n):
                self.pointsInLine.append(Point3D(p[0], p[1], p[2]))
                if err1 > 0:
                    p[0] += xInc
                    err1 -= az
                if err2 > 0:
                    p[1] += yInc
                    err2 -= az
                err1 += ax
                err2 += ay
                p[2] += zInc
        self.pointsInLine.append(Point3D(p[0], p[1], p[2]))
        # return self.pointsInLine

    def LineOfSight(self, obstacle):
        self.GetAllPoint()
        for item in self.pointsInLine:
            if item._IsExistedIn(obstacle):
                return False
        return True
