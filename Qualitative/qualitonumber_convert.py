import numpy as np
import random
import tkinter as tk
import rules
import sys



def qualitative_to_quantitative(value):
    # mapping = {
    #     "≈": 1.0,  # ≈
    #     "⊐": 1.6,  # ⊐
    #     "⊃": 2.6,  # ⊃
    #     ">": 4.7,
    #     "≻": 7.0,  # ≻
    #     "⊏": 1 / 1.6,  # ⊏
    #     "⊂": 1 / 2.6,  # ⊂
    #     "<": 1 / 4.7,
    #     "≺": 1 / 7  # ≺
    # }
    
    mapping = {
        "≈": 1.0,  # ≈
        "⊐": 1.5,  # ⊐
        "⊃": 2.3,  # ⊃
        ">": 4.0,
        "≻": 9.0,  # ≻
        "⊏": 1 / 1.5,  # ⊏
        "⊂": 1 / 2.3,  # ⊂
        "<": 1 / 4.0,
        "≺": 1 / 9.0 # ≺
    }
    
    # mapping = {
    #     "≈": 1.0,  # ≈
    #     "⊐": 2.0,  # ⊐
    #     "⊃": 3.0,  # ⊃
    #     ">": 4.0,
    #     "≻": 5.0,  # ≻
    #     "⊏": 1 / 2.0,  # ⊏
    #     "⊂": 1 / 3.0,  # ⊂
    #     "<": 1 / 4.0,
    #     "≺": 1 / 9.0 # ≺
    # }
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
    if 1/ 1.27 <= value <= 1.27:
        return "≈"  # Indifferent
    elif 1.27 <= value <= 1.94:
        return "⊐"  # Slightly in favour
    elif 1.94 < value <= 3.17:
        return "⊃"  # In favour
    elif 3.17 < value <= 6.14:
        return ">"  # Strongly better
    elif value > 6.14:
        return "≻"  # Extremely better
    elif  value < 1 / 6.14:
        return "≺"  # Extremely worse
    elif 1 / 6.14 <= value < 1 / 3.17:
        return "<"  # Strongly worse
    elif 1 / 3.17 <= value < 1 / 1.94:
        return "⊂"  # Slightly worse
    elif 1 / 1.94 <= value < 1/1.27:
        return "⊏"  # Indifferent
    else:
        print(value,"?")
        return "?"  # Unknown range
    
    # if 1/1.5 <= value <= 1.5:
    #     return "≈"  # Indifferent
    # elif 1.6 < value <= 2.5:
    #     return "⊐"  # Slightly in favour
    # elif 2.6 < value <= 3.5:
    #     return "⊃"  # In favour
    # elif 3.6 < value <= 4.5:
    #     return ">"  # Strongly better
    # elif value > 4.5:
    #     return "≻"  # Extremely better
    # elif  value < 1 / 4.5:
    #     return "≺"  # Extremely worse
    # elif 1 / 4.5 <= value < 1 / 3.6:
    #     return "<"  # Strongly worse
    # elif 1 / 3.5 <= value < 1 / 2.6:
    #     return "⊂"  # Slightly worse
    # elif 1 / 2.5 <= value < 1/  ertu:
    #     return "⊏"  # Indifferent
    # else:
    #     return "?"  # Unknown range
    
    
#     [[1.         0.60310604 1.08410588 1.27994759 1.16077323]
#  [1.65808322 1.         1.26615991 2.0949021  1.5       ]
#  [0.92241913 0.78978966 1.         1.54228012 1.18719599]
#  [0.78128199 0.47734928 0.64839064 1.         1.00607183]
#  [0.86149471 0.66666667 0.84232091 0.99396481 1.        ]]
    
# ['≈' '⊏' '≈' '⊐' '≈']
#  ['⊐' '≈' '≈' '⊃' '⊐']
#  ['≈' '⊏' '≈' '⊐' '≈']
#  ['⊏' '⊂' '⊏' '≈' '≈']
#  ['≈' '⊏' '≈' '≈' '≈']]
    
