import os as OS
import numpy as NUM
import numpy.random as RAND
import SSDataObject as SSDO
import SSDataObject_102 as SSDO_102
import arcgisscripting as ARC
import OptimizedHotSpotAnalysis as OHSA
import OptimizedHotSpotAnalysis_102 as OHSA_102
import arcpy as ARCPY

class OptimizedHSA(object):
    def __init__(self, inputFC, fieldName):
        ssdo1 = SSDO_102.SSDataObject(inputFC)
        ssdo1.obtainDataGA(ssdo1.oidName, [fieldName])

        ssdo2 = SSDO.SSDataObject(inputFC)
        ssdo2.obtainDataGA(ssdo2.oidName, [fieldName])

        n = ssdo1.numObs

        self.doOHSA(inputFC, n, ssdo1, ssdo2)

    def doOHSA(self, inputFC, n, ssdo1, ssdo2):
        import MyProfiler as PROF

        resDict ={}

        outPath, outName = OS.path.split(inputFC)
        output1 = outPath + "/temp1.shp"
        output2 = outPath + "/temp2.shp"

        print "Timing Hot Spot Analysis for {0}...{1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName

        testPy = PROF.measureFunction(OHSA_102.OptHotSpots, resDict, resName)
        runTestPy = testPy(ssdo1, output1, varName = None,
                           aggType = 1, polygonFC = None,
                           boundaryFC = None, outputRaster = None)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(OHSA.OptHotSpots, resDict, resName)
        runTestSS = testSS(ssdo2, output2, varName = None,
                           aggType = 1, polygonFC = None,
                           boundaryFC = None, outputRaster = None)

        self.table = PROF.printProfile(resDict)

        ARCPY.Delete_management(output1, "")
        ARCPY.Delete_management(output2, "")

if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    analysisFields = 'RANDEXP'
    N = [256]

    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        ohsa = OptimizedHSA(inputFC, analysisFields)
        print "\n"
        print ohsa.table
        print "\n"



