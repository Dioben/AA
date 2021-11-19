import random
import math

def dXroll(min,max):
    return min + math.floor(random.random()*(max+1-min))

def biasedChoiceRoll(probs):
    range = sum(probs.values())
    val = random.randint(0,range)
    cum = 0
    for x,y in sorted(probs.items()):#sorted for consistency
        cum+=y
        if cum>=val:
            return x

def rollMultiple(min,max,count):
    return [dXroll(min,max) for _ in range(count)]

def rollMultipleWeights(weights,count):
    return [biasedChoiceRoll(weights) for _ in count] 

if __name__ == "__main__":
    '''
    events = {}
    for i in range(int(1e7)):
        r = dXroll(1,6)
        if r in events:
            events[r]+=1
        else:
            events[r] =1

    print("equal prob diceroll: ",sorted(events.items()))
    print("total score is: ",sum(x*y for x,y in events.items()) )
    probs = {1:2,2:1,3:1,4:1,5:1,6:1}
    events = {}
    for i in range(int(1e7)):
        r = biasedChoiceRoll(probs)
        if r in events:
            events[r]+=1
        else:
            events[r] =1
    print("weighted dice toss: ",sorted(events.items()))
    print("total score is: ",sum(x*y for x,y in events.items()) )
    '''
    '''
    #red/green coin toss game
    events = [0,0]
    for i in range(int(1e7)):
        r = dXroll(1,6)
        g = dXroll(1,6)
        if r>g:
            events[1]+=1
        else:
            events[0]+=1
    print("red ([1]) does not pay off, ",events)

    #total eyes guessing game
    balance=0
    for i in range(int(1e7)):
        r = dXroll(1,6)
        g = dXroll(1,6)
        if r+g==12:
            balance+=12
        else:
            balance-=1
    print("does picking 12 constantly pay off?, ",balance)
        '''
    events= {}
    for i in range(int(1e7)):
        c = dXroll(0,1)
        if c:
            c = "g"
        else:
            c = "r"
        r = dXroll(1,6)
        if (c,r) in events:
            events[(c,r)]+=1
        else:
            events[(c,r)]=1
    for x in sorted(events):
        print(x,events[x])