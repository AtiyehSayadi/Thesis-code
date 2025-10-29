import missing_gp_number
import numpy as np
import matplotlib.pyplot as plt 
import time

def process_matrix(matrix):
    """Dummy function to process a matrix. Replace with your actual function."""
    print(f"Processing matrix:\n{matrix}\n")


import numpy as np

def read_matrices_from_file(filename):
    """Reads matrices from a file and returns a list of numpy arrays with dtype=object, preserving '?'."""
    matrices = []
    with open(filename, 'r') as file:
        matrix = []
        for line in file:
            line = line.strip()
            if line.startswith("Matrix"):
                if matrix:
                    matrices.append(np.array(matrix, dtype=object))
                    matrix = []
            elif line:
                row = [x if x == "?" else float(x) for x in line.split()]
                matrix.append(row)
        if matrix:
            matrices.append(np.array(matrix, dtype=object))
    return matrices

filename = "d:/research/code/Missing-Information/51matrices52.txt"
matrices = read_matrices_from_file(filename)
num_generation=[]
all_min_inconsistencies = []
i=0
for matrix in matrices:
    min_inconsistencies, num_generation_each = missing_gp_number.main(matrix,[])
    #print("min: ",min_inconsistencies)
    all_min_inconsistencies.append(min_inconsistencies)
    num_generation.append(num_generation_each)
    i+=1
    print(i,num_generation_each)#print(i,main_gp.main(matrix)[1])
print(num_generation)    
if all_min_inconsistencies:
    #print (all_min_inconsistencies[0])
    generations = range(len(all_min_inconsistencies[0])) 
    #print (len(all_min_inconsistencies[0])) 
    plt.plot(generations, all_min_inconsistencies[0], 'b')
    plt.xticks(generations[::5])
    plt.yticks(fontsize=13, fontname= 'DejaVu Serif',fontweight= 'bold')
    plt.xticks(fontsize=13,fontname= 'DejaVu Serif', fontweight= 'bold')  
    plt.xlabel("\nGenerations",fontdict={'fontsize': 17, 'fontweight': 'bold', 'fontname': 'DejaVu Serif'})
    plt.ylabel("Fitness (Inconsistency)", fontdict={'fontsize': 17, 'fontweight': 'bold', 'fontname': 'DejaVu Serif'})
    plt.title('\nEvolution of Fitness Over Number of Generations\n', 
        fontdict={'fontsize': 22, 'fontweight': 'bold', 'fontname': 'DejaVu Serif'})
    #plt.title(f"Evolutionary Algorithm on RMatrix")
    plt.show()


#5matricenumber51 with childe[i,j]<1
#data=[38, 21, 31, 26, 7, 17, 28, 24, 23, 26, 30, 34, 41, 18, 26, 7, 27, 28, 31, 26, 19, 24, 28, 38, 15, 45, 14, 7, 30, 35, 20, 32, 18, 12, 29, 24, 22, 25, 38, 26, 28, 35, 28, 24, 24, 40, 20, 21, 41, 47, 38, 22, 25, 6, 19, 5, 38, 17, 39, 55, 39, 30, 52, 42, 43, 36, 34, 17, 32, 55, 16, 10, 31, 14, 43, 31, 20, 21, 22, 16, 51, 26, 32, 18, 21, 19, 46, 23, 18, 17, 26, 39, 50, 57, 38, 40, 23, 49, 4, 20]

#5matricenumber51 without childe[i,j]<1
#data=[8, 11, 10, 8, 3, 10, 8, 6, 9, 11, 8, 9, 15, 9, 17, 8, 16, 10, 11, 10, 8, 10, 12, 13, 10, 12, 6, 5, 12, 15, 10, 10, 7, 7, 11, 13, 9, 12, 14, 8, 13, 15, 7, 10, 7, 13, 4, 4, 13, 15, 12, 11, 13, 1, 10, 3, 16, 7, 14, 12, 19, 10, 18, 16, 15, 15, 12, 5, 13, 18, 9, 4, 14, 8, 19, 8, 9, 6, 9, 11, 13, 10, 10, 10, 11, 6, 16, 13, 13, 7, 13, 16, 17, 19, 11, 17, 6, 16, 3, 10]

