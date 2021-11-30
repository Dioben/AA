import random
def is_prime( P, K ): # P > 3
    for  i in range(K):
    # Repeating Fermat’s test
        a = random.randint( 2, P - 2 )
        if(  a ** (P - 1) % P != 1 ):
            return False # Composite !
    return True # PROBABLY prime !


print(is_prime(1123,100))