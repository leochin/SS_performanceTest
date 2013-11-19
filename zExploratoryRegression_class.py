import os as OS
import numpy as NUM
import numpy.random as RAND
import SSDataObject as SSDO
import arcgisscripting as ARC
import ExploratoryRegression_102 as ER_102
import ExploratoryRegression as ER
import SSDataObject_102 as SSDO_102
import SSDataObject as SSDO
import SSUtilities_102 as UTILS_102
import SSUtilities_102 as UTILS

class ExploratoryRegression(object):
    def __init__(self, inputFC, masterField, depVarName, indVarNames):
        allVars = [depVarName] + indVarNames

        ssdo1 = SSDO_102.SSDataObject(inputFC)
        ssdo1.obtainDataGA(masterField, allVars, minNumObs = 5, warnNumObs = 30)
        ssdo2 = SSDO.SSDataObject(inputFC)
        ssdo2.obtainDataGA(masterField, allVars, minNumObs = 5, warnNumObs = 30)

        n = ssdo1.numObs

        self.doER(inputFC, depVarName, indVarNames, n, ssdo1, ssdo2)

    def doER(self, inputFC, depVarName, indVarNames, n, ssdo1, ssdo2):
        import MyProfiler as PROF

        print "Timing Exploratory Regression for {0}...{1}".format(inputFC, n)

        resDict ={}

        resName = "10.2({0})".format(n)
        print resName

        testPy = PROF.measureFunction(ER_102.ExploratoryRegression, resDict, resName)
        runTestPy = testPy(ssdo1, depVarName, indVarNames, weightsFile = None,
                     outputReportFile = None, outputTable = None,
                     maxIndVars = 5, minIndVars = 1, minR2 = .5,
                     maxCoef = .01, maxVIF = 5.0, minJB = .1, minMI = .1)

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(ER.ExploratoryRegression, resDict, resName)
        runTestSS = testSS(ssdo2, depVarName, indVarNames, weightsFile = None,
                     outputReportFile = None, outputTable = None,
                     maxIndVars = 5, minIndVars = 1, minR2 = .5,
                     maxCoef = .01, maxVIF = 5.0, minJB = .1, minMI = .1)

        self.table = PROF.printProfile(resDict)



if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    masterField = "UID"
    depVarName = "RANDINT"
    indVarNames = ['RANDN', 'RANDEXP', 'RANDLOG']

    N = [256]

    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        er = ExploratoryRegression(inputFC, masterField, depVarName, indVarNames)
        print "\n"
        print er.table
        print "\n"






