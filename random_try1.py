import random

result = random.choice(["heads", "tails"])
cho = input("heads or tails? (Please don't use even a single capital words) :")
if cho == result:
    print("The coin has a ", result, "You win!")
    print("Coin result :", result)
elif cho != result:
    print("The coin has a ", result, "You lose!")
    print("Coin result:", result)
else:
    print("Invalid Input!")
