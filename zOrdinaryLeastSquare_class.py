import os as OS
import numpy as NUM
import numpy.random as RAND
import SSDataObject as SSDO
import SSDataObject_102 as SSDO_102
import arcgisscripting as ARC
import OLS
import OLS_102

class OrdinaryLeastSquare(object):
    def __init__(self, inputFC, masterField, depVarName, indVarNames):
        outputFC = ""
        fieldList = [depVarName] + indVarNames

        ssdo1 = SSDO_102.SSDataObject(inputFC, templateFC = outputFC)
        ssdo1.obtainData(masterField, fieldList, minNumObs = 5)

        ssdo2 = SSDO.SSDataObject(inputFC, templateFC = outputFC, useChordal = False)
        ssdo2.obtainData(masterField, fieldList, minNumObs = 5)
        n = ssdo1.numObs

        self.doOLS(inputFC, n, depVarName, indVarNames, ssdo1, ssdo2)

    def doOLS(self, inputFC, n, depVarName, indVarNames, ssdo1, ssdo2):
        import MyProfiler as PROF

        resDict = {}
        print "Timing Ordinary Least Square for {0}...{1}".format(inputFC, n)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(OLS_102.OLS, resDict, resName)
        runTestPy = testPy(ssdo1, depVarName, indVarNames)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(OLS.OLS, resDict, resName)
        runTestSS = testSS(ssdo2, depVarName, indVarNames)

        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)


if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    masterField = "UID"
    depVarName = "RANDINT"
    indVarNames = ['RANDN', 'RANDEXP', 'RANDLOG']
    N = [256]

    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        ols = OrdinaryLeastSquare(inputFC, masterField, depVarName, indVarNames)
        print "\n"
        print ols.table
        print "\n"




