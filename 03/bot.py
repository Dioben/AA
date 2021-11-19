dists = {0:0,1:1,2:2,3:4}
target = 15

def calculate_possibilities(target):
    if target not in dists:
        dists[target] = calculate_possibilities(target-3)+calculate_possibilities(target-2)+calculate_possibilities(target-1) 
    return dists[target]


def calculate_possibilities_array(number,known=[0,1,2,4]):
    if number>=len(known):
        known.append(calculate_possibilities_array(number-1,known)+calculate_possibilities_array(number-2,known)+calculate_possibilities_array(number-3,known))
    return known[number]

def poss_4vars(number):
    x,y,z = 1,2,4
    for n in range(4,number+1):
        t = y+z+x
        x,y,z = y,z,t
    return t

print(target,calculate_possibilities(target))
print(target,calculate_possibilities_array(target))
print(target,poss_4vars(target))
