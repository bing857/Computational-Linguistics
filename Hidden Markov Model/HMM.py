import random
import argparse
import math
import itertools
import copy


def getWords(wordList):
    # file = open(targetfile, "r")
    file = open("english1000.txt", "r")  #change targetfiles both here and bottom
    for word in file:
        word=word.lower().strip()
        if word[-1]!="#":
            word += "#"
        wordList.append(word)

def initializeRandomDist(lettersDict):
    totalsum = 0
    for i in lettersDict.keys():
        temp = random.randint(1, 10000)
        lettersDict[i]=temp
        totalsum += temp
    for (k, v) in lettersDict.items():
        lettersDict[k]=v/totalsum   

def initializeLetterDist(lettersDict, wordList):
    for word in wordList:
        for letter in word:
            if letter not in lettersDict:
                lettersDict[letter]=1
            else:
                lettersDict[letter]+=1
    initializeRandomDist(lettersDict)    

def initializeZeroDist(lettersDict, wordList):
    for word in wordList:
        for letter in word:
            if letter not in lettersDict:
                lettersDict[letter]=0


def printTransitions(stateDict):
    print("Transitions:")
    for (k, v) in sorted(list(stateDict.items()), key=lambda tup : tup[0][3]):
            print("    To State    " + k[3] + "  ", v)
    print("")

def Initialization(A_01=0.5, A_10=.5):
    # State 0
    state0_transitionDict={}
    state0_transitionDict["A_01"]=A_01
    state0_transitionDict["A_00"]=1-A_01
    state0_wordList=[]
    state0_emissionDict={}
    getWords(state0_wordList)
    initializeLetterDist(state0_emissionDict, state0_wordList)
    # State 1
    state1_transitionDict={}
    state1_transitionDict["A_10"]=A_10
    state1_transitionDict["A_11"]=1-A_10
    state1_wordList=[]
    state1_emissionDict={}
    getWords(state1_wordList)
    initializeLetterDist(state1_emissionDict, state1_wordList)
    
    #Pi
    pi_dict={"0":1, "1":1}
    initializeRandomDist(pi_dict)
    state0={"transition":state0_transitionDict, "emission":state0_emissionDict}
    state1={"transition":state1_transitionDict, "emission":state1_emissionDict}
    return(pi_dict, state0, state1)

def forwardProbability(word, pi_dict, state0, state1):
    # Accessible Data:
    #   pi[pi1/pi0]
    #   state0["transition"][STATECHANGE]
    #   state0["emission"][LETTER]
    #   state1["transition"][STATECHANGE]
    #   state1["emission"][LETTER] 

    # alpha:[time][state]
    alpha={}
    # initialize time subdictionaries
    for i in range(len(word)+1):
        alpha[str(i+1)]={}
    alpha["1"]["0"]=pi_dict["0"]
    alpha["1"]["1"]=pi_dict["1"]
    for i in range(2,len(word)+2):
        # to state 0 
        to0fromState0 = alpha[str(i-1)]["0"] * state0["transition"]["A_00"] * state0["emission"][word[i-2]]
        to0fromState1 = alpha[str(i-1)]["1"] * state1["transition"]["A_10"] * state1["emission"][word[i-2]]
        alpha[str(i)]["0"]= to0fromState0 + to0fromState1 
        # to state 1 
        to1fromState0 = alpha[str(i-1)]["0"] * state0["transition"]["A_01"] * state0["emission"][word[i-2]]
        to1fromState1 = alpha[str(i-1)]["1"] * state1["transition"]["A_11"] * state1["emission"][word[i-2]]
        alpha[str(i)]["1"]= to1fromState0 + to1fromState1 
        # print(alpha[str(i)]["0"])
        # print(alpha[str(i)]["1"])
    return alpha

