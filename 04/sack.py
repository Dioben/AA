from itertools import combinations


def sack_combs(array,max):
    costs = sorted([x[0] for x in array])
    add_cost = 0
    elements = 0
    for x in costs:
        add_cost+=x
        if add_cost>=max:
            break
        elements+=1
        
    poss = set()
    for x in range(1,elements+1):
        poss.update(set(combinations(arr,x)))
    
    best = 0
    chosen = None
    for x in poss:
        cost = sum([ y[0] for y in x])
        if cost>max:
            continue
        value = sum([ y[1] for y in x])
        if value>best:
            best = value
            chosen = x
    return best,chosen


def sack_combs_v3(array,max):
    if len(array)==0:
        return []
    current = array[0]
    inc = []
    if max>=current[0]:
        if len(array)==1:
            return [current]
        inc = [current] + sack_combs_v3(array[1:],max-current[0])
    exc = sack_combs_v3(array[1:],max)
    incval = sum([x[1] for x in inc])
    excval = sum([x[1] for x in exc])
    if incval>excval:
        return inc
    else:
        return exc

def sack_combs_v4(array,max):
    states = [(0,0,[])]#cost,value,nodes
    for x in array:
        states+= [(y[0]+x[0],y[1]+x[1],y[2]+[x]) for y in states if y[0]+x[0]<=max]
    return sorted(states,key=lambda x:x[1],reverse=True)[0]

arr= [(7,42),(3,12),(4,40),(5,25)]

print(sack_combs(arr,10))
print(sack_combs_v3(arr,10))
print(sack_combs_v4(arr,10))