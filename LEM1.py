#!usr/bin/python
"""
    LEM1.py, by Madhu Chegondi
    This program takes a data file and generate rules for the DATASET
"""
import LEM1Utility

def LEM1Classifier(trainDataAttr, trainDataDes, DesName):
    """Compute Rules from the given dataset"""
    updatedAttr = LEM1Utility.cutpointStrategy(trainDataAttr)

    # Converiting list of dictionaries to "list of List of tuples"
    attributes = LEM1Utility.dictToTuple(updatedAttr)

    desPart =  LEM1Utility.computePartitions(trainDataDes)
    attrPart = LEM1Utility.computePartitions(attributes)

    # Finds number of classes and class Names
    x = LEM1Utility.tupleToDict(trainDataDes)
    numClasses = len(set([item[DesName] for item in x]))
    classes = list(set([item[DesName] for item in x]))

    Rules = []
    for i in range(numClasses):
        lowerClass = LEM1Utility.lowerApprox(classes[i], attrPart[0], desPart)
        singleLowerCovering = LEM1Utility.LEM1(attributes, lowerClass)
        ruleset = LEM1Utility.generateRules(singleLowerCovering, lowerClass)
        desSet = ((DesName, classes[i]),)
        for i in range(len(ruleset)):
            Rules.append(ruleset[0] + desSet)

    for i in range(numClasses):
        if(LEM1Utility.isConsistent(attrPart[0], desPart[0])):
            break
        else:
            upperClass = LEM1Utility.upperApprox(classes[i], attrPart[0], desPart)
            singleUpperCovering = LEM1Utility.LEM1(attributes, upperClass)
            ruleset = LEM1Utility.generateRules(singleUpperCovering, upperClass)
            desSet = ((DesName, classes[i]),)
            for i in range(len(ruleset)):
                Rules.append(ruleset[0] + desSet)
    tempRules = LEM1Utility.tupleToDict(Rules)
    for j in range(len(tempRules)):
        for i in tempRules[j].keys():
            index = i.find('***')
            if index > 0:
                tempRules[j][i[0:index]] = tempRules[j].pop(i)
            else:
                tempRules[j][i] = tempRules[j].pop(i)

    return tempRules


if __name__ == "__main__":
    LEM1Classifier()
