import os as OS
import numpy as NUM
import numpy.random as RAND
import SSDataObject as SSDO
import SSDataObject_102 as SSDO_102
import arcgisscripting as ARC
import Gi as GI
import Gi_102 as GI_102

class HotSpot(object):
    def __init__(self, inputFC, fieldName):
        ssdo1 = SSDO_102.SSDataObject(inputFC)
        ssdo1.obtainDataGA(ssdo1.oidName, [fieldName])

        ssdo2 = SSDO.SSDataObject(inputFC)
        ssdo2.obtainDataGA(ssdo2.oidName, [fieldName])

        n = ssdo1.numObs

        self.doGiInverseDist(inputFC, fieldName, n, ssdo1, ssdo2)

    def doGiInverseDist(self, inputFC, fieldName, n, ssdo1, ssdo2):
        import MyProfiler as PROF

        resDict ={}

        print "Timing Hot Spot Analysis for {0}...{1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName

        testPy = PROF.measureFunction(GI_102.LocalG, resDict, resName)
        runTestPy = testPy(ssdo1, fieldName, "", wType= 1, weightsFile = None,
                           concept = "EUCLIDEAN", threshold = None, numNeighs = 0,
                           exponent = 1.0, potentialField = None, permutations = None,
                           applyFDR = True, pType = "BOOT")

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(GI.LocalG, resDict, resName)
        runTestSS = testSS(ssdo2, fieldName, "", wType= 1, weightsFile = None,
                           concept = "EUCLIDEAN", threshold = None, numNeighs = 0,
                           exponent = 1.0, potentialField = None, permutations = None,
                           applyFDR = True, pType = "BOOT")

        self.table = PROF.printProfile(resDict)



if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    analysisFields = 'RANDEXP'
    N = [256]

    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        hs = HotSpot(inputFC, analysisFields)
        print "\n"
        print hs.table
        print "\n"


