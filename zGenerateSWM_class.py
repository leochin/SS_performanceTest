import os as OS
import numpy as NUM
import numpy.random as RAND
import arcgisscripting as ARC
import Weights as WEIGHTS
import Weights_102 as WEIGHTS_102
import SSUtilities as UTILS
import arcpy as ARCPY

class SWM(object):
    def __init__(self, inputFC, masterField):
        n = UTILS.getCount(inputFC)
        self.doSWM(inputFC, masterField, n)

    def doSWM(self, inputFC, masterField, n):
        import MyProfiler as PROF

        resDict = {}

        outPath, outName = OS.path.split(inputFC)
        output1 = outPath + "/temp1.swm"
        output2 = outPath + "/temp2.swm"

        print "Timing Generate Spatial Weight Matrix for {0}...{1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(WEIGHTS_102.kNearest2SWM, resDict, resName)
        runTestPy = testPy(inputFC, output1, masterField, concept = "EUCLIDEAN",
                           kNeighs = 1, rowStandard = True)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(WEIGHTS.kNearest2SWM, resDict, resName)
        runTestSS = testSS(inputFC, output2, masterField, concept = "EUCLIDEAN",
                           kNeighs = 1, rowStandard = True)

        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)

        ARCPY.Delete_management(output1, "")
        ARCPY.Delete_management(output2, "")

if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    masterField = "UID"
    N = [256]

    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        swm = SWM(inputFC, masterField)
        print "\n"
        print swm.table
        print "\n"



