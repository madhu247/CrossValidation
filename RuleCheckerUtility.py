#!usr/bin/python

"""
RuleCheckerUtility.py, by Madhu Chegondi
"""
import re
import LEM1Utility

def getRuleTrainStats(Rules, trainAttr, trainDes, DesName):
    """This method is used to return the 3 numbers preceding the Rules"""
    Cases = []
    for i in trainAttr:
        Cases.append(dict(i))
    tempDecisions = LEM1Utility.tupleToDict(trainDes)
    for i in range(len(trainDes)):
        Cases[i][DesName] = tempDecisions[i][DesName]
    RuleStats = []
    for i in range(len(Rules)):
        strength = 0
        flag = 1
        d = {}
        numOfTrainCasesMatched = 0
        for j in range(len(Cases)):
            Keys = [ k for k in Rules[i].keys() if k != DesName]
            count = 0
            keyLen = len(Keys)
            for k in Keys:
                if Rules[i][k] == Cases[j][k]:
                    count = count + 1
                elif Rules[i][k].find('..') > 0:
                    values = getValues(Rules[i][k])
                    if Cases[j][k] >= values[0] and Cases[j][k] <= values[1]:
                        count = count + 1

            if count == keyLen:
                numOfTrainCasesMatched = numOfTrainCasesMatched + 1
                if Rules[i][DesName] == Cases[j][DesName]:
                    strength = strength + 1

        d['numOfTrainCasesMatched'] = numOfTrainCasesMatched
        d['strength'] = strength
        d['specificity'] = len(Rules[i])-1
        RuleStats.append(d)
    return RuleStats


def checkRulesForPartialMatching(Rules, Cases, DesName):
    """returns number of matched conditions in partial matching"""
    Keys = [ k for k in Rules.keys() if k not in ['specificity', 'strength', 'numOfTrainCasesMatched', DesName, 'numOfConditions']]
    flag = 0
    matchedCases = 0
    for k in Keys:
        if Cases[k] == '-' or Cases[k] == '*':
            Cases[k] = Rules[k]
        # Code to handle '?'
        # elif Cases[k] == '?':
        #     Cases[k] = 'Madhu'
        if Rules[k] == Cases[k]:
            matchedCases = matchedCases + 1
        elif Rules[k].find('..') > 0:
            values = getValues(Rules[k])
            if Cases[k] >= values[0] and Cases[k] <= values[1]:
                matchedCases = matchedCases + 1
    if matchedCases:
        return matchedCases
    else:
        return matchedCases


def checkRules(Rules, Cases, DesName):
    """Checks for complete matching and returns matched cases which helps to classify the case based on comp or part or notClass at all"""
    Keys = [ k for k in Rules.keys() if k not in ['specificity', 'strength', 'numOfTrainCasesMatched', DesName, 'numOfConditions']]
    flag = 0
    matchedCases = 0
    for k in Keys:
        if Cases[k] == '-' or Cases[k] == '*':
            Cases[k] = Rules[k]
        # Code to handle '?'
        # elif Cases[k] == '?':
        #     Cases[k] = 'Madhu'
        if Rules[k] == Cases[k]:
            matchedCases = matchedCases + 1
            flag = 1
        elif Rules[k].find('..') > 0:
            values = getValues(Rules[k])
            if Cases[k] >= values[0] and Cases[k] <= values[1]:
                matchedCases = matchedCases + 1
                flag = 1
            else:
                flag = 0
                break
        else:
            flag = 0
            break
    if flag:
        return True, matchedCases
    else:
        return False, matchedCases


def getValues(symNumericals):
    if symNumericals.find('..'):
        stingValues = symNumericals.split('..')
    else:
        return
    values = [float(i) for i in stingValues]
    return values


def getRuleStats(Rule, caseNum, DesName, j, id, matchedCases, strengthFactor, matchingFactor='n', specificityFactor='n'):
    """check which rules are matched with a particular case. Output is used to resolve conflicts on rules by voting"""
    matchedRuleStats = {}
    matchedRuleStats['id'] = id
    matchedRuleStats['decision'] = Rule[DesName]
    matchedRuleStats['CaseNumber'] = caseNum
    if specificityFactor == 'y':
        matchedRuleStats['specificity'] = Rule['specificity']
    else:
        matchedRuleStats['specificity'] = 1
    matchedRuleStats['RuleNum'] = j
    matchedRuleStats['matchedCases'] = matchedCases
    if matchingFactor == 'y':
        partialMatchingFactor = float(matchedCases/Rule['specificity'])
        matchedRuleStats['partialMatchingFactor'] = partialMatchingFactor
    else:
        matchedRuleStats['partialMatchingFactor'] = 1
    if strengthFactor == 'p':
        condProb = round(float(Rule['strength'])/float(Rule['numOfTrainCasesMatched']),2)
        matchedRuleStats['sp'] = condProb
    else:
        matchedRuleStats['sp'] = Rule['strength']
    return matchedRuleStats


def classificationOfCases(caseNum, Cases, RuleStats, DesName, strengthFactor, matchingFactor='n', specificityFactor='n', supportFactor='n'):
    """Classifies the cases based on voting receiving user inputs on the strategies"""
    support = {}
    id1 = []
    id3 = []
    maxSpecificity = 0
    maxStrength = 0
    maxSupport = 0
    maxCondProb = 0
    flag = 0
    listOfDecisions = list(set([item['decision'] for item in RuleStats if item['CaseNumber'] == caseNum]))
    for i in listOfDecisions:
        support[i] = sum([item['partialMatchingFactor'] * item['sp'] * item['specificity'] for item in RuleStats if item['CaseNumber'] == caseNum and item['decision'] == i])
    if supportFactor == 'y':
        keyValueTup = [(value, key) for key, value in support.items()]
        # if support of both decisions is same this program picks the desicion Name in Alphabetical order
        desFromSupport = max(keyValueTup)[1]
        if Cases[caseNum][DesName] == desFromSupport:
            flag = 1
        else:
            flag = 0
    for item in RuleStats:
        maxPartialMatchingFactor = 0
        if item['CaseNumber'] == caseNum:
            if specificityFactor == 'y':
                if item['specificity'] >= maxSpecificity:
                    maxSpecificity = item['specificity']
                    id1.append(item['id'])
            if strengthFactor == 's':
                if item['sp'] >= maxStrength:
                    maxStrength = item['sp']
                    id2 = item['id']
            else:
                if item['sp'] >= maxCondProb:
                    maxCondProb = item['sp']
                    id2 = item['id']
            if matchingFactor == 'y':
                if item['partialMatchingFactor'] >= maxPartialMatchingFactor:
                    maxPartialMatchingFactor = item['partialMatchingFactor']
                    id3.append(item['id'])
    if (id2 in id1 or id1 == []) and (id2 in id3 or id3 == []):
        if [Cases[caseNum][DesName]] == [i['decision'] for i in RuleStats if i['id'] == id2] or flag == 1:
            return 1
        else:
            return 0
