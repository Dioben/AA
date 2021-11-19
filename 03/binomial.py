from math import ceil
target = 9,3
seen={}
sums=0
def calc_binomial(targetx,targety):
    if targety==0:
        return 1
    if targetx==targety:
        return 1
    if (targetx,targety) not in seen:
        seen[(targetx,targety)] = calc_binomial(targetx-1,targety)+calc_binomial(targetx-1,targety-1)
    return seen[(targetx,targety)]

def calc_binomial_matrix(targetx,targety):
    if targety>targetx//2: #symmetrical
        targety= targetx-targety
    if not known[targetx][targety]:
        var2 = calc_binomial_matrix(targetx-1,targety-1)
        var1 = calc_binomial_matrix(targetx-1,targety)
        global sums
        sums+=1
        known[targetx][targety] = var1+var2
    return known[targetx][targety]


known=[[None for y in range(ceil(x/2)+1)] for x in range(target[0]+1) ]
for x in range(len(known)):
    known[x][0]=1

for x in range(1,len(known)):
    known[x][1]=x

def calc_binomial_1D(targetx,targety):
    if targety>=targetx/2: #symmetrical
        targety= targetx-targety
    indexcalc = sum( [ceil((x+1)/2) for x in range(targetx) ] )+targety
    if not known1D[indexcalc]:
        var1  = calc_binomial_1D(targetx-1,targety-1)
        var2 = calc_binomial_1D(targetx-1,targety)
        global sums
        sums+=1
        known1D[indexcalc] =  var1+var2
    return known1D[indexcalc]

oneDspots = sum( [ceil((x+1)/2) for x in range(target[0]+1) ] )
known1D= [None for x in range(oneDspots)]
for x in range(target[0]+1):
    startidx = sum( [ceil((y+1)/2) for y in range(x) ] )
    known1D[startidx]=1
    if x>1:
        known1D[startidx+1]=x



print(calc_binomial(target[0],target[1]))
print(calc_binomial_matrix(target[0],target[1]))
print("sums ",sums)
sums=0

print(calc_binomial_1D(target[0],target[1]))
print("sums ",sums)