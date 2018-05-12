# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 13:26:45 2018

@author: DINESH
"""
import pickle
from tables import *
import operator
import string
from operator import attrgetter

eng_vocab = {}
unigramData = {}
bigramData = {}
suggestions = []
class dataStorage:
    
    #database={}
    def __init__(self):
        self.unigramData = unigramData
        self.bigramData = bigramData
        self.eng_vocab = eng_vocab

class candidate:
    def __init__(self,arg1,arg2,arg3,arg4,arg5,arg6,arg7):
        self.candidateCorrection = arg1
        self.correctLetter = arg2
        self.errorLetter = arg3
        self.x_to_w_ratio = arg4
        self.x_to_word_prob = round(arg5,10)
        self.word_prob = round(arg6,10)
        self.final_prob = round(arg7,10)
    def printCandidate(self):
        print(self.candidateCorrection.ljust(10),self.correctLetter.ljust(3),self.errorLetter.ljust(3),self.x_to_w_ratio.ljust(6),repr(self.x_to_word_prob).ljust(15),repr(self.word_prob).ljust(15),repr(self.final_prob).ljust(15))
    
#def addCandidateToList(word):    
def convertListToDict(freq):
    dic ={}
    for curr in freq:
        #dic[curr[0]]
        newDic = {}
        offset = 97
        for i in range(1,len(curr)):
            #if(i == len(curr) - 1):
             #   newDic['@'] = int(curr[i])    
            #else:
            newDic[chr(i+offset-1)] = int(curr[i])
        dic[curr[0]] = newDic
    return dic
def findWordProb(word):
    totalWords = sum([eng_vocab[key] for key in eng_vocab])
    #print("Total Words",totalWords)
    freq = eng_vocab[word]
    #print("Word ",word, " Freq: ",freq)
    v = len(eng_vocab)
    #print("Distinct words" ,v)
    return (freq+0.5)/(totalWords + (0.5*v))
## Finds deletion probability.
def findDeleteProb(deletionLetter,prevLetter,kernData):
        deletions = kernData[prevLetter][deletionLetter] 
        word = prevLetter + deletionLetter
        if(prevLetter == '@'):
            word = '<'+word[1:]
        totalOccurances = bigramData[word]
        return deletions/totalOccurances


# Finds insertion probability.
def findInsertionProb(prevLetter,currLetter,kernData):
    word = prevLetter
    if(prevLetter == '@'):
        word = '<'
    return (kernData[prevLetter][currLetter])/unigramData[word]

#find substituion probability
def findSubProb(subLetter,corrLetter,kernData):
    return kernData[subLetter][corrLetter]/unigramData[corrLetter]

#find transposition probability
def findTransposProb(prevLetter,currLetter,kernData):
    word = prevLetter+currLetter
    if(prevLetter == '@'):
       word = '<' + currLetter
    return kernData[prevLetter][currLetter]/bigramData[word];
#This method finds all letters possible by inserting in to typo.
def addLetter(typo,del_dict):
    validWords = []
    global suggestions    
    for i in range(len(typo)):
        for letter in list(string.ascii_lowercase):    
            word = typo[0:i]+letter+typo[i:]
            if word in eng_vocab:
                p = '@'
                if(i != 0):
                    p = typo[i-1]
                word_prob = findWordProb(word)
                cand_prob = findDeleteProb(letter,p,del_dict)
                
                final_prob = (word_prob * cand_prob) * (10**9)
                suggestions.append(candidate(word,letter,'-',p+'|'+p+letter,cand_prob,word_prob,final_prob))
                validWords.append(word)
    return validWords

#This method finds all the word possible by deleting a letter in the typo 
#and calculates the probability of each possible word. 
def deleteLetter(typo,add_dict):
    validWords = []
    global suggestions
    for i in range(len(typo)):
        word = typo[0:i]+typo[i+1:]
        if word in eng_vocab:
            l = ''
            if(i == 0):
                l = '@'
            else:
                l = typo[i-1]
            #c1 = candidate()
            word_prob = findWordProb(word)
            del_prob = findInsertionProb(l,typo[i],add_dict)
            final_prob = (word_prob*del_prob)*(10**9)
            suggestions.append(candidate(word,'-',typo[i],l+typo[i]+'|'+l,del_prob,word_prob,final_prob));
            validWords.append(word)
    return validWords
#This method finds all the words possible by substituting a letter by 
#some other letter and finds probability of each possible word.
def substituteLetter(typo,sub_data):
    validWords = []
    global suggestions
    for i in range(len(typo)):
        for letter in list(string.ascii_lowercase):
            word = typo[0:i] + letter + typo[i+1:]
            if word in eng_vocab:
                #print("Checking -> ",letter)
                word_prob = findWordProb(word)
                sub_prob = findSubProb(typo[i],letter,sub_data)
                final_prob = word_prob * sub_prob*(10**9)
                suggestions.append(candidate(word,letter,typo[i],typo[i]+'|'+letter,sub_prob,word_prob,final_prob))
                
                validWords.append(word)
    return validWords
#This method finds all the words possible by transposing a two consecutive letters 
#from the typo and calculates the probability of each transposed word.
def transposeLetters(typo,trans_data):
    validWords = []
    prev = -1
    global suggestions
    for curr in range(len(typo)):
        if(prev != -1):
            word = typo[0:prev]+typo[curr] + typo[prev]+typo[curr+1:]
            if word in eng_vocab:
                word_prob = findWordProb(word)
                trans_prob = findTransposProb(typo[curr],typo[prev],trans_data)
                final_prob = word_prob * trans_prob * (10**9)
                suggestions.append(candidate(word,typo[curr]+typo[prev],typo[prev]+typo[curr],typo[curr]+typo[prev]+'|'+typo[prev]+typo[curr],trans_prob,word_prob,final_prob))
                validWords.append(word)
        prev = curr
    return validWords

def printSuggestions():
    print('candidate'.ljust(10),'c'.ljust(3),'e'.ljust(3),'x|w'.ljust(6),'p(x|w)'.ljust(15),'P(word)'.ljust(15),'10^9*P(x|w)p(w))'.ljust(15))
    for curr in suggestions:
        curr.printCandidate()
#def findCorrectWord(typo):
def printDatabase(data,t):
    print(t.ljust(7),'counts'.ljust(15))
    for key in data:
        print(key.ljust(7),repr(data[key]).ljust(15))

if __name__ == '__main__':
    objects=[]
    global suggestions
    with (open('pickle_data3.dat','rb')) as openFile:
        try:
            objects.append(pickle.load(openFile))
        except EOFError:
            print("Error Occured Reading")
       
        unigramData = objects[0].unigramData
        bigramData = objects[0].bigramData
        eng_vocab = objects[0].eng_vocab
        
        print("Size of unigramDatabase :",len(unigramData))
            
        #print(len(database))
        print("Size of English Vocabulary:", len(eng_vocab))
        
        sorted_database = sorted(unigramData.items(),key=operator.itemgetter(1))
        printDatabase(sorted_database,'Unigram');
        sorted_database = sorted(bigramData.items(),key=operator.itemgetter(1))
        printDatabase(sorted_database,'Bigram')
        
        del_dict = convertListToDict(del_table)
        add_dict = convertListToDict(add_table)
        sub_dict = convertListToDict(sub_table)
        transpose_dict = convertListToDict(transpose_table)
         
        word = input("Please Enter a String\n")
        validWords=[]
        validWords.extend(addLetter(word,del_dict))
        validWords.extend(substituteLetter(word,sub_dict))
        validWords.extend(deleteLetter(word,add_dict))
        validWords.extend(transposeLetters(word,transpose_dict))
        suggestions = sorted(suggestions,key = attrgetter('final_prob','candidateCorrection'),reverse = True)
        printSuggestions()
        print(validWords)
