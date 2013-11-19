import os as OS
import numpy as NUM
import numpy.random as RAND
import arcgisscripting as ARC
import SSDataObject_102 as SSDO_102
import SSDataObject as SSDO
import GeneralG as GG
import GeneralG_102 as GG_102

class GeneralG(object):
    def __init__(self, inputFC, varName):
        ssdo1 = SSDO_102.SSDataObject(inputFC)
        ssdo1.obtainDataGA(ssdo1.oidName, [varName], minNumObs = 3, warnNumObs = 30)
        ssdo2 = SSDO.SSDataObject(inputFC)
        ssdo2.obtainDataGA(ssdo2.oidName, [varName], minNumObs = 3, warnNumObs = 30)
        n = ssdo1.numObs
        self.doGeneralG(inputFC, varName, n, ssdo1, ssdo2)

    def doGeneralG(self, inputFC, varName, n, ssdo1, ssdo2):
        import MyProfiler as PROF


        resDict = {}
        print "High/Low Clustering for {0}.... {1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(GG_102.GeneralG, resDict, resName)
        runTestPy = testPy(ssdo1, varName, wType = 0, weightsFile = None,
                     concept = "EUCLIDEAN", rowStandard = True, threshold = 0,
                     exponent = 1.0, displayIt = False)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(GG.GeneralG, resDict, resName)
        runTestSS = testSS(ssdo2, varName, wType = 0, weightsFile = None,
                     concept = "EUCLIDEAN", rowStandard = True, threshold = 0,
                     exponent = 1.0, displayIt = False)

        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)

if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    varName = "RANDINT"
    N = [256]
    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        gg = GeneralG(inputFC, varName)
        print "\n"
        print gg.table
        print "\n"






