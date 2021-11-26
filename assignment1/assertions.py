import pandas as pd
import numpy as np

if __name__=="__main__":
    results = pd.read_csv("results.csv",header=0)
    exhaustive = results.loc[results["solution method"]=="exhaustive"]
    greedy = results.loc[results["solution method"]=="greedy"]
    
    #check total solution equation
    exhaustive["bad math"] = np.where(2**(exhaustive['edges'])-1 != exhaustive['solutions seen'],1,0)
    error = exhaustive["bad math"].sum()
    if error:
        raise ValueError("math for solution count was wrong")
    
    exhaustive = exhaustive.drop("bad math", axis=1)

    #check total add equation
    exhaustive["bad math"] = np.where(2**(exhaustive['edges'])*exhaustive['edges'] != exhaustive['adds'],1,0)
    error = exhaustive["bad math"].sum()
    if error:
        print(exhaustive)
        raise ValueError("math for set add count was wrong")