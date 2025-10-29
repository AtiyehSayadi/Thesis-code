import random

def generate_matrix():
    """Generates a 4x4 matrix where aii = 1 and aij = 1/aji, with values between 1 and 9."""
    size = 5  # Set size to 4 for a 4x4 matrix
    matrix = [[0] * size for _ in range(size)]  # Initialize a 4x4 matrix with zeros

    for i in range(size):
        matrix[i][i] = 1  # Set diagonal elements aii = 1

    # for i in range(size):
    #     for j in range(i + 1, size):
    #         value = random.uniform(1/9, 5) # Generate a random value between 1 and 9
    #         matrix[i][j] = float(value)   # Assign random value to aij
    #         matrix[j][i] = 1 / float(value)  # Set aji = 1 / aij
    for i in range(size):
        for j in range(i + 1, size):
            value = float(random.randint(1, 9))
            if random.random() < 0.5:
                # Normal direction: >1 above, <1 below
                matrix[i][j] = value
                matrix[j][i] = 1 / value
            else:
                # Flipped direction: >1 below, <1 above
                matrix[i][j] = 1 / value
                matrix[j][i] = value

    return matrix

def save_matrices_to_file(filename, num_matrices=1000):
    """Saves 100 randomly generated 4x4 matrices to a file."""
    with open(filename, 'w') as file:
        for idx in range(1, num_matrices + 1):
            matrix = generate_matrix()
            file.write(f"Matrix {idx}:\n")
            for row in matrix:
                file.write(" ".join(f"{value:.6f}" for value in row) + "\n")
            file.write("\n")

# Generate and save 100 matrices to a file
save_matrices_to_file("d:/research/code/Project-quanti/1000_scale9_size5.txt")
