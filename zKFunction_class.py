import os as OS
import numpy as NUM
import numpy.random as RAND
import arcgisscripting as ARC
import SSDataObject as SSDO
import SSDataObject_102 as SSDO_102
import KFunction as KF
import KFunction_102 as KF_102
import SSUtilities as UTILS

class KFunction(object):
    def __init__(self, inputFC):
        n = UTILS.getCount(inputFC)
        self.doKFunction(inputFC, n)

    def doKFunction(self, inputFC, n):
        import MyProfiler as PROF

        resDict = {}
        print "Timing K Function for {0}.... {1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(KF_102.KFunction, resDict, resName)
        runTestPy = testPy(inputFC, outputTable = None, nIncrements = 10,
                     permutations = 0, weightField = None, begDist = None,
                     dIncrement = None, edgeCorrection = None,
                     studyAreaMethod = 0, studyAreaFC = None)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(KF.KFunction, resDict, resName)
        runTestSS = testSS(inputFC, outputTable = None, nIncrements = 10,
                     permutations = 0, weightField = None, begDist = None,
                     dIncrement = None, edgeCorrection = None,
                     studyAreaMethod = 0, studyAreaFC = None)

        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)

if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    N = [256]
    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        kf = KFunction(inputFC)
        print "\n"
        print kf.table
        print "\n"





