import random
import numpy as np

def generate_symmetric_matrix(size=5):
    symbols = ['≻','>','⊃','⊐','≈', '⊏', '⊂', '<', '≺'] 
    opposites = {'⊏': '⊐', '⊂': '⊃', '<': '>', '≺': '≻', '≻': '≺', '>': '<', '⊃': '⊂', '⊐': '⊏', '≈': '≈'}
    
    matrix = np.empty((size, size), dtype=object)
    
    # Set diagonal elements to '≈'
    np.fill_diagonal(matrix, '≈')
    
    for i in range(size):
        for j in range(i + 1, size):
            symbol = random.choice(symbols)  # Choose a random symbol
            opposite_symbol = opposites.get(symbol, symbol)  # Get its opposite
            matrix[i, j] = symbol
            matrix[j, i] = opposite_symbol  # Ensure correct opposite assignment
    
    return matrix

def generate_matrices(count=100, size=5):
    return [generate_symmetric_matrix(size) for _ in range(count)]

def save_matrices_to_file(filename, num_matrices=1000, size=5):
    """Saves randomly generated matrices to a file."""
    matrices = generate_matrices(num_matrices, size)
    with open(filename, 'w', encoding="utf-8") as file:
        for idx, matrix in enumerate(matrices, 1):
            file.write(f"Matrix {idx}:\n")
            for row in matrix:
                file.write(" ".join(row) + "\n")
            file.write("\n")

# Generate and save 100 matrices to a file
file_path = "d:/research/code/Qualitative/10000matrices5.txt"
save_matrices_to_file(file_path)

print(f"Matrices saved to {file_path}")
