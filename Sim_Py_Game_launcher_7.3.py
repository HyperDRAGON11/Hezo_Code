import tkinter as tk
import random

class GuessingGame:
    def __init__(self, master):
        self.master = master
        self.number = random.randint(1, 100)
        self.attempts = 0

        self.label = tk.Label(master, text="Guess a number between 1 and 100:", font=("Arial", 12))
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
                self.result_label.config(text=f"Higher than {guess}! Try again.")
            elif guess > self.number:
                self.result_label.config(text=f"Lower than {guess}! Try again.")
            else:
                self.result_label.config(text=f"Congratulations! You guessed the number in {self.attempts} attempts.")
                self.guess_button.config(state=tk.DISABLED)
        except ValueError:
            self.result_label.config(text="Invalid input. Please enter a number.")

    def reset(self):
        self.number = random.randint(1, 100)
        self.attempts = 0
        self.result_label.config(text="")
        self.entry.delete(0, tk.END)
        self.guess_button.config(state=tk.NORMAL)

class CoinFlipGame:
    def __init__(self, master):
        self.master = master
        self.label = tk.Label(master, text="Flip a Coin!", font=("Arial", 12))
        self.label.pack(pady=10)

        self.lable = tk.Label(master, text="Heads or Tails?(H/T):", font=("Arial", 12))
        self.lable.pack(pady=10)

        self.entry = tk.Entry(master, font=("Arial", 12))
        self.entry.pack()

        self.flip_button = tk.Button(master, text="Flip", command=self.flip, font=("Arial", 12))
        self.flip_button.pack(pady=10)

        self.result_label = tk.Label(master, text="", font=("Arial", 12), fg="blue")
        self.result_label.pack()

    def flip(self):
        result = random.choice(["Heads", "Tails"])
        self.result_label.config(text=result)
    def dgus(self, master):
        dgus = self.label
        if dgus == flip:
            self.lable = tk.Label(master, text="You Win!", font=("Arial", 12), fg="blue")
            self.lable.pack(pady=10)
        elif dgus != flip:
            self.lable = tk.Label(master, text="You lose!", font=("Arial", 12), fg="blue")
            self.lable.pack(pady=10)
        else:
            self.label = tk.Label(master, text="Invalid Input! Please enter values H or T!", font=("Arial", 12), fg="blue")
            self.label.pack(pady=10)

class GameLauncher:
    def __init__(self, master):
        self.master = master
        master.title("Sim Py Game® RunR™ 7")
        master.geometry("300x200")

        self.guessing_game_button = tk.Button(master, text="Guessing Game", command=self.launch_guessing_game, font=("Arial", 12))
        self.guessing_game_button.pack(pady=10)

        self.coin_flip_game_button = tk.Button(master, text="Coin Flip Game", command=self.launch_coin_flip_game, font=("Arial", 12))
        self.coin_flip_game_button.pack(pady=10)

        self.lable = tk.Label(master, text="Sim Py Game® RunR™ 7 developed by Abhir b", font=("Arial", 10))
        self.lable.pack(pady=10)

        self.lable = tk.Label(master, text="Version 1.2", font=("Arial", 8))
        self.lable.pack(pady=10)

    def launch_guessing_game(self):
        self.new_window = tk.Toplevel(self.master)
        self.new_window.geometry("300x250")
        self.guessing_game = GuessingGame(self.new_window)
        reset_button = tk.Button(self.new_window, text="Reset Game", command=self.guessing_game.reset, font=("Arial", 12))
        reset_button.pack(pady=10)

    def launch_coin_flip_game(self):
        self.new_window = tk.Toplevel(self.master)
        self.new_window.geometry("300x200")
        self.coin_flip_game = CoinFlipGame(self.new_window)

root = tk.Tk()
launcher = GameLauncher(root)
root.mainloop()
