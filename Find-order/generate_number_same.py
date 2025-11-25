import random
import copy

def generate_matrix_with_one_missing(size=5):
    """Generates a 5x5 reciprocal matrix with one '?' pair randomly placed off-diagonal."""
    matrix = [[0] * size for _ in range(size)]

    for i in range(size):
        matrix[i][i] = 1.0

    for i in range(size):
        for j in range(i + 1, size):
            value = round(random.uniform(1/5, 5), 6)
            matrix[i][j] = value
            matrix[j][i] = round(1 / value, 6)

    # Insert one "?" pair
    off_diag_pairs = [(i, j) for i in range(size) for j in range(i + 1, size)]
    missing_pair = random.choice(off_diag_pairs)
    i, j = missing_pair
    matrix[i][j] = "?"
    matrix[j][i] = "?"

    return matrix, missing_pair

def generate_and_save_two_versions():
    file1 = "d:/research/code/Missing-Information/51matrices51.txt"
    file2 = "d:/research/code/Missing-Information/51matrices52.txt"
    count = 100
    size = 5

    matrices_with_one_missing = []
    missing_pairs_list = []

    # Step 1: Generate and save matrices with one "?" pair
    with open(file1, 'w') as f1:
        for idx in range(1, count + 1):
            matrix, missing_pair = generate_matrix_with_one_missing(size)
            matrices_with_one_missing.append(matrix)
            missing_pairs_list.append(missing_pair)
            f1.write(f"Matrix {idx}:\n")
            for row in matrix:
                f1.write(" ".join(str(val) for val in row) + "\n")
            f1.write("\n")

    # Step 2: Add one more "?" pair and save to second file
    with open(file2, 'w') as f2:
        for idx, (matrix, existing_pair) in enumerate(zip(matrices_with_one_missing, missing_pairs_list), 1):
            matrix_copy = copy.deepcopy(matrix)
            i0, j0 = existing_pair

            # Get all valid remaining off-diagonal pairs
            off_diag_pairs = [(i, j) for i in range(size) for j in range(i + 1, size)
                              if (i, j) != (i0, j0) and matrix_copy[i][j] != "?"]

            if off_diag_pairs:
                i2, j2 = random.choice(off_diag_pairs)
                matrix_copy[i2][j2] = "?"
                matrix_copy[j2][i2] = "?"

            f2.write(f"Matrix {idx}:\n")
            for row in matrix_copy:
                f2.write(" ".join(str(val) for val in row) + "\n")
            f2.write("\n")

    print(f"✔ Saved 100 matrices with 1 '?' to: {file1}")
    print(f"✔ Saved 100 matrices with 2 '?' to: {file2}")

# Run the function
generate_and_save_two_versions()
