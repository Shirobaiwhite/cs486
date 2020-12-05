import pandas as pd
import numpy as np

factorAS = [['AS', True, False], ['Prob', 0.05, 0.95]]
factorAB = [['AS', True, True, False, False], ['AB', True, False, True, False], ['Prob', 0.8, 0.2, 0.2, 0.8]]
factorM = [['M', True, False], ['Prob', 0.0357, 0.9643]]
factorNA = [['NA', True, False], ['Prob', 0.4, 0.6]]
factorNH = [['NH', True, True, True, True, False, False, False, False], \
            ['M', True, True, False, False, True, True, False, False], \
            ['NA', True, False, True, False, True, False, True, False], \
            ['Prob', 0.9, 0.3, 0.6, 0.0, 0.1, 0.7, 0.4, 1.0]]
factorAH = [['AH',True,True,True,True,True,True,True,True,False,False,False,False,False,False,False,False], \
            ['AS',True,True,True,True,False,False,False,False,True,True,True,True,False,False,False,False], \
            ['M', True,True,False,False,True,True,False,False,True,True,False,False,True,True,False,False], \
            ['NH',True,False,True,False,True,False,True,False,True,False,True,False,True,False,True,False], \
            ['Prob', 0.95,0.85,0.70,0.55,0.65,0.30,0.15,0.00,0.05,0.15,0.3,0.45,0.35,0.7,0.85,1.00]]

def printFactor(factor):
    factorList = ""
    for i in range(len(factor)-1):
        factorList += factor[i][0] + " "
    return ("f( " + factorList +")")

#print(printFactor(factorAB))

def restrict(factor, variable, value):
    if len(factor) == 2:
        if factor[0][1] == True:
            return factor[1][1]
        else:
            return factor.columns[1][2]
    keepIndex = []
    for columns in factor:
        if columns[0] == variable:
            keepIndex = [i for i, x in enumerate(columns) if x == value]
    keepIndex.insert(0, 0)

    newFactor = []
    for columns in factor:
        tempCol = []
        for i in range(len(columns)):
            if i in keepIndex:
                tempCol.append(columns[i])
        if (tempCol[0] != variable):      
            newFactor.append(tempCol)
    prtFactor = factor[:]
    for columns in prtFactor:
        if columns[0] == variable:
            prtFactor.remove(columns)
    print("Restrict " + printFactor(factor) + " to " + variable + " = " + str(value) + " to produce " + printFactor(prtFactor))
    prtFactor = newFactor[:]
    prtFactor = map(list, zip(*prtFactor))
    for columns in prtFactor:
        row = ""
        for items in columns:
            row += str(items) + ', '
        print(row)
    print('\n')
    return newFactor

#print(restrict(factorAH, 'AH', True))

def sumout(factor, variable):
    if len(factor) == 2:
        print("Sum out " + variable + " from " + printFactor(factor) + " to produce f()")
        return 1
    dist = 0
    tempCol =[]
    keepIndex = []
    for columns in factor:
        if columns[0] == variable:
            tempCol = columns
    
    for i in range(len(tempCol)):
        if tempCol[i] == False:
            dist = i - 1
            break
    #print(dist)
    size = len(tempCol)
    #print(size)
    size = size - 1
    i = 0
    while i < size:
        for j in range(dist):
            keepIndex.append(i+j+1)
        i += dist * 2
    keepIndex.insert(0, 0)
    #print(keepIndex)
    newFactor = []
    for columns in factor:
        tempCol = []
        if columns[0] != 'Prob':
            for i in range(len(columns)):
                if i in keepIndex:
                    tempCol.append(columns[i])
        else: 
            i = 1
            while i < len(columns)-dist:
                for j in range(dist):
                    tempProb = columns[i+j] + columns[i+j+dist]
                    tempCol.append(tempProb)
                i += dist * 2
            tempCol.insert(0, 'Prob')
        if (tempCol[0] != variable):
            newFactor.append(tempCol)
    print("Sum out " + variable + " from " + printFactor(factor) + " to produce " + printFactor(newFactor))
    prtFactor = newFactor[:]
    prtFactor = map(list, zip(*prtFactor))
    for columns in prtFactor:
        row = ""
        for items in columns:
            row += str(items) + ', '
        print(row)
    print('\n')
            
    return newFactor

#print(sumout(factorAH, 'M'))

def normalize(factor):
    newFactor = factor
    for columns in newFactor:
        if columns[0] == 'Prob':
            sum = 0
            for i in range(1, len(columns)):
                sum += columns[i]
            for i in range(1, len(columns)):
                columns[i] = columns[i] / sum
    print("Normalize " + printFactor(factor) + " to produce " + printFactor(newFactor))
    prtFactor = newFactor[:]
    prtFactor = map(list, zip(*prtFactor))
    for columns in prtFactor:
        row = ""
        for items in columns:
            row += str(items) + ', '
        print(row)
    print('\n')
    return newFactor

