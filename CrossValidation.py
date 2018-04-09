from sklearn.utils import resample
from sklearn.model_selection import LeaveOneOut
import LEM1
import RuleCheckerUtility
import LEM1Utility

def CrossValidation(attr, decisions, DesName, meathod, iterations = 10):
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
    if meathod == 'Bootstrap':
        for _ in range(int(iterations)):
            numOfCases = len(attr)
            trainDataInd = 0
            testDataInd = 0
            trainDataInd = resample(range(numOfCases))
            testDataInd = [x for x in range(numOfCases) if x not in trainDataInd]
            stats = []
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
            print RuleStats
