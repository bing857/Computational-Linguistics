import argparse
import pandas as pd

def dictPrintTest(dictionary):
    for x in dictionary:
        print (x, ":")
        for y in dictionary[x]:
            print (y)

def intendedOutput(dictionaryItems):
    for tuple in dictionaryItems:
        print("Anagrams of SIZE " + str(tuple[0]))
        for innerTuple in tuple[1]:
            print("Anagrams of LENGTH " + str(innerTuple[0]))
            for sets in innerTuple[1]:
                print(' '.join(sets))
        print('\n')



def main(targetfile):
    file = open(targetfile, "r")
    anagramDict={}
    anagramDict_size={}
    for x in file:
        #only words len 8 or greater
        if (len(x)>=8):
            # Lowercase each word & remove newline
            x=x.lower().strip()
            # Alphabetizing each word 
            x_list=list(x)
            x_list.sort()
            x_alphabetized=''.join(x_list)
            # Add each word to dict with alphabetized word as key
            if (x_alphabetized in anagramDict):
                anagramDict[x_alphabetized].append(x)
            else:
                anagramDict[x_alphabetized]=[x]
    tempdict=anagramDict.copy()
    # remove single word entries in dict
    for key in tempdict:
        if (len(anagramDict[key]) < 2):
            del anagramDict[key]

    
    # Now, we are left with a dictionary of Anagrams. Lets group them 
    # by size into a new dictionary
    # print(anagramDict)
    for key in anagramDict.keys():
        size = len(anagramDict[key])
        if (size in anagramDict_size):
            (anagramDict_size[size]).append(anagramDict[key])
        else:
            anagramDict_size[size]=[anagramDict[key]]

    for key in anagramDict_size.keys():
        lengthDict={}
        for set in anagramDict_size[key]:
            wordlength =  len(set[0])
            if (wordlength in lengthDict):
                lengthDict[wordlength].append(set)
            else:
                lengthDict[wordlength]=[set]
        anagramDict_size[key]=lengthDict

    
    # We want sorted by size(ascending), length(ascending) then alphabet (ascending)
    # Do it in reverse order, since python sort implementation is stable


    # for key in anagramDict_size.keys():
    #     anagramDict_size[key].sort(key= lambda set:set[0])  #sort by alphabet
    #     anagramDict_size[key].sort(key= lambda set:len(set[0]))  #sort by length

    for key in anagramDict_size.keys():
        for innerkey in anagramDict_size[key]:
            anagramDict_size[key][innerkey].sort(key = lambda set:set[0]) #sort by alphabet
        sortedValue = sorted(anagramDict_size[key].items(), key= lambda set:set[0]) #sort by length
        anagramDict_size[key]=sortedValue

    # print(anagramDict_size)

    sortedAnagrams=sorted(anagramDict_size.items())
    
    
    #printed out 
    intendedOutput(sortedAnagrams)
    print("\n\n\n")
    print("OUTPUT REPORT: \n")

    #table
    tempDict=dict(sortedAnagrams)
    tableDict= {k:dict(v) for k, v in tempDict.items()}
    for size in list(tableDict.keys()):
        for length in list(tableDict[size].keys()):
            numEntries = len(tableDict[size][length])
            tableDict[size][length]=numEntries

    # print TABLEOUTPUT REPORT
    pd.set_option('precision', 0)
    dataframe = pd.DataFrame(tableDict).T
    dataframe.fillna(0, inplace=True)
    print(dataframe)




    

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("targetfile", help="Target Filepath")
    args = parser.parse_args()
    main(args.targetfile)
    # main()