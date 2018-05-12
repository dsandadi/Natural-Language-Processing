# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 19:10:41 2018
Assignment 3
@author: DINESH
"""
import pickle
import re
import operator
import string

import time;

fileName = 'G:\\NIU_Masters\\Semester4\\Natural Language Processing\\Assignments\\Kernighans_Algorithm_SpellChecker\\ap88.txt';
fileHandler = open(fileName)
count = 0
data = ""
unigramData = {}
bigramData = {}
eng_vocab = {}
wordCount = 0

class dataStorage:
    def __init__(self):
        self.unigramData = unigramData
        self.bigramData = bigramData
        self.eng_vocab = eng_vocab
        
def populateDict(words):
    global unigramData
    global bigramData
    for word in words:
        prev = ''
        for letter in word:
            if letter in unigramData:
                unigramData[letter] += 1
            else:
                unigramData[letter] = 1
            if prev != '':
                curr = prev+letter
                if curr in bigramData:
                    bigramData[curr] += 1
                else:
                    bigramData[curr] = 1
            prev = letter
  
def loadFile(fileHandler):
    global count
    global wordCount
    global words_file
    for line in fileHandler: 
        count += 1
        line = line.lower()
        line = line[13:]
        line = re.sub('[^a-z]',' ',line)
        #line = re.sub(r'\s',')
        words = line.split()
        tempWords = []
        for i in range(len(words)):
            if words[i] in eng_vocab:
                eng_vocab[words[i]] += 1
            else:
                eng_vocab[words[i]] = 1
            tempWords.append('<'+words[i]+'>')
            wordCount += 1
        populateDict(tempWords)
        print('Filled line ',count)
    
if __name__ == "__main__":
    t1 = time.perf_counter()
    t3 = time.process_time()
    print('cpu time :',t3)
    #data+= line
    #words.appe

    loadFile(fileHandler)
    t2 = time.perf_counter()
    t4 = time.process_time()
    print("Before CPU Time:",t3)
    print('CPU time :',t4)
    print('Done...')
    ## Splitting the data in to words
    print("Number of Lines" , count)
    print("Number of Words",wordCount)
    print("Total Time taken", t2 - t1)
    print("Total CPU time :", t4 - t3)
    
    storage = dataStorage()
    #print("Length of Database: ",len(database))
    #print("Length of storage: ",len(dataStorage.instance.database))
#print('Key Values')
    my_file = open("pickle_data3.dat","wb")
    pickle.dump(storage,my_file)
    print("Done Loading the Pickle File")
    my_file.close()
    #words = data.split()
    #p1 = ''
    #p2 = ''

#wordCount = 0
## Adding begin and end seperator to the word.
#for word in words:
 #   word = '<'+word+'>'
  #  wordCount += 1
#print('Total Number Of Lines',wordCount)

#database= {}
    '''
    
   '''     