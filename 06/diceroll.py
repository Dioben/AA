import random
import math


def rollUntilRepeat(min,max):
    values = []
    while True:
        val = dXroll(min,max)
        if val in values:
            values.append(val)
            break
        values.append(val)
    return values

def rollUntilAll(min,max):
    values = []
    while True:
        val = dXroll(min,max)
        values.append(val)
        if len(set(values))==max-min:
            break
        
    return values

def rollUntilAllBiased(weights):
    values = []
    rollrange = sum(weights.values())
    constsort = sorted(weights.items())
    done=False
    while not done:
        val = random.randint(0,rollrange)
        cum = 0
        for x,y in constsort:#sorted for consistency
            cum+=y
            if cum>=val:
                values.append(x)
                if len(set(values))==len(constsort):
                    done=True
                break
    return values



def rollUntilRepeatBiased(weights):
    values = []
    rollrange = sum(weights.values())
    constsort = sorted(weights.items())
    done=False
    while not done:
        val = random.randint(0,rollrange)
        cum = 0
        for x,y in constsort:#sorted for consistency
            cum+=y
            if cum>=val:
                if x in values:
                    done=True
                values.append(x)
                break
    return values



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
    values = []
    rollrange = sum(weights.values())
    constsort = sorted(weights.items())
    for x in range(count):
        val = random.randint(0,rollrange)
        cum = 0
        for x,y in constsort:#sorted for consistency
            cum+=y
            if cum>=val:
                values.append(x)
                break
    return values
def mapXrolls(min,max,len):
    events = {}
    for i in range(int(1e7)):
        rolls = tuple(rollMultiple(min,max,len))
        if rolls not in events:
            events[rolls]=1
        else:
            events[rolls]+=1
    return events


def mapXrollsBiased(probs,len):
    events = {}
    for i in range(int(1e7)):
        rolls = tuple(rollMultipleWeights(probs,len))
        if rolls not in events:
            events[rolls]=1
        else:
            events[rolls]+=1
    return events

def transformEventsToRollCount(events,counted):
    mapped = {}
    for x,y in events.items():
        ind = x.count(counted)
        if ind in mapped:
            mapped[ind]+=y
        else:
            mapped[ind]=y
    return mapped
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
        '''
    '''
    events = mapXrollsBiased({0:1,1:2},15)

    mapped = transformEventsToRollCount(events,1)
    for x in sorted(mapped.keys()):
        print(x,"=>",mapped[x],",",mapped[x]/1e7)
    '''
    '''
    #birthday paradox
    rollstorepeat={}
    for x in range(10000):
        rolls=len(rollUntilRepeat(1,366))
        if rolls in rollstorepeat:
            rollstorepeat[rolls]+=1
        else:
            rollstorepeat[rolls]=1

    percentadd=0
    for x,y in sorted(rollstorepeat.items()):
        print(x," => ",y,",",y/10000)
        percentadd+=y/10000
        if percentadd>=.5:
            print("This is the 50% milestone")
            percentadd=-100#will never reach .5 again
    '''