from flask import Flask, render_template, request, redirect, url_for
import random
import os
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# ... [keep your evaluate_guess and generate_puzzle functions here]
def overlay_text_on_image(image_path='codecracktemplate.png', text='', position=(100, 100), font_path="path_to_font.ttf"):
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, 30)  # Set font size to 30, modify as needed
        draw.text(position, text, font=font, fill="white")  # Fill can be adjusted to desired text color
        img.save("output_image.png")

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

def generate_puzzle(target = 111, design = "design1"):
    all_numbers = list(range(100, 1000))  # All 3-digit numbers
    random.shuffle(all_numbers)  # Shuffle them randomly

    seen_hints = set()  # To keep track of unique hints
    hints_dict = {}

    for guess in all_numbers:
        if len(hints_dict) >= 4:
            break  # We only need 4 unique hints

        hint = evaluate_guess(target, guess)
        # If the hint is unique and not empty, add it
        if hint and hint not in seen_hints:
            print(f"Guess: {guess}, Hint: {hint}")
            seen_hints.add(hint)
            hints_dict[guess] = hint

    # Once hints are generated, overlay them on the image
    image_path = overlay_hints_on_image(hints_dict, target, design)
    print(hints_dict)
    return hints_dict, image_path

def wrap_text_approx(text, max_chars):
    """
    This function wraps the text based on a given maximum number of characters.
    """
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + word) <= max_chars:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    
    if current_line:
        lines.append(current_line.strip())
    
    return lines

def overlay_hints_on_image(hints_dict, usednumber, design):
    # Load your selected design image
    design_image_path = f"static/designs/{design}.png"  # Update the path accordingly
    img = Image.open(design_image_path)
    draw = ImageDraw.Draw(img)

    # Use a basic font bundled with PIL, or you can use any other TTF font
    number_font = ImageFont.truetype("arial.ttf", 70)
    text_font = ImageFont.truetype("arial.ttf", 30)

    # Determine starting position
    x, y = 150, 320
    spacing_between_hints = 50
    line_space = 375 - spacing_between_hints  # <-- Adjust this based on your font and image width
    max_width = 500  # <-- Adjust this based on your desired max width
    some_offset_value = 370  # <-- Adjust this based on where you want the hint to start relative to the digits 
    digit_spacing = 120
    for key, value in hints_dict.items():
      # Split the three-digit number
      digits = [int(d) for d in str(key)]

      # Draw digits
      draw.text((x, y), f"{digits[0]}", font=number_font, fill="black")
      draw.text((x + digit_spacing, y), f"{digits[1]}", font=number_font, fill="black")
      draw.text((x + digit_spacing * 2, y), f"{digits[2]}", font=number_font, fill="black")
      
      # Move x position for the hint
      x_hint_position = x + some_offset_value  # Adjust this based on where you want the hint to start relative to the digits

      # This is an estimate. Adjust based on your font and image width.
      max_chars = 40  # Assume 25 characters per line as an example, adjust as needed.

      # Static values
      single_line_height = 30  # Adjust as necessary
      gap_between_hints = 90  # Adjust as desired

      lines = wrap_text_approx(value, max_chars)
      hint_height = 0  # Calculate the height for each hint
      for line in lines:
          draw.text((x_hint_position, line_space), line, font=text_font, fill="black")
          line_space += single_line_height
          hint_height += single_line_height  # Add to the hint's height

      line_space += gap_between_hints  # Add some gap between each hint set
      hint_height += gap_between_hints  # Add gap to the total hint height
      # Now draw a line from this hint to a specific point on the image
      # line_end = (x_hint_position - 48, line_space - (hint_height / 2) - 40)  # This is just an example. Define where you want the line to end.
      # line_start = (x_hint_position, line_space - (hint_height / 2) - 40)  # Taking the midpoint of the current hint block.

      # draw.line([line_start, line_end], fill="black", width=10)  # Draws a black line with width 2.
      
      
      y += 145  # Additional vertical spacing before drawing next hint

    image_path = f"static/output.png"
    img.save(image_path)

    return image_path
  
@app.route('/', methods=['GET', 'POST'])
def index():
    hints = None
    usednumber = None
    image_path = None
    design = "design1"  # Default design

    # default_number = 222  # Generate a random 3-digit number
    if request.method == 'POST':
        number = request.form.get('number', type=int)
        default_number = number  # Update the default number
        design = request.form.get('design', "design1")  # Get the selected design or use default
        usednumber = number
        hints, image_path = generate_puzzle(number, design)  # <-- adjusted this line to receive image_path
    return render_template('index.html', hints=hints, usednumber=usednumber, image_path=image_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)  # <-- Adjusted this line
    # app.run(debug=True)  # <-- Adjusted this line

