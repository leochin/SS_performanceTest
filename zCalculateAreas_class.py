import os as OS
import numpy as NUM
import numpy.random as RAND
import arcgisscripting as ARC
import CalculateAreas as CA
import CalculateAreas_102 as CA_102
import SSUtilities as UTILS
import arcpy as ARCPY

class CalAreas(object):
    def __init__(self, inputFC):
        n = UTILS.getCount(inputFC)

        self.doCalAreas(inputFC, n)

    def doCalAreas(self, inputFC, n):
        import MyProfiler as PROF

        resDict = {}

        outPath, outName = OS.path.split(inputFC)
        output1 = outPath + "/temp1.shp"
        output2 = outPath + "/temp2.shp"

        print "Timing Calculate Areas for {0}...{1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(CA_102.calculateAreas, resDict, resName)
        runTestPy = testPy(inputFC, output1)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(CA.calculateAreas, resDict, resName)
        runTestSS = testSS(inputFC, output2)

        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)

        ARCPY.Delete_management(output1, "")
        ARCPY.Delete_management(output2, "")

if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPolygon'
    N = [256]

    for n in N:
        inputFC = OS.path.join(inDir, 'pg' + str(n) + '.shp')
        ca = CalAreas(inputFC)
        print "\n"
        print ca.table
        print "\n"




