import random
import tkinter as tk
from tkinter import ttk

def evaluate_guess(target, guess):
    target_digits = list(str(target))
    guess_digits = list(str(guess))

    correct_well_placed = sum([1 for i in range(3) if target_digits[i] == guess_digits[i]])
    correct_wrongly_placed = sum([1 for i in range(3) if guess_digits[i] in target_digits]) - correct_well_placed
    not_in_code = 3 - correct_well_placed - correct_wrongly_placed

    hint_map = {
        (1, 0, 2): "One number is correct and well placed, the other two are not in the code.",
        (2, 0, 1): "Two numbers are correct, one is well placed, the other is not in the code.",
        (1, 1, 1): "One number is correct and well placed, the second one is wrongly placed, the third is not in the code.",
        (1, 0, 0): "One number is correct and well placed.",
        (2, 0, 0): "Two numbers are correct and both are well placed.",
        (3, 0, 0): "All numbers are correct and well placed.",
        (0, 0, 3): "Nothing is right.",
        (0, 1, 2): "One number is correct but wrongly placed.",
        (0, 2, 1): "Two numbers are correct but wrongly placed.",
        (0, 3, 0): "All numbers are correct but wrongly placed.",
        (1, 1, 0): "Two numbers are correct, one is well placed, the other is wrongly placed.",
        (0, 2, 0): "Two numbers are correct but both are wrongly placed.",
        (2, 1, 0): "Two numbers are correct, one is well placed, the other is wrongly placed.",
        (0, 0, 2): "Two numbers are not in the code, the third is wrongly placed.",
        (0, 0, 1): "Two numbers are not in the code, the third is correctly placed.",
        (0, 1, 1): "One number is not in the code, the other two are wrongly placed.",
        (1, 0, 1): "One number is not in the code, the other two are correctly placed.",
        (0, 1, 0): "One number is correct but wrongly placed, the other two are not in the code.",
        (2, 0, 0): "Two numbers are correct and both are well placed.",
        (1, 2, 0): "One number is correct and well placed, the other two are wrongly placed."
    }

    return hint_map.get((correct_well_placed, correct_wrongly_placed, not_in_code))

def generate_puzzle(target):
    all_numbers = list(range(100, 1000))  # All 3-digit numbers
    random.shuffle(all_numbers)  # Shuffle them randomly

    seen_hints = set()  # To keep track of unique hints
    result = []

    for guess in all_numbers:
        if len(result) >= 4:
            break  # We only need 4 unique hints

        hint = evaluate_guess(target, guess)

        # If the hint is unique and not empty, add it
        if hint and hint not in seen_hints:
            seen_hints.add(hint)
            result.append(f"{guess} - {hint}")

    return result



def on_generate_click():
    number = int(number_entry.get())
    hints_listbox.delete(0, tk.END)
    hints = generate_puzzle(number)
    for hint in hints:
        hints_listbox.insert(tk.END, hint)

app = tk.Tk()
app.title('Crack the Code Generator')

frame = ttk.Frame(app, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

number_label = ttk.Label(frame, text="Enter 3-digit number:")
number_label.grid(row=0, column=0, sticky=tk.W, pady=5)

number_entry = ttk.Entry(frame, width=5)
number_entry.grid(row=0, column=1, pady=5, padx=5)
number_entry.insert(0, "573")  # Default number

generate_btn = ttk.Button(frame, text="Generate Hints", command=on_generate_click)
generate_btn.grid(row=1, column=0, columnspan=2, pady=5)

hints_listbox = tk.Listbox(frame, width=80, height=4)
hints_listbox.grid(row=2, column=0, columnspan=2, pady=5)

app.mainloop()
