import numpy as np
import random

def read_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        matrix = []
        for line in file:
            matrix.append([float(x) for x in line.split()])
    return np.array(matrix)

def create_child(matrix,fixed,n):
    
    size = matrix.shape[0]
    child = np.copy(matrix)
    population=[matrix]
    count= 0
    while count < n-1:
        i, j = np.random.choice(size, 2, replace=False)
        #while i == j or ((i,j)  in fixed) or child[i,j] =="?" or (child[i,j]=="?") or (float(child[i,j])<1): 
        while i == j  or ((i,j) in fixed)or child[i,j] =="?" or (child[j,i]=="?"): 
            i, j = np.random.choice(size, 2, replace=False)
        new_value = child[i, j] + random.uniform(-0.5, 0.5)
        if (5>=new_value >= 1/5) and (5>=(1 / new_value) >= 1/5):
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
                    if A[i, j] == "?" or A[i, k] == "?" or A[k, j] == "?":
                        continue
                    # try:
                    #     a_ij = float(A[i, j])
                    #     a_ik = float(A[i, k])
                    #     a_kj = float(A[k, j])
                    # except (ValueError, TypeError):
                    #     continue  # fallback protection if an element still can't be converted
                    # term1 = abs(1 - a_ij / (a_ik * a_kj))
                    # term2 = abs(1 - (a_ik * a_kj) / a_ij)
                    term1 = abs(1 - A[i, j] / (A[i, k] * A[k, j]))
                    term2 = abs(1 - (A[i, k] * A[k, j]) / A[i, j])
                    min_inconsistency = min(term1, term2)
                    cm_A = max(cm_A, min_inconsistency)
    return cm_A


def select_top_population(population,inconsitency,n=0.5):
    inconsistency1= inconsitency
    population1=population
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

def select_mutate(cross,fixed,n=0.9):
    size=len(cross)
    count=int(n*size)
    i= np.random.choice(size, count, replace=False)  
    new_pop=[] 
    for  a in i:
        new_pop.append(mutation(cross[a],fixed))
    return new_pop

def mutation(cross,fixed):
    size = cross.shape[0]
    child = np.copy(cross)
    i, j = np.random.choice(size, 2, replace=False)
    # while i == j  or ((i,j) in fixed)or child[i,j] =="?" or (child[i,j]=="?") or (child[i,j]<1): 
    while i == j  or ((i,j) in fixed)or child[i,j] =="?" or (child[j,i]=="?"): 
        i, j = np.random.choice(size, 2, replace=False)
    new_value = child[i, j] + random.uniform(-0.5, 0.5)
    if (5>=new_value >= 1/5) and (5>=1 / new_value >= 1/5):
        child[i, j] = new_value
        child[j, i] = 1 / new_value
    return child

def main(matrix,fixed):
    population_size=1000
    current_generation= create_child(matrix,fixed,population_size)
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
        best_min.append(min_inconsistency)
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
        next_generation=next_generation+select_crossover(cross_child)+select_mutate(cross_child,fixed)
        current_generation=next_generation
        number_generaration+=1
        #print(best_min)

    # print(matrix,best_matrix,min_inconsistency,number_generaration)
    #print(best_matrix,number_generaration,min_inconsistency)
    # print(best_min)
    # print(len(all_inconsistency))
    return best_min,number_generaration,best_matrix
matrix = np.array([
    [1, 2, 5, 9],
    [0.5, 1, 3, "?"],
    [0.2, 1/3, 1,  4],
    [1/9, "?", 0.25, 1]
], dtype=object)
# matrix = np.array([
#     [1.000000, 2.812488, 0.5, 2.584059, "?"],
#     [0.355557, 1.000000, 0.338721, 0.841543, "?"],
#     [2, 2.952285, 1.000000, 3.042874, 2.252451],
#     [0.386988, 1.188293, 0.328637, 1.000000, "?"],
#     ["?", "?", 0.443961, "?", 1.000000]
# ], dtype=object)
# b=main(matrix,[(4,2),(2,4)])
# print(b)
c=main(matrix,[(0,2),(2,0)])
print(compute_inconsistency_formula(matrix))
print(c)

