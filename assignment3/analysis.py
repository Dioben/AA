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
    avg_rel_err = sum([ (other[x] - real[x])/real[x] for x in other.keys()]) / N
    squaresum =  sum([ (other[x] - real[x])**2 for x in other.keys()])
    deviation = sqrt( squaresum/ N )

    return max_err_abs , max_err_rel, avg_err,avg_rel_err, deviation

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


    

def drawPostScatters(data,interactive):
    df = pd.DataFrame(data)
    for metric in ["Max Absolute Error","Max Relative Error","Average Absolute Error","Average Deviation","Average Relative Error"]:
        fig = px.scatter_3d(df,color="Language",x="Hashes",y="Slot Ratio",z=metric)
        fig.update_layout(title_text=metric, title_x=0.5)
        if interactive:
            fig.show()
        else:
            fig.write_image(f"graphs/{metric}.png")
            for lang in df['Language'].unique():  #these are not necessary in interative view because interactive mode can be real time filtered
                subdf = df.loc[df['Language']==lang]
                fig = px.scatter_3d(subdf,x="Hashes",y="Slot Ratio",z=metric)
                fig.update_layout(title_text=f"{lang} - {metric}", title_x=0.5)
                fig.write_image(f"graphs/{lang}{metric}.png")
    

def plotSnapshotGraphs(data,interactive):
    df = pd.DataFrame(data)
    for metric in ["Overlapping Words","Word Matches"]:
        fig = px.scatter_3d(df,color="Language",x="Hashes",y="Slot Ratio",z=metric)
        fig.update_layout(title_text=metric, title_x=0.5)
        if interactive:
            fig.show()
        else:
            fig.write_image(f"graphs/{metric}.png")
            for lang in df['Language'].unique():  #these are not necessary in interative view because interactive mode can be real time filtered
                subdf = df.loc[df['Language']==lang]
                fig = px.scatter_3d(subdf,x="Hashes",y="Slot Ratio",z=metric)
                fig.update_layout(title_text=f"{lang} - {metric}", title_x=0.5)
                fig.write_image(f"graphs/{lang}{metric}.png")


 
if __name__ == "__main__":
    parser= argparse.ArgumentParser()
    parser.add_argument("--source",help="input data json file", default="results.json")
    parser.add_argument('--interactive', dest='interact', action='store_true')
    parser.set_defaults(interact=False)
    args = parser.parse_args()
    with open(args.source,"r") as f:
        data = json.load(f)

    results = []
    topX = []
    for lang, info in data.items():
        real = info["real"]
        sketches = info["sketch"]
        for sketch in sketches:
            hashcount = sketch["hashes"]
            slots = sketch['size']
            max_err_abs , max_err_rel, avg_err,avg_rel_err, deviation = getErrorStats(real,sketch['values'])
            results.append(
                {"Language":lang,"Hashes":hashcount,"Slot Ratio":slots,"Max Absolute Error":max_err_abs,
                "Max Relative Error":max_err_rel,"Average Absolute Error":avg_err,"Average Relative Error":avg_rel_err,"Average Deviation":deviation}
                )
        topcounts = info['snapshot']
        realTop100 = sorted(real.keys(), key=lambda x:real[x], reverse=True)[:100]
        top100set = set(realTop100)
        for snapshot in topcounts:
            top = snapshot['values']
            count = 0
            for i in range(100):
                if realTop100[i]==top[i]:
                    count +=1
            overlap = len( top100set.intersection(top))/100
            topX.append({"Language":lang,"Hashes":snapshot["hashes"],"Slot Ratio":snapshot["size"],"Overlapping Words":overlap,"Word Matches": count/100})
    if not args.interact:
        if not os.path.exists("graphs"):
            os.mkdir("graphs")    
    drawPostScatters(results,args.interact)
    plotSnapshotGraphs(topX,args.interact)