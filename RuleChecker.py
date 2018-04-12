#!usr/bin/python

"""
main.py, by Madhu Chegondi, 03-23-2018
"""

import RuleCheckerUtility

def RuleChecker(Rules, Cases, DesName, strengthFactor, matchingFactor = None, specificityFactor = None, supportFactor = None):
    correctlyClassifiedCases = []
    inCorrectlyClassifiedCases = []
    notClassifiedCases = []
    correctAndInCorrectlyClassifiedCases = []
    partiallyMatchedCases = []

    for i in range(len(Cases)):
        for j in range(len(Rules)):
            if RuleCheckerUtility.checkRules(Rules[j], Cases[i], DesName)[0]:
                try:
                    if type(float(Rules[j][DesName])) == float:  #isinstance(value, type)
                        Rules[j][DesName] = float(Rules[j][DesName])
                except ValueError:
                    Rules[j][DesName] = Rules[j][DesName]
                if Rules[j][DesName] == Cases[i][DesName]:
                    if i not in correctlyClassifiedCases:
                        correctlyClassifiedCases.append(i)
                if Rules[j][DesName] != Cases[i][DesName]:
                    if i not in inCorrectlyClassifiedCases:
                        correctAndInCorrectlyClassifiedCases.append(i)
        for j in range(len(Rules)):
            if RuleCheckerUtility.checkRulesForPartialMatching(Rules[j], Cases[i], DesName) > 0 and i not in correctlyClassifiedCases and i not in correctAndInCorrectlyClassifiedCases:
                if i not in partiallyMatchedCases:
                    partiallyMatchedCases.append(i)
        for j in range(len(Rules)):
            if RuleCheckerUtility.checkRules(Rules[j], Cases[i], DesName)[1] == 0 and i not in correctlyClassifiedCases and i not in correctAndInCorrectlyClassifiedCases and i not in partiallyMatchedCases:
                if i not in notClassifiedCases:
                    notClassifiedCases.append(i)

    # CASES THAT ARE CLASSIFED EITHER CORRECTLY OR INCORRECTLY
    correctSet = set(correctlyClassifiedCases)
    correctAndInCorrectSet = set(correctAndInCorrectlyClassifiedCases)
    inCorrectSet = correctAndInCorrectSet.difference(correctSet)

    corrAndinCorrCases = correctSet.intersection(correctAndInCorrectSet)
    listOfcorrAndinCorrCases = list(corrAndinCorrCases)
    correctSet = correctSet.difference(correctAndInCorrectSet)
    notClassifiedCases = len(notClassifiedCases)

    RuleStats = []
    id = 0
    for caseNum in listOfcorrAndinCorrCases:
        for j in range(len(Rules)):
            [condition, matchedCases] = RuleCheckerUtility.checkRules(Rules[j], Cases[caseNum], DesName)
            if condition:
                RuleStats.append(RuleCheckerUtility.getRuleStats(Rules[j], caseNum, DesName, j, id, matchedCases, strengthFactor, matchingFactor))
                id = id + 1

    for caseNum in listOfcorrAndinCorrCases:
        if RuleCheckerUtility.classificationOfCases(caseNum, Cases, RuleStats, DesName, strengthFactor, matchingFactor, specificityFactor, supportFactor):
            correctSet.add(caseNum)
        else:
            inCorrectSet.add(caseNum)

    compInCorClass = len(inCorrectSet)
    compCorClass = len(correctSet)

    RuleStats = []
    id = 0
    for caseNum in partiallyMatchedCases:
        for j in range(len(Rules)):
            matchedCases = RuleCheckerUtility.checkRulesForPartialMatching(Rules[j], Cases[caseNum], DesName)
            if matchedCases:
                RuleStats.append(RuleCheckerUtility.getRuleStats(Rules[j], caseNum, DesName, j, id, matchedCases, strengthFactor, matchingFactor))
                id = id + 1

    for caseNum in partiallyMatchedCases:
        if RuleCheckerUtility.classificationOfCases(caseNum, Cases, RuleStats, DesName, strengthFactor, matchingFactor, specificityFactor, supportFactor):
            correctSet.add(caseNum)
        else:
            inCorrectSet.add(caseNum)

    parInCorClass = len(inCorrectSet)
    parCorClass = len(correctSet)

    notClassifiedPlusInCorrCases = parInCorClass + notClassifiedCases
    if len(Cases) == 0:
        return 0
    return round(float(notClassifiedPlusInCorrCases)/float(len(Cases)) , 2)
