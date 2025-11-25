import random

def generate_matrix_with_missing():
    """Generates a 5x5 reciprocal matrix with one '?' pair (aij and aji) randomly placed off-diagonal."""
    size = 5
    matrix = [[0] * size for _ in range(size)]

    for i in range(size):
        matrix[i][i] = 1  # Set diagonal to 1

    # Fill the upper triangle with random values and assign reciprocals to the lower triangle
    for i in range(size):
        for j in range(i + 1, size):
            value = random.uniform(1/5, 5)
            matrix[i][j] = round(value, 6)
            matrix[j][i] = round(1 / value, 6)

    # Randomly pick one off-diagonal pair to set as '?'
    # while True:
    #     i, j = random.randint(0, size - 1), random.randint(0, size - 1)
    #     if i != j:  # must be off-diagonal
    #         matrix[i][j] = "?"
    #         matrix[j][i] = "?"
    #         break
    off_diag_pairs = [(i, j) for i in range(size) for j in range(i + 1, size)]

    # Randomly choose two distinct pairs
    missing_pairs = random.sample(off_diag_pairs, 2)

    for i, j in missing_pairs:
        matrix[i][j] = "?"
        matrix[j][i] = "?"

    return matrix

def save_matrices_to_file(filename, num_matrices=100):
    """Saves `num_matrices` matrices with one '?' per matrix to a file."""
    with open(filename, 'w') as file:
        for idx in range(1, num_matrices + 1):
            matrix = generate_matrix_with_missing()
            file.write(f"Matrix {idx}:\n")
            for row in matrix:
                file.write(" ".join(str(value) for value in row) + "\n")
            file.write("\n")

# Save 100 matrices with one "?" pair each
save_matrices_to_file("d:/research/code/Missing-Information/5matrices52.txt", num_matrices=100)