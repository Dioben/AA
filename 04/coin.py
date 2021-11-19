def coin_recursive(array):
    if not array:
        return 0
    if len(array)==1:
        return array[0]
    return max([array[0]+coin_recursive(array[2:]),coin_recursive(array[1:])]) 


def coin_array(array):
    if len(array)==0:
        return 0
    if len(array)<3:
        return max(array)
    sols = [0,array[0]] #dont pick or pick first for now
    for x in range(1,len(array)):
        sols.append(max(array[x]+sols[-2],sols[-1]))
    print(sols)
    return sols[-1]




arr = [5,1,2,10,6,2]

print(coin_recursive(arr))
print(coin_array(arr))
