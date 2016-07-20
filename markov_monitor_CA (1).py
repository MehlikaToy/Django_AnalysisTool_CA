'''
Author: Calvin Yin, Gerry MeiXiong, Jasmine Kim
Made July 2015
Markov Model Emulator of Hepatitis B
'''

from nodes_monitor_CA import *

# Touch this part
age = 45
total_stages = 20
stage_timeFrame = 1  # in years
# The initial Probabilities
initialList = [Node36(0), Node02(0.0998), Node04(0.0060), Node05(0.0209), Node06(0.0014), Node26(0.4060), Node28(0.0959), Node29(0.3327), Node30(0.0373)]
cohortPop = 10000
#initialList = getInitialNodes(age)


# Don't touch this part=====
cummDict = {}
oldList = initialList
newList = []

# No More Touching
print "                     Origin State"
print "                     AGE:", age
printList(initialList)
print ""
age += 1

for curr_stage in range(1, total_stages+1):

    if curr_stage != 1:
        oldList = newList
        newList = []

    for node in oldList:

        if age - 1 >= 50 and node.getProbValAFF():
            temp = node.getProbValAFF()
        elif age - 1 >= 40 and node.getProbValAFR():
            temp = node.getProbValAFR()
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

        print "PVAR:" , temp

        temp = node.nextStage(node.getDestStates(), node.getOriginValue(), temp)

        for i in temp:
            newList.append(i)

    newList = trimList(newList)

   # for node in newList:
     #   if not str(node.getVarName()) in cummDict:
     #       cummDict[str(node.getVarName())] = node.getOriginValue()
     #   else:
      #      cummDict[str(node.getVarName())] += (node.getOriginValue())

    def getCummDict(query):
        try:
            return cummDict[query]
        except:
            return 0

    for node in newList:
        try:
            cummDict[node.getVarName()] += (node.getOriginValue() - guacDict[node.getVarName()]) * cohortPop
        except:
            try:
                cummDict[node.getVarName()] += node.getOriginValue() * cohortPop
            except:
                cummDict[node.getVarName()] = node.getOriginValue() * cohortPop


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