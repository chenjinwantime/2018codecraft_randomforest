import math
import random
import copy
import Tools



def splitDataSet(dataSet, featIndex, value):
    leftData, rightData = [], []
    for dt in dataSet:
        if dt[featIndex] <= value:
            leftData.append(dt[-1])
        else:
            rightData.append(dt[-1])
    return leftData, rightData
    
def chooseBestFeature(dataSet):
    bestR2 = float('inf')
    bestFeatureIndex = -1
    bestSplitValue = None
    
    for i in range(len(dataSet[0]) - 1):
        featList = [dt[i] for dt in dataSet]
        
        sortfeatList = sorted(list(set(featList)))
        splitList = []
        
        if len(sortfeatList) == 1:
            splitList.append(sortfeatList[0])
        else:
            for j in range(len(sortfeatList) - 1):
                splitList.append((sortfeatList[j] + sortfeatList[j + 1]) / 2)
        
        for splitValue in splitList:
            subDataSet0, subDataSet1 = splitDataSet(dataSet, i, splitValue)
            lenLeft, lenRight = len(subDataSet0), len(subDataSet1)
            
            if lenLeft == 0 and lenRight != 0:
                rightMean = Tools.get_mean_1(subDataSet1)
                R2 = sum([(x - rightMean)**2 for x in subDataSet1])
            elif lenLeft != 0 and lenRight == 0:
                leftMean = Tools.get_mean_1(subDataSet0)
                R2 = sum([(x - leftMean) ** 2 for x in subDataSet0])
            else:
                leftMean, rightMean = Tools.get_mean_1(subDataSet0), Tools.get_mean_1(subDataSet1)
                leftR2 = sum([(x - leftMean)**2 for x in subDataSet0])
                rightR2 = sum([(x - rightMean)**2 for x in subDataSet1])
                R2 = leftR2 + rightR2
            if R2 < bestR2:
                bestR2 = R2
                bestFeatureIndex = i
                bestSplitValue = splitValue
    return bestFeatureIndex, bestSplitValue


def splitData(dataSet, featIndex, features, value):
    newFeatures = copy.deepcopy(features)
    newFeatures.remove(features[featIndex])
    leftData, rightData = [], []
    for dt in dataSet:
        temp = []
        temp.extend(dt[:featIndex])
        temp.extend(dt[featIndex + 1:])
        if dt[featIndex] <= value:
            leftData.append(temp)
        else:
            rightData.append(temp)
    return newFeatures, leftData, rightData


def regressionTree(dataSet, features):
    classList = [dt[-1] for dt in dataSet]
    
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    
    if len(features) == 1:
        return Tools.get_mean_1(classList)
    bestFeatureIndex, bestSplitValue = chooseBestFeature(dataSet)
    bestFeature = features[bestFeatureIndex]
    
    newFeatures, leftData, rightData = splitData(dataSet, bestFeatureIndex, features, bestSplitValue)

    
    if len(leftData) == 0 or len(rightData) == 0:
        return Tools.get_mean_1([dt[-1] for dt in leftData] + [dt[-1] for dt in rightData])
    else:
        
        myTree = {bestFeature: {'<' + str(bestSplitValue): {}, '>' + str(bestSplitValue): {}}}
        myTree[bestFeature]['<' + str(bestSplitValue)] = regressionTree(leftData, newFeatures)
        myTree[bestFeature]['>' + str(bestSplitValue)] = regressionTree(rightData, newFeatures)
    return myTree


def treeClassify(decisionTree, featureLabel, testDataSet):
    firstFeature_temp = decisionTree.keys()
    firstFeature=firstFeature_temp[0]
    secondFeatDict = decisionTree[firstFeature]
    #print 'type'
    #print type(secondFeatDict.keys()[0][1:])
    #print secondFeatDict.keys()[0][1:]
    splitValue = float(secondFeatDict.keys()[0][1:])
    featureIndex = featureLabel.index(firstFeature)
    if testDataSet[featureIndex] <= splitValue:
        valueOfFeat = secondFeatDict['<' + str(splitValue)]
    else:
        valueOfFeat = secondFeatDict['>' + str(splitValue)]
    if isinstance(valueOfFeat, dict):
        pred_label = treeClassify(valueOfFeat, featureLabel, testDataSet)
    else:
        pred_label = valueOfFeat
    return pred_label




def baggingDataSet(case,vm_type):
    #print 'baggingDataSet' 
    #print vm_type
    m=len(case.his_data_RF[vm_type])
    n=len(case.his_data_RF[vm_type][0])
    #print m
    #print n
    features = random.sample(case.his_data_features[:-1], int(math.sqrt(m - 1)))
    #print 'features'
    features.append(case.his_data_features[-1])
    #print features
    rows = [random.randint(0, n-1) for _ in range(n)]
    #print rows
    trainData=[]
    for i in rows:
        #print i
        sub_trainData=[]
        for j in features:
            #print j
            #print case.his_data_features_dict[j]
            sub_trainData.append(case.his_data_RF[vm_type][case.his_data_features_dict[j]][i])
        trainData.append(sub_trainData)
    #print rows
    #print 'trainData'
    #print trainData
    return trainData, features

    
def RandomForestRegression(case,vm_type):
    print vm_type
    treeCounts=100
    treeList=[]
    predict_flavor_dict={}
    for i in range(treeCounts):
        baggingData, bagginglabels = baggingDataSet(case,vm_type)
        decisionTree = regressionTree(baggingData, bagginglabels)
        treeList.append(decisionTree)
    #print treeList
    
    sub_testData=[]
    for j in case.his_data_features[1:]:
        #print j
        sub_testData.append(case.his_data_RF[vm_type][case.his_data_features_dict[j]][-1])
    #print 'sub_testData'
    #print sub_testData
    for i in range(case.predict_data_range_days):
        labelPred = [] 
        sub_count=0
        for tree in treeList:
            #print case.his_data_features[:-1]
            #print type(tree)
            #if str(type(tree))=='<type \'dict\'>':
            if isinstance(tree,dict):
                #print 'sub_testData'
                #print sub_testData
                label = treeClassify(tree, case.his_data_features[:-1], sub_testData)
                labelPred.append(label)
            else:
                labelPred.append(tree)
        sub_count=Tools.get_mean_1(labelPred)
        del sub_testData[0]
        sub_testData.append(0)
        sub_testData[case.his_data_features_dict['d1']]=sub_count
        sub_testData[case.his_data_features_dict['mean']]=Tools.get_mean(sub_testData[:case.his_data_features_dict['d1']])
        sub_testData[case.his_data_features_dict['max']]=max(sub_testData[:case.his_data_features_dict['d1']])
        sub_testData[case.his_data_features_dict['median']]=Tools.get_median(sub_testData[:case.his_data_features_dict['d1']])
        sub_testData[case.his_data_features_dict['variance']]=Tools.get_variance(sub_testData[:case.his_data_features_dict['d1']])
        #print sub_count
    predict_flavor_dict[vm_type]=Tools.get_sum(sub_testData)
  
    return predict_flavor_dict[vm_type]
