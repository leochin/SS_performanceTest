import os as OS
import numpy as NUM
import numpy.random as RAND
import SSDataObject as SSDO
import SSDataObject_102 as SSDO_102
import arcgisscripting as ARC
import MeanCenter as MC
import MeanCenter_102 as MC_102

class MeanCenter(object):
    def __init__(self, inputFC):
        outputFC = ""
        fieldList = []

        ssdo1 = SSDO_102.SSDataObject(inputFC, templateFC = outputFC)
        ssdo1.obtainData(ssdo1.oidName, fieldList, minNumObs = 1, dateStr = True)

        ssdo2 = SSDO.SSDataObject(inputFC, templateFC = outputFC, useChordal = False)
        ssdo2.obtainData(ssdo2.oidName, fieldList, minNumObs = 1, dateStr = True)
        n = ssdo1.numObs

        self.doMC(inputFC, n, ssdo1, ssdo2)

    def doMC(self, inputFC, n, ssdo1, ssdo2):
        import MyProfiler as PROF

        resDict = {}
        print "Timing Mean Center for {0}...{1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(MC_102.MeanCenter, resDict, resName)
        runTestPy = testPy(ssdo1, weightField = None, caseField = None,
                           dimField = None)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(MC.MeanCenter, resDict, resName)
        runTestSS = testSS(ssdo2, weightField = None, caseField = None,
                           dimField = None)


        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)


if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    N = [256]

    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        mc = MeanCenter(inputFC)
        print "\n"
        print mc.table
        print "\n"



