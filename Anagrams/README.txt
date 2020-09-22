CONTENTS

README.txt             - Readme file for explanation
anagrams.py             - Run this
                        - Usage: python3 anagrams.py [TARGET FILENAME]
                          Example: python3 anagrams.py english-words-235k.txt 
english-words-small.txt - Small self-created sample to run anagrams.py on for quick testing
english-words-235k.txt  - Sample from canvas to run anagrams.py on
235kOutput.txt          - Output from running anagrams.py on english-words-235k.txt
smallOutput.txt         - Output from running anagrams.py on english-words-small.txt


I have created “anagrams.py” that reads in a list of words from files with .txt 
extension. It takes a minimum word length of 8 and lowercases every word. It then 
finds sets of anagrams. The anagrams are then organized by size, then length, then 
alphabetized by first word. 

This output is printed out with "Anagrams of size {x}" and "Anagrams of length {y}"
at the beginning of every section. 

The way I have done it is utilize a dictionary to find all the sets of anagrams. I then 
create another dictionary to hold anagrams of the same size together, and then create
sub-dictionaries to replace the value in the key-value pairs, with the inner key being the
anagram length. 

So we end up with a nested dictionary (anagramDict_size), where we can access sets of anagrams
by using the syntax "anagramDict_size[SIZE][LENGTH]". I then convert it to nested tuple-arrays, 
and use that to sort (since we are unable to sort dictionaries) to the desired sorting before 
using my output function to create the printed output. 

Then to create the output report table, I convert the sorted nested tuple-arrays back into nested 
dictionaries. I then access the nested dictionary and replace every nested value with the count 
of anagrams. Then I create a dataframe, to store the nested dictionaries and print it out. 