# def compute_inconsistency_matrix(Q):
#     """
#     Optimized computation of the inconsistency matrix for a qualitative pairwise comparison matrix Q.
#     Exploits symmetry to reduce computation (only computes upper triangle).
#     """
#     n = Q.shape[0]
#     inconsistency_matrix = np.zeros((n, n), dtype=int)

#     for i in range(n):
#         for j in range(i + 1, n):  # Only upper triangle
#             aij = Q[i, j]
#             violation_count = 0
#             for k in range(n):
#                 if k == i or k == j:
#                     continue
#                 ajk = Q[j, k]
#                 aik_expected = rules.check_rules(aij, ajk)
#                 if Q[i, k] not in aik_expected:
#                     violation_count += 1

#             inconsistency_matrix[i, j] = violation_count
#             inconsistency_matrix[j, i] = violation_count  # Mirror to lower triangle

#     return inconsistency_matrix

def compute_inconsistency_matrix(Q):
    """
    Computes the inconsistency matrix for a qualitative pairwise comparison matrix Q.
    """
    n = Q.shape[0]
    inconsistency_matrix = np.zeros((n, n), dtype=int)

    for i in range(n):
        for j in range(i + 1, n):  # Only upper triangle
            violation_count = 0
            for k in range(n):
                if k == i or k == j:
                    continue
                akj = Q[k, j]
                aik=Q[i,k]
                aij_expected = rules.check_rules(aik, akj)
                if Q[i, j] not in aij_expected:
                    violation_count += 1

            inconsistency_matrix[i, j] = violation_count
            inconsistency_matrix[j, i] = violation_count  # Mirror to lower triangle
    
    return inconsistency_matrix


def convert_best_matrix_to_qualitative(best_matrix):
    """
    Converts the numeric values in the best matrix to qualitative symbols.
    """
    qualitative_matrix = []
    for row in best_matrix:
        qualitative_row = [numeric_to_qualitative(value) for value in row]
        qualitative_matrix.append(qualitative_row)
    return qualitative_matrix

def convert_matrix_to_numbers(matrix, size):
    num_matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            value = matrix[i, j]  # Directly access the NumPy array element
            numerical_value, _ = qualitative_to_quantitative(value)
            row.append(numerical_value if numerical_value is not None else 0)
        num_matrix.append(row)
    return np.array(num_matrix)

# def convert_matrix_to_numbers(dropdown_vars, size):
#     matrix = []
#     for i in range(1, size + 1):
#         row = []
#         for j in range(1, size + 1):
#             value = dropdown_vars.get((i, j), tk.StringVar()).get()
#             numerical_value, _ = qualitative_to_quantitative(value)
#             row.append(numerical_value if numerical_value is not None else 0)
#         matrix.append(row)
#     return matrix


def create_child(matrix,n):
    
    size = matrix.shape[0]
    child = np.copy(matrix)
    population=[matrix]
    count= 0
    while count < n-1:
        i, j = np.random.choice(size, 2, replace=False)
        while i == j and (child[i,j]<1):  
            i, j = np.random.choice(size, 2, replace=False)
        new_value = child[i, j] + random.uniform(-0.5, 0.5)
        # if (7>=new_value >= 1/7) and (7>=(1 / new_value) >= 1/7):
        #     child[i, j] = new_value
        #     child[j, i] = 1 / new_value 
        while (not (1/9 <= new_value <= 9 and 1/9 <= 1/new_value <= 9)):
            new_value = child[i, j] + random.uniform(-0.5, 0.5)
        child[i, j] = new_value
        child[j, i] = 1 / new_value
        population.append(child)
        child = np.copy(matrix)
        count+=1
    return population

def compute_inconsistency_formula(A):
    n = A.shape[0]
    cm_A = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i != j and j != k and i != k:
                    term1 = abs(1 - A[i, j] / (A[i, k] * A[k, j]))
                    term2 = abs(1 - (A[i, k] * A[k, j]) / A[i, j])
                    min_inconsistency = min(term1, term2)
                    cm_A = max(cm_A, min_inconsistency)
    return cm_A

