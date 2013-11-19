import os as OS
import numpy as NUM
import numpy.random as RAND
import arcgisscripting as ARC
import SSDataObject as SSDO
import SSDataObject_102 as SSDO_102
import CollectEvents as CE
import CollectEvents_102 as CE_102
import SSUtilities as UTILS
import arcpy as ARCPY

class CollectEvent(object):
    def __init__(self, inputFC):
        outputFC = ""
        ssdo1 = SSDO_102.SSDataObject(inputFC, templateFC = outputFC)
        ssdo2 = SSDO.SSDataObject(inputFC, templateFC = outputFC)

        n = UTILS.getCount(inputFC)

        self.doCollectEvent(inputFC, n, ssdo1, ssdo2)

    def doCollectEvent(self, inputFC, n, ssdo1, ssdo2):
        import MyProfiler as PROF

        outPath, outName = OS.path.split(inputFC)
        output1 = outPath + "/temp1.shp"
        output2 = outPath + "/temp2.shp"
        resDict = {}

        print "Timing Collect Event for {0}...{1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(CE_102.collectEvents, resDict, resName)
        runTestPy = testPy(ssdo1, output1)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(CE.collectEvents, resDict, resName)
        runTestSS = testSS(ssdo2, output2)


        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)


        ARCPY.Delete_management(output1, "")
        ARCPY.Delete_management(output2, "")

if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    N = [256]

    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        ce = CollectEvent(inputFC)
        print "\n"
        print ce.table
        print "\n"



