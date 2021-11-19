calls=0

def r1(x):
    global calls
    calls+=1
    if x==0: return 0
    return 1+ r1(x-1)

def r2(x):
    global calls
    calls+=1
    if x==0: 
        return 0
    if x==1: 
        return 1
    return x+ r2(x-2)

def r3(x):
    global calls
    calls+=1
    if x==0:
        return 0
    return 1+2*r3(x-1)


def r4(x):
    global calls
    calls+=1
    if x==0:
        return 0
    return 1+r4(x-1)+r4(x-1)


print("R1:")
for x in range (1,9):
    calls=0
    print(x,r1(x),calls)
print("\n")

print("R2:")
for x in range (1,9):
    calls=0
    print(x,r2(x),calls)
print("\n")

print("R3:")
for x in range (1,9):
    calls=0
    print(x,r3(x),calls)
print("\n")

print("R4:")
for x in range (1,9):
    calls=0
    print(x,r4(x),calls)
print("\n")