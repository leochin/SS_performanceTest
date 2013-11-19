import os as OS
import numpy as NUM
import numpy.random as RAND
import arcgisscripting as ARC
import SSDataObject as SSDO
import SSDataObject_102 as SSDO_102
import MedianCenter as MDC
import MedianCenter_102 as MDC_102

class MedianCenter(object):
    def __init__(self, inputFC, masterField, weightField):
        ssdo1 = SSDO_102.SSDataObject(inputFC)
        ssdo1.obtainDataGA(masterField)

        ssdo2 = SSDO.SSDataObject(inputFC)
        ssdo2.obtainDataGA(masterField)

        n = ssdo1.numObs

        self.doMDC(inputFC, n, ssdo1, ssdo2)

        ssdo1 = SSDO_102.SSDataObject(inputFC)
        ssdo1.obtainData(ssdo1.oidName, [weightField])

        ssdo2 = SSDO.SSDataObject(inputFC)
        ssdo2.obtainData(ssdo2.oidName, [weightField])

        self.doMDC_Weighted(inputFC, weightField, n, ssdo1, ssdo2)

    def doMDC(self, inputFC, n, ssdo1, ssdo2):
        import MyProfiler as PROF

        resDict = {}

        print "Timing Median Center for {0}.... {1}".format(inputFC, n)
        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(MDC_102.MedianCenter, resDict, resName)
        runTestPy = testPy(ssdo1)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(MDC.MedianCenter, resDict, resName)
        runTestSS = testSS(ssdo2)

        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)


##        medX_Py, medY_Py = runTestPy.medianCenter[1]
##        medX_SS, medY_SS = runTestSS.medianCenter[1]
##
##        print "X = {0}, Y = {1}".format(medX_Py, medY_Py)
##        print "X = {0}, Y = {1}".format(medX_SS, medY_SS)
##
##        if medX_Py == medX_SS and medY_Py == medY_SS:
##            return True
##        else:
##            return False


    def doMDC_Weighted(self, inputFC, weightField, n, ssdo1, ssdo2):
        import MyProfiler as PROF

        resDict = {}
        print "Timing Median Center for {0}.... {1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(MDC_102.MedianCenter, resDict, resName)
        runTestPy = testPy(ssdo1, weightField = weightField)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(MDC.MedianCenter, resDict, resName)
        runTestSS = testSS(ssdo2, weightField = weightField)

                #### Sorted by Time (Seconds) ####
        self.table2 = PROF.printProfile(resDict)


##        medX_Py, medY_Py = runTestPy.medianCenter[1]
##        medX_SS, medY_SS = runTestSS.medianCenter[1]
##
##        print "X = {0}, Y = {1}".format(medX_Py, medY_Py)
##        print "X = {0}, Y = {1}".format(medX_SS, medY_SS)
##
##        if medX_Py == medX_SS and medY_Py == medY_SS:
##            return True
##        else:
##            return False

if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    weightField = "RANDN"
    masterField = 'UID'
    N = [256]
    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        mdc = MedianCenter(inputFC, masterField, weightField)
        print "\n"
        print mdc.table
        print "\n"
        print mdc.table2
        print "\n"

