# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 01:03:27 2018

@author: Ayberk Yaraneri
"""

import pylab as plt
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
    
    def getCoord(self):
        return (self.x, self.y, self.z)
    
    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

class Airfoil(object):
    def __init__(self, filename):
        self.filename = filename
        self.airfoilName = ''
        self.points = []
        self.twist = 0
        self.twisted_points = []

    def set_airfoilName(self, airfoilName):
        self.airfoilName = airfoilName
        
    def addPoint(self, x, y, z):
        point = Point(x, y, z)
        self.points.append(point)

    def twistAirfoil(self, theta):
        """
        Twists the given airfoil by theta degrees around the mid chord point (0.5, 0).
        theta: a float
        """
        self.twist += theta
        midChord = Point(0.5, 0.0, 0.0)
        self.twisted_points = []

        for point in self.points:
            x = point.getX()
            y = point.getY()

            alpha = math.degrees(math.atan2(y, (x-0.5)))
            hypotenuse_length = point.distance(midChord)
            
            newY = math.sin(math.radians(alpha+theta)) * hypotenuse_length
            newX = math.cos(math.radians(alpha+theta)) * hypotenuse_length

            self.twisted_points.append(Point(newX, newY, 0.0))
    
    def plotAirfoil(self):
        xVals = []
        yVals = []
        
        if self.twist != 0:
            for point in self.twisted_points:
                xVals.append(point.getX())
                yVals.append(point.getY())
        else:
            for point in self.points:
                xVals.append(point.getX())
                yVals.append(point.getY())
                pass
            
        plt.figure('plot1')
        plt.plot(xVals, yVals, label = self.airfoilName + ' twist:' + str(self.twist), linewidth = 0.5)
        plt.legend(loc = 'upper left')
        plt.ylim(-0.5, 0.5)
        plt.show()

    def __str__(self):
        return self.airfoilName + ' twist:' + str(self.twist)
    
def ConvertAirfoil(filename):
    '''
    input: selig format airfoil file to be converted into an Airfoil instance.
    returns an instance of the Airfoil class, with all coordinates from the input.
    '''
    try:
        origin = open(filename, 'r')
    except IOError:
        print("Couldn't open file or files.")
    else:
        airfoil = Airfoil(filename)

        pointArray = origin.read().split('\n')

        airfoil.set_airfoilName(pointArray[0])

        for point in pointArray[1:]:
            coordinates = point.split()
            if len(coordinates):
                airfoil.addPoint(float(coordinates[0]), float(coordinates[1]), 0.0)

        return airfoil

airfoil1 = ConvertAirfoil('clarky.dat')

airfoil1.twistAirfoil(20)
# airfoil1.twistAirfoil(0)
# airfoil1.twistAirfoil(20)
# airfoil1.twistAirfoil(20)

#Something weird is going on when I twist multiple times. The last twist angle always prevails in the plot, whereas the twist angle should be incremented.

airfoil1.plotAirfoil()
