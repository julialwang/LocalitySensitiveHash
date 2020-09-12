import csv
import mmh3
import string
import random
import time
import numpy as np
from matplotlib import pyplot as plt 

SIZE_FILE = 3594
File = "BigTitleTest.csv"
rand_hash = [] #array containing hash codes with randomly generated key
hash_threshold = 16 #how many hash functions we are using. Needs to be an even number
maxHash = 1000 #max hash value

for i in range(hash_threshold):
    rand_hash.append(random.randint(1, 100))

def hash(x, i) -> int:  
    return mmh3.hash(str(x), i) % maxHash
    
def initialize(f) -> map: #create min heap
    titles = []
    for x in f:
        #formatting the titles for most accurate result.
        x = x.replace('...', '').rstrip("\n").lower() #remove unneccessary characters 
        stopwords = ['for', 'to', 'of', 'a', 'at', 'is', 'and', 'the', 'an', 'in', 'with', 'by', 'it', 'its'] 
        query = x.split()
        resultwords  = [word for word in query if word.lower() not in stopwords]
        x = ' '.join(resultwords) #remove unimportant words
        table = str.maketrans(dict.fromkeys(string.punctuation)) 
        x = x.translate(table)#remove punctuation
        titles.append(x)
    result = {} # will be filled with the formatted titles and its min hash values
    for x in titles:
        hashed = [] #min hash values of x 
        for i in range(hash_threshold):
            min = maxHash
            for y in x.split(' '):
                temp = hash(y, rand_hash[i])
                if temp < min:
                    min = temp
            hashed.append(min) 
        result[x] = hashed #add x and hashed to the map result
    return result
        
def createGroup(result) -> [[]]: # create a 2d array with first array being a combined string of first k indices of each minhash, second array being a combine string of next k indices of each minhash
    rows, cols = (int(hash_threshold/2), 0) 
    groups = [['' for i in range(cols)] for j in range(rows)] 
    for x in result:
        for i in range(int(hash_threshold/2)):
            groups[i].append(str(result.get(x)[2 * i]) + str(result.get(x)[2 * i + 1]))
    return groups

def LSH(result, user) ->[]:
    groups = createGroup(result)
    user2 = createGroup(user)
    values = [0] * SIZE_FILE
    for i in range(int(hash_threshold/2)): #increment the index of the title that matches the user input 
        for j in range(SIZE_FILE):
            if str(user2[i][0]) == str(groups[i][j]):
                values[j] += 1
    return values
    
def prompt(user) -> float:
    start = time.time()   
    user = user.split('\n')
    user += " a" #arbitrary string that can be cancelled out by algorithm for inputs size 1
    init2 = initialize(user)
    results = LSH(init, init2)
    answer = ''
    indices = []
    for i in range (len(results)):
        val = results[i]
        if val >= 2:
            indices.append(i)
    for val in indices:
        answer += names[val] + '\n'
    if (len(answer) == 0):
        print('No relevant documents! Try again.')
    else:
        print('Here are some related documents : \n' + answer)
        pass
    end = time.time()
    return ("%.20f" % (end - start))
if __name__ == '__main__':
    database = open(File, 'r')
    init = initialize(database)
    names = []
    temp = open(File, 'r')
    for x in temp:
        names.append(x.rstrip("\n")) #unedited list of titles in database
    print("Welcome to a database of papers!")
    user = input("Insert the name of a paper or keywords to find similar titles: ")
    prompt(user)

    ########################################### code for creating graph 
    # size = np.arange(1, 3594, 500) 
    # x = []
    # y = []
    # for num in size:
    #     SIZE_FILE=num
    #     x.append(num)
    #     total = float(prompt(user)) + float(prompt(user)) + float(prompt(user)) + float(prompt(user)) + float(prompt(user))
    #     y.append(round(total/5,6))
    # print(str(x) + ' ' +  str(y))
    # plt.title("Size of File vs RunTime") 
    # plt.xlabel("Number of documents in database") 
    # plt.ylabel("RunTime (seconds)") 
    # plt.plot(x,y,"ob")
    # plt.savefig("mainLSHruntime.png")
    ########################################### 

