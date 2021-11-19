def bernv1(t,x,y):
    if t<0 or t>1:
        raise ValueError("come on man")
    if x==0 and y==0:
        return 1
    if x==y:
        return t**x
    if y==0:
        return (1-t)**x
    return (1-t)*bernv1(x-1,y,t)+t*bernv1(x-1,y-1,t)

print(bernv1(0.75,7,7))