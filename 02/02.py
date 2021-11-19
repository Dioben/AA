from math import floor

def BF_POW_IT(x,pow):
    it = 0
    base = x
    for i in range(pow-1):
        it+=1
        x*= base
    return x,it

def BF_POW_REC(x,pow,it=0,carry=1):
    it+=1
    if pow==0:
        return carry,it
    pow-=1
    carry*=x
    return BF_POW_REC(x,pow,it,carry)

def DAC_POW(x,pow):
    global it
    it+=1
    if pow==0:
        return 1
    if pow==1: 
        return x
    return DAC_POW(x,floor(pow/2))*DAC_POW(x,floor((pow+1)/2))


def DecAC_POW(x,pow):
    global it
    it+=1
    if pow==0:
        return 1
    if pow==1: 
        return x
    if pow%2==0:
        reshalf = DecAC_POW(x,pow/2)
        return reshalf*reshalf
    else:
        reshalf = DecAC_POW(x,floor(pow/2))
        return reshalf*reshalf*x

print(BF_POW_IT(2,10))
print(BF_POW_REC(2,10))

it=0
print((DAC_POW(2,10),it))


it=0
print((DecAC_POW(2,10),it))