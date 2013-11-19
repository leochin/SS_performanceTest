import os as OS
import numpy as NUM
import numpy.random as RAND
import arcgisscripting as ARC
import SSDataObject as SSDO
import SSDataObject_102 as SSDO_102
import MoransI as MI
import MoransI_102 as MI_102

class GlobalI(object):
    def __init__(self, inputFC, varName):
        ssdo1 = SSDO_102.SSDataObject(inputFC)
        ssdo1.obtainDataGA(ssdo1.oidName, [varName], minNumObs = 3, warnNumObs = 30)
        ssdo2 = SSDO.SSDataObject(inputFC)
        ssdo2.obtainDataGA(ssdo2.oidName, [varName], minNumObs = 3, warnNumObs = 30)
        n = ssdo1.numObs

        self.doGlobalI(inputFC, varName, n, ssdo1, ssdo2)

    def doGlobalI(self, inputFC, varName, n, ssdo1, ssdo2):
        import MyProfiler as PROF

        resDict = {}
        print "Timing Spatial Autocorrelation for {0}.... {1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(MI_102.GlobalI, resDict, resName)
        runTestPy = testPy(ssdo1, varName, wType = 0, weightsFile = None,
                     concept = "EUCLIDEAN", rowStandard = True, threshold = 0,
                     exponent = 1.0)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(MI.GlobalI, resDict, resName)
        runTestSS = testSS(ssdo2, varName, wType = 0, weightsFile = None,
                     concept = "EUCLIDEAN", rowStandard = True, threshold = 0,
                     exponent = 1.0)


        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)


if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    weightField = "RANDINT"
    N = [256]
    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        gmi = GlobalI(inputFC, weightField)
        print "\n"
        print gmi.table
        print "\n"