def backwardProbability(word, pi_dict, state0, state1):
    # Accessible Data:
    #   DICT pi[pi1/pi0]
    #   DICT state0["transition"][STATECHANGE]
    #   DICT state0["emission"][LETTER]
    #   DICT state1["transition"][STATECHANGE]
    #   DICT state1["emission"][LETTER] 

    # LIST beta:[time][state]
    beta={}
    # initialize time subdictionaries
    for i in range(len(word)+1):
        beta[str(i+1)]={}
    beta[str(len(word)+1)]["0"]=1
    beta[str(len(word)+1)]["1"]=1
    for i in reversed(range(1,len(word)+1)):
        # to state 0 
        to0fromState0 = beta[str(i+1)]["0"] * state0["transition"]["A_00"] * state0["emission"][word[i-1]]
        to1fromState0 = beta[str(i+1)]["1"] * state0["transition"]["A_01"] * state0["emission"][word[i-1]]
        beta[str(i)]["0"]= to0fromState0 + to1fromState0 
        # to state 1 
        to0fromState1 = beta[str(i+1)]["0"] * state1["transition"]["A_10"] * state1["emission"][word[i-1]]
        to1fromState1 = beta[str(i+1)]["1"] * state1["transition"]["A_11"] * state1["emission"][word[i-1]]
        beta[str(i)]["1"]= to0fromState1 + to1fromState1 
        # print(beta[str(i)]["0"])
        # print(beta[str(i)]["1"])
    # print(beta)
    return beta
    
def plog(x):
    return (-1)*math.log2(x)

def wordRunner(word, pi_dict, state0, state1):   #total):
    # print(pi_dict)
    # print(state0)
    # print(state1)
    alpha=forwardProbability(word, pi_dict, state0, state1)
    beta=backwardProbability(word, pi_dict, state0, state1)
    # alpha=forwardProbability("babi#", {'0': 0.6814, '1': 0.3186}, {'transition': {'A_01': 0.5, 'A_00': 0.5}, 'emission': {'b': 0.1571, 'a': 0.1896, 'i': 0.3744, '#': 0.1680, 'd': 0.1109}}, {'transition': {'A_10': 0.5, 'A_11': 0.5}, 'emission': {'b': 0.2787, 'a': 0.0916, 'i': 0.2393, '#': 0.0633, 'd': 0.3272}})
    # beta=backwardProbability("babi#", {'0': 0.6814, '1': 0.3186}, {'transition': {'A_01': 0.5, 'A_00': 0.5}, 'emission': {'b': 0.1571, 'a': 0.1896, 'i': 0.3744, '#': 0.1680, 'd': 0.1109}}, {'transition': {'A_10': 0.5, 'A_11': 0.5}, 'emission': {'b': 0.2787, 'a': 0.0916, 'i': 0.2393, '#': 0.0633, 'd': 0.3272}})
    alphaStringProbability = alpha[str(len(alpha))]["0"] + alpha[str(len(alpha))]["1"]
    betaStringProbability = beta["1"]["0"] * pi_dict["0"] + beta["1"]["1"] * pi_dict["1"]
    return (alpha, beta, alphaStringProbability, betaStringProbability)

#### PART 2 ####

def initializeSoftCountsTable():
    wordList=[]
    getWords(wordList)
    # DICT softCounts[letter][fromState][toState]
    softCounts={}
    for word in wordList:
        for letter in word:
            if letter not in softCounts:
                softCounts[letter]={"0":{"0":0, "1":0}, "1":{"0":0, "1":0}} 
    return softCounts


def printWordSC(wordSC, word, alphaStringProbability, betaStringProbability):
    print("----------------------------------------")
    print("-  Soft Counts                         -")
    print("----------------------------------------")
    print("WORD: ", word[:-1])
    print("\nString probability from Alphas:", alphaStringProbability)
    print("String probability from Betas:", betaStringProbability)
    print()
    for letterIndex in range(len(wordSC)):
        sum = 0
        print("Letter:", word[letterIndex])
        for fromState in range(len(wordSC[letterIndex])):
            print("\tFrom state: ", fromState)
            for toState in range(len(wordSC[letterIndex][fromState])):
                tempSoftCount = wordSC[letterIndex][fromState][toState]
                print("\t  To state:    ", toState, "\t", tempSoftCount)
                sum += tempSoftCount
            print()
        print("\tSum for letter:", sum, "\n")


