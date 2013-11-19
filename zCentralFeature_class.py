import os as OS
import numpy as NUM
import numpy.random as RAND
import SSDataObject as SSDO
import SSDataObject_102 as SSDO_102
import arcgisscripting as ARC
import CentralFeature as CF
import CentralFeature_102 as CF_102

class CentralFeature(object):
    def __init__(self, inputFC):
        outputFC = ""
        fieldList = []

        ssdo1 = SSDO_102.SSDataObject(inputFC, templateFC = outputFC)
        ssdo1.obtainData(ssdo1.oidName, fieldList, minNumObs = 1, dateStr = True)

        ssdo2 = SSDO.SSDataObject(inputFC, templateFC = outputFC, useChordal = False)
        ssdo2.obtainData(ssdo2.oidName, fieldList, minNumObs = 1, dateStr = True)
        n = ssdo1.numObs

        self.doCF(inputFC, n, ssdo1, ssdo2)

    def doCF(self, inputFC, n, ssdo1, ssdo2):
        import MyProfiler as PROF

        resDict = {}
        print "Timing Central Feature for {0}...{1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(CF_102.CentralFeature, resDict, resName)
        runTestPy = testPy(ssdo1, distanceMethod = "EUCLIDEAN", weightField = None,
                           potentialField = None, caseField = None)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(CF.CentralFeature, resDict, resName)
        runTestSS = testSS(ssdo2, distanceMethod = "EUCLIDEAN", weightField = None,
                           potentialField = None, caseField = None)

        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)

if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    N = [256]

    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        cf = CentralFeature(inputFC)
        print "\n"
        print cf.table
        print "\n"




