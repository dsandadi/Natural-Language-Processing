# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 14:38:14 2018

@author: DINESH
"""
import sys
import unicodedata
'''
Method  : displayDetails
Purpose : displays the file details.
Argments : fileName, and list of Vowels. 
Return Value : count of vowels, and consonants.
'''    
def displayDetails(fileName,vowels):
    fileHandler1 = open(fileName,encoding='UTF-8') # opening file in UTF-8 format.
    lineCount = 0
    characterCount = 0
    letterCount = 0
    vowelCount = 0
    for line in fileHandler1:
        line = line.lower()
        for curr in line:
            #curr = curr.lower()
            if(unicodedata.category(curr)[0] =='L'):
                if curr in vowels:
                    vowelCount += 1
                letterCount += 1
            characterCount += 1
        lineCount += 1
    fileHandler1.close()
    ## printing details of the file.    
    print('FileName' ,fileName)
    print('{:<40}'.format('Total Number of lines in the file'),'=','{:>8}'.format(lineCount))
    print('{:<40}'.format('Total Number of Characters in the file'),'=','{:>8}'.format(characterCount))
    print('{:<40}'.format('Total Number of letters in the file'),'=' ,'{:>8}'.format(letterCount))
    print('{:<40}'.format('Total Number of vowels in the file'),'=','{:>8}'.format(vowelCount))
    print('{:<40}'.format('Total Number of consonants in the file'), '=','{:>8}'.format(letterCount-vowelCount))
    print('{:<40}'.format("% vowels"),"=", '{:>8}'.format(round((vowelCount/letterCount)*100, 2)),'%')
    return vowelCount, letterCount-vowelCount
'''
Method : printChiDetails
Purpose : helper function to findChiSquare for printing details
Arguments: list of vowel and consonant counts and book names.
'''
def printChiDetails(actual,book1,book2):
    print('{:<20}'.format('Book'),end = "")
    print('{:<20}'.format('Vowels'),end = "")
    print('Consonants')
    print('{:<20}'.format(book1),end = "")
    print('{:<20}'.format(round(actual[0]),2), end = "")
    print(round(actual[1],2))
    print('{:<20}'.format(book2),end = "")
    print('{:<20}'.format(round(actual[2],2)), end = "")
    print(round(actual[3],2))

'''
Method  : findChiSquare
Purpose : Finds the chisquare between two files.
Return value : chisquare value is returned.
Arguments : list of vowels, and list of consonants, book1, book2 names
            vowels has a list of vowel count values in two values and 
            consonants has list of count of consonants in two files
'''
## vowels and consonants are the lists which contain corresponding vowels and consonants.
def findChiSquare(vowels,consonants,book1,book2):
    ## Calculating the expected frequencies.
    letterCount1 = vowels[0] + consonants[0]
    letterCount2 = vowels[1] + consonants[1]
    vowelSum = sum(vowels)
    consonantSum = sum(consonants)
    totalSum = vowelSum + consonantSum
    
    #lists to store the actual and expected values.
    actual = []
    expected = []
    
    actual.append(vowels[0])
    actual.append(consonants[0])
    actual.append(vowels[1])
    actual.append(consonants[1])
    expected.append((vowelSum/totalSum)* letterCount1)
    expected.append((consonantSum/totalSum)* letterCount1)
    expected.append((vowelSum/totalSum)*letterCount2)
    expected.append((consonantSum/totalSum)*letterCount2)
    print('Actual:')
    printChiDetails(actual,book1,book2)

    print('Expected: ')
    printChiDetails(expected,book1,book2)
    
    chiSquare = 0
    for i in range(len(actual)):
        chiSquare += ((actual[i] -expected[i])**2)/expected[i]
    return chiSquare
if(__name__ == '__main__'): 
    file1 ="pride.txt"
    file2 ="swann.txt"
    if(len(sys.argv) < 2):
        print("Please enter two arguments")
        #exit()
    else:
        file1 = sys.argv[0]
        file2 = sys.argv[1]
        print("Files Entered to be compared are ", sys.argv[0]," and ", sys.argv[1])
        
    vowels = ['a','e','i','o','u','\u00e9','\u00e2','\u00ea',
              '\u00ee','\u00f4' ,'\u00fb','\u00e0' ,'\u00e8',
              '\u00f9' ,'\u00eb' ,'\u00ef' ,'\u00fc']
    a,b = displayDetails(file1,vowels)## a,b have vowel and consonant count of file1.
    c,d = displayDetails(file2,vowels)## c,d have vowel and consonant count of file2.
    v = [a,c];
    c = [b,d]
    ## loaded the count of vowels and consonants.
    
    chisquare = round(findChiSquare(v, c,file1,file2),2);
    print('Value of Chisquare is: ', chisquare)
    print('==================================================')
    ## chisquare values at different probabilities with degrees of freedom as 1.
    chiValues= {0.001:10.8, 
                0.01:6.64,
                0.05:	3.84}
    df = (len(sys.argv) - 1) * (2 - 1)
    p = 0
    chances = 0
    times = 0
    #dynamically checking the chivalues and loading times and chances.
    if(chisquare > chiValues[0.001]):
        p = 0.001
        times = 1
        chances = 1000
    elif(chisquare > chiValues[0.01]):
        p = 0.01
        times = 1
        chances = 100
    elif(chisquare > chiValues[0.05]):
        p = 0.05
        times = 5
        chances =100 
    print('The null hypothesis is that the text in the two books is drawn from the same population.')
    if(p == 0 and chances == 0 and times == 0):
        print("Null hypothesis can't be rejected as chisquare value ", chisquare, " is less than the chisquare value at 5% level of significance." )
    else:
        print("Chi-square = ",chisquare, "df= ", df, ", which is significant at p < ",p)
        print("There is only ",times, " chance in ",chances," that this result happened by chance, i.e., by accident.")
    