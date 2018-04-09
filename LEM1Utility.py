#!usr/bin/python

"""
utility.py, by Madhu Chegondi, 03-23-2018
"""
import pandas as pd

def computePartitions(S):
    """
    Takes a list of list of list of tuples and gives you two vectors that
    stores both partition sets and concept name of that partition set
    """
    # gets unique list of cases which are used as keys for dictionaries
    a = list(set([tuple(i) for i in S]))
    partitionset = dict.fromkeys(a, [])
    for i in range(len(a)):
        # Creating a dictionary with all unique cases
        partitionset[a[i]] = []
    for i in range(len(a)):
        for j in range(len(S)):
            if(a[i] == tuple(S[j])):
                partitionset[a[i]].append(j)
    partset = []
    concept = []
    for keys in partitionset:
        concept.append(keys)
        partset.append(set(partitionset[keys]))
    return partset,concept


def isConsistent(attrPartitions, decPartitions):
    """
    inputs          : output of compute Partitions
    Returns true    : when A* is subset of d*
    Returns false   : when A* is not subset of d*
    """
    for t in attrPartitions:
        logicalValue = False
        for s in decPartitions:
            # returns false if all the A* elements are not subset of d*
            # because d* is a list of sets for unique concepts
            logicalValue = logicalValue or t.issubset(s)
        if(logicalValue == False):
            return False
    return True


def LEM1(S, R):
    """
    input       : list of list of tuples of attributes and decisions
    output      : list of list of tuples after applying LEM1 with
                  few attribute values
    """
    R_partitions = computePartitions(R)
    S_partitions = computePartitions(S)
    P = S[:]
    if(isConsistent(S_partitions[0], R_partitions[0])):
        tempS = tupleToDict(S)

        df = pd.DataFrame(tempS)
        # collect all the column names to keep track of removed attribute name
        XColNames = list(df.columns.values)
        for i in range(len(df.columns)):
            # Reomve first column Name and pass to the dataFrame
            bkpCol = XColNames.pop(0)
            Q = df.ix[:, XColNames].T.to_dict().values()
            Q1 = dictToTuple(Q)
            Q_partitions = computePartitions(Q1)
            if (isConsistent(Q_partitions[0], R_partitions[0])):
                P = Q1[:]
            else:
                # after removing column if the dataset if not consistent append the
                # column to the end of Column Names. Cause everytime we are removing
                # the first element from the Column Names
                XColNames.append(bkpCol)
        return P
    return """ Something went wrong with LOWER and UPPER approximations !!! """

def LEM(S, R):
    """
    input       : list of list of tuples of attributes and decisions
    output      : list of list of tuples after applying LEM1 with
                  few attribute values
    """
    R_partitions = computePartitions(R)
    S_partitions = computePartitions(S)
    P = S[:]
    if(isConsistent(S_partitions[0], R_partitions[0])):
        df = tupleToDict(S)

        # df = pd.DataFrame(tempS)
        # collect all the column names to keep track of removed attribute name
        XColNames = df[0].keys()
        for i in renage(len(df)):
            # Reomve first column Name and pass to the dataFrame
            bkpCol = XColNames.pop(i)
            for item in df:
                for key in XColNames:
                    tempQ[key] = item[i]
                    Q.append(tempQ.items())
            # Q = df.ix[:, XColNames].T.to_dict().values()
            Q1 = dictToTuple(Q)
            Q_partitions = computePartitions(Q1)
            if (isConsistent(Q_partitions[0], R_partitions[0])):
                P = Q1[:]
            else:
                # after removing column if the dataset if not consistent append the
                # column to the end of Column Names. Cause everytime we are removing
                # the first element from the Column Names
                XColNames.append(bkpCol)
        return P
    return """ Something went wrong with LOWER and UPPER approximations !!! """


def cutpointStrategy1(listOfDict):
    """
    Applying discritization using all cutpoint strategy
    """
    allNumValues = []
    Keys = listOfDict[0].keys()
    listOfDict1 = []
    for item in listOfDict:
        listOfDict1.append(dict(item))
    for j in Keys:
        if isinstance(listOfDict1[0][j], int) or isinstance(listOfDict1[0][j], float):
            try:
                distNumValues = list(set([listOfDict1[i][j] for i in range(len(listOfDict1))]))
                distNumValues.sort()
                cutPoints = [round((distNumValues[x]+distNumValues[x+1])/2 ,2) for x in range(len(distNumValues)-1)]
                for m in range(len(cutPoints)):
                    for k in range(len(listOfDict1)):
                        if listOfDict1[k][j] < cutPoints[m]:
                            listOfDict1[k][j+'***'+str(cutPoints[m])] = str(min(distNumValues)) + ".." + str(cutPoints[m])
                        else:
                            listOfDict1[k][j+'***'+str(cutPoints[m])] = str(cutPoints[m]) + ".." + str(max(distNumValues))
                for item in range(len(listOfDict1)):
                    if j in listOfDict1[item].keys():
                        listOfDict1[item].pop(j)
            except ValueError:
                continue
    return listOfDict1


