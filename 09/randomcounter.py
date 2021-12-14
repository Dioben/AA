import random
import plotly.express as px
import math

def randCounter(p=0.5):
    return random.random()<=p
    


counters = []
for _ in range(10000):
    val = 0
    for i in range(100):
        val+=randCounter(1/32)
    counters.append(val)

hist = px.histogram(counters,labels={'x':'value', 'y':'count'})
hist.update_xaxes(range=[0,100])
hist.show()

mean = sum(counters)/len(counters)
std = math.sqrt( sum([(x-mean)**2 for x in counters]) /len(counters))
variance = sum([(x-mean)**2 for x in counters]) / (len(counters)-1)

print(mean,std,variance)