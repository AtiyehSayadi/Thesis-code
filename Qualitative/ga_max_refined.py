import numpy as np
import random
import rules


priority = ["≻",">","⊃","⊐","≈", "⊏", "⊂", "<", "≺"]
inverse = {"≈": "≈", "⊏": "⊐", "⊐": "⊏", "⊂": "⊃", "⊃": "⊂", "<": ">", ">": "<", "≺": "≻", "≻": "≺"}


# def create_child(matrix,n):
    
#     size = matrix.shape[0]
#     child = np.copy(matrix)
#     population=[matrix]
#     count= 0
#     inconsistency_matrix = compute_inconsistency_matrix(matrix)
#     max_violation = np.max(inconsistency_matrix)
#     while count < n-1:
#         candidates = [(i, j) for i in range(len(matrix)) for j in range(len(matrix)) 
#                     if inconsistency_matrix[i, j] == max_violation and i!=j]  
#         i, j = random.choice(candidates)
#         current_symbol = matrix[i][j]
#         idx = priority.index(current_symbol)
#         if idx == 0:
#             new_symbol = priority[1]  # Only one choice (lower value)
#         elif idx == len(priority) - 1:
#             new_symbol = priority[len(priority)-2]  # Only one choice (upper value)
#         else:
#             new_symbol = random.choice([priority[idx - 1], priority[idx + 1]])
            
#         child[i][j] = new_symbol
#         child[j][i] = inverse[new_symbol]
        
#         population.append(child)
#         child = np.copy(matrix)
#         count+=1
#     return population

def create_child(matrix,n):
    
    size = matrix.shape[0]
    child = np.copy(matrix)
    population=[matrix]
    count= 0
    while count < n-1:
        i, j = np.random.choice(size, 2, replace=False)
        while i == j and (child[i,j]<1):  
            i, j = np.random.choice(size, 2, replace=False)
        current_symbol = matrix[i][j]
        idx = priority.index(current_symbol)
        if idx == 0:
            new_symbol = priority[1]  # Only one choice (lower value)
        elif idx == len(priority) - 1:
            new_symbol = priority[len(priority)-2]  # Only one choice (upper value)
        else:
            new_symbol = random.choice([priority[idx - 1], priority[idx + 1]])
            
        child[i][j] = new_symbol
        child[j][i] = inverse[new_symbol]
        
        population.append(child)
        child = np.copy(matrix)
        count+=1
    return population


# def compute_inconsistency_matrix(Q):
#     """
#     Computes the inconsistency matrix for a qualitative pairwise comparison matrix Q.
#     """
#     n = Q.shape[0]
#     inconsistency_matrix = np.zeros((n, n), dtype=int)
    
#     for i in range(n):
#         for j in range(n):
#             if i != j:
#                 violation_count = 0
#                 for k in range(n):
#                     if k != i and k != j:
#                         aij = Q[i, j]
#                         ajk = Q[j, k]
#                         aik_expected = rules.check_rules(aij, ajk)
#                         if Q[i, k] not in aik_expected:
#                             violation_count += 1
                
#                 inconsistency_matrix[i, j] = violation_count
    
#     return inconsistency_matrix

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
    # print(size)
    child = np.copy(parent1)
    crossover_point = np.random.randint(size)
    # print(crossover_point)
    for i in range(crossover_point):
        for j in range(crossover_point):
            child[i, j] = parent2[i, j]
            # if j != i:  
            #     child[j, i] = inverse[child[i, j]]
    return child

def select_crossover(cross,n=0):
    size=len(cross)
    count=int(n*size)
    i= np.random.choice(size, count, replace=False) 
    new_pop=[] 
    for  a in i:
        new_pop.append(cross[a])
    return new_pop

