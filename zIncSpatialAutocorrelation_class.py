import os as OS
import numpy as NUM
import numpy.random as RAND
import arcgisscripting as ARC
import SSDataObject as SSDO
import SSDataObject_102 as SSDO_102
import MoransI_Increment as INC
import MoransI_Increment_102 as INC_102

class IncAuto(object):
    def __init__(self, inputFC, fieldName):
        ssdo1 = SSDO_102.SSDataObject(inputFC)
        ssdo1.obtainDataGA(ssdo1.oidName, [fieldName])

        ssdo2 = SSDO.SSDataObject(inputFC)
        ssdo2.obtainDataGA(ssdo2.oidName, [fieldName])
        n = ssdo1.numObs
        self.doIncAuto(inputFC, n, fieldName, ssdo1, ssdo2)

    def doIncAuto(self, inputFC, n, fieldName, ssdo1, ssdo2):
        import MyProfiler as PROF

        resDict = {}
        print "Timing Incremental Spatial Autocorrelation for {0}.... {1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(INC_102.GlobalI_Step, resDict, resName)
        runTestPy = testPy(ssdo1, fieldName)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(INC.GlobalI_Step, resDict, resName)
        runTestSS = testSS(ssdo2, fieldName)

        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)

        pyRes = []
        ssRes = []
        for testIter in xrange(runTestPy.nIncrements):
            d, gi, ei, vi, zi, pv = runTestPy.giResults[testIter]
            pyRes.append(gi)
            d, gi, ei, vi, zi, pv = runTestSS.giResults[testIter]
            ssRes.append(gi)

        pyRes = NUM.array(pyRes)
        ssRes = NUM.array(ssRes)
        return NUM.alltrue(pyRes == ssRes)

if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    weightField = "RANDEXP"
    N = [256]
    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        inc = IncAuto(inputFC, weightField)
        print "\n"
        print inc.table
        print "\n"





