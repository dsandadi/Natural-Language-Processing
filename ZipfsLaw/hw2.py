#!/usr/bin/python3

# -*- coding: utf-8 -*-
"""
CSCI680(Intro To NLP)
Name :Dinesh Sandadi
Assignment : 2
Due Date:3/2/2018
"""
import re
from collections import defaultdict
import math
import sys
'''
Method: printTable
Purpose : prints the table showing letters and their frequency
Arguments : dictionary that contains frequency of each character.
Return : Nothing.
'''
def printTable(table):
    sortedKeySet =sorted(table,key = table.__getitem__,reverse = True)
    rowCount = 5 ## Number of rows
    rows = []## Extra space to store the rows.
    runner = 0 ## pointer that points to the row.
    ## Goes throught the dictionay and add to the 
    for k in sortedKeySet:
        if(len(rows) - 1 < runner):
            rows.append('{:>3}'.format(k) +'{:>6}'.format(table[k]))
        else:
            rows[runner] += '{:>3}'.format(k) +'{:>6}'.format(table[k])
        runner = (runner+1)%rowCount
    for row in rows:
        print(row)
'''
Method : printLetterCountTable
Arguments : dictionary that contains wod lengths and their frequency.
Purpose :prints the table.
Returns : Nothing.
'''        
def printLetterCountTable(table):
    
    rows = [] # Extra space to hold the rows.
    runner = 0## pointer to the table.
    rowCount = 5 ## count the number of rows.
    
    for k in table:
        if(runner == 0):
            if(len(rows) - 1 < runner):
                rows.append('{:>5}'.format('len')+'{:>7}'.format('count')) 
            else:
                rows[0] +='{:>5}'.format('len')+'{:>7}'.format('count')
            runner += 1
        if(len(rows) - 1 < runner):
            rows.append('{:>5}'.format(k)+'{:>7}'.format(table[k]))
        else:
            rows[runner] += '{:>5}'.format(k)+'{:>7}'.format(table[k])
            
        runner = (runner+1)%rowCount;
    for row in rows:
        print(row)
'''
Method : printGrid
Argument : table, dictionary of word and their length counts.
Returns : Nothing.
'''
def printGrid(table):
    print('{:>5}'.format('rank'), '{:>7}'.format('length'),
          '{:>5}'.format('freq'),'{:>9}'.format('len*fre'),'{:>9}'.format('rank*fre'), '{:>9}'.format('lgf/lgr'))
    rank = 1;## rank is incremented.
    sortedList = sorted(table,key = table.__getitem__, reverse = True)
    for t in sortedList:
        
        print('{:>5}'.format(rank), '{:>7}'.format(t),
          '{:>5}'.format(table[t]),'{:>9}'.format(t*table[t]),
          '{:>9}'.format(rank*table[t]),end = '')
        if(rank != 1):  
            print('{:>9}'.format(round(math.log(table[t])/math.log(rank),2)),end = '')
        print()
        rank += 1
'''
Method: readFile
Argument : fileName
Purpose : reads the file with the given filename
Return value : text and lineCount.
'''
def readFile(fileName):
    fileHandle = open(fileName, encoding = "ISO-8859-1")
    text =""
    lineCount = 0## lineCount counts the number of lines.
    for line in fileHandle:
        text +=line
        lineCount += 1
    print(len(text))
    text = text.replace('--','  ')## replaces double hypens.
    print(len(text))
    text = re.sub("[^a-zA-Z'-]",' ',text) ## replaces all characters excepts alphabets.
    #print(text)
    text = text.lower()
    ## text is loaded up.
    return text,lineCount
'''
Method : findFrequency
Argument : text
Returns : dictionary that has frequency of each letter and character count.
Purpose :Calculates the frequency of each character.
'''
def findFrequency(text):
    frequencyDict  = defaultdict(int)
    charCount = 0## counts the number of characters
    for c in text:
        if(c.isalpha()): ## if character is alphabet.
            frequencyDict[c] += 1;
            charCount += 1
    return frequencyDict,charCount
'''
Method : findWordFreq
Argument : text
Returns : returns the dictionary that has length of words and their counts.
'''
def findWordFreq(text):
    countDict = defaultdict(int)## using default dict.
    for word in text.split():
        countDict[len(word)] += 1
    return countDict
'''
Boiler plate code or driver method.
'''
if(__name__ == "__main__" ):
    if(sys.argc < 2 or sys.argc > 2):
        print('Please enter two arguments')
        exit()
    text,lineCount = readFile(sys.argv[1])
    freqDict, charCount = findFrequency(text)
    printTable(freqDict)
    letDict = findWordFreq(text)
    print('=============================================')
    printLetterCountTable(letDict)
    print('=============================================')
    printGrid(letDict)
    print('=============================================')
    print('Total counted characters', charCount)
    print('Total records read', lineCount)
    print('Total Characters', len(text))
    