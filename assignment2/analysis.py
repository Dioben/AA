import argparse
import json
from math import inf
import plotly.express as px
import pandas as pd

def upscaleValues(data,fixedMult,dynamicMod,memorized = []):
    for idx in range(len(data['static'])):
        run = data['static'][idx]
        data['static'][idx] = {key:value*fixedMult for key,value in run.items()}

    for idx in range(len(data['dynamic'])):
        run = data['dynamic'][idx]
        for key,value in run.items():
            try:
                run[key] = memorized[value]
            except:
                memorized+=[dynamicMod(x) for x in range(len(memorized),value+21)] #advance memorization
                run[key] = memorized[value]
    return data


def getStats(data):
    results = []
    sizes = [1,10,25,50,100,175,250,375,500,750,1000]
    real = data['real']
    for size in sizes:
        staticList = data['static'][:size]
        dynamicList = data['dynamic'][:size]
        max,min = getDiffs(real,staticList)
        dyn_max,dyn_min = getDiffs(real,dynamicList)

        avgStatic = {x:sum([item.get(x,0) for item in staticList])/size for x in real.keys()}
        avgDynamic = {x:sum([item.get(x,0) for item in dynamicList])/size for x in real.keys()}
        
        print(avgStatic)
        print(avgDynamic)
        print(real)
        print("linebreak")
        avgErrorStatic = sum( [abs(y-avgStatic[x]) for x,y in real.items()] ) /len(real.keys()) 
        avgErrorDynamic = sum( [abs(y-avgDynamic[x]) for x,y in real.items()] ) /len(real.keys())

        realSorted = sorted(real.keys(),key=lambda x:real[x])
        staticSorted = sorted(avgStatic.keys(),key=lambda x:avgStatic[x])
        dynamicSorted = sorted(avgDynamic.keys(),key=lambda x:avgDynamic[x])
        
        staticSwaps = countSwaps(realSorted,staticSorted)
        dynamicSwaps = countSwaps(realSorted,dynamicSorted)
        
        results.append({"size":size, "label":"static","max":max,"min":min, "avg":avgErrorStatic,"swaps":staticSwaps})
        results.append({"size":size,"label":"dynamic","max":dyn_max,"min":dyn_min, "avg":avgErrorDynamic,"swaps":dynamicSwaps})
    return results


def getDiffs(real,list):
    max= 0
    min = inf
    for letter,value in real.items():
        for datapoint in list:
            value2 = datapoint.get(letter,0)
            delta = abs(value-value2)
            if max<delta:
                max = delta
            if min>delta:
                min = delta
    return max,min

def countSwaps(realSorted,otherSorted):
    swaps = 0
    for index in range(len(realSorted)):
            realChar = realSorted[index]
            otherChar = otherSorted[index]
          
            if otherChar!=realChar:
                swaps+=1
                otheridx = otherSorted.index(realChar)
                otherSorted[otheridx]= otherChar
                otherSorted[index]=realChar

    assert realSorted == otherSorted
    return swaps



def drawLineGraphs(results):
    #TODO: plot max, min,avg diff based on size
    #TODO plot necessary swaps based on size
    for lang,data in results.items():
        df = pd.DataFrame(data)
    print(df)
    pass 

def drawBarGraphs(info):
    #TODO: overlap bar graph of letter appearances per lang using ['real'] and padding with 0s
    pass

def inverseDynamicMod(value):
    #my factor is 1/(sqrt(2)**k)
    #equivalent to 1/(2 **1/2 **k) = 1/(2 **k/2)
    #meaning 2**(k/2)-1 events until expected value is k
    #from slides: k = log2( n/2 + 1 ) = floor(log2(n/2))+1 = floor(log2(n)-1+1) = floor(log(2))
    # k = floor(log2(n)) -> 2**k = n ?
    return 2 ** value  #TODO: ASK TEACHER ABOUT THIS

if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--source",help="input data json file", default="results.json")
    args = parser.parse_args()
    f = open(args.source,"r")
    data = json.load(f)
    f.close()
    results = {}
    for name,info in data.items():
        info = upscaleValues(info,16,inverseDynamicMod,[inverseDynamicMod(x) for x in range(101)])
        results[name] = getStats(info)
    
        
drawLineGraphs(results)
drawBarGraphs(data)