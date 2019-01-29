# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 01:03:27 2018

@author: Ayberk Yaraneri
"""

import matplotlib.pyplot as plt
import math

class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getZ(self):
        return self.z

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setZ(self, z):
        self.z = z

    def getCoord(self):
        return (self.x, self.y, self.z)

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

    def move(self, deltaX=0, deltaY=0, deltaZ=0):
        self.x += deltaX
        self.y += deltaY
        self.z += deltaZ

class Airfoil(object):
    def __init__(self, filename):
        self.filename = filename
        self.airfoil_name = ''
        self.points = []
        self.midPoint = Point(0.5, 0, 0)
        self.twist = 0
        self.chord = 1

        try:
            origin = open(self.filename, 'r')
        except IOError:
            print("Couldn't open file or files.")
        else:
            point_list = origin.read().split('\n')

            self.airfoil_name = point_list[0]

            for point in point_list[1:]:
                coordinates = point.split()
                if len(coordinates):
                    self.points.append(Point(float(coordinates[0]), float(coordinates[1]), 0.0))

    def set_airfoil_name(self, airfoil_name):
        self.airfoil_name = airfoil_name

    def addPoint(self, x, y, z, index):
        """
        x, y, z = coordinates of point to be added
        index = index at which the new point will be
        """
        point = Point(x, y, z)
        leftSplit = self.points[:index]
        rightSplit = self.points[(index + 1):]

        self.points = (leftSplit + [point] + rightSplit)

    def changeTwist(self, theta):
        """
        Rotates airfoil around midPoint by theta degrees.
        theta: a float
        """
        self.twist = theta

        for point in self.points:
            x = point.getX()
            y = point.getY()

            alpha = math.degrees(math.atan2((y - self.midPoint.getY()), (x - self.midPoint.getX())))
            hypotenuse_length = point.distance(self.midPoint)

            newY = math.sin(math.radians(alpha + self.twist)) * hypotenuse_length
            newX = math.cos(math.radians(alpha + self.twist)) * hypotenuse_length

            point.setX(newX + self.midPoint.getX())
            point.setY(newY + self.midPoint.getY())

    def moveAirfoil(self, deltaX=0, deltaY=0, deltaZ=0):
        self.midPoint.move(deltaX, deltaY, deltaZ)
        for point in self.points:
            point.move(deltaX, deltaY, deltaZ)

    def scaleAirfoil(self, scaleFactor):
        for point in self.points:
            x = point.getX()
            y = point.getY()

            point.setX(((x - self.midPoint.getX()) * scaleFactor) + self.midPoint.getX())
            point.setY(((y - self.midPoint.getY()) * scaleFactor) + self.midPoint.getY())

    def addSlot(self, xPos, yPos, r):
        """
        ONLY WORKS WHEN TWIST = 0 !!!
        Adds a circular slot for a carbon fiber tube in the airfoil.
        xPos and yPos = coordinates of the center of the  slot relative to the airfoil's midPoint
        r = radius of slot
        """
        if self.twist != 0:
            print('Twist angle not zero! Cannot add slot.')
        else:
            slotPoints = []
            numPoints = len(self.points)

            for i in range(numPoints//2, numPoints):
                xVal = self.points[i].getX()
                if xVal > xPos:
                    p2 = self.points[i]
                    p2_index = i
                    p1 = self.points[(i-1)]
                    break

            x1, y1 = p1.getX(), p1.getY()
            x2, y2 = p2.getX(), p2.getY()

            p = xPos
            q = (y1 + y2)/2

            slotStart = Point(p, q, 0.0)
            slotPoints.append(slotStart)

            circleStart = Point(xPos, (yPos - r), 0.0)
            slotPoints.append(circleStart)

            theta = 270
            for i in range(60):
                theta -= 6
                theta_r = math.radians(theta)

                newY = (math.sin(theta_r) * r) + yPos
                newX = (math.cos(theta_r) * r) + xPos

                slotPoints.append(Point(newX, newY, 0.0))

            slotPoints.append(slotStart)

            leftSplit = self.points[:p2_index]
            rightSplit = self.points[(p2_index + 1):]

            self.points = (leftSplit + slotPoints + rightSplit)

    def plotAirfoil(self):
        xVals = []
        yVals = []

        for point in self.points:
            xVals.append(point.getX())
            yVals.append(point.getY())

        plt.figure('plot1')
        plt.plot(xVals, yVals, 'r-', label = self.airfoil_name + ' twist:' + str(self.twist), linewidth = 0.5)
        plt.legend(loc = 'upper left')
        plt.ylim(-1, 1)
        plt.xlim(-1, 1)
        plt.axvline(self.midPoint.getX(), color = 'r', linewidth = 0.2)
        plt.axhline(self.midPoint.getY(), color = 'r', linewidth = 0.2)
        plt.show()

    def __str__(self):
        return self.airfoil_name + ' twist:' + str(self.twist)

airfoil1 = Airfoil('clarky.dat')

airfoil1.moveAirfoil(-0.5, 0.5)
# airfoil1.scaleAirfoil(3.0)

# airfoil1.changeTwist(-10)
# airfoil1.changeTwist(0)


airfoil1.moveAirfoil(0, -0.5)

# airfoil1.addPoint(0, 0, 0, 55)

airfoil1.addSlot(-0.3, 0.03, 0.02)
airfoil1.addSlot(-0.15, 0.03, 0.02)

airfoil1.moveAirfoil(1.0, 0)

airfoil1.addSlot(0.15, 0.03, 0.02)

# airfoil1.changeTwist(25)


airfoil1.plotAirfoil()
