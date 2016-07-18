'''
Author: Calvin Yin, Gerry MeiXiong, Jasmine Kim
Made July 2015
Markov Model Emulator of Hepatitis B
'''


from nodes_monitor_e1 import *

# Touch this part
age = 25
# age = age + 1
total_stages = 23
stage_timeFrame = 1  # in years
# The initial Probabilities
initialList = [Node36(0), Node02(0.0762), Node04(0.0176), Node05(0.0187), Node06(0), Node26(0.3102), Node28(0.2794), Node29(0.2979), Node30(0)]
#initialList = getInitialNodes(age)

age += 1

print '>>> INITIAL LIST Stage: BASE, Age: %s' % (age)
printList(initialList)


# Don't touch this part
cummDict = {}
oldList = initialList
newList = []

guacDict = {}

DeathHBV = [['Stages', 'Treatment (dotted)', 'Natural History (solid)']]
Cirrhosis = [['Stages', 'Treatment (dotted)', 'Natural History (solid)']]
HCC = [['Stages', 'Treatment (dotted)', 'Natural History (solid)']]
LT = [['Stages', 'Treatment (dotted)', 'Natural History (solid)']]

cummCirr = 0;

for curr_stage in range(1, total_stages+2):


    if curr_stage != 1:
        oldList = newList
        newList = []

    for node in oldList:

        if age - 1 >= 50 and node.getProbValAFF():
            temp = node.getProbValAFF()
        elif age - 1 >= 40 and node.getProbValAFR():
            temp = node.getProbValAFR()
        elif age - 1 <= 25 and node.getProbValUTF():
            temp = node.getProbValUTF()
        elif age - 1 > 25 and node.getProbValATF():
            temp = node.getProbValATF()
        elif age - 1 <= 30 and node.getProbValLET():
            temp = node.getProbValLET()
        elif age - 1 >= 30 and node.getProbValAT():
            temp = node.getProbValAT()
        else:
            temp = node.getProbValUT()

        try:
            for i in range(0, len(temp)):
                temp[i] = temp[i] * node.secBranch[i]
        except:
            pass

        temp = dVarReplace(temp, age)
        temp = pVarReplace(temp)
        temp, cummCirr = node.nextStage(node.getDestStates(), node.getOriginValue(), temp, cummCirr, currNode = node)

        for i in temp:
            if i.getGuac() != 0:
                guacDict[i.getVarName()] = i.getGuac()

        for i in temp:
            newList.append(i)

    newList = trimList(newList)

    def getCummDict(query):
        try:
            return cummDict[query]
        except:
            return 0

    t_death = [curr_stage ,0, 0]
    t_cirr = [curr_stage ,0, 0]
    t_hcc = [curr_stage ,0, 0]
    t_lt =[curr_stage ,0, 0]

    for node in newList:
        try:
            cummDict[node.getVarName()] += (node.getOriginValue() - guacDict[node.getVarName()]) * cohortPop
        except:
            try:
                cummDict[node.getVarName()] += node.getOriginValue() * cohortPop
            except:
                cummDict[node.getVarName()] = node.getOriginValue() * cohortPop

    t_death[1] = round(getCummDict('Death HBV'), 3)
    t_death[2] = round(getCummDict('Death HBV NH'), 3)

    t_cirr[1] = round(cummCirr * cohortPop, 3)
    t_cirr[2] = round(getCummDict('Cirrhosis NH'), 3)

    t_hcc[1] = round(getCummDict('HCC'), 3)
    t_hcc[2] = round(getCummDict('HCC NH'), 3)

    t_lt[1] = round(getCummDict('Liver Transplantation'), 3)
    t_lt[2] = round(getCummDict('Liver Transplantation NH'), 3)

    DeathHBV.append(t_death)
    Cirrhosis.append(t_cirr)
    HCC.append(t_hcc)
    LT.append(t_lt)


    output = {}
    for i in newList:
        output[i.getVarName()] = i.getOriginValue()

    finalList = [['Cirrhosis', 0, 0], ['HCC', 0, 0], ['Liver Transplantation', 0, 0], ['Death HBV', 0, 0]]
    try:
        finalList[0][1] = cummCirr * cohortPop
        finalList[0][2] = (getCummDict('Cirrhosis NH'))
    except:
        pass
    try:
        finalList[1][1] = (getCummDict('HCC'))
        finalList[1][2] = (getCummDict('HCC NH'))
    except:
        pass
    try:
        finalList[2][1] = (getCummDict('Liver Transplantation'))
        finalList[2][2] = (getCummDict('Liver Transplantation NH'))
    except:
        pass
    try:
        finalList[3][1] = (getCummDict('Death HBV'))
        finalList[3][2] = (getCummDict('Death HBV NH'))
    except:
        pass



    print "====================================================\n"
    print "                     STAGE:", curr_stage
    print "                     AGE:", age
    printList(newList)
    print "Cumulative States:", cummDict
    print ""

    age += stage_timeFrame

if round(sumList(initialList), 10) == round(sumList(newList), 10):
    print "No Data Leak"
else:
    print "Data Leak Check Node Values"

