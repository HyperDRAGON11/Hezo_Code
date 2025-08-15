import tkinter as tk
import random

class GuessingGame:
    def __init__(self, master):
        self.master = master
        master.title("Guess the Number Game")
        master.title("Sim Py Game® BETA™")
        master.geometry("300x200")

        self.number = random.randint(1, 100)
        self.attempts = 0

        self.label = tk.Label(master, text="Guess a number between 1 and 100:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.lable = tk.Label(master, text="A Sim Py Game® developed by Abhir b", font=("Arial", 8))
        self.label.pack(pady=10)

        self.entry = tk.Entry(master, font=("Arial", 12))
        self.entry.pack()

        self.guess_button = tk.Button(master, text="Guess", command=self.guess, font=("Arial", 12))
        self.guess_button.pack(pady=10)

        self.result_label = tk.Label(master, text="", font=("Arial", 12), fg="blue")
        self.result_label.pack()

    def guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1

            if guess < self.number:
                self.result_label.config(text=f"Higher than {guess}! Try again.") # Modified to show the guess
            elif guess > self.number:
                self.result_label.config(text=f"Lower than {guess}! Try again.") # Modified to show the guess
            else:
                self.result_label.config(text=f"Congratulations! You guessed the number in {self.attempts} attempts.")
                self.guess_button.config(state=tk.DISABLED) # Disable the button after correct guess
        except ValueError:
            self.result_label.config(text="Invalid input. Please enter a number.")

root = tk.Tk()
game = GuessingGame(root)
root.mainloop()