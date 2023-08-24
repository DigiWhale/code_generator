from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# ... [keep your evaluate_guess and generate_puzzle functions here]
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
  
@app.route('/', methods=['GET', 'POST'])
def index():
    hints = None
    if request.method == 'POST':
        number = request.form.get('number', type=int)
        hints = generate_puzzle(number)
    return render_template('index.html', hints=hints)

if __name__ == '__main__':
    app.run(debug=True)
