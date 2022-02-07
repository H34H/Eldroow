from ast import Try
import datetime
import math
from cmath import pi
from os import path
import random
#from random import random
from re import L
from anytree import Node, RenderTree, Resolver, AsciiStyle, search, LevelOrderIter, PreOrderIter, util
from itertools import takewhile
import matplotlib.pyplot as plt
from numpy.lib.histograms import histogram
from numpy import prod
import numpy as np
from collections import Counter
time = datetime.datetime.now()

with open('.\words.txt') as f:
    t = f.readlines()
words = [x.strip() for x in t] 

#walk through the complete list:

#Iterations: 
#1: random guessing 
#2: walk the entire list from top to bottom
#3: exclude words that contain letters that are not in the word
#4: make sure that words contain letters if they should be in the word
#5: check that letter is on right position:
#6: remove words that have the right letter, but on the wrong position (if word contains only 1 of that letter) => turns on: doesn't make a difference
#7: evaluate performance of each word to start with based on a sample of 100 words:
# ------------------------------
# starting word: pruim
# avg. # of guesses: 4.514249639249639
# max. # of guesses: 12
# Counter({4: 1403, 5: 1146, 3: 1081, 6: 742, 2: 432, 7: 367, 8: 165, 9: 86, 1: 84, 10: 31, 12: 3, 11: 3, 0: 1})
# ------------------------------
#8 shuffle lijst ipv random:
# avg. # of guesses: 4.281565656565657
# distribution # of guesses: 
# 0: 1, 1: 71, 2: 525, 3: 1268,4: 1475, 5: 1106, 6: 614, 7: 282, 8: 130, 9: 46, 10: 19, 11: 6, 14: 1
# avg. time need / run: 0:00:00.040734
#9: sluit woorden uit die zelfde letter hebben op yellow plek hebben. 
#10: shuffle woorden na elke run: -> werkt niet, reverted


def letterIsInToBeGuessedWord(letter, toBeGuessedWord):
    return letter in toBeGuessedWord

def letterIsOnRightPlace(position, letter, toBeGuessedWord):
    return toBeGuessedWord[position] == letter

def hasLettersOnRightPosition(word):
    for letter in letterOnPosition:
        if letterOnPosition[letter] != word[letter]:
            return False
    for idx, letter in enumerate(word):
        if letter in letterNotOnPosition[idx]:
            return False
    return True

def hasNoExcludedLetters(word):
    for letter in word:
        if letter in excludedLetters:
            return False
    return True

def hasNoIncludedLetters(word):
    for letter in word:
        if letter in includedLetters:
            return False
    return True

def matchesIncludedLetters(word):
    for letter in includedLetters:
        if letter not in word:
            return False     
    return True

def determineMostLikelyword(wordList):
    histoLetter = []
    for x in range(5):
        histoLetter.append({'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0})
    for word in wordList:
        for idx, letter in enumerate(word):
            if idx not in letterOnPosition.keys():
                histoLetter[idx][letter] += 1

    # for idx, x in enumerate(histoLetter):
    #     if idx not in letterOnPosition.keys():
    #         print({k: v for k, v in sorted(x.items(), key=lambda item: item[1], reverse=True)})
    #     else:
    #         print (letterOnPosition[idx])
    
    #[print (histoLetter.index(x), x) for x in histoLetter]
    maxScore = 0
    maxWord = ''
    for word in notUsed:
        score = 0
        for idx, letter in enumerate(word):
            score += histoLetter[idx][letter]
        if score > maxScore:
            maxScore = score
            maxWord = word
    return maxWord

sample = list(words)
random.shuffle((words))

guessesNeeded = []
for run in range(len(words)):
    toBeGuessedWord = words[run]
    notUsed = list(words)
    i = 0
    wordGuessed = False
    excludedLetters = set()
    includedLetters = set()
    letterOnPosition = {}
    letterNotOnPosition = [set(),set(),set(),set(),set()]
    while not wordGuessed:
        if i == 0:
            guess = 'pruim'
            notUsed.remove('pruim')
        else:
            guess = determineMostLikelyword(notUsed)
            #notUsed.remove(guess)
            #guess = notUsed.pop()
        if guess == toBeGuessedWord:
            #if i>=0:
            #     print ('----- '+ str(i) + '  ------')
            wordGuessed = True
            guessesNeeded.append(i)
        else:
            i+=1
            for idx, letter in enumerate(guess):
                if letterIsOnRightPlace(idx, letter, toBeGuessedWord):
                    letterOnPosition[idx] = letter
                elif letterIsInToBeGuessedWord(letter, toBeGuessedWord):
                    if letter not in includedLetters:
                        includedLetters.add(letter)
                    if letter not in letterNotOnPosition[idx]:
                        letterNotOnPosition[idx].add(letter)
                elif letter not in excludedLetters:
                    excludedLetters.add(letter)
            notUsed = [x for x in notUsed if hasLettersOnRightPosition(x) and hasNoExcludedLetters(x) and matchesIncludedLetters(x)]
            #if i>=0:
            #     print(toBeGuessedWord, i, guess, includedLetters, excludedLetters, len(notUsed))
MaxGuessesNeeded = sum(guessesNeeded)
print ('avg. # of guesses: ' + str(sum(guessesNeeded)/len(sample)))
print ('distribution # of guesses: ')
histoGuesses = sorted(Counter(guessesNeeded).items())
for x in histoGuesses:
    print(str(x[0]) + ': ' + str(x[1])) 
print ('% in <= 6 guesses: {:.2f}%'.format(len([x for x in guessesNeeded if x < 7]) / len(words)*100))    
runtime  = datetime.datetime.now() - time
print ('avg. time need / run: ' + str(runtime/1000))
print (runtime)
