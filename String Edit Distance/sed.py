import argparse
import copy
import sys

vowels=['a', 'e', 'i', 'o', 'u']

def cost(l1, l2):
    if l1==l2:
        # identity
        return 0

    if l1!="*":
        l1type=('v' if l1 in vowels else 'c')
    else:
        l1type=l1
    if l2!="*":
        l2type=('v' if l2 in vowels else 'c')
    else:
        l2type=l2

    if l1type==l2type:
        if l1type=='v':
            # vowel-vowel
            return 0.5
        elif l1type=='c':
            # consonant-consonant
            return 0.6
    else: #not same type
        if l1type=='*':
            # insertion/deletion
            return 2
        elif l2type=='*':
            return 2
        else: 
            #consonant vowel
            return 3

def printTable(table, w1, w2):
    xlabel=' #'+w1
    ylabel='#'+w2
    for letter in xlabel:
        print('------', end='')
    print()
    for letter in xlabel:
        print(letter.center(6), end='')
    print()
    for letter in xlabel:
        print('------', end='')
    print()
    for rowindex in range(len(table)):
        print(ylabel[rowindex].center(6), end='')
        for value in table[rowindex]:
            print(str(value).center(6), end="")
        print()
    for letter in xlabel:
        print('------', end='')
    print("\n\n\n")

def initTable(w1, w2):
    # table[word2][word1]
    table=[[None for x in range(len(w1)+1)] for x in range(len(w2)+1)]
    table[0][0]=0
    return(table)

def recursiveComplete(w1, w2):
    xlabel='#'+w1
    ylabel='#'+w2
    table=initTable(w1,w2)
    # table[J / word2] [I / word1]
    # paths[j][i] = list of tuples
    paths={"0_0":[(0,0)]}
    letters={"0_0":["#:#"]}
    for i in range(1, len(w1)+1):
        table[0][i]=2*i
        paths["0_"+str(i)]=paths["0_"+str(i-1)] + [(0,i)]
        letters["0_"+str(i)]=letters["0_"+str(i-1)] + ["*:"+xlabel[i]]
        
    for j in range(1, len(w2)+1):
        table[j][0]=2*j
        paths[str(j)+'_0']=paths[str(j-1)+'_0'] + [(j,0)]
        letters[str(j)+'_0']=letters[str(j-1)+'_0'] + [ylabel[j]+":*"]
    for j in range(1, len(w2)+1):
        for i in range(1, len(w1)+1):
            temp1=round(table[j-1][i] + 2,1)
            temp2=round(table[j-1][i-1] + cost(w1[i-1], w2[j-1]),1)
            temp3=round(table[j][i-1] + 2,1)
            value = min(temp1, temp2, temp3)
            table[j][i]=value
            if value==temp1:
                paths[str(j)+'_'+str(i)]=paths[str(j-1)+'_'+str(i)] + [(j,i)]
                letters[str(j)+'_'+str(i)]=letters[str(j-1)+'_'+str(i)] + [ylabel[j]+":*"]
            elif value==temp2:
                paths[str(j)+'_'+str(i)]=paths[str(j-1)+'_'+str(i-1)] + [(j,i)]
                letters[str(j)+'_'+str(i)]=letters[str(j-1)+'_'+str(i-1)] + [ylabel[j]+":"+xlabel[i]]
            elif value==temp3:
                paths[str(j)+'_'+str(i)]=paths[str(j)+'_'+str(i-1)] + [(j,i)]
                letters[str(j)+'_'+str(i)]=letters[str(j)+'_'+str(i-1)] + ["*:"+xlabel[i]]
    return(table, paths, letters)

def drawtables(table, paths, letters, w1, w2):
    lastIndex=str(len(w2)) + '_' + str(len(w1))       
    tblcpy2=copy.deepcopy(table)
    lettersCounter=0
    for j in range(0, len(w2)+1):
        for i in range(0, len(w1)+1):
            if (j, i) not in paths[lastIndex]:
                tblcpy2[j][i]=''
            else:
                tblcpy2[j][i]=letters[lastIndex][lettersCounter]
                lettersCounter+=1
    tblcpy=copy.deepcopy(table)
    for j in range(0, len(w2)+1):
        for i in range(0, len(w1)+1):
            if (j, i) not in paths[lastIndex]:
                tblcpy[j][i]=''
    printTable(tblcpy2, w1, w2) 
    printTable(tblcpy, w1, w2)  
    original_stdout = sys.stdout
    with open('sed_'+w1+'_'+w2+'.txt', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.
        printTable(tblcpy2, w1, w2) 
        printTable(tblcpy, w1, w2)  
        sys.stdout = original_stdout # Reset the standard output to its original value
                
    



if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("word1", help="First Word")
    parser.add_argument("word2", help="Second Word")
    # parser.add_argument("--VerboseFlag", dest='VerboseFlag', default=True, action='store_true', help="Verbose Flag")
    args = parser.parse_args()
    table, paths, letters = recursiveComplete(args.word1, args.word2)
    # print(letters[str(len(args.word2))+'_'+str(len(args.word1))])
    drawtables(table, paths, letters, args.word1, args.word2)