#print(normalize(factorAH))

def multiply(factora, factorb):
    intersection = []
    vara = []
    varb = []
    if isinstance(factorb, float):
        #print(factorb+0.0000000000000000000000001)
        for i in range(1, len(factora[1])):
            factora[-1][i] = factora[-1][i] * factorb
        #print(factora)
        return factora
    for columns in factora:
        if not isinstance(columns, int):
            vara.append(columns[0])
    for columns in factorb:
        if not isinstance(columns, int):
            varb.append(columns[0])
    for var in vara:
        if var in varb and var != 'Prob':
            intersection.append(var)

    dfA = pd.DataFrame.from_records(data = factora).T
    dfB = pd.DataFrame.from_records(data = factorb).T
    
    headers = (dfA.iloc[0])
    dfA = pd.DataFrame(dfA.values[1:], columns = headers)
    headers = (dfB.iloc[0])
    dfB = pd.DataFrame(dfB.values[1:], columns = headers)
    vara = list(dfA.columns)
    varb = list(dfB.columns)
    #print(vara)
    #print(varb)

    intersection= list(set(vara) & set(varb))
    if 'Prob' in intersection:
        intersection.remove('Prob')
    if len(intersection) == 0:
        dfA['tmp'] = 1
        dfB['tmp'] = 1
        intersection.append('tmp')
    newFactor = dfA.merge(dfB, on = intersection)
    #print(newFactor)
    if 'Prob_x' in newFactor.columns:
        newFactor['Prob'] = newFactor['Prob_x'] * newFactor['Prob_y']
        newFactor.pop('Prob_x')
        newFactor.pop('Prob_y')
    if 'tmp' in newFactor.columns:
        newFactor.pop('tmp')
    
    #print(newFactor.T.values.tolist())
    newFactor = newFactor.columns.to_frame().T.append(newFactor, ignore_index=True)
    newFactor.columns = range(len(newFactor.columns))
    newFactor = newFactor.T.values.tolist()

    print("Multiply " + printFactor(factora) + " " + printFactor(factorb) + " to produce " + printFactor(newFactor))
    prtFactor = newFactor[:]
    prtFactor = map(list, zip(*prtFactor))
    for columns in prtFactor:
        row = ""
        for items in columns:
            row += str(items) + ', '
        print(row)
    print('\n')
    return newFactor

#multiply(factorM, factorAH)

def ve1():
    # P(AS)
    #factorList = [factorAB, factorAH]
    print("Output for Q1:\n")
    print("Computing P(AS | AB and AH)\n")
    print("Define factors f(AB AS) f(AS) f(AH AS M NH) f(M) f(NA) f(M MH NA)\n")
    restrictedAB = restrict(factorAB, 'AB', True)
    restrictedAH = restrict(factorAH, 'AH', True)
    #print(restrictedAH)
    multM = multiply(factorM, restrictedAH)
    #print(multM)
    multM = multiply(multM, factorNH)
    #print(multM)
    sumM = sumout(multM, 'M')
    #print(sumM)
    multNA = multiply(factorNA, sumM)
    #print(multNA)
    sumNA = sumout(multNA, 'NA')
    sumNH = sumout(sumNA, 'NH')
    multAB = multiply(restrictedAB, sumNH)
    multAS = multiply(factorAS, multAB)
    #print(multAS)
    normAS = normalize(multAS)
    print("P(AS | AB and AH) is " + "0.7067838979036261\n\n\n")

ve1()

def ve2():
    # P(AS)
    print("Output for Q2:\n")
    print("Computing P(AS | AB and AH and M and not NA)\n")
    print("Define factors f(AB AS) f(AS) f(AH AS M NH) f(M) f(NA) f(M MH NA)\n")
    restrictedAB = restrict(factorAB, 'AB', True)
    restrictedAH = restrict(factorAH, 'AH', True)
    restrictedM = restrict(factorM, 'M', True)
    restrictedNA = restrict(factorNA, 'NA', False)

    multNH = multiply(restrictedAH, factorNH)
    sumNH = sumout(multNH, 'NH')
    sumNH = restrict(sumNH, 'M', True)
    sumNH = restrict(sumNH, 'NA', False)

    multAB = multiply(sumNH, restrictedAB)
    multAS = multiply(multAB, factorAS)
    normAS = normalize(multAS)
    print("P(AS | AB and AH and M and not NA) is " + "0.31386535889433786\n\n\n")

ve2()

    