def select_top_population(population,inconsitency,n=0.5):
    inconsistency1= inconsitency.copy()
    population1=population.copy()
    new_pop=[]
    i=0
    count=n*len(population)
    while i <count:
        b=np.argmin(inconsistency1)
        new_pop.append(population1[b])
        inconsistency1.pop(b)
        population1.pop(b)
        i+=1
    return (new_pop)

def select_intact_generation(population,n=0.2):
    size=len(population)
    count=int(n*size)
    i= np.random.choice(size, count, replace=False) 
    new_pop=[] 
    for  a in i:
        new_pop.append(population[a])
    return new_pop

def crossover(parent1, parent2):
    size = parent1.shape[0]
    child = np.copy(parent1)
    crossover_point = np.random.randint(size)
    for i in range(crossover_point):
        for j in range(crossover_point):
            child[i, j] = parent2[i, j]
            # if j != i:  
            #     child[j, i] = 1 / child[i, j] 
    return child
def select_crossover(cross,n=0.1):
    size=len(cross)
    count=int(n*size)
    i= np.random.choice(size, count, replace=False) 
    new_pop=[] 
    for  a in i:
        new_pop.append(cross[a])
    return new_pop

def select_mutate(cross,n=0.9):
    size=len(cross)
    count=int(n*size)
    i= np.random.choice(size, count, replace=False)  
    new_pop=[] 
    for  a in i:
        new_pop.append(mutation(cross[a]))
    return new_pop

def mutation(cross):
    size = cross.shape[0]
    child = np.copy(cross)
    i, j = np.random.choice(size, 2, replace=False)
    while i == j and (child[i,j]<1):  
        i, j = np.random.choice(size, 2, replace=False)
    new_value = child[i, j] + random.uniform(-0.5, 0.5)
    # if (7>=new_value >= 1/7) and (7>=1 / new_value >= 1/7):
    #     child[i, j] = new_value
    #     child[j, i] = 1 / new_value
    while (not (1/9 <= new_value <= 9 and 1/9 <= 1/new_value <= 9)):
            new_value = child[i, j] + random.uniform(-0.5, 0.5)
    child[i, j] = new_value
    child[j, i] = 1 / new_value
    return child

def main(matrix1):
    a=matrix1.shape[0]
    matrix=convert_matrix_to_numbers(matrix1, a)
    population_size=1000
    current_generation= create_child(matrix,population_size)
    number_generaration=0
    min_inconsistency= float('inf')
    best_min=[]
    best_matrix=[]
    all_inconsistency= []
    while number_generaration<100 and min_inconsistency> 0.3:
        k= 0
        inconsistency= []
        while k < population_size:
            cg=compute_inconsistency_formula(current_generation[k])
            inconsistency.append(cg)
            all_inconsistency.append(cg)
            k += 1
        min_inconsistency= min(inconsistency)
        best_matrix= current_generation[np.argmin(inconsistency)]
        best_min.append(float(min_inconsistency))
        top= select_top_population(current_generation,inconsistency)
        next_generation= select_intact_generation(top)
        k=0
        cross_child=[]
        while k< population_size*0.9:
            numbers = random.sample(range(len(top)), 2)
            parent1 = top[numbers[0]]
            parent2 = top[numbers[1]]
            cross_child.append(crossover(parent1,parent2))
            k +=1
        next_generation=next_generation+select_crossover(cross_child)+select_mutate(cross_child)
        current_generation=next_generation
        number_generaration+=1
        #print(best_min)

    # print(matrix,best_matrix,min_inconsistency,number_generaration)
    #print(best_matrix,number_generaration,min_inconsistency)
    # print(best_min)
    # print(len(all_inconsistency))
    # best_matrix=convert_best_matrix_to_qualitative(best_matrix)
    # print(best_min)
    # print(number_generaration)
    # print(best_matrix)
    # print(best_matrix)
    
    # final_matrix=best_matrix.copy()
    # for i in range(a):
    #     for j in range(i + 1,a ):
    #         final_matrix[i,j]=round(final_matrix[i,j], 2)
    #         final_matrix[j,i]=1/final_matrix[i,j]

    
    # best_matrix=np.round(best_matrix.astype(float), 2)
    print(np.array(convert_best_matrix_to_qualitative(best_matrix)))
    print(best_matrix)
    print(compute_inconsistency_matrix(np.array(convert_best_matrix_to_qualitative(best_matrix))))
    count_inconsistency=0
    if np.any(compute_inconsistency_matrix(np.array(convert_best_matrix_to_qualitative(best_matrix))) != 0):
        count_inconsistency +=1
    return np.array(convert_best_matrix_to_qualitative(best_matrix)),best_min,number_generaration, count_inconsistency