def expectationHelper(softCounts, initialSoftCounts, word, pi_dict, state0, state1, alpha, beta, alphaStringProbability, betaStringProbability):
    # Accessible Data:
    #   pi[pi1/pi0]
    #   state0["transition"][STATECHANGE]
    #   state0["emission"][LETTER]
    #   state1["transition"][STATECHANGE]
    #   state1["emission"][LETTER]  
    #   alpha[time][state]
    #   beta[time][state]
    #   alphaStringProbability 
    #   betaStringProbability
    #   softCounts[letter][fromState][toState]
    # wordSoftCounts[letterIndex][fromState][tostate]
    # eg: wordSoftCounts[0][1][0] 
    wordSoftCounts=[[[0 for i in range(2)] for i in range(2)] for i in range(len(word))]

    # other helper structs
    states={"0":state0, "1":state1}

    for letterIndex in range(len(word)):
        
        
        if (letterIndex==0):
            for fromState in states.keys():
                for toState in states.keys():
                    tempSoftCount=alpha[str(letterIndex+1)][fromState] * states[fromState]["transition"]["A_"+str(fromState)+str(toState)] * states[fromState]["emission"][word[letterIndex]] * beta[str(letterIndex+2)][toState] / alphaStringProbability
                    # print(tempSoftCount)
                    wordSoftCounts[letterIndex][int(fromState)][int(toState)]=tempSoftCount
                    softCounts[word[letterIndex]][fromState][toState]+=tempSoftCount
                    initialSoftCounts[word[letterIndex]][fromState][toState]+=tempSoftCount
        else:
            for fromState in states.keys():
                for toState in states.keys():
                    tempSoftCount=alpha[str(letterIndex+1)][fromState] * states[fromState]["transition"]["A_"+str(fromState)+str(toState)] * states[fromState]["emission"][word[letterIndex]] * beta[str(letterIndex+2)][toState] / alphaStringProbability
                    # print(tempSoftCount)
                    wordSoftCounts[letterIndex][int(fromState)][int(toState)]=tempSoftCount
                    softCounts[word[letterIndex]][fromState][toState]+=tempSoftCount
            
        
        # print("Sum for letter:", sum, "\n")
        # print("\tFrom state: 0")
    

def printSC(softCounts):
    print("Expected Counts Table (so far)")
    for letter in softCounts.keys():
        for fromState in softCounts[letter]:
            for toState in softCounts[letter][fromState]:
                print("\t", letter, "\t", fromState, "\t", toState, "\t", softCounts[letter][fromState][toState])

def printISC(softCounts):
    print("Initial Expected Counts Table (so far)")
    for letter in softCounts.keys():
        for fromState in softCounts[letter]:
            for toState in softCounts[letter][fromState]:
                print("\t", letter, "\t", fromState, "\t", toState, "\t", softCounts[letter][fromState][toState])

def expectation(file, pi_dict, state0, state1):
    # pi_dict, state0, state1=Initialization(0.7, 0.6)
    softCounts=initializeSoftCountsTable()
    initialSoftCounts=initializeSoftCountsTable()
    file = open(file, "r")
    # sum_plogs=0
    for word in file:
        word=word.lower().strip()
        if word[-1]!="#":
            word += "#"
        alpha, beta, alphaStringProbability, betaStringProbability= wordRunner(word, pi_dict, state0, state1) 
        expectationHelper(softCounts, initialSoftCounts, word, pi_dict, state0, state1, alpha, beta, alphaStringProbability, betaStringProbability)
        # sum_plogs+=wordPlog
        # printSC(softCounts)
    # print("\nString probability from Alphas:", alphaStringProbability)
    # print("String probability from Betas:", betaStringProbability, "\n\n")
    # printISC(initialSoftCounts)
    return (softCounts, initialSoftCounts)

#################################################
# PART 3: RECOMPUTING TRANSITION PROBABILITIES###
#################################################
def printNewTransition(newTransition, expectedNumItoJ, expectedTransitionFrom):
    print("----------------------------------------")
    print("- TRANSITION PROBABILITIES             -")
    print("----------------------------------------")
    for fromState in range(2):
        print("\tFrom State: ", fromState)
        for toState in range(2):
            transitionString="A_"+str(fromState)+str(toState)
            print("\t\tTo State: ", toState, "\tProb: ", newTransition[transitionString], "\t("+str(expectedNumItoJ[transitionString]), "over", str(expectedTransitionFrom[str(fromState)])+")")

def printNewEmission(expectedEmissionFrom):
    print("----------------------------------------")
    print("-  Emission Probabilities              -")
    print("----------------------------------------")
    print("\tState 0\t\t\t\t\t State 1")
    for key in expectedEmissionFrom["0"].keys():
        print(key, "\t", expectedEmissionFrom["0"][key],"\t", expectedEmissionFrom["1"][key])
    print("\n")

