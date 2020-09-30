import random
import argparse
import math

# getWords
# OUTPUT: sorted List of words from targetfile.
def getWords(file):
    file = open(file, "r")
    wordList=[]
    for word in file:
        word = word.lower().strip()
        wordList.append(word)
    wordList.sort()
    return wordList

def reverseWL(wordList):
    reversedList=[]
    for word in wordList:
        reversedList.append(word[::-1])
    reversedList.sort()
    return reversedList

def getNestedDictionary(wordList):
    nestedDict={}
    for word in wordList:
        pointer=nestedDict
        for letter in word:
            pointer=pointer.setdefault(letter, {})
        pointer["#"]="#"
        # print(nestedDict)
    return nestedDict

def wordSuccessorSplit(nestedDict, word, k):
    # CASE 1: Word Shorter than min length
    if len(word)<k:
        return [word]
    # CASE 2: Word Longer than min length
    output=[]
    tempSplit=word[:k]
    letterPointer=k
    tempDict=nestedDict
    for i in range(letterPointer):
        tempDict=tempDict[word[i]]
    while tempDict!="#" and (letterPointer < len(word)) :
        if len(tempDict) == 1:
            tempSplit+=word[letterPointer]
            tempDict=tempDict[word[letterPointer]]
            letterPointer+=1
        else:
            output.append(tempSplit)
            tempSplit=word[letterPointer]
            tempDict=tempDict[word[letterPointer]]
            letterPointer+=1
    output.append(tempSplit)
    return output

def wordSuccessorSplitWordList(wordList, nestedDict, k):
    listOfSplits=[]
    maximum=0
    for word in wordList:
        split=wordSuccessorSplit(nestedDict, word, k)
        listOfSplits.append(split)
        if len(split)>maximum:
            maximum=len(split)
    for split in listOfSplits:
        while len(split)<maximum:
            split.append('')
    return listOfSplits


def wordPredecessorSplit(reversedNestedDict, word, k):
    # CASE 1: Word Shorter than min length
    if len(word)<k:
        return [word]
    # CASE 2: Word Longer than min length
    output=[]
    tempSplit=word[:k]
    letterPointer=k
    tempDict=reversedNestedDict
    for i in range(letterPointer):
        tempDict=tempDict[word[i]]
    while tempDict!="#" and (letterPointer < len(word)) :
        if len(tempDict) == 1:
            tempSplit+=word[letterPointer]
            tempDict=tempDict[word[letterPointer]]
            letterPointer+=1
        else:
            output.insert(0, tempSplit[::-1])
            tempSplit=word[letterPointer]
            tempDict=tempDict[word[letterPointer]]
            letterPointer+=1
    output.insert(0, tempSplit[::-1])
    return output

def wordPredecessorSplitWordList(wordList, reversedNestedDict, k):
    listOfSplits=[]
    maximum=0
    for word in wordList:
        split=wordPredecessorSplit(reversedNestedDict, word, k)
        listOfSplits.append(split)
        if len(split)>maximum:
            maximum=len(split)
    for split in listOfSplits:
        while len(split)<maximum:
            split.insert(0, '')
    return listOfSplits


def printListOfSplits(listOfSplits):
    bracketlength=[0 for x in range(100)]
    for split in listOfSplits:
        for index in range(len(split)):
            if len(split[index]) > bracketlength[index]:
                bracketlength[index]= len(split[index])
    # bracketlength = max(len(segment) for split in listOfSplits for segment in split)
    for split in listOfSplits:
        print(''.join(split[index].ljust(bracketlength[index] + 2) for index in range(len(split))))
        # for segment in split:
        #     print(segment, end='\t\t\t')
    print()

def SFParser(targetfile):
    wordList=getWords(targetfile) 
    # wordList=getWords("small_wordlist.txt") 
    # REVERSED
    if args.Predecessor:
        reversedWordList=reverseWL(wordList)
        # print(reversedWordList)
        reversedNestedDict=getNestedDictionary(reversedWordList)
        listOfPredecessorSplits=wordPredecessorSplitWordList(reversedWordList, reversedNestedDict, 4)
        # print(listOfPredecessorSplits)
        printListOfSplits(listOfPredecessorSplits)
    else:
        nestedDict=getNestedDictionary(wordList)
        listOfSuccSplits=wordSuccessorSplitWordList(wordList, nestedDict, 4)
        printListOfSplits(listOfSuccSplits)

#######################
###     PART 2     ####
#######################

def lexSplitWordList(wordList, nestedDict, k):
    listOfSplits=[]
    maximum=0
    for word in wordList:
        split=wordSuccessorSplit(nestedDict, word, k)
        listOfSplits.append(split)
        if len(split)>maximum:
            maximum=len(split)
    return listOfSplits

def lexCreate(lexSplits):
    # key is stem, value is list of suffixes
    Lexicon={}
    for split in lexSplits:
        for i in range(1,len(split)):
            prefix= ''.join(split[:i])
            suffix= ''.join(split[i:])
            if prefix in Lexicon:
                Lexicon[prefix].append(suffix)
            else:
                Lexicon[prefix]=[suffix]
        Lexicon[''.join(split)]=["NULL"]
    for key in Lexicon.keys():
        Lexicon[key].sort()
        Lexicon[key]='='.join(Lexicon[key])
    # print(Lexicon)
    return Lexicon

def signaturesCreate(Lexicon):
    Signatures={}
    for k,v in Lexicon.items():
        if v not in Signatures:
            Signatures[v]=[k]
        else:
            Signatures[v].append(k)
    printSig(Signatures)
    return(Signatures)

def printSig(Signatures):
    sigList=list(Signatures.items())
    sigList.sort(key=lambda tup:len(tup[1]), reverse=True)


    bracketlength = max(len(stem) for signature in sigList for stem in signature[1])  
    print("------------------------")     
    for signature in sigList:
        print(signature[0], "\n   ", len(signature[1]), "STEMS\n")
        for i in range(len(signature[1])//6+1):
            for j in range(i*5, (i+1)*5):
                try:
                    print(signature[1][j].ljust(bracketlength+1), end=' ')
                except:
                    pass
            print()
        print("------------------------")
    

if __name__ == '__main__':
    random.seed(0)
    parser=argparse.ArgumentParser()
    parser.add_argument("targetfile", help="Target Filepath")
    parser.add_argument("--Predecessor", dest='Predecessor', default=False, action='store_true', help="Verbose Flag")
    parser.add_argument("--Signatures", dest='Signatures', default=False, action='store_true', help="Verbose Flag")
    args = parser.parse_args()
    # PART 1
    if not args.Signatures:
        SFParser(args.targetfile)

    # PART 2
    else:
        wordList=getWords(args.targetfile)
        # wordList=getWords("browncorpus_wordlist.txt") 
        nestedDict=getNestedDictionary(wordList)
        lexSplits=lexSplitWordList(wordList, nestedDict, 4)
        Lexicon=lexCreate(lexSplits)
        Signatures=signaturesCreate(Lexicon)
    
    
