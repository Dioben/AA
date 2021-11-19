import random

number = random.randrange(1,100)
print(f"New number generated, is {number}")
guess = 50
guesses = [50]

lowbound = 1
highbound=100

while guess!=number:            
        if guess<number:
            lowbound=guess
        if guess>number:
            highbound=guess
        guess =  (lowbound+highbound)//2
        guesses.append(guess)
        
print(">".join([str(x) for x in guesses]))
exit()