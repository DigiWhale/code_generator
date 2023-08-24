import random

def generate_clue(number, clue_type):
    digits = list(str(number))
    guess = list(str(number))
    if clue_type == 0:  # One number is correct and well placed.
        correct_index = random.choice([0, 1, 2])
        for i in range(3):
            if i != correct_index:
                while guess[i] == digits[i] or guess[i] in digits:
                    guess[i] = str(random.randint(0, 9))
    elif clue_type == 1:  # Nothing is right.
        for i in range(3):
            while guess[i] == digits[i]:
                guess[i] = str(random.randint(0, 9))
    elif clue_type == 2:  # One number is correct but wrongly placed.
        correct_index = random.choice([0, 1, 2])
        wrong_positions = [i for i in range(3) if i != correct_index]
        swap_position = random.choice(wrong_positions)
        guess[correct_index], guess[swap_position] = guess[swap_position], guess[correct_index]
        for i in wrong_positions:
            if i != swap_position:
                while guess[i] == digits[i] or guess[i] in digits:
                    guess[i] = str(random.randint(0, 9))
    elif clue_type == 3:  # Two numbers are correct but wrongly placed.
        incorrect_index = random.choice([0, 1, 2])
        positions = [0, 1, 2]
        positions.remove(incorrect_index)
        guess[positions[0]], guess[positions[1]] = guess[positions[1]], guess[positions[0]]
        while guess[incorrect_index] == digits[incorrect_index] or guess[incorrect_index] in digits:
            guess[incorrect_index] = str(random.randint(0, 9))

    return ''.join(guess)

def generate_puzzle(number):
    clues_order = [0, 1, 2, 3]
    random.shuffle(clues_order)
    puzzle = [generate_clue(number, clue) for clue in clues_order]

    hints = [
        "One number is correct and well placed.",
        "Nothing is right.",
        "One number is correct but wrongly placed.",
        "Two numbers are correct but wrongly placed."
    ]

    for i in range(4):
        print(puzzle[i], "-", hints[clues_order[i]])

number = 573
generate_puzzle(number)
