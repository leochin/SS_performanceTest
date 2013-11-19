import os as OS
import numpy as NUM
import numpy.random as RAND
import SSDataObject as SSDO
import SSDataObject_102 as SSDO_102
import arcgisscripting as ARC
import StandardEllipse as SE
import StandardEllipse_102 as SE_102

class StandardEllipse(object):
    def __init__(self, inputFC):
        outputFC = ""
        fieldList = []

        ssdo1 = SSDO_102.SSDataObject(inputFC, templateFC = outputFC)
        ssdo1.obtainData(ssdo1.oidName, fieldList, minNumObs = 3, dateStr = True)

        ssdo2 = SSDO.SSDataObject(inputFC, templateFC = outputFC, useChordal = False)
        ssdo2.obtainData(ssdo2.oidName, fieldList, minNumObs = 3, dateStr = True)
        n = ssdo1.numObs

        self.doSE(inputFC, n, ssdo1, ssdo2)


    def doSE(self, inputFC, n, ssdo1, ssdo2):
        import MyProfiler as PROF

        resDict = {}
        print "Timing Directional Distribution for {0}...{1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(SE_102.StandardEllipse, resDict, resName)
        runTestPy = testPy(ssdo1, weightField = None, caseField = None,
                           stdDeviations = 1.0)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(SE.StandardEllipse, resDict, resName)
        runTestSS = testSS(ssdo2, weightField = None, caseField = None,
                           stdDeviations = 1.0)

        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)

if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    N = [256]

    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        se = StandardEllipse(inputFC)
        print "\n"
        print se.table
        print "\n"




