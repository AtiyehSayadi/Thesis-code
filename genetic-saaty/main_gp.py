import numpy as np
import random

def read_matrix_from_file(file_path):
    with open(file_path, 'r') as file:
        matrix = []
        for line in file:
            matrix.append([float(x) for x in line.split()])
    return np.array(matrix)

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
        # if (9>=new_value >= 1/9) and (9>=(1 / new_value) >= 1/9):
        #     child[i, j] = new_value
        #     child[j, i] = 1 / new_value 
        while (not (1/9 <= new_value <= 9 and 1/9 <= (1/new_value) <= 9)):
            new_value = child[i, j] + random.uniform(-0.5, 0.5)
        child[i, j] = new_value
        child[j, i] = 1 / new_value
        population.append(child)
        child = np.copy(matrix)
        count+=1
    return population

RI = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,
    5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
    9: 1.45, 10: 1.49
}

def compute_saaty_cr(A):
    n = A.shape[0]

    eigvals, eigvecs = np.linalg.eig(A)
    idx = np.argmax(eigvals.real)

    lambda_max = eigvals[idx].real

    weights = eigvecs[:, idx].real
    weights = np.abs(weights)
    weights = weights / np.sum(weights)

    CI = (lambda_max - n) / (n - 1)
    CR = CI / RI[n]

    return CR

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
            if j != i:  
                child[j, i] = 1 / child[i, j] 
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
    # if (9>=new_value >= 1/9) and (9>=(1 / new_value) >= 1/9):
    #     child[i, j] = new_values
    #     child[j, i] = 1 / new_value
    while (not (1/9 <= new_value <= 9 and 1/9<= (1/new_value) <= 9)):
        new_value = child[i, j] + random.uniform(-0.5, 0.5)
    child[i, j] = new_value
    child[j, i] = 1 / new_value
    return child

def main(matrix):
    population_size=1000
    current_generation= create_child(matrix,population_size)
    number_generaration=0
    min_inconsistency= float('inf')
    best_min=[]
    best_matrix=[]
    all_inconsistency= []
    while number_generaration<100 and min_inconsistency> 0.1:
        k= 0
        inconsistency= []
        while k < population_size:
            inconsistency.append(compute_saaty_cr(current_generation[k]))
            all_inconsistency.append(compute_saaty_cr(current_generation[k]))
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
        next_generation=next_generation+select_crossover(cross_child)+select_mutate(cross_child)
        current_generation=next_generation
        number_generaration+=1
        #print(best_min)

    # print(matrix,best_matrix,min_inconsistency,number_generaration)
    #print(best_matrix,number_generaration,min_inconsistency)
    # print(best_min)
    # print(len(all_inconsistency))
    return best_min, number_generaration, best_matrix
matrix = np.array([
    [1.0,        1.53508881, 1.53606326, 1.06410982],
    [0.65142811, 1.0,        2.0,        1.51939751],
    [0.65101485, 0.5,        1.0,        1.62946607],
    [0.93975263, 0.65815561, 0.61369796, 1.0]
])
a= compute_saaty_cr(matrix)
print(a)
print(main(matrix))
