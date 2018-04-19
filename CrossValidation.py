#!usr/bin/python

"""
CrossValidation.py, by Madhu Chegondi
"""

from sklearn.utils import resample
import LEM1
import RuleCheckerUtility
import LEM1Utility
import RuleChecker
import json
import datetime
import os

def writeToLog(logData, df):
    if not os.path.exists('Logs'):    # Create an output folder for storing
        os.makedirs('Logs')           # output files with rules
    index = df.find('.')
    with open('Logs/'+'log_'+df[0:index]+'.json', 'a') as outfile:
        outfile.write(json.dumps(logData, default = str)+"\n")
    outfile.close()

def CrossValidation(attr, decisions, DesName, meathod, samples, df):
    print "\n\tCONFIGURING RULE CHECKER"
    matchingFactor = raw_input("\t\tDo you wish to use Matching Factor ? (y / RETURN) ")
    while (True):
        if matchingFactor == 'y' or not matchingFactor :
            break
        else:
            matchingFactor = raw_input("\t\tDo you wish to use Matching Factor ? (y / RETURN) ")

    strengthFactor = raw_input("\t\tDo you want to use Strength or Conditional Probability as Strength Factor ? (s/p) ")
    while True:
        if strengthFactor == 's' or strengthFactor == 'p':
            break
        else:
            strengthFactor = raw_input("\t\tDo you want to use Strength or Conditional Probability as Strength Factor ? (s/p) ")

    specificityFactor = raw_input("\t\tDo you wish to use Specificity ? (y / RETURN) ")
    while True:
        if specificityFactor == 'y' or not specificityFactor:
            break
        else:
            specificityFactor = raw_input("\t\tDo you wish to use Specificity ? (y / RETURN) ")

    supportFactor = raw_input("\t\tDo you wish to use Support of other rules ? (y / RETURN) ")
    while True:
        if supportFactor == 'y' or not supportFactor:
            break
        else:
            supportFactor = raw_input("\t\tDo you wish to use Support of other rules ? (y / RETURN) ")

    print '\n\tExecution in progress...'


    logData = {}
    if meathod == 'Bootstrap':
        if not samples:
            samples = 200
        for numIter in range(30):
            print "\tIterations Completed {0}".format(numIter+1),
            ErrorRates = []
            for m in range(int(samples)):
                numOfCases = len(attr)
                trainDataInd = resample(range(numOfCases))
                testDataInd = [x for x in range(numOfCases) if x not in trainDataInd]
                trainDataAttr = [attr[i] for i in trainDataInd]
                trainDataDes = [decisions[i] for i in trainDataInd]
                testDataAttr = []
                testDataDes = []
                for i in testDataInd:
                    testDataAttr.append(dict(attr[i]))
                tempDecisions = LEM1Utility.tupleToDict(decisions)
                for i in testDataInd:
                    testDataDes.append(dict(tempDecisions[i]))
                for i in range(len(testDataDes)):
                    testDataAttr[i][DesName] = testDataDes[i][DesName]
                Rules = LEM1.LEM1Classifier(trainDataAttr, trainDataDes, DesName)
                RuleStats = RuleCheckerUtility.getRuleTrainStats(Rules, trainDataAttr, trainDataDes, DesName)
                for i in range(len(Rules)):
                    Rules[i].update(RuleStats[i])
                ErrorRates.append(RuleChecker.RuleChecker(Rules, testDataAttr, DesName, strengthFactor, matchingFactor, specificityFactor, supportFactor))
            print '\033[F'
            logData['ErrorRate'] = round(sum(ErrorRates)/float(len(ErrorRates)),2)
            logData['Acc'] = round(100 - logData['ErrorRate'],2)
            logData['NumberOfSamplesCreated'] = int(samples)
            logData['method'] = 'Bootstrap'
            logData['FileName'] = df
            logData['time'] = datetime.datetime.now()
            writeToLog(logData, df)
            logData = {}
    else:
        for numIter in range(30):
            print "\tIterations Completed {0}".format(numIter+1),
            ErrorRates = []
            for i in range(len(attr)):
                numOfCases = len(attr)
                CaseNumbers = list(range(numOfCases))
                testDataInd = [i]
                trainDataInd = [j for j in CaseNumbers if j not in testDataInd]
                trainDataAttr = [attr[i] for i in resample(trainDataInd, replace=False)]
                trainDataDes = [decisions[i] for i in trainDataInd]
                testDataAttr = []
                testDataDes = []
                for i in testDataInd:
                    testDataAttr.append(dict(attr[i]))
                tempDecisions = LEM1Utility.tupleToDict(decisions)
                for i in testDataInd:
                    testDataDes.append(dict(tempDecisions[i]))
                for i in range(len(testDataDes)):
                    testDataAttr[i][DesName] = testDataDes[i][DesName]
                Rules = LEM1.LEM1Classifier(trainDataAttr, trainDataDes, DesName)
                RuleStats = RuleCheckerUtility.getRuleTrainStats(Rules, trainDataAttr, trainDataDes, DesName)
                for i in range(len(Rules)):
                    Rules[i].update(RuleStats[i])
                ErrorRates.append(RuleChecker.RuleChecker(Rules, testDataAttr, DesName, strengthFactor, matchingFactor, specificityFactor, supportFactor))
            print '\033[F'
            logData['ErrorRate'] = round(sum(ErrorRates)/float(len(attr)),2)
            logData['Acc'] = round(100 - logData['ErrorRate'],2)
            logData['NumberOfFoldsCreated'] = len(attr)
            logData['method'] = 'LOOCV'
            logData['FileName'] = df
            logData['time'] = datetime.datetime.now()
            writeToLog(logData, df)
            logData ={}
    print "\n\tSuccessfully Executed. Check Logs for Results"
