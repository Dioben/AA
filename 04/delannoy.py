def calc(x,y):
    if (x,y) in calc.known:
        return calc.known[(x,y)]
    if x==0 or y==0:
        calc.known[(x,y)]=1
        calc.known[(y,x)]=1
        return 1
    res = calc(x-1,y-1)+calc(x-1,y)+calc(x,y-1)
    calc.known[(x,y)]=res
    calc.known[(y,x)]=res
    return res
calc.known = {}

def calc_v2(m, n):
    array = [[1 for _ in range(n+1)]]
    array.extend([[1] for _ in range(m+1)])
    calc_v2.num_adds = 0
    for mi in range(1, m+1):
        for ni in range(1, n+1):
            calc_v2.num_adds += 1
            array[mi].append(array[mi-1][ni] + array[mi-1][ni-1] + array[mi][ni-1])
    return array[m][n]

if __name__ =="__main__":
    print(calc(20,20))