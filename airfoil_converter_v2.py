# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 01:03:27 2018

@author: Ayberk Yaraneri
"""

import pylab as plt
from math import sqrt

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
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

class Airfoil(object):
    def __init__(self, name):
        self.name = name
        self.points = []
        
    def addPoint(self, x, y, z):
        point = Point(x, y, z)
        self.points.append(point)
    
    def plotAirfoil(self):
        xVals = []
        yVals = []
        
        for point in self.points:
            xVals.append(point.getX())
            yVals.append(point.getY())
            
        plt.figure('plot1')
        plt.plot(xVals, yVals, label = self.name, linewidth = 0.5)
        plt.legend(loc = 'upper left')
        # plt.ylim(-0.5, 0.5)
        plt.show()
    
def importAirfoil(filename):
    '''
    input: selig format airfoil file to be converted into an Airfoil instance.
    returns an instance of the Airfoil class, with all coordinates from the input.
    '''
    try:
        origin = open(filename, 'r')
    except IOError:
        print('Couldn''t open file or files, please try again.')