import argparse
import json
from math import sqrt
import plotly.express as px
import pandas as pd
import os




def getErrorStats(real,other):
    max_err_abs,max_err_rel = getDiffs(real,other)

    N = len(other.keys())
    
    avg_err = sum([other[x] - real[x] for x in other.keys()]) / N
    squaresum =  sum([ (other[x] - real[x])**2 for x in other.keys()])
    deviation = sqrt( squaresum/ N )

    return max_err_abs , max_err_rel, avg_err, deviation

def getDiffs(real,list):
    max = percent_max= 0
    for word,value in real.items():
        value2 = list[word]
        delta = value2 - value #always gte 0
        percent_delta = delta/value*100
        if max<delta:
            max = delta
        if percent_max<percent_delta:
            percent_max = percent_delta
    return max,percent_max


    

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
 
if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--source",help="input data json file", default="results.json")
    parser.add_argument('--interactive', dest='interact', action='store_true')
    parser.set_defaults(interact=False)
    args = parser.parse_args()
    with open(args.source,"r") as f:
        data = json.load(f)

    results = []
    for lang, info in data.items():
        real = info["real"]
        sketches = info["sketch"]
        for sketch in sketches:
            hashcount = sketch["hashes"]
            slots = sketch['size']
            max_err_abs , max_err_rel, avg_err, deviation = getErrorStats(real,sketch['values'])
            results.append(
                {"Language":lang,"Hashes":hashcount,"Slots":slots,"Max Absolute Error":max_err_abs,
                "Max Relative Error":max_err_rel,"Average Absolute Error":avg_err,"Average Deviation":deviation}
                )
    if not args.interact:
        if not os.path.exists("graphs"):
            os.mkdir("graphs")    
    for x in results[:10]:
        print(x)
    print("...")
    for x in results[-10:]:
        print(x)
    #draw3DScatters(results,args.interact)