def printIterationSummary(softCounts):

    expectedEmissionFrom={"0":{}, "1":{}}
    
    # DICT softCounts[Letter][fromstate][tostate] 
    SCFrom0=0
    SCFrom1=0
    
    for letter in softCounts.keys():
        SCFrom0+= softCounts[letter]["0"]["0"] + softCounts[letter]["0"]["1"] 
        SCFrom1+= softCounts[letter]["1"]["0"] + softCounts[letter]["1"]["1"] 
    for letter in softCounts.keys():
        expectedEmissionFrom["0"][letter] = (softCounts[letter]["0"]["0"] + softCounts[letter]["0"]["1"])/SCFrom0
        expectedEmissionFrom["1"][letter] = (softCounts[letter]["1"]["0"] + softCounts[letter]["1"]["1"])/SCFrom1
    printIterationSummaryHelper(softCounts, expectedEmissionFrom)

def printIterationSummaryHelper(softCounts, expectedEmissionFrom):
    print("----------------------------------------")
    print("-  Start Iteration Summary             -")
    print("----------------------------------------")
    print("Emission")
    totalSC={}
    for fromState in expectedEmissionFrom:
        print("\tFROM State:", fromState)
        for letter in expectedEmissionFrom[fromState]:
            print("\t\tLetter:", letter)
            SCSum=0
            for toState in softCounts[letter][fromState]:
                print("\t\t  To State: ", toState, "\t", softCounts[letter][fromState][toState])
                SCSum+=softCounts[letter][fromState][toState]
            print("\t\t  Total soft count of", letter, "from state=", fromState, "equals", SCSum)
            print()
            totalSC[letter]=SCSum
        print("\tNormalize Soft Counts to get emission probabilities:")
        TotalSCSUM=0
        for k,v in totalSC.items():
            TotalSCSUM+=v
        for k,v in totalSC.items():
            print("\tLetter:", k, "Probability:", v/TotalSCSUM, "("+str(v), "over", str(TotalSCSUM)+")")
        print()
    print("----------------------------------------")
    print("-  End of Iteration Summary            -")
    print("----------------------------------------")

def printLogRatios(logRatios):
    positive=[]
    negative=[]
    for (k,v) in logRatios.items():
        if (v < 0):
            negative.append((k,v))
        else:
            positive.append((k,v))
    positive.sort(key=lambda tup : tup[1], reverse=True)
    negative.sort(key=lambda tup : tup[1], reverse=False)
    print("Log ratios of emissions from the 2 States")
    print("\tState 0\t\t\t\t\t State 1")
    for a, b in itertools.zip_longest(positive, negative, fillvalue=(' ','                  ')):
        print(a[0], a[1],"\t", b[0],  b[1], sep='\t')
        # print(a[0], a[1], b[0], b[1])



def newTransitionProbabilities(softCounts):
    newTransition={"A_00":0,"A_01":0,"A_10":0,"A_11":0}
    expectedNumItoJ={"A_00":0,"A_01":0,"A_10":0,"A_11":0}
    expectedTransitionFrom={}
    for letter in softCounts.keys():
        expectedNumItoJ["A_00"]+=softCounts[letter]["0"]["0"]
        expectedNumItoJ["A_01"]+=softCounts[letter]["0"]["1"]
        expectedNumItoJ["A_10"]+=softCounts[letter]["1"]["0"]
        expectedNumItoJ["A_11"]+=softCounts[letter]["1"]["1"]
    expectedTransitionFrom["0"]=expectedNumItoJ["A_00"]+expectedNumItoJ["A_01"]
    expectedTransitionFrom["1"]=expectedNumItoJ["A_10"]+expectedNumItoJ["A_11"]
    
    newTransition["A_00"]+=expectedNumItoJ["A_00"]/expectedTransitionFrom["0"]
    newTransition["A_01"]+=expectedNumItoJ["A_01"]/expectedTransitionFrom["0"]
    newTransition["A_10"]+=expectedNumItoJ["A_10"]/expectedTransitionFrom["1"]
    newTransition["A_11"]+=expectedNumItoJ["A_11"]/expectedTransitionFrom["1"]
    return (newTransition, expectedNumItoJ, expectedTransitionFrom)
        
