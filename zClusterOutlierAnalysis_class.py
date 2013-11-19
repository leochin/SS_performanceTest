import os as OS
import numpy as NUM
import numpy.random as RAND
import arcgisscripting as ARC
import SSDataObject as SSDO
import SSDataObject_102 as SSDO_102
import LocalMoran as LM
import LocalMoran_102 as LM_102
import arcpy as ARCPY

class LocalMoran(object):
    def __init__(self, inputFC, varName):
        ssdo1 = SSDO_102.SSDataObject(inputFC)
        ssdo1.obtainDataGA(ssdo1.oidName, [varName], minNumObs = 3, warnNumObs = 30)
        ssdo2 = SSDO.SSDataObject(inputFC)
        ssdo2.obtainDataGA(ssdo2.oidName, [varName], minNumObs = 3, warnNumObs = 30)
        n = ssdo1.numObs

        self.doLocalMoral(inputFC, varName, n, ssdo1, ssdo2)

    def doLocalMoral(self, inputFC, varName, n, ssdo1, ssdo2):
        import MyProfiler as PROF

        outPath, outName = OS.path.split(inputFC)
        output1 = outPath + "/temp1.shp"
        output2 = outPath + "/temp2.shp"

        resDict = {}
        print "Timing Cluster and Outlier Analysis for {0}.... {1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(LM_102.LocalI, resDict, resName)
        runTestPy = testPy(ssdo1, varName, output1 ,wType = 0, weightsFile = None,
                     concept = "EUCLIDEAN", rowStandard = True, threshold = 0,
                     exponent = 1.0, applyFDR = False)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(LM.LocalI, resDict, resName)
        runTestSS = testSS(ssdo2, varName, output2 ,wType = 0, weightsFile = None,
                     concept = "EUCLIDEAN", rowStandard = True, threshold = 0,
                     exponent = 1.0, applyFDR = False)

        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)


        ARCPY.Delete_management(output1, "")
        ARCPY.Delete_management(output2, "")


if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    weightField = "RANDINT"
    N = [256]
    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        lm = LocalMoran(inputFC, weightField)
        print "\n"
        print lm.table
        print "\n"




