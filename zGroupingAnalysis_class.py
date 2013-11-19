import os as OS
import numpy as NUM
import numpy.random as RAND
import SSDataObject as SSDO
import SSDataObject_102 as SSDO_102
import arcgisscripting as ARC
import Partition as PART
import Partition_102 as PART_102

class Grouping(object):
    def __init__(self, inputFC, masterField, analysisFields, initField):
        ssdo1 = SSDO_102.SSDataObject(inputFC)
        allFields = analysisFields + [initField]
        ssdo1.obtainData(ssdo1.oidName, allFields)
        seedData = ssdo1.fields[initField].data
        seedIndices = NUM.array(NUM.where(seedData == 1)[0], NUM.int32)
        kPartitions = len(seedIndices)

        ssdo2 = SSDO.SSDataObject(inputFC)
        ssdo2.obtainData(ssdo2.oidName, allFields)

        n = ssdo1.numObs
        self.doKMeansSeeds(inputFC, n, masterField, analysisFields, initField, kPartitions, ssdo1, ssdo2)
        self.doKMeansKNN(inputFC, n, masterField, analysisFields, 15, 8, ssdo1, ssdo2)

    def doKMeansSeeds(self, inputFC, n,masterField, analysisFields, initField, kPartitions, ssdo1, ssdo2):
        import MyProfiler as PROF

        resDict = {}
        print "Timing Partition (Seeds) for {0}...{1}".format(inputFC, n)
        print "Number of Groups = {0}".format(kPartitions)

        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(PART_102.Partition, resDict, resName)
        runTestPy = testPy(ssdo1, analysisFields,
                           initMethod = "GET_SEEDS_FROM_FIELD",
                           kPartitions = kPartitions, initField = initField)
    ##    runTestPy.report()

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(PART.Partition, resDict, resName)
        runTestSS = testSS(ssdo2, analysisFields,
                           initMethod = "GET_SEEDS_FROM_FIELD",
                           kPartitions = kPartitions, initField = initField)
    ##    runTestSS.report()

        #### Sorted by Time (Seconds) ####
        self.table = PROF.printProfile(resDict)

    ##    return NUM.alltrue(runTestPy.partition == runTestSS.partition)

    def doKMeansKNN(self, inputFC, n, masterField, analysisFields, kPartitions, KNN, ssdo1, ssdo2):
        import MyProfiler as PROF

        ssdo1 = SSDO_102.SSDataObject(inputFC)
        ssdo1.obtainDataGA(masterField, analysisFields)

        ssdo2 = SSDO.SSDataObject(inputFC)
        ssdo2.obtainDataGA(masterField, analysisFields)
        resDict = {}

        n = ssdo1.numObs
        print "Timing Partition KNN for {0}...{1}".format(inputFC, n)
        print "Number of Groups = {0}, Number of Neighbors = {1}".format(kPartitions, KNN)
        resName = "10.2({0})".format(n)
        print resName
        testPy = PROF.measureFunction(PART_102.Partition, resDict, resName)
        runTestPy = testPy(ssdo1, analysisFields,
                           spaceConcept = "K_NEAREST_NEIGHBORS",
                           numNeighs = KNN,
                           kPartitions = kPartitions)

    ##    runTestPy.report()

        resName = "10.2.1({0})".format(n)
        print resName
        testSS = PROF.measureFunction(PART.Partition, resDict, resName)
        runTestSS = testSS(ssdo2, analysisFields,
                           spaceConcept = "K_NEAREST_NEIGHBORS",
                           numNeighs = KNN,
                           kPartitions = kPartitions)

    ##    runTestSS.report()

        print "\n"
        #### Sorted by Time (Seconds) ####
        self.table2 = PROF.printProfile(resDict)


    ##    print "All Paritions Same?:...", NUM.alltrue(runTestPy.partition == runTestSS.partition)


if __name__ == '__main__':
    inDir = r'C:\Data\Performance\timingPoint'
    masterField = 'UID'
    analysisFields = ['RANDEXP']
    initField = 'RANDGEOM'
    N = [256]

    for n in N:
        inputFC = OS.path.join(inDir, 'point' + str(n) + '.shp')
        ga = Grouping(inputFC, masterField, analysisFields, initField)
        print "\n"
        print ga.table
        print "\n"
        print ga.table2
        print "\n"




