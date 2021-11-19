def f1(x):
    return x,sum([i for i in range(x+1)])

def f2(x):
    i = 0
    for i1 in range(1,x+1):
        for i2 in range(1,x+1):
            i =  i+1
            
    return x,i
def f3(x):
    i=0
    for i1 in range(1,x+1):
        for i2 in range(i1,x+1):
            i = i + 1
    return x,i

def f4(x):
    i=0
    for i1 in range(1,x+1):
        for i2 in range(1,i1+1):
            i =  i+i2
    return x,i

print("F1:")
for x in range (1,9):
    print(f1(x))
print("\n")

print("F2:")
for x in range (1,9):
    print(f2(x))
print("\n")

print("F3:")
for x in range (1,9):
    print(f3(x))
print("\n")

print("F4:")
for x in range (1,9):
    print(f4(x))
print("\n")