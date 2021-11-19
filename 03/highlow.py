import random

guess = -1
while 1:
    number = random.randrange(1,100)
    print("New number generated, start guessing")
    while guess!=number:
        guess = int(input("Provide a number: "))
        if guess==number:
            print("Congratulations")
        if guess<number:
            print("Too low")
        if guess>number:
            print("Too high")
