import random
import numpy as np
import copy

def generate_symmetric_matrix_with_one_missing(size=5):
    symbols = ['≻', '>', '⊃', '⊐', '≈', '⊏', '⊂', '<', '≺']
    opposites = {'⊏': '⊐', '⊂': '⊃', '<': '>', '≺': '≻',
                 '≻': '≺', '>': '<', '⊃': '⊂', '⊐': '⊏', '≈': '≈'}

    matrix = np.empty((size, size), dtype=object)
    np.fill_diagonal(matrix, '≈')

    for i in range(size):
        for j in range(i + 1, size):
            symbol = random.choice(symbols)
            matrix[i, j] = symbol
            matrix[j, i] = opposites[symbol]

    # Insert one "?" pair
    off_diag_pairs = [(i, j) for i in range(size) for j in range(i + 1, size)]
    missing_pair = random.choice(off_diag_pairs)
    i, j = missing_pair
    matrix[i][j] = "?"
    matrix[j][i] = "?"

    return matrix, missing_pair


def generate_and_save_matrices():
    file1 = "d:/research/code/Missing-Information/51quali1.txt"
    file2 = "d:/research/code/Missing-Information/51quali2.txt"
    count = 100
    size = 5

    matrices_with_one_missing = []
    missing_pairs_list = []

    # Step 1: Generate and save matrices with one "?" pair
    with open(file1, 'w', encoding="utf-8") as f1:
        for idx in range(1, count + 1):
            matrix, missing_pair = generate_symmetric_matrix_with_one_missing(size)
            matrices_with_one_missing.append(matrix)
            missing_pairs_list.append(missing_pair)
            f1.write(f"Matrix {idx}:\n")
            for row in matrix:
                f1.write(" ".join(row) + "\n")
            f1.write("\n")

    # Step 2: Create a deep copy and add one more "?" pair to each
    with open(file2, 'w', encoding="utf-8") as f2:
        for idx, (matrix, existing_pair) in enumerate(zip(matrices_with_one_missing, missing_pairs_list), 1):
            matrix_copy = copy.deepcopy(matrix)
            i0, j0 = existing_pair

            # Get all other available off-diagonal pairs
            off_diag_pairs = [(i, j) for i in range(size) for j in range(i + 1, size)
                              if (i, j) != (i0, j0)]

            # Only consider pairs not already missing
            valid_new_pairs = [(i, j) for (i, j) in off_diag_pairs if matrix_copy[i][j] != "?"]
            if valid_new_pairs:
                i2, j2 = random.choice(valid_new_pairs)
                matrix_copy[i2][j2] = "?"
                matrix_copy[j2][i2] = "?"

            f2.write(f"Matrix {idx}:\n")
            for row in matrix_copy:
                f2.write(" ".join(row) + "\n")
            f2.write("\n")

    print(f"Saved 100 matrices with 1 '?' to: {file1}")
    print(f"Saved 100 matrices with 2 '?' to: {file2}")

# Run it
generate_and_save_matrices()
