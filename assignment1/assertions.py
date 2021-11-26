import pandas as pd
import numpy as np
import math
pd.options.mode.chained_assignment = None


def calc_greedy_sol_limit(row):
    return sum(math.comb(row['edges'],x) for x in range(1,math.floor(row['nodes']/2)+1))

def calc_greedy_add_limit(row):
    return 2*sum(math.comb(row['edges']*x,x) for x in range(1,math.floor(row['nodes']/2)+1))


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
        raise ValueError("math for set add count was wrong")

    
    #doing it again for greedy now

    greedy['max sols'] = greedy.apply(lambda row: calc_greedy_sol_limit(row),axis=1)
    greedy['max adds'] = greedy.apply(lambda row: calc_greedy_add_limit(row),axis=1)
    greedy["bad math"] = np.where(greedy['solutions seen']> greedy["max sols"],1,0)
    error = greedy["bad math"].sum()
    if error:
        raise ValueError("greedy math for solution count was proven wrong")
    greedy = greedy.drop("bad math",axis=1)
    
    greedy["bad math"] = np.where(greedy['adds']> greedy["max adds"],1,0)
    error = greedy["bad math"].sum()
    if error:
        raise ValueError("greedy math for add count was proven wrong")