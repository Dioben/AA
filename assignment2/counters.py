import random
from math import sqrt

def normalCounter(text):
    results = {}
    for char in text:
        if char not in results:
            results[char]=1
        else:
            results[char]+=1
    return results

def staticProbabilityCounter(text,prob):
    results = {}
    for char in text:
        roll = random.random()
        if roll<=prob:
            if char not in results:
                results[char]=1
            else:
                results[char]+=1
    return results

def dynamicProbabilityCounter(text,probf,memorized = []):
    results = {}
    for char in text:
        roll = random.random()
        if roll<=prob:
            if char not in results:
                results[char]=1
            else:
                results[char]+=1
    return results


def invSqrtFunc(value):
    return 1/(sqrt(2)**value)

if __name__ == "__main__":
    filepaths = ["english.txt","french.txt","german.txt"]
    table = [invSqrtFunc(x) for x in range(0,20001)] #pre calculate character 
    for filepath in filepaths:
        f = open(filepath,"r")
        text = f.read()
        f.close()
        accurateCount = normalCounter(text)
        staticProbCount = staticProbabilityCounter(text,1/16)
        dynamicProbCount = dynamicProbabilityCounter(text,invSqrtFunc,table)

