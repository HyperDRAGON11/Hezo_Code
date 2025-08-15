import tkinter as tk
import random

def generate_number():
    num = random.randint(100, 999)

root = tk.Tk()
root.title("Random 3-Digit Number Generator")
root.geometry("300x150")

generate_btn = tk.Button(root, text="Generate 3-Digit Number", command=generate_number, font=("Arial", 12))
generate_btn.pack(pady=20)

result_label = tk.Label(root, text="", font=("Arial", 18), fg="blue")
result_label.pack(pady=10)

gus=input("Guess the no. :")
if gus <= num:
     result_label.config(text="more than ", str(gus))
elif gus >= num:
     result_label.config(text="less than ", str(gus))
else:
    result_label.config(text="correct guess!")
    
root.mainloop()
