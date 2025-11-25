
import missing_gp_quali
import numpy as np

#import matplotlib.pyplot as plt 
import time

# def process_matrix(matrix):
#     """Dummy function to process a matrix. Replace with your actual function."""
#     print(f"Processing matrix:\n{matrix}\n")


def read_symbolic_matrices_from_file(filename):
    matrices = []
    matrix = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith("Matrix"):
                if matrix:
                    matrices.append(np.array(matrix))  # ⬅️ convert here
                    matrix = []
            elif line:
                matrix.append(line.split())
        if matrix:
            matrices.append(np.array(matrix))  # ⬅️ and here too
    
    return matrices

# Example usage:
filename = "d:/research/code/Missing-Information/51quali2.txt"  # Your uploaded file
matrices = read_symbolic_matrices_from_file(filename)
num_generation=[]
all_min_inconsistencies = []
i=0
for matrix in matrices:
    min_inconsistencies, num_generation_each =missing_gp_quali.main(matrix,[])
    #print("min: ",min_inconsistencies)
    all_min_inconsistencies.append(min_inconsistencies)
    num_generation.append(num_generation_each)
    i+=1
    print(i,num_generation_each)#print(i,main_gp.main(matrix)[1])
print(num_generation)


#5quali1
#data= [11, 15, 9, 2, 14, 47, 30, 2, 4, 8, 23, 11, 13, 18, 43, 14, 26, 12, 29, 31, 10, 7, 21, 12, 20, 19, 6, 3, 7, 28, 11, 1, 10, 3, 6, 25, 22, 5, 21, 18, 11, 7, 12, 12, 7, 13, 14, 10, 19, 23, 3, 7, 11, 6, 1, 14, 4, 12, 53, 36, 14, 23, 6, 5, 7, 31, 4, 6, 16, 20, 17, 16, 15, 6, 18, 12, 3, 14, 13, 16, 13, 10, 4, 10, 17, 14, 6, 39, 12, 13, 2, 6, 6, 39, 2, 7, 7, 6, 26, 12]

#5quali2
#data=[21, 12, 6, 1, 9, 13, 14, 24, 2, 2, 11, 22, 17, 7, 29, 3, 7, 20, 8, 5, 5, 11, 4, 9, 8, 13, 8, 3, 12, 13, 12, 3, 7, 32, 6, 5, 4, 9, 8, 5, 12, 4, 20, 31, 8, 9, 1, 6, 13, 7, 6, 12, 6, 10, 9, 32, 7, 5, 9, 7, 4, 6, 8, 2, 4, 9, 16, 3, 18, 9, 6, 7, 6, 23, 2, 18, 14, 21, 2, 29, 4, 2, 5, 4, 7, 12, 21, 2, 2, 7, 2, 14, 49, 6, 25, 8, 11, 13, 3, 17]

#5quali1same
#data= [70, 8, 8, 23, 4, 16, 30, 23, 22, 6, 17, 11, 24, 16, 8, 11, 15, 17, 25, 28, 18, 20, 10, 10, 11, 15, 11, 8, 2, 27, 17, 10, 18, 6, 35, 26, 6, 23, 10, 3, 9, 15, 16, 9, 19, 15, 26, 13, 11, 26, 19, 20, 4, 10, 5, 35, 14, 26, 10, 3, 14, 10, 26, 7, 5, 2, 3, 10, 7, 6, 5, 5, 25, 6, 20, 19, 8, 25, 19, 9, 2, 11, 9, 10, 29, 20, 29, 4, 8, 10, 7, 5, 24, 21, 9, 3, 4, 13, 18, 2]

#5quali2same
#data=[18, 7, 7, 24, 4, 11, 16, 11, 17, 6, 6, 7, 14, 11, 7, 8, 13, 4, 10, 27, 17, 11, 15, 4, 10, 7, 13, 7, 1, 14, 12, 7, 9, 2, 9, 21, 3, 14, 7, 3, 13, 33, 20, 5, 15, 17, 16, 10, 19, 6, 12, 5, 4, 12, 5, 29, 15, 10, 7, 2, 11, 13, 42, 4, 2, 1, 2, 9, 4, 5, 4, 5, 28, 6, 8, 8, 7, 21, 11, 6, 2, 7, 8, 13, 17, 27, 10, 2, 5, 7, 5, 3, 13, 15, 8, 3, 2, 10, 13, 1]

#after correction inconsistency

#5quali1same
#data= [58, 9, 8, 34, 4, 12, 25, 19, 22, 5, 10, 13, 20, 12, 13, 9, 15, 17, 20, 25, 13, 23, 11, 10, 17, 21, 11, 12, 2, 35, 20, 16, 23, 10, 36, 24, 5, 19, 8, 4, 9, 11, 17, 10, 17, 21, 14, 11, 12, 26, 18, 11, 3, 13, 5, 44, 19, 28, 9, 3, 13, 11, 22, 7, 6, 2, 3, 10, 7, 6, 5, 6, 21, 6, 23, 16, 6, 24, 15, 10, 3, 11, 8, 12, 20, 200, 28, 4, 9, 8, 6, 4, 34, 19, 7, 3, 3, 10, 20, 2]


#5quali2same
#data=[19, 9, 6, 21, 4, 11, 20, 10, 18, 6, 6, 8, 18, 12, 7, 7, 13, 5, 10, 22, 13, 12, 18, 4, 11, 7, 12, 10, 1, 9, 12, 8, 9, 2, 18, 19, 3, 14, 7, 3, 14, 24, 17, 5, 14, 13, 14, 10, 15, 7, 9, 5, 3, 10, 8, 41, 11, 7, 7, 2, 14, 12, 46, 4, 2, 1, 2, 8, 4, 6, 6, 8, 33, 6, 11, 9, 9, 17, 12, 7, 2, 6, 7, 11, 17, 27, 12, 2, 5, 6, 5, 4, 20, 22, 7, 3, 2, 9, 16, 1]