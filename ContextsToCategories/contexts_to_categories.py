import argparse
import re 

def findcontexts(string, contextDict):
    stringList=string.split()
    for i in range(0, len(stringList)-2):
        context=stringList[i]+'__'+stringList[i+2]
        if context in contextDict:
            contextDict[context].append(stringList[i+1])
        else:
            contextDict[context]=[stringList[i+1]]

def dust(contextDict):
    mincount=3 #change to 50 for brown corpus
    contextDictCopy=contextDict.copy()
    for key in contextDictCopy.keys():
        if len(contextDict[key]) < mincount:
            del(contextDict[key])

def subDictionary(contextDict):
    for key in contextDict.keys():
        tempdict={}
        for innerword in contextDict[key]:
            if innerword in tempdict:
                tempdict[innerword] += 1
            else:
                tempdict[innerword] = 1
        contextDict[key]=tempdict

# Sort contexts by the number of different words that appear in them. 
# Print a list of contexts, one per line, with the number of different 
# words that appear in them. Call this file “context list.txt”.
def output1(contextDict):
    dictcopy=contextDict.copy()
    for key in contextDict.keys():
        dictcopy[key]=list(dictcopy[key])
    with open('context_list.txt', 'w') as f:
        for (k, v) in sorted(list(dictcopy.items()), key=lambda tup : len(tup[1])):
            print(k+":", len(v), file=f)
            
    
def output2(contextDict):
    dictcopy=contextDict.copy()
    for key in contextDict.keys():
        dictcopy[key]=sorted(list(dictcopy[key].items()), key=lambda tup: tup[1], reverse=True)
    dictcopylist=sorted(list(dictcopy.items()), key=lambda tup : len(tup[1]), reverse=True)
    # print(dictcopylist)

    with open('words_in_contexts.txt', 'w') as f:
        for tup in dictcopylist:
            print('\n'+tup[0]+ ':', file=f)
            # print(str(tup[1])[1:-1])
            for i in range(len(tup[1])//5+1):
                print (str(tup[1][i*5:(i+1)*5])[1:-1], file=f)




def main(targetfile):
    contextDict={}
    file = open(targetfile, "r")
    for x in file:
        # ensuring space on either side of punctuation with regex 
        x = re.sub('([.,;:!?()])', r' \1 ', x)
        x = re.sub('\s{2,}', ' ', x)
        x=x.lower()
        findcontexts(x, contextDict)
    dust(contextDict)
    subDictionary(contextDict)
    # print(contextDict)
    output1(contextDict)
    output2(contextDict)



if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("targetfile", help="Target Filepath")
    args = parser.parse_args()
    main(args.targetfile)