#5matricenumber71 without childe[i,j]<1
#data=[45, 54, 40, 39, 34, 34, 53, 46, 38, 55, 40, 41, 49, 37, 46, 37, 46, 55, 57, 47, 38, 43, 50, 43, 41, 50, 50, 55, 52, 55, 44, 50, 55, 47, 41, 66, 45, 45, 47, 48, 40, 43, 44, 52, 40, 46, 57, 49, 35, 36, 38, 39, 56, 49, 53, 43, 48, 46, 37, 42, 35, 41, 44, 54, 45, 53, 57, 34, 50, 47, 39, 50, 47, 59, 28, 57, 42, 39, 53, 42, 54, 38, 54, 41, 38, 53, 52, 41, 45, 41, 47, 50, 49, 39, 51, 38, 46, 49, 59, 55]

#5matricenumber72 without childe[i,j]<1
#data= [39, 50, 49, 49, 49, 37, 31, 41, 36, 46, 46, 43, 38, 51, 46, 30, 34, 51, 29, 37, 39, 39, 32, 46, 53, 32, 44, 46, 31, 28, 54, 55, 34, 58, 43, 50, 40, 35, 39, 42, 46, 50, 36, 33, 47, 46, 42, 34, 43, 57, 32, 45, 53, 41, 35, 43, 37, 44, 33, 41, 46, 28, 51, 35, 30, 37, 34, 43, 39, 46, 38, 30, 37, 47, 43, 40, 45, 40, 39, 45, 56, 38, 49, 42, 49, 46, 33, 44, 51, 45, 24, 29, 55, 38, 42, 45, 42, 41, 50, 50]

#5matricenumber73 without childe[i,j]<1
#data= [40, 28, 36, 27, 31, 39, 35, 37, 38, 41, 33, 38, 46, 32, 35, 41, 24, 35, 31, 32, 34, 33, 38, 36, 36, 33, 40, 40, 35, 38, 44, 47, 35, 33, 30, 47, 17, 35, 22, 32, 35, 36, 39, 44, 41, 34, 41, 39, 42, 35, 39, 28, 39, 38, 27, 30, 35, 32, 35, 36, 44, 46, 46, 37, 41, 37, 33, 40, 33, 34, 51, 32, 30, 37, 42, 41, 43, 38, 46, 44, 26, 37, 51, 31, 28, 32, 33, 31, 30, 40, 41, 30, 30, 28, 34, 39, 31, 37, 49, 40]

#5matricenumber52 without childe[i,j]<1
#data=[9, 9, 3, 6, 8, 5, 15, 8, 2, 5, 13, 4, 8, 10, 6, 11, 6, 6, 2, 2, 12, 10, 8, 5, 4, 4, 9, 8, 11, 4, 7, 8, 4, 7, 6, 13, 7, 7, 7, 5, 10, 10, 3, 7, 10, 11, 13, 12, 6, 6, 9, 10, 4, 13, 5, 8, 4, 12, 11, 13, 12, 5, 7, 6, 5, 10, 6, 4, 11, 9, 11, 1, 10, 16, 6, 5, 2, 7, 4, 11, 2, 10, 14, 3, 6, 10, 10, 5, 4, 5, 5, 3, 10, 11, 2, 13, 6, 5, 5, 9]

#5matricenumber51 same without childe[i,j]<1
#data= [8, 5, 7, 4, 9, 11, 19, 10, 17, 10, 14, 14, 14, 13, 11, 10, 10, 13, 19, 11, 15, 12, 9, 11, 6, 7, 6, 18, 5, 6, 11, 12, 4, 12, 9, 9, 10, 10, 11, 13, 15, 9, 6, 3, 7, 15, 10, 6, 20, 22, 11, 5, 13, 12, 7, 9, 15, 17, 10, 12, 12, 4, 6, 7, 18, 11, 13, 12, 11, 13, 8, 7, 13, 14, 8, 6, 8, 12, 9, 9, 10, 21, 13, 7, 11, 12, 11, 15, 8, 7, 8, 10, 15, 13, 9, 17, 11, 12, 9, 13]


#5matricenumber52 same without childe[i,j]<1
#data= [5, 4, 2, 4, 9, 6, 10, 6, 10, 6, 2, 10, 10, 6, 11, 5, 6, 13, 12, 10, 9, 7, 8, 4, 7, 5, 3, 16, 6, 5, 10, 7, 3, 12, 4, 5, 11, 3, 3, 11, 12, 5, 5, 4, 7, 8, 9, 2, 12, 16, 7, 5, 8, 8, 5, 8, 10, 13, 2, 13, 8, 4, 5, 2, 10, 7, 10, 6, 8, 9, 5, 5, 10, 11, 7, 4, 2, 12, 6, 6, 8, 14, 13, 5, 9, 6, 7, 11, 4, 5, 5, 10, 14, 11, 3, 13, 10, 9, 5, 10]
