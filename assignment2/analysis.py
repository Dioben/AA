import argparse
import json
from math import inf
import plotly.express as px
import pandas as pd
import os

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
        max,min,percent_max,percent_min = getDiffs(real,staticList)
        dyn_max,dyn_min,dyn_percent_max,dyn_percent_min = getDiffs(real,dynamicList)

        avgStatic = {x:sum([item.get(x,0) for item in staticList])/size for x in real.keys()}
        avgDynamic = {x:sum([item.get(x,0) for item in dynamicList])/size for x in real.keys()}
        
        avgErrorStatic = sum( [abs(y-avgStatic[x]) for x,y in real.items()] ) /len(real.keys()) 
        avgErrorDynamic = sum( [abs(y-avgDynamic[x]) for x,y in real.items()] ) /len(real.keys())

        avgDevStatic = sum( [abs(y-avgStatic[x])/y*100 for x,y in real.items()] ) /len(real.keys()) 
        avgDevDynamic = sum( [abs(y-avgDynamic[x])/y*100 for x,y in real.items()] ) /len(real.keys())

        realSorted = sorted(real.keys(),key=lambda x:real[x])
        staticSorted = sorted(avgStatic.keys(),key=lambda x:avgStatic[x])
        dynamicSorted = sorted(avgDynamic.keys(),key=lambda x:avgDynamic[x])
        
        staticSwaps = countSwaps(realSorted,staticSorted)
        dynamicSwaps = countSwaps(realSorted,dynamicSorted)
        
        #static
        results.append({"sample size":size, "label":"static","metric":"max","value":max})
        results.append({"sample size":size, "label":"static","metric":"min","value":min})
        results.append({"sample size":size, "label":"static","metric":"average", "value":avgErrorStatic})
        results.append({"sample size":size, "label":"static","metric":"swaps", "value":staticSwaps})
        results.append({"sample size":size, "label":"static","metric":"relative swaps", "value":staticSwaps/len(realSorted) *100})
        results.append({"sample size":size, "label":"static","metric":"deviation max","value":percent_max})
        results.append({"sample size":size, "label":"static","metric":"deviation min","value":percent_min})
        results.append({"sample size":size, "label":"static","metric":"deviation average","value":avgDevStatic})
        #dynamic
        results.append({"sample size":size, "label":"dynamic","metric":"max","value":dyn_max})
        results.append({"sample size":size, "label":"dynamic","metric":"min","value":dyn_min})
        results.append({"sample size":size, "label":"dynamic","metric":"average", "value":avgErrorDynamic})
        results.append({"sample size":size, "label":"dynamic","metric":"swaps", "value":dynamicSwaps})
        results.append({"sample size":size, "label":"dynamic","metric":"relative swaps", "value":dynamicSwaps/len(realSorted) *100})
        results.append({"sample size":size, "label":"dynamic","metric":"deviation max","value":dyn_percent_max})
        results.append({"sample size":size, "label":"dynamic","metric":"deviation min","value":dyn_percent_min})
        results.append({"sample size":size, "label":"dynamic","metric":"deviation average","value":avgDevDynamic})
               
    return results


def getDiffs(real,list):
    max = percent_max= 0
    min= percent_min = inf
    for letter,value in real.items():
        for datapoint in list:
            value2 = datapoint.get(letter,0)
            delta = abs(value-value2)
            percent_delta = delta/value*100
            if max<delta:
                max = delta
            if min>delta:
                min = delta
            if percent_max<percent_delta:
                percent_max = percent_delta
            if percent_min>percent_delta:
                percent_min = percent_delta
    return max,min,percent_max,percent_min

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



