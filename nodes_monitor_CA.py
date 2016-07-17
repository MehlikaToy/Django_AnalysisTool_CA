'''
Author: Gerry Meixiong
Made July 2015
Markov States of Hepatitis B
'''
pVar = -1.0
dVar = -2.0

cCHB = 1483
cCirr = 4414
cDecompCirr = 11690
cEntecavir = 8400
cHCC = 46538
cLT = 182040
cMonitor = 710
discountC = 0.03
discountU = 0.03
uCHB = 0.85
uCHBinactive = 0.95
uCHBseroclearance = 0.99
uResolution = 1
uSVR = 1
uSeroclearance = 1
cTenofovir = 11964

tested_rate = 0.346
followup_rate = 0.57
treatment_rate = 0.30

p_adherence = 0.85
p_monitor = 0.351

# Touch this part
cohortPop = 100
class BasicNode(object):

    def __init__(self, OV):
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = None
        self.destStates = []
        self.probValUT =  None
        self.probValLET = None
        self.probValAT =  None
        self.probValAFR = None
        self.probValAFF = None

    def __str__(self):
        return str(self.originValue)

    def getID(self):
        return self.ID

    def getOriginValue(self):
        return self.originValue

    def getVarName(self):
        return self.varName

    def getDestStates(self):
        return self.destStates

    def getProbValUT(self):
        return self.probValUT

    def getProbValLET(self):
        return self.probValLET

    def getProbValAT(self):
        return self.probValAT

    def getProbValAFR(self):
        return self.probValAFR

    def getProbValAFF(self):
        return self.probValAFF


    def nextStage(self,destStates, originVal, probList):
        temp = []
        for i in range(0, len(destStates)):
            tempNode = destStates[i](originVal * probList[i])
            temp.append(tempNode)
        return temp

def getMort(age):
    dic = {
    '1': 5.958E-3,
    '2': 1.021E-3,
    '3': 1.021E-3,
    '4': 1.021E-3,
    '5': 1.021E-3,
    '6': 5.9E-4,
	'7': 5.9E-4,
	'8': 5.9E-4,
	'9': 5.9E-4,
	'10': 5.9E-4,
	'11': 7.05E-4,
	'12': 7.05E-4,
	'13': 7.05E-4,
	'14': 7.05E-4,
	'15': 7.05E-4,
	'16': 2.227E-3,
	'17': 2.227E-3,
	'18': 2.227E-3,
	'19': 2.227E-3,
	'20': 2.227E-3,
	'21': 4.158E-3,
	'22': 4.158E-3,
	'23': 4.158E-3,
	'24': 4.158E-3,
	'25': 4.158E-3,
	'26': 4.869E-3,
	'27': 4.869E-3,
	'28': 4.869E-3,
	'29': 4.869E-3,
	'30': 4.869E-3,
	'31': 5.727E-3,
	'32': 5.727E-3,
	'33': 5.727E-3,
	'34': 5.727E-3,
	'35': 5.727E-3,
	'36': 7.072E-3,
	'37': 7.072E-3,
	'38': 7.072E-3,
	'39': 7.072E-3,
	'40': 7.072E-3,
	'41': 9.949E-3,
	'42': 9.949E-3,
	'43': 9.949E-3,
	'44': 9.949E-3,
	'45': 9.949E-3,
	'46': 1.5604E-2,
	'47': 1.5604E-2,
	'48': 1.5604E-2,
	'49': 1.5604E-2,
	'50': 1.5604E-2,
	'51': 2.4272E-2,
	'52': 2.4272E-2,
	'53': 2.4272E-2,
	'54': 2.4272E-2,
	'55': 2.4272E-2,
	'56': 3.5563E-2,
	'57': 3.5563E-2,
	'58': 3.5563E-2,
	'59': 3.5563E-2,
	'60': 3.5563E-2,
	'61': 5.006E-2,
	'62': 5.006E-2,
	'63': 5.006E-2,
	'64': 5.006E-2,
	'65': 5.006E-2,
	'66': 7.1576E-2,
	'67': 7.1576E-2,
	'68': 7.1576E-2,
	'69': 7.1576E-2,
	'70': 7.1576E-2,
	'71': 0.109091,
	'72': 0.109091,
	'73': 0.109091,
	'74': 0.109091,
	'75': 0.109091,
	'76': 0.170567,
	'77': 0.170567,
	'78': 0.170567,
	'79': 0.170567,
	'80': 0.170567,
	'81': 0.271135,
	'82': 0.271135,
	'83': 0.271135,
	'84': 0.271135,
	'85': 0.271135,
	'86': 0.425836,
	'87': 0.425836,
	'88': 0.425836,
	'89': 0.425836,
	'90': 0.425836,
	'91': 0.614587,
	'92': 0.614587,
	'93': 0.614587,
	'94': 0.614587,
	'95': 0.614587,
	'96': 0.786397,
	'97': 0.786397,
	'98': 0.786397,
	'99': 0.786397,
	'100':  1
    }
    if str(age) in dic.keys():
        return dic[str(age)]
    elif age >= 111 :
        return 1
    else:
        return dic['100']

