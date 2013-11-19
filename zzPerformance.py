"""
Tool Name:          Performance Test
Source Name:        zzPerformance.py
Version:            ArcGIS 10.2 and 10.2.1
Description:        Provides the differences of execution time, memory and
                    K-Stones index between new and old version script file
Tested Script List:
    Analyzing Patterns:
        Average Nearest Neighbor
        High/Low Clustering
        Incremental Spatial Autocorrelation
        Multi-Distance Spatial Cluster Analysis (K Function)
        Spatial Autocorrelation (Moran's I)
    Mapping Clusters:
        Cluster and Outlier Analysis
        Grouping Analysis
        Hot Spot Analysis
        Optimized Hot Spot Analysis
    Measuring Geographic Distribution:
        Central Feature
        Directional Distribution
        Mean Center
        Median Center
        Standard Distance
    Modeling Spatial Relationships:
        Exploratory Regression
        Generate Spatial Weight Matrix
        Ordinary Least Squares
    Utilities:
        Calculate Areas
        Calculate Distance Band from Neighbor Count
        Collect Events

"""

################### Imports ########################
import os as OS
import zAverageNearestNeighbor_class as ANN
import zHighLowClustering_class as HLC
import zIncSpatialAutocorrelation_class as ISA
import zKFunction_class as KF
import zSpatialAutocorrelation_class as SA
import zClusterOutlierAnalysis_class as COA
import zGroupingAnalysis_class as GA
import zHotSpotAnalysis_class as HSA
import zOptimizedHotSpotAnalysis_class as OHSA
import zCentralFeature_class as CF
import zDirectionalDistribution_class as DD
import zMeanCenter_class as MEC
import zMedianCenter_class as MDC
import zStandardDistance_class as SD
import zExploratoryRegression_class as ER
import zGenerateSWM_class as GSWM
import zOrdinaryLeastSquare_class as OLS
import zCalculateAreas_class as CA
import zCalculateDistanceBand_class as CDB
import zCollectEvent_class as CE

################### Tests ########################
inDirPoint = r"C:\Data\Performance\timingPoint"
inDirPoly = r'C:\Data\Performance\timingPolygon'
N = [256, 1024]
varName = 'RANDINT'
masterField = 'UID'
analysisFields = ['RANDEXP']
indVarNames = ['RANDN', 'RANDEXP', 'RANDLOG']
initField = 'RANDGEOM'

tool = ["Avarage Nearest Neighbor", "General G", "Inc Spatial Autocorrelation",
        "K Function", "Global Moran I", "Local Moran", "Grouping with seeds",
        "Grouping with K-NN", "Gi", "OHSA", "Central Feature", "Standard Ellipse",
        "Mean Center", "Median Center", "Median Center with weights",
        "Standard Distance", "ER", "Generate SWM", "OLS", "Calculate Areas",
        "Calculate Distance Band", "Collect Event"]

numOfTools = len(tool)
result = []

def tableFormat(table):
    table = table.replace(" ", ",")
    table = table.replace(",,,,,,,,", ",")
    table = table.replace(",,,", ",")
    table = table.replace(",,", ",")
    table = table.replace(",,,,", "")

    return table

for n in N:
    inputFCPoint = OS.path.join(inDirPoint, 'point' + str(n) + '.shp')
    #### Analyzing Patterns ####
    # Average Nearest Neighbor
    temp = ANN.NearestNeighbor(inputFCPoint)
    result.append(temp.table)
    # High/Low clustering (General G)
    temp = HLC.GeneralG(inputFCPoint, varName)
    result.append(temp.table)
    # Incremental Spatial Autocorrelation
    temp = ISA.IncAuto(inputFCPoint, varName)
    result.append(temp.table)
    # Multi-Distance Spatial Cluster Analysis (K Function)
    temp = KF.KFunction(inputFCPoint)
    result.append(temp.table)
    # Spatial Autocorrelation (Moran's I)
    temp = SA.GlobalI(inputFCPoint, varName)
    result.append(temp.table)

    #### Mapping Clusters ####
    # Cluster and Outlier Analysis (Local Moran)
    temp = COA.LocalMoran(inputFCPoint, varName)
    result.append(temp.table)
    # Grouping Analysis (Partition)
    temp = GA.Grouping(inputFCPoint, masterField, analysisFields, initField)
    result.append(temp.table)
    result.append(temp.table2)
    # Hot Spot Analysis (Gi)
    temp = HSA.HotSpot(inputFCPoint, varName)
    result.append(temp.table)
    # Optimized Hot Spot Analysis
    temp = OHSA.OptimizedHSA(inputFCPoint, varName)
    result.append(temp.table)

    #### Measuring Geographic Distribution ####
    # Central Feature
    temp = CF.CentralFeature(inputFCPoint)
    result.append(temp.table)
    # Directional Distribution (Standard Ellipse)
    temp = DD.StandardEllipse(inputFCPoint)
    result.append(temp.table)
    # Mean Center
    temp = MEC.MeanCenter(inputFCPoint)
    result.append(temp.table)
    # Median Center
    temp = MDC.MedianCenter(inputFCPoint, masterField, varName)
    result.append(temp.table)
    result.append(temp.table2)
    # Standard Distance
    temp = SD.StandardDistance(inputFCPoint)
    result.append(temp.table)

    #### Modeling Spatial Relationships ####
    # Exploratory Regression
    temp = ER.ExploratoryRegression(inputFCPoint, masterField, varName, indVarNames)
    result.append(temp.table)
    # Generate Spatial Weights Matrix
    temp = GSWM.SWM(inputFCPoint, masterField)
    result.append(temp.table)
    # Ordinary Least Squares
    temp = OLS.OrdinaryLeastSquare(inputFCPoint, masterField, varName, indVarNames)
    result.append(temp.table)

    #### Utilities ####
    # Calculate Areas
    inputFCPoly = OS.path.join(inDirPoly, 'pg' + str(n) + '.shp')
    temp = CA.CalAreas(inputFCPoly)
    result.append(temp.table)
    # Calculate Distance Band from Nearest Neighbor
    temp = CDB.CalDisBand(inputFCPoint)
    result.append(temp.table)
    # Collect Events
    temp = CE.CollectEvent(inputFCPoint)
    result.append(temp.table)


resultFile = open(r"test_result.csv", "w")
for i in xrange(numOfTools):
    resultFile.write("Timing for," + tool[i] + "\n")
    for j in xrange(len(N)):
        table = tableFormat(result[i + (j * numOfTools)])
        resultFile.write(table)
    resultFile.write("\n\n")

resultFile.close()