def drawLineGraphs(results,interactive):
    for lang,data in results.items():
        df = pd.DataFrame(data)
        lang = lang.removesuffix(".txt").capitalize() #requires python 3.9
        staticAbsDF = df.loc[df["label"]=="static"].loc[df['metric'].isin(["max","min","average"])]
        staticRelDF = df.loc[df["label"]=="static"].loc[df['metric'].isin(["deviation max","deviation min","deviation average"])]
        dynamicAbsDF = df.loc[df["label"]=="dynamic"].loc[df['metric'].isin(["max","min","average"])]
        dynamicRelDF = df.loc[df["label"]=="dynamic"].loc[df['metric'].isin(["deviation max","deviation min","deviation average"])]
        
        absSwaps = df.loc[df['metric']=="swaps"]
        relSwaps = df.loc[df['metric']=="relative swaps"]

        fig = px.scatter(staticAbsDF,x="sample size",y="value", color="metric")
        fig.update_layout(title_text=f"{lang} - Static", title_x=0.5)

        if interactive:
            fig.show()
        else:
            fig.write_image(f"graphs/{lang}StaticAbs.png")

        fig = px.scatter(dynamicAbsDF,x="sample size",y="value", color="metric")
        fig.update_layout(title_text=f"{lang} - Dynamic", title_x=0.5)
        
        if interactive:
            fig.show()
        else:
            fig.write_image(f"graphs/{lang}DynamicAbs.png")

        fig = px.scatter(absSwaps,x="sample size",y="value",color="label")
        fig.update_layout(title_text=f"{lang} - Swaps", title_x=0.5)
        
        if interactive:
            fig.show()
        else:
            fig.write_image(f"graphs/{lang}SwapsAbs.png")

        # now do it again in relative terms

        fig = px.scatter(staticRelDF,x="sample size",y="value", color="metric")
        fig.update_layout(title_text=f"{lang} - Percent Deviation Static", title_x=0.5)

        if interactive:
            fig.show()
        else:
            fig.write_image(f"graphs/{lang}StaticRel.png")

        fig = px.scatter(dynamicRelDF,x="sample size",y="value", color="metric")
        fig.update_layout(title_text=f"{lang} - Percent Deviation Dynamic", title_x=0.5)
        
        if interactive:
            fig.show()
        else:
            fig.write_image(f"graphs/{lang}DynamicRel.png")

        fig = px.scatter(relSwaps,x="sample size",y="value",color="label")
        fig.update_layout(title_text=f"{lang} - Swaps %", title_x=0.5)
        
        if interactive:
            fig.show()
        else:
            fig.write_image(f"graphs/{lang}SwapsRel.png")

    

def drawBarGraphs(data,interactive):
    data = {x:y['real'] for x,y in data.items()}
    #pad 0s
    for name,info in data.items():
        others = set(data.keys())
        others.remove(name)
        for other in others:
            info.update({x:0 for x in data[other].keys() if x not in info})
    
    #convert into a better format for graphing        
    merged = []
    for name,info in data.items():
        for letter,value in info.items():
            merged.append({"text":name.removesuffix(".txt").capitalize(),"letter":letter,"value":value})
    df = pd.DataFrame(merged)
    fig= px.bar(df, x="letter", color="text",y="value", barmode="group")
    fig.update_layout(title_text="Letter Frequency Distribution", title_x=0.5)
    if interactive:
        fig.show()
    else:
        fig.write_image("graphs/hist.png")
    
def inverseDynamicMod(value):
    return 2 ** (value/2) -1  #TODO: ASK TEACHER ABOUT THIS

if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--source",help="input data json file", default="results.json")
    parser.add_argument('--interactive', dest='interact', action='store_true')
    parser.set_defaults(interact=False)
    args = parser.parse_args()
    f = open(args.source,"r")
    data = json.load(f)
    f.close()
    results = {}
    for name,info in data.items():
        info = upscaleValues(info,16,inverseDynamicMod,[inverseDynamicMod(x) for x in range(101)])
        results[name] = getStats(info)
    if not args.interact:
        if not os.path.exists("graphs"):
            os.mkdir("graphs")    
    drawLineGraphs(results,args.interact)
    drawBarGraphs(data,args.interact)