def newEmissionProbabilities(softCounts):

    expectedEmissionFrom={"0":{}, "1":{}}
    
    # DICT softCounts[Letter][fromstate][tostate] 
    SCFrom0=0
    SCFrom1=0
    
    for letter in softCounts.keys():
        SCFrom0+= softCounts[letter]["0"]["0"] + softCounts[letter]["0"]["1"] 
        SCFrom1+= softCounts[letter]["1"]["0"] + softCounts[letter]["1"]["1"] 
    for letter in softCounts.keys():
        expectedEmissionFrom["0"][letter] = (softCounts[letter]["0"]["0"] + softCounts[letter]["0"]["1"])/SCFrom0
        expectedEmissionFrom["1"][letter] = (softCounts[letter]["1"]["0"] + softCounts[letter]["1"]["1"])/SCFrom1
    # printIterationSummaryHelper(softCounts, expectedEmissionFrom)
    
    return expectedEmissionFrom




def newPiProbabilities(initialSoftCounts):
    wordList=[]
    getWords(wordList)
    Z=(len(wordList))
    pi0=0
    pi1=0
    for letter in initialSoftCounts.keys():
        pi0 += initialSoftCounts[letter]["0"]["0"] + initialSoftCounts[letter]["0"]["1"]
        pi1 += initialSoftCounts[letter]["1"]["0"] + initialSoftCounts[letter]["1"]["1"]
    pi0/=Z
    pi1/=Z


    return(pi0, pi1)

def maximisation(initialSoftCounts, softCounts):
    pi0, pi1=newPiProbabilities(initialSoftCounts)
    expectedEmissionFrom=newEmissionProbabilities(softCounts)
    newTransition, expectedNumItoJ, expectedTransitionFrom=newTransitionProbabilities(softCounts)
    return (pi0, pi1, expectedEmissionFrom, newTransition, expectedNumItoJ, expectedTransitionFrom)

def Output(pi0, pi1, expectedEmissionFrom, softCounts, newTransition, expectedNumItoJ, expectedTransitionFrom, iteration):
    print("----------------------------------------")
    print("-  Final Values                        -")
    print("----------------------------------------")
    print()
    print("----------------------------------------")
    print("- Pi:                                  -")
    print("----------------------------------------")
    print("State\t0\t", pi0)
    print("State\t1\t", pi1)
    printNewEmission(expectedEmissionFrom)

    #LogRatios of Emissions
    logRatios={}
    for letter in softCounts.keys():
        logRatios[letter]=math.log2(expectedEmissionFrom["0"][letter]/expectedEmissionFrom["1"][letter])
    
    # print(logRatios)
    printLogRatios(logRatios)
    print()
    printNewTransition(newTransition, expectedNumItoJ, expectedTransitionFrom)

### PART 4 ###

def wordRunnerPlog(word, pi_dict, state0, state1, total):
    alpha=forwardProbability(word, pi_dict, state0, state1)
    beta=backwardProbability(word, pi_dict, state0, state1)
    alphaStringProbability = alpha[str(len(alpha))]["0"] + alpha[str(len(alpha))]["1"]
    betaStringProbability = beta["1"]["0"] * pi_dict["0"] + beta["1"]["1"] * pi_dict["1"]
    # print(alphaStringProbability)
    # print(betaStringProbability)
    
    
    # print("String probability from the Alphas: ", alphaStringProbability)
    # print("String probability from the Betas: ", betaStringProbability)
    return plog(alphaStringProbability)

def fileRunnerPlog(file, pi_dict, state0, state1):
    file = open(file, "r")
    sum_plogs=0
    for word in file:
        word = word.lower().strip()
        wordPlog=wordRunnerPlog(word, pi_dict, state0, state1, sum_plogs)
        sum_plogs+=wordPlog
    print("Sum of the Plogs: ", sum_plogs)
    return sum_plogs

