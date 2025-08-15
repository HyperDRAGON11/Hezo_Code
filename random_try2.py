import random

for i in range(100):
    rno = random.randint(1, 100)
    guess = int(input("Guess a number between 1 and 100 :"))
    if guess == rno:
        print("Congralituation, You win!")
    elif guess >= rno:
        print("Smaller than ", guess)
    elif guess <= rno:
        print("greater than ", guess)
    else:
        print("invalid input!")

        
    
