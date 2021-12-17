import argparse
import random
from math import sqrt
import json

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
        
        if char not in results:
            value = 0
        else:
            value = results[char]
        
        roll = random.random()
        try:
            limit = memorized[value]
            if roll<=limit:
                results[char] = value+1
        except:
            #we have gone past the memorized maximum
            memcount = len(memorized)
            memorized+= [probf(x) for x in range(memcount,memcount+21)] #calculate the next 20 entries
            limit = memorized[value]
            if roll<=limit:
                results[char] = value+1
    return results


def invSqrtFunc(value):
    return 1/(sqrt(2)**value)

if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--files",help="comma separated input files", default="english.txt,french.txt,german.txt")
    parser.add_argument("--count",help="how many times to run each counter",type=int, default=1000)
    parser.add_argument("--output",help="file to dump information into")
    args = parser.parse_args()
    filepaths = args.files.split(",")
    table = [invSqrtFunc(x) for x in range(101)] #pre calculate character

    results = {}
    for filepath in filepaths:
        f = open(filepath,"r")
        text = f.read()
        f.close()
        accurateCount = normalCounter(text)
        staticProbCount = []
        dynamicProbCount = []
        for _ in range(args.count):
            staticProbCount.append( staticProbabilityCounter(text,1/16))
            dynamicProbCount.append(dynamicProbabilityCounter(text,invSqrtFunc,table))
        results[filepath] = {"real":accurateCount,"static":staticProbCount,"dynamic":dynamicProbCount}

    if args.output:
        f = open(args.output,"w")
        json.dump(results,f)
        f.close()
    else:
        print(results)  