def select_mutate(cross,n=1):
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
    inconsistency_matrix = compute_inconsistency_matrix(cross)
    max_violation = np.max(inconsistency_matrix)
    candidates = [(i, j) for i in range(len(cross)) for j in range(len(cross)) 
                          if inconsistency_matrix[i, j] == max_violation and i!=j]  
    i, j = random.choice(candidates)
    current_symbol = cross[i][j]
    idx = priority.index(current_symbol)
    if idx == 0:
        new_symbol = priority[1]  # Only one choice (lower value)
    elif idx == len(priority) - 1:
        new_symbol = priority[len(priority)-2]  # Only one choice (upper value)
    else:
        new_symbol = random.choice([priority[idx - 1], priority[idx + 1]])
            
    child[i][j] = new_symbol
    child[j][i] = inverse[new_symbol]
    
    return child

def main(matrix):
    population_size=1000
    current_generation= create_child(matrix,population_size)
    number_generaration=0
    min_inconsistency= float('inf')
    best_min=[]
    best_matrix=[]
    all_inconsistency= []
    while number_generaration<100 and min_inconsistency != 0:
        k= 0
        inconsistency= []
        while k < population_size:
            current_inconsistency= int(np.max(compute_inconsistency_matrix(current_generation[k])))
            inconsistency.append(current_inconsistency)
            all_inconsistency.append(current_inconsistency)
            k += 1
        #print (min_inconsistency)
        min_inconsistency= int(min(inconsistency))
        #print(np.argmin(inconsistency))
        best_matrix= current_generation[np.argmin(inconsistency)]
        #print (best_matrix)
        best_min.append(int(min_inconsistency))
        # print(best_min)
        top= select_top_population(current_generation,inconsistency)
        next_generation= select_intact_generation(top)
        # print("next_ge",len(next_generation))
        k=0
        cross_child=[]
        while k< population_size*0.9:
            numbers = random.sample(range(len(top)), 2)
            parent1 = top[numbers[0]]
            parent2 = top[numbers[1]]
            cross_child.append(crossover(parent1,parent2))
            k +=1
        # while k< population_size*0.9:
        #     numbers = random.sample(range(len(top)), 1)
        #     parent1 = top[numbers[0]]
        #     cross_child.append(parent1)
        #     k +=1
        next_generation=next_generation+select_crossover(cross_child)+select_mutate(cross_child)
        #next_generation=next_generation+select_mutate(cross_child)
        current_generation=next_generation
        # print("next_ge",len(current_generation))
        number_generaration+=1
        #print(best_min)

    #print(matrix,best_matrix,min_inconsistency,number_generaration)
    # print(best_matrix,number_generaration,min_inconsistency)
    # print(best_min)
    # #print(all_inconsistency)
    print("best maatrix=",best_matrix)
    # print(compute_inconsistency_matrix(best_matrix))
    count_inconsistency=0
    if np.any(compute_inconsistency_matrix(np.array(best_matrix)) != 0) and number_generaration<200:
        count_inconsistency +=1
    return best_matrix,best_min,number_generaration,count_inconsistency

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
# Q_example = np.array([
#     ["≈", "⊂", "≈", "⊏", "⊃", "≈", "<", "⊐"],
#     ["⊃", "≈", ">", "≈", "≻", "⊐", "≈", ">"],
#     ["≈", "<", "≈", "⊂", "⊐", "⊏", "<", "⊏"],
#     ["⊐", "≈", "⊃", "≈", "≻", "≈", "⊏", ">"],
#     ["⊂", "≺", "⊏", "≺", "≈", "<", "≺", "≈"],
#     ["≈", "⊏", "⊐", "≈", ">", "≈", "⊂", "⊃"],
#     [">", "≈", ">", "⊐", "≻", "⊃", "≈", "≻"],
#     ["⊏", "<", "⊐", "<", "≈", "⊂", "≺", "≈"]
# ])

# matrix =np.array( [
#     ["≈", "≻", "≺", "⊂", "⊐"],
#     ["≺", "≈", "≺", "⊃", ">"],
#     ["≻", "≻", "≈", "≻", "⊏"],
#     ["⊃", "⊂", "≺", "≈", "≺"],
#     ["⊏", "<", "⊐", "≻", "≈"]
# ])
# children_matrices = create_child(matrix,10)
# print(children_matrices)
# print(compute_inconsistency_matrix(Q_example))
# print( main(Q_example))
# print("a",crossover(matrix,Q_example))