def tupleToDict(tup):
    """convets a tuple to dictionary"""
    dic = []
    for i in range(len(tup)):
        dic.append(dict(tup[i]))
    return dic


def dictToTuple(dic):
    """Converts a ditionary to tuple"""
    tup = []
    for i in range(len(dic)):
        tup.append(dic[i].items())
    return tup


def generateRules1(singleCovering, decisions):
    """
    Generate Rules from the given single covering to the decisions
    """
    tempCovering1 = tupleToDict(singleCovering)
    tempDecisions = tupleToDict(decisions)
    dictKey = tempDecisions[0].keys()[0]
    tempCovering = []
    for i in tempCovering1:
        tempCovering.append(dict(i))

    for i in range(len(tempDecisions)):
        tempCovering[i][dictKey] = tempDecisions[i][dictKey]
        tempCovering[i]['ids'] = i

    ruleDF = []
    for n in range(len(tempCovering)):
        if tempCovering[n][dictKey] != 'madhu':
            ruleDF.append(tempCovering[n])

    for d in ruleDF:
        del d[dictKey]

    ruleset = set([item['ids'] for item in ruleDF])

    for d in ruleDF:
        del d['ids']

    ruleTuple = dictToTuple(ruleDF)

    for i in range(len(ruleTuple)):
        listofsets = []
        count = 0

        for j in range(len(ruleTuple[i])):
            # collect the cases that are satisfying a rule from the ruleTuple
            listItems = []
            for x in range(len(tempCovering)):
                if tempCovering[x][ruleTuple[i][j][0]] == ruleTuple[i][j][1] and ruleTuple[i][j][0] != 'ids':
                    listItems.append(x)
            listofsets.append(set(listItems))

        for m in range(len(listofsets)):
            if (len(listofsets) > 1):
                # drop the first condition from the rule
                appendlast = listofsets.pop(0)

            # compute the case Numbers thar are satifying the ruleTUple
            u = set.intersection(*listofsets)

            if (not u.issubset(ruleset)):
                # Check whether the remaining attributes satisfy the cases
                # if not append the condition to the attribute list
                listofsets.append(appendlast)
            elif(len(ruleTuple[i]) > 1):
                # if yes remove the dropped attribute from the list
                ruleTuple[i].pop(m-count)
                count = count + 1
    return list(set([tuple(i) for i in ruleTuple]))


def lowerApprox(concept, attrPartitions, decPartitions):
    """ generates a decision vector satisfying lower approximations"""
    conceptList = []
    dictKey = 'class' #'LowerApprox['+concept+']'
    lowAConcet = {}
    lowAConcept = []
    conceptList.append(concept)
    lowA = set()
    for i in range(len(decPartitions[0])):
        if conceptList == [j[1] for j in decPartitions[1][i]]:
            for a in attrPartitions:
                if(a.issubset(decPartitions[0][i])):
                    lowA = lowA.union(a)
    numCases = max([max(a) for a in attrPartitions])
    # Add place holder for the cases that doesnt belong to the concept
    desRow = [concept if (i in lowA) else 'madhu' for i in range(numCases+1)]
    for m in range(len(desRow)):
        lowAConcet[dictKey] = desRow[m]
        lowAConcept.append(lowAConcet.items())
    return lowAConcept


def upperApprox(concept, attrPartitions, decPartitions):
    """ generates a vector with that decision satisfying upper Approximations"""
    conceptList = []
    dictKey = 'class'     #'UpperApprox['+concept+']'
    upAConcet = {}
    upAConcept = []
    conceptList.append(concept)
    upA = set()
    for i in range(len(decPartitions[0])):
        if (conceptList == [j[1] for j in decPartitions[1][i]]):
            for a in attrPartitions:
                if(a.intersection(decPartitions[0][i])):
                    upA = upA.union(a)
    numCases = max([max(a) for a in attrPartitions])
    # Add place holder for the cases that doesnt belong to the concept
    desRow = [concept if (i in upA) else 'madhu' for i in range(numCases+1)]
    for m in range(len(desRow)):
        upAConcet[dictKey] = desRow[m]
        upAConcept.append(upAConcet.items())
    return upAConcept
