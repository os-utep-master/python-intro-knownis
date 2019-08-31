#!/usrs/bin/env python3

import sys  
import re
import os 

if length(sys.argv) is not 3:
    print("Wrong format. usage = wordCount.py <input> <output>")
    exit()

fileName = sys.argv[1]

if not os.path.exists(fileName):
    print ("file %s does not exists!" % fileName)
    exit()

wordList = {}

with open(fileName, "r") as inputFile:
    for line in inputFile:
        splicedList = re.split(r'\W+',line)
        for word in splicedList:
            word = word.lower()
            if word not in wordList.keys():
                wordList[word] = 1
            else:
                wordList[word] += 1
                
del wordList[""] 
inputFile.close()
#write the file
with open(sys.argv[2],'w') as outputFile:
    for x, y in sorted(wordList.items()):
        outputFile.write( "%s %d\n" % (x, y))
outputFile.close()
print("file written")