def HMM(epsilon, targetFile):
    pi_dict, state0, state1=Initialization(0.8, 0.8)
    # pi_dict={'0': 0.8740900959744541, '1': 0.12590990402554605}
    # state0={'transition': {'A_01': 0.7928939420106325, 'A_00': 0.20710605798936751}, 'emission': {'a': 0.02564956663346186, '#': 0.10890583537472398, 'b': 0.027240349494328762, 'l': 0.052937351175842556, 'e': 0.027877902904551288, 'o': 0.014509481346037446, 'u': 0.005908087819760299, 't': 0.0922208271983293, 'v': 0.015016667595077917, 'c': 0.04794491206704952, 'p': 0.03794498596614442, 'r': 0.09799484232672932, 's': 0.08579291112182856, 'y': 0.037843630676963835, 'd': 0.03606879103087849, 'm': 0.0407419280539188, 'i': 0.005876640618888316, 'f': 0.028259530842529412, 'n': 0.08991757216656412, 'g': 0.03209665152188244, 'h': 0.034160964674856, 'w': 0.035252487535335233, 'z': 0.0015291584627890565, "'": 0.00016092449417800297, 'k': 0.01162026963672614, 'x': 0.0015870588237596414, 'j': 0.002879434130145369, '.': 0.00014206487711534814, 'q': 0.0019191714296046382}}
    # state1={'transition': {'A_10': 0.7945360139278125, 'A_11': 0.2054639860721876}, 'emission': {'a': 0.09032606962460682, '#': 0.21114847573525, 'b': 0.002234121598882078, 'l': 0.031000816502649204, 'e': 0.1710747769746217, 'o': 0.09826240805407359, 'u': 0.04695373533654175, 't': 0.027599305289288733, 'v': 4.0942637323272406e-05, 'c': 0.003315037660273643, 'p': 0.0017814750725310326, 'r': 0.013175173644402861, 's': 0.009678745245310804, 'y': 0.0009217063043243363, 'd': 0.020317153669177024, 'm': 0.0018679051569185884, 'i': 0.07774115237380767, 'f': 0.0021760643080687312, 'n': 0.004592960143188069, 'g': 0.005707561402018426, 'h': 0.036321466200213405, 'w': 0.0003091025879952335, 'z': 7.271496618979314e-05, "'": 0.011052189508673945, 'k': 0.01400970522693546, 'x': 0.002577812091585368, 'j': 3.938042016561454e-06, '.': 0.0004986844944761919, 'q': 3.076685169981281e-06}}

    improvement = 1.0
    initial_sum_plogs=fileRunnerPlog(targetFile, pi_dict, state0, state1)
    iteration=0
    print("Iteration number: ", iteration, "  Total Plog: ", initial_sum_plogs, "  Transitions: 0 to 1 (", state0["transition"]["A_01"], ")  1 to 0 (", state1["transition"]["A_10"], sep='')

    while improvement > epsilon:
    # for i in range(10):
        iteration+=1
        softCounts, initialSoftCounts=expectation(targetFile, pi_dict, state0, state1)
        pi0, pi1, expectedEmissionFrom, newTransition, expectedNumItoJ, expectedTransitionFrom=maximisation(initialSoftCounts, softCounts)
        pi_dict["0"]=pi0
        pi_dict["1"]=pi1
        state0["transition"]["A_00"]=newTransition["A_00"]
        state0["transition"]["A_01"]=newTransition["A_01"]
        state1["transition"]["A_10"]=newTransition["A_10"]
        state1["transition"]["A_11"]=newTransition["A_11"]
        state0["emission"]=expectedEmissionFrom["0"]
        state1["emission"]=expectedEmissionFrom["1"]

        current_sum_plogs=fileRunnerPlog(targetFile, pi_dict, state0, state1)
        print("Iteration number: ", iteration, "  Total Plog: ", current_sum_plogs, "  Transitions: 0 to 1 (", state0["transition"]["A_01"], ")  1 to 0 (", state1["transition"]["A_10"],")", sep='')
        improvement=initial_sum_plogs-current_sum_plogs
        initial_sum_plogs=current_sum_plogs
    Output(pi0, pi1, expectedEmissionFrom, softCounts, newTransition, expectedNumItoJ, expectedTransitionFrom, iteration)
    print("\n\n\n")
    # print(oldpi_dict, oldstate_0, oldstate_1, sep='\n')
        # initial_sum_plogs=current_sum_plogs
    
        

        

        
    # printSC(softCounts)
    # printIterationSummary(softCounts)
    # newPiProbabilities(initialSoftCounts)
    # newEmissionProbabilities(softCounts)
    # newTransitionProbabilities(softCounts)
    # Output(pi0, pi1, expectedEmissionFrom, softCounts, newTransition, expectedNumItoJ, expectedTransitionFrom)

    


if __name__ == '__main__':
    # random.seed(0)
    parser=argparse.ArgumentParser()
    parser.add_argument("--VerboseFlag", dest='VerboseFlag', default=True, action='store_true', help="Verbose Flag")
    args = parser.parse_args()
    for i in range(10):
        HMM(0.1, "./english1000.txt")

     
    