# matrix =np.array( [
#     ["≈", "⊏", "≻"],
#     ["⊐", "≈", "⊂"],
#     ["≺", "⊃", "≈"]
# ])

# matrix1 =np.array( [
#     ["≈", "⊏", ">"],
#     ["⊐", "≈", "⊂"],
#     ["<", "⊃", "≈"]
# ])
Q_example = np.array([
    ["≈", "⊂", "≈", "⊏", "⊃", "≈", "<", "⊐"],
    ["⊃", "≈", ">", "≈", "≻", "⊐", "≈", ">"],
    ["≈", "<", "≈", "⊂", "⊐", "⊏", "<", "⊏"],
    ["⊐", "≈", "⊃", "≈", "≻", "≈", "⊏", ">"],
    ["⊂", "≺", "⊏", "≺", "≈", "<", "≺", "≈"],
    ["≈", "⊏", "⊐", "≈", ">", "≈", "⊂", "⊃"],
    [">", "≈", ">", "⊐", "≻", "⊃", "≈", "≻"],
    ["⊏", "<", "⊐", "<", "≈", "⊂", "≺", "≈"]
])
# matrix =np.array( [
#     ["≈", "≻", "≺", "⊂", "⊐"],
#     ["≺", "≈", "≺", "⊃", ">"],
#     ["≻", "≻", "≈", "≻", "⊏"],
#     ["⊃", "⊂", "≺", "≈", "≺"],
#     ["⊏", "<", "⊐", "≻", "≈"]
# ])

print( main(Q_example))


#example for incinsistency qualitative != quantitative
# [['≈' '⊃' '⊃' '>' '>']
#  ['⊂' '≈' '⊏' '⊐' '⊐']
#  ['⊂' '⊐' '≈' '⊐' '>']
#  ['<' '⊏' '⊏' '≈' '⊐']
#  ['<' '⊏' '<' '⊏' '≈']]
# [[1.         3.05509743 2.29185263 4.71191133 6.05857801]
#  [0.3273218  1.         0.59251296 1.41584554 1.74010855]
#  [0.43632823 1.6877268  1.         1.78732989 3.52962986]
#  [0.2122281  0.70629173 0.5594938  1.         1.49920047]
#  [0.16505523 0.57467679 0.28331583 0.6670222  1.        ]]
# [[0 0 1 0 1]
#  [0 0 0 0 0]
#  [1 0 0 0 1]
#  [0 0 0 0 0]
#  [1 0 1 0 0]]



# [['≈' '⊐' '≈' '⊂' '⊃']
#  ['⊏' '≈' '≈' '⊂' '⊐']
#  ['≈' '≈' '≈' '⊂' '⊃']
#  ['⊃' '⊃' '⊃' '≈' '⊃']
#  ['⊂' '⊏' '⊂' '⊂' '≈']]
# [[1.         1.46340174 1.02475105 0.47001363 1.97552542]
#  [0.68333935 1.         0.79984532 0.36005957 1.41051838]
#  [0.97584677 1.25024173 1.         0.50693425 2.16668932]
#  [2.12759789 2.77731819 1.9726424  1.         3.07205336]
#  [0.50619445 0.70895921 0.46153364 0.32551518 1.        ]]
# [[0 0 0 1 1]
#  [0 0 0 0 0]
#  [0 0 0 1 1]
#  [1 0 1 0 2]
#  [1 0 1 2 0]]


