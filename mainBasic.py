import csv
import string
import random
import time
from matplotlib import pyplot as plt
import numpy as np

file = "TitlesTest.csv"
size = 0

def clean(f) -> []:
    cleaned = []
    for x in f:
        x = x.replace('...', '').rstrip("\n")
        x = x.lower()
        stopwords = ['for', 'to', 'of', 'a', 'at', 'is', 'and', 'the', 'an', 'in', 'with', 'by', 'it', 'its']
        query = x.split()
        resultwords  = [word for word in query if word.lower() not in stopwords]
        x = ' '.join(resultwords)
        table = str.maketrans(dict.fromkeys(string.punctuation))
        x = x.translate(table)
        cleaned.append(x)
    return cleaned

if __name__ == '__main__':
    
    print("Welcome to a database of papers!")
    user = input("Insert the name of a paper or keywords to find similar titles: ")
    start = time.time()
    user = user.lower()    
    user = user.split('\n')
    userClean = clean(user)
    userSet = set()
    for title in userClean:
        for word in title.split(' '):
            userSet.add(word)
    names = []
    a = open(file, 'r')
    for x in a:
        names.append(x.rstrip("\n"))
    cleaned = clean(names)
    size = len(cleaned)
    hits = [0]*size
    i = 0
    for title in cleaned:
        for word in title.split(' '):
            if word in userSet:
                hits[i] += 1
        i += 1
    indices = []
    answer = ""
    for i in range(len(hits)):
        val = hits[i]
        if val >= 2:
            indices.append(i)
    for val in indices:
        answer += names[val] + '\n'
    if (len(answer) == 0):
        print('No relevant documents! Try again.')
    else:
        print('Here are some related documents : \n' + answer)
    end = time.time()
    print("%.20f" % (end - start))

