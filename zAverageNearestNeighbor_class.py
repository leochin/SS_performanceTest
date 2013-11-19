import os as OS
import numpy as NUM
import numpy.random as RAND
import arcgisscripting as ARC
import SSDataObject_102 as SSDO_102
import SSDataObject as SSDO
import NearestNeighbor as NN
import NearestNeighbor_102 as NN_102

class NearestNeighbor(object):
    def __init__(self, inputFC):
        ssdo1 = SSDO_102.SSDataObject(inputFC)
        ssdo1.obtainDataGA(ssdo1.oidName, minNumObs = 2)
        ssdo2 = SSDO.SSDataObject(inputFC)
        ssdo2.obtainDataGA(ssdo2.oidName, minNumObs = 2)
        n = ssdo1.numObs
        self.doNearestNeighbor(inputFC, n, ssdo1, ssdo2)

    def doNearestNeighbor(self, inputFC, n, ssdo1, ssdo2):
        import MyProfiler as PROF

        inPath, inName = OS.path.split(inputFC)
        resDict = {}
        print "Timing Average Nearest Neighbor for {0}.... {1}".format(inName, n)

        resName = "10.2({0})".format(n)
##        print resName
        testPy = PROF.measureFunction(NN_102.NearestNeighbor, resDict, resName)
        runTestPy = testPy(ssdo1, concept = "EUCLIDEAN", studyArea = None)

        resName = "10.2.1({0})".format(n)
##        print resName
        testSS = PROF.measureFunction(NN.NearestNeighbor, resDict, resName)
        runTestSS = testSS(ssdo2, concept = "EUCLIDEAN", studyArea = None)

        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)


if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    N = [256]
    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        nn = NearestNeighbor(inputFC)
        print "\n"
        print nn.table
        print "\n"