#Basic Calculation Functions
def printList(list):
    for i in list:
        print ("%-40s %10.5f" % (i.getVarName(), round(i.getOriginValue(),5),))

def sumList(list):
    sum = 0
    for i in list:
        sum += i.getOriginValue()
    return sum

#Prob List Manipulation Functions
def pVarReplace(list):
    pVarOcc = 0

    for i in range(0, len(list)):
        if list[i] < 0:
            pVarOcc += 1

    if pVarOcc is not 0:
        total = sum(list)
        for i in range(0, len(list)):
            if  list[i] < 0:
               list[i] *= total

    return list

def dVarReplace(list, age):
    if dVar in list:
        dIndex = list.index(dVar)
        list[dIndex] = getMort(age - 1)
    return list

def trimList(array):   # sums up all nodes with same name to create a neat array
    resultList = sorted(array, key=lambda array: array.ID)
    i = 0
    while i < len(resultList)-1:
        if resultList[i].getID() == resultList[i+1].getID():
            resultList[i].originValue = (resultList[i].getOriginValue() + resultList[i+1].getOriginValue())
            del resultList[i+1]
        else:
            i += 1
    return resultList


#The Nodes
class Node01(BasicNode):

    def __init__(self, OV):
        super(Node01, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg Seroclearance"
        self.destStates = [Node01, Node08, Node35]
        self.probValUT =  [pVar  , 0.00155     , dVar]
        self.probValAFF = [pVar  , 0.00155  , dVar]

pMonitor = 1
pAdherence = 1

class Node02(BasicNode):

    def __init__(self, OV):
        super(Node02, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg +"
        self.destStates = [Node36    ,       Node26]
        self.probValUT =  [pMonitor  , 1 - pMonitor]

class Node03(BasicNode):

    def __init__(self, OV):
        super(Node03, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBeAg Seroconversion"
        self.destStates = [Node03, Node01, Node18, Node29,  Node35]
        self.probValUT =  [pVar  , 0.008 , 0.029 , 0.029 ,  dVar]
        self.probValAT =  [pVar  , 0.007 , 0.038 , 0.038 ,  dVar]
        self.probValAFR = [pVar  , 0.003 , 0.086 , 0.086 ,  dVar]
        self.secBranch =  [1     , 1     , pAdherence  , 1-pAdherence  ,  1]

class Node04(BasicNode):

    def __init__(self, OV):
        super(Node04, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe+"
        self.destStates = [Node11, Node28 , Node03 , Node08, Node17 , Node29 , Node14 , Node30 , Node35]
        self.probValLET = [pVar  , pVar   , 0.09   , 0.0048,  0.019  , 0.019  , 0.001  ,  0.001  ,  dVar ]
        self.probValAT =  [pVar  , pVar   , 0.07   , 0.0048,  0.019  , 0.019  , 0.0235 , 0.0235 ,  dVar ]
        self.secBranch =  [pAdherence, 1-pAdherence, 1  ,   1    , pAdherence   , 1-pAdherence   , pAdherence   , 1-pAdherence   ,  1]

class Node05(BasicNode):

    def __init__(self, OV):
        super(Node05, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe- disease"
        self.destStates = [Node08, Node17, Node29, Node14, Node30, Node24]
        self.probValUT =  [0.0048,  pVar  , pVar  , 0.0235, 0.0235, dVar]
        self.secBranch =  [1, pAdherence , 1-pAdherence  , pAdherence  , 1-pAdherence, 1 ]

class Node06(BasicNode):

    def __init__(self, OV):
        super(Node06, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis"
        self.destStates = [Node14, Node30, Node35]
        self.probValUT =  [pVar  , pVar  , dVar]
        self.secBranch =  [pAdherence  , 1-pAdherence, 1 ]

class Node07(BasicNode):

    def __init__(self, OV):
        super(Node07, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "DecompCirr"
        self.destStates = [Node07, Node08, Node09, Node23, Node35]
        self.probValUT =  [pVar  , 0.0710,   0.185, 0.1495,   dVar]
        self.probValAT =  [pVar  , 0.0710,   0.185, 0.1495,   dVar]

class Node08(BasicNode):

    def __init__(self, OV):
        super(Node08, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HCC"
        self.destStates = [Node08,  Node09, Node23, Node35]
        self.probValUT =  [pVar  ,   0.063,  0.545,   dVar]
        self.probValAT =  [pVar  ,   0.063,  0.545,   dVar]

class Node09(BasicNode):

    def __init__(self, OV):
        super(Node09, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Liver Transplantation"
        self.destStates = [Node09, Node23, Node24]
        self.probValUT =  [pVar  ,  0.066,   dVar]
        self.probValAT =  [pVar  ,  0.066,   dVar]

class Node10(BasicNode):
    def __init__(self, OV):
        super(Node10, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Sustained Virological Response"
        self.destStates = [Node08, Node10, Node14, Node35]
        self.probValLET  = [0.0048 * 0.5, pVar  , 0.001 * 0.5, dVar]
        self.probValAT = [0.0048 * 0.5, pVar  , 0.0235 * 0.5, dVar]

class Node11(BasicNode):
    def __init__(self, OV):
        super(Node11, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHB initial Rx"
        self.destStates = [Node10, Node12, Node15, Node08, Node35]
        self.probValUT =  [0.22  , pVar  , 0.0029, 0.002 , dVar]

class Node12(BasicNode):

    def __init__(self, OV):
        super(Node12, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHB Long Term Rx"
        self.destStates = [Node10, Node12, Node13, Node15 , Node08, Node35]
        self.probValUT =  [0.27  , pVar  , 0.01  , 0.00295, 0.002 , dVar]

class Node13(BasicNode):

    def __init__(self, OV):
        super(Node13, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHB Long Term with Rx with Resistance"
        self.destStates = [Node10, Node13, Node16, Node08, Node35]
        self.probValUT =  [0.05  , pVar  , 0.0295, 0.004 , dVar]

class Node14(BasicNode):

    def __init__(self, OV):
        super(Node14, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrohosis Initial Rx"
        self.destStates = [Node10, Node15, Node08, Node35]
        self.probValUT =  [0.22  , pVar  , 0.009 , dVar]

class Node15(BasicNode):

    def __init__(self, OV):
        super(Node15, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis Long Term Rx"
        self.destStates = [Node10, Node15, Node16, Node07, Node08, Node23, Node35]
        self.probValUT =  [0.27  , pVar  , 0.01  , 0.0071, 0.0167, 0.0239, dVar]

class Node16(BasicNode):

    def __init__(self, OV):
        super(Node16, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis Long Term Rx with resistance"
        self.destStates = [Node10, Node16, Node07, Node08, Node23, Node35]
        self.probValUT =  [0.05  , pVar  , 0.079 , 0.018 , 0.0478, dVar]

class Node17(BasicNode):

    def __init__(self, OV):
        super(Node17, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe- initial Rx"
        self.destStates = [Node10, Node18, Node20, Node08, Node35]
        self.probValUT =  [0.11  ,   pVar,  0.006, 0.002,   dVar]

class Node18(BasicNode):

    def __init__(self, OV):
        super(Node18, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe- longterm Rx"
        self.destStates = [Node10, Node18, Node19,  Node21, Node08, Node35]
        self.probValUT =  [0.11  ,   pVar,   0.01, 0.00295, 0.006,   dVar]

class Node19(BasicNode):

    def __init__(self, OV):
        super(Node19, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe- longterm Rx resistance"
        self.destStates = [Node10, Node19, Node21, Node08, Node35]
        self.probValUT =  [0.005 ,   pVar,  0.062, 0.002,   dVar]

class Node20(BasicNode):

    def __init__(self, OV):
        super(Node20, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis e- initial Rx"
        self.destStates = [Node10, Node21, Node08, Node35]
        self.probValUT =  [0.11  ,   pVar, 0.015,   dVar]

class Node21(BasicNode):

    def __init__(self, OV):
        super(Node21, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis e- longterm Rx"
        self.destStates = [Node10, Node21, Node22, Node07, Node08, Node23, Node35]
        self.probValUT =  [0.11  ,   pVar,   0.01, 0.0071, 0.0167, 0.0239,   dVar]

class Node22(BasicNode):

    def __init__(self, OV):
        super(Node22, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis e- longterm Rx with resistance"
        self.destStates = [Node10, Node22, Node07, Node08, Node23, Node35]
        self.probValUT =  [0.005 ,   pVar,  0.079,  0.029, 0.0478,   dVar]

class Node23(BasicNode):

    def __init__(self, OV):
        super(Node23, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Death HBV"
        self.destStates = [Node23]
        self.probValUT = [1]

class Node24(BasicNode):

    def __init__(self, OV):
        super(Node24, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Death (Other)"
        self.destStates = [Node24]
        self.probValUT =  [1]
        self.probValAT =  [1]

class Node25(BasicNode):

    def __init__(self, OV):
        super(Node25, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg SeroclearanceNH"
        self.destStates = [Node25, Node32, Node35]
        self.probValUT =  [pVar  , 0.00155   , dVar]
        self.probValAFF = [pVar  , 0.00155  , dVar]

class Node26(BasicNode):

    def __init__(self, OV):
        super(Node26, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg + NH"
        self.destStates = [Node25, Node28, Node30 , Node32  , Node35, Node26]
        self.probValUT =  [0.0077, 0.0087, 0.00038, 0.0017, dVar  ,   pVar]
        self.probValAT =  [0.0107, 0.0143, 0.00049, 0.0017, dVar  ,   pVar]
        self.probValAFR = [0.0165, 0.0278, 0.00068, 0.0017, dVar  ,   pVar]
        self.probValAFF = [0.0183, 0.0202, 0.00150, 0.0017, dVar  ,   pVar]

class Node27(BasicNode):

    def __init__(self, OV):
        super(Node27, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBeAg SeroconversionNH"
        self.destStates = [Node27, Node25, Node29, Node30, Node32, Node35]
        self.probValUT =  [pVar  , 0.008 , 0.029 , 0.002 , 0.00155    , dVar]
        self.probValAT =  [pVar  , 0.007 , 0.038 , 0.01  , 0.00155     , dVar]
        self.probValAFR = [pVar  , 0.003 , 0.086 , 0.042 , 0.00155     , dVar]
        self.probValAFF = [pVar  , 0.003 , 0.086 , 0.042 , 0.00155  , dVar]

class Node28(BasicNode):

    def __init__(self, OV):
        super(Node28 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHBe+NH"
        self.destStates = [Node28, Node27, Node29, Node30, Node32, Node34, Node35]
        self.probValLET = [pVar  , 0.09  , 0.019 , 0.001 , 0.0048 , 0.0011, dVar]
        self.probValAT =  [pVar  , 0.07  , 0.019 , 0.0235, 0.0048 , 0.0011, dVar]

class Node29(BasicNode):

    def __init__(self, OV):
        super(Node29 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "CHB e- diseaseNH"
        self.destStates = [Node29, Node26, Node30, Node32, Node34, Node35]
        self.probValUT  = [pVar  , 0.016 , 0.0235, 0.0048, 0.0011, dVar]

class Node30(BasicNode):

    def __init__(self, OV):
        super(Node30 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Cirrhosis NH"
        self.destStates = [Node30, Node31, Node32, Node34, Node35]
        self.probValUT =  [pVar  , 0.039 , 0.0316  , 0.0489, dVar]

class Node31(BasicNode):

    def __init__(self, OV):
        super(Node31 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "DecompCirr NH"
        self.destStates = [Node31, Node32, Node33, Node34, Node35]
        self.probValUT =  [pVar  , 0.0710, 0.185  , 0.1495, dVar]

class Node32(BasicNode):

    def __init__(self, OV):
        super(Node32 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HCC NH"
        self.destStates = [Node32, Node33, Node34, Node35]
        self.probValUT =  [pVar  , 0.063 , 0.545 , dVar]

class Node33(BasicNode):

    def __init__(self, OV):
        super(Node33 , self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Liver Transplantation NH"
        self.destStates = [Node33, Node34, Node35]
        self.probValUT  = [pVar  , 0.066 , dVar]

class Node34(BasicNode):

    def __init__(self, OV):
        super(Node34, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Death HBV NH"
        self.destStates = [Node34]
        self.probValUT =  [1]

class Node35(BasicNode):

    def __init__(self, OV):
        super(Node35, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "Death Other NH"
        self.destStates = [Node35]
        self.probValUT =  [1]

class Node36(BasicNode):

    def __init__(self, OV):
        super(Node36, self).__init__(1)
        self.ID = type(self).__name__
        self.originValue = OV
        self.varName = "HBsAg + Monitor"
        self.destStates = [Node01, Node04,  Node14,   Node08, Node35, Node36]
        self.probValUT =  [0.0077, 0.0087 , 0.00038, 0.0017 , dVar  ,  pVar ]
        self.probValAT =  [0.0107, 0.0143 , 0.00049, 0.0017 , dVar  ,  pVar ]
        self.probValAFR = [0.0165, 0.0278 , 0.00068, 0.0017 , dVar  ,  pVar ]
        self.probValAFF = [0.0183, 0.0202 , 0.00150, 0.0017 , dVar  ,  pVar ]

