target =100
adds = 0
seen = {0:0,1:1}

def fib(number):
    global adds
    if number not in seen:
        adds+=1
        seen[number]=fib(number-2)+fib(number-1)
    return seen[number]

def fib_array(number,known=[0,1]): #should be iterative instead, oh well
    if number>=len(known):
        global adds
        adds+=1
        known.append(fib_array(number-2,known)+fib_array(number-1,known))
    return known[number]
       
def fib_array_iterative(number,known=[0,1]):
    if number<=len(known)-1:
        return known[number]
    for n in range(len(known),number+1):
        global adds
        adds+=1
        known.append(known[n-2]+known[n-1])
    return known[number]

def fib_3vars(number):
    x,y = 0,1
    global adds
    for n in range(2,number+1):
        adds+=1
        t = x+y
        x,y = y,t
    return t

print(target,fib(target),adds)
adds=0
print(target,fib_array(target),adds)
adds=0
print(target,fib_array_iterative(target),adds)
adds=0
print(target,fib_3vars(target),adds)