import os as OS
import numpy as NUM
import numpy.random as RAND
import arcgisscripting as ARC
import CalculateDistanceBand as CDB
import CalculateDistanceBand_102 as CDB_102
import SSUtilities as UTILS

class CalDisBand(object):
    def __init__(self, inputFC):
        n = UTILS.getCount(inputFC)

        self.doCalDisBand(inputFC, n)

    def doCalDisBand(self, inputFC, n):
        import MyProfiler as PROF

        resDict = {}

        print "Timing Calculate Distance Band for {0}...{1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(CDB_102.calculateDistanceBand, resDict, resName)
        runTestPy = testPy(inputFC, kNeighs = 8, concept = "EUCLIDEAN")

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(CDB.calculateDistanceBand, resDict, resName)
        runTestSS = testSS(inputFC, kNeighs = 8, concept = "EUCLIDEAN")


        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)


if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    N = [256]

    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        cdb = CalDisBand(inputFC)
        print "\n"
        print cdb.table
        print "\n"




