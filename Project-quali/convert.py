import tkinter as tk
from tkinter import ttk
import numpy as np
from main_gp import main  # Import the main function

def qualitative_to_quantitative(value):
    mapping = {
        "≈": 1.0,  # ≈
        "⊐": 1.6,  # ⊐
        "⊃": 2.6,  # ⊃
        ">": 4.7,
        "≻": 7.0,  # ≻
        "⊏": 1 / 1.6,  # ⊏
        "⊂": 1 / 2.6,  # ⊂
        "<": 1 / 4.7,
        "≺": 1 / 7  # ≺
    }
    reverse_mapping = {
        "≈":"≈",
        "⊐": "⊏",
        "⊃": "⊂",
        ">": "<",
        "≻": "≺",
        "⊏": "⊐",
        "⊂": "⊃",
        "<": ">",
        "≺": "≻"
    }
    return mapping.get(value, None), reverse_mapping

def numeric_to_qualitative(value):
    """
    Converts a numeric value to its corresponding qualitative symbol based on the given ranges.
    """
    if 0.79 <= value <= 1.27:
        return "≈"  # Indifferent
    elif 1.27 < value <= 1.94:
        return "⊐"  # Slightly in favour
    elif 1.94 < value <= 3.17:
        return "⊃"  # In favour
    elif 3.17 < value <= 6.14:
        return ">"  # Strongly better
    elif value > 6.14:
        return "≻"  # Extremely better
    elif 1 / 7 <= value < 1 / 6.14:
        return "≺"  # Extremely worse
    elif 1 / 6.14 <= value < 1 / 3.17:
        return "<"  # Strongly worse
    elif 1 / 3.17 <= value < 1 / 1.94:
        return "⊂"  # Slightly worse
    elif 1 / 1.94 <= value < 1.27:
        return "⊏"  # Indifferent
    else:
        return "?"  # Unknown range

def convert_best_matrix_to_qualitative(best_matrix):
    """
    Converts the numeric values in the best matrix to qualitative symbols.
    """
    qualitative_matrix = []
    for row in best_matrix:
        qualitative_row = [numeric_to_qualitative(value) for value in row]
        qualitative_matrix.append(qualitative_row)
    return qualitative_matrix

def convert_matrix_to_numbers(dropdown_vars, size):
    matrix = []
    for i in range(1, size + 1):
        row = []
        for j in range(1, size + 1):
            value = dropdown_vars.get((i, j), tk.StringVar()).get()
            numerical_value, _ = qualitative_to_quantitative(value)
            row.append(numerical_value if numerical_value is not None else 0)
        matrix.append(row)
    return matrix

def display_matrix_values():
    numerical_matrix = np.array(convert_matrix_to_numbers(dropdown_vars, current_size))
    print("Matrix:")
    print(numerical_matrix)
    return numerical_matrix

def show_qualitative_matrix(qualitative_matrix):
    """
    Display the qualitative matrix in a new Tkinter window.
    """
    qualitative_window = tk.Toplevel()
    qualitative_window.title("Qualitative Matrix")

    for i, row in enumerate(qualitative_matrix):
        for j, value in enumerate(row):
            label = tk.Label(qualitative_window, text=value, width=5, borderwidth=1, relief="solid")
            label.grid(row=i, column=j, padx=2, pady=2)

def run_main_function():
    matrix = display_matrix_values()
    print("Running the main function...")
    results = main(matrix)  # Call the main function

    if isinstance(results, tuple) and len(results) == 3:
        best_min, number_generations, best_matrix = results
        print("Results from main function:")
        print(f"Best Minimum: {best_min}")
        print(f"Number of Generations: {number_generations}")
        print(f"Best Numeric Matrix:\n{best_matrix}")

        # Convert the best matrix to qualitative form
        qualitative_matrix = convert_best_matrix_to_qualitative(best_matrix)
        print("Best Qualitative Matrix:")
        for row in qualitative_matrix:
            print(row)

        # Show the qualitative matrix in a new UI window
        show_qualitative_matrix(qualitative_matrix)
    else:
        print("Unexpected output from main function.")

def create_matrix_interface():
    def update_matrix():
        global current_size
        current_size = int(size_entry.get())
        create_matrix(current_size)

    def create_matrix(size):
        # Clear existing matrix UI
        for widget in matrix_frame.winfo_children():
            widget.destroy()

        # Add row and column headers
        for i in range(size + 1):
            if i > 0:
                header_label = tk.Label(matrix_frame, text=str(i), width=5, borderwidth=1, relief="solid")
                header_label.grid(row=0, column=i, padx=2, pady=2)
                header_label = tk.Label(matrix_frame, text=str(i), width=5, borderwidth=1, relief="solid")
                header_label.grid(row=i, column=0, padx=2, pady=2)

        # Generate matrix UI
        for i in range(1, size + 1):
            for j in range(1, size + 1):
                if i == j:
                    # Fixed diagonal value
                    label = tk.Label(matrix_frame, text="≈", width=5, borderwidth=1, relief="solid")
                    label.grid(row=i, column=j, padx=2, pady=2)
                    dropdown_vars[(i, j)] = tk.StringVar(value="≈")
                elif j > i:
                    # Dropdown for upper triangle
                    var = tk.StringVar()

                    def on_selection(event, i=i, j=j):
                        value = dropdown_vars[(i, j)].get()
                        _, reverse_mapping = qualitative_to_quantitative(value)
                        reverse_value = reverse_mapping.get(value, "")
                        if (j, i) in dropdown_vars:
                            dropdown_vars[(j, i)].set(reverse_value)

                    dropdown = ttk.Combobox(matrix_frame, width=5, state="readonly", textvariable=var)
                    dropdown["values"] = ["≈", "⊐", "⊃", ">", "≻", "⊏", "⊂", "<", "≺"]
                    dropdown.grid(row=i, column=j, padx=2, pady=2)
                    dropdown.bind("<<ComboboxSelected>>", on_selection)
                    dropdown_vars[(i, j)] = var
                elif j < i:
                    # Dropdown for lower triangle
                    var = tk.StringVar()
                    dropdown = ttk.Combobox(matrix_frame, width=5, state="readonly", textvariable=var)
                    dropdown["values"] = ["≈", "⊐", "⊃", ">", "≻", "⊏", "⊂", "<", "≺"]
                    dropdown.grid(row=i, column=j, padx=2, pady=2)
                    dropdown_vars[(i, j)] = var

    # Initialize main window
    root = tk.Tk()
    root.title("Matrix Qualitative Mapping")

    # Frame for size input
    size_frame = tk.Frame(root)
    size_frame.pack(pady=10)

    size_label = tk.Label(size_frame, text="Matrix Size:")
    size_label.pack(side=tk.LEFT, padx=5)

    size_entry = tk.Entry(size_frame, width=5)
    size_entry.pack(side=tk.LEFT, padx=5)

    size_button = tk.Button(size_frame, text="Create Matrix", command=update_matrix)
    size_button.pack(side=tk.LEFT, padx=5)

    # Frame for matrix
    matrix_frame = tk.Frame(root)
    matrix_frame.pack(pady=10)

    # Button to display numerical matrix
    display_button = tk.Button(root, text="Display Matrix Values", command=display_matrix_values)
    display_button.pack(pady=5)

    # Button to run the main function
    run_button = tk.Button(root, text="Run Main Function", command=run_main_function)
    run_button.pack(pady=5)

    # Dropdown variables and current size
    global dropdown_vars
    dropdown_vars = {}
    global current_size
    current_size = 0

    root.mainloop()

# Run the program
create_matrix_interface()
