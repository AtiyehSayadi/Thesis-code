import numpy as np
import random
from collections import Counter





def build_matrix(pairs, n):
    Q = np.full((n, n), "?", dtype=object)
    np.fill_diagonal(Q, 1)

    for (i, j), rel in pairs.items():
        # i -= 1
        # j -= 1
        Q[i, j] = rel
        Q[j, i] = 1/rel

    return Q


# def read_matrix_from_file(file_path):
#     with open(file_path, 'r') as file:
#         matrix = []
#         for line in file:
#             matrix.append([float(x) for x in line.split()])
#     return np.array(matrix)

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
    while number_generaration<400 and min_inconsistency> 0.3:
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
    print("numbr-gen=",number_generaration)
    return best_matrix

def find_missing(matrix):
    consistent_matrix=main(matrix,[])
    size=len(consistent_matrix)
    fixed=[]
    for i in range(size):
        for j in range(i + 1, size):
            if consistent_matrix[i,j]!= "?":
                fixed.append((i,j))
                fixed.append((j,i))
            else:
                value=float(random.randint(1, 5))
                consistent_matrix[i,j]=value
                consistent_matrix[j,i]=1/value
    print(consistent_matrix)
    print(compute_inconsistency_formula(consistent_matrix))
    final_matrix=consistent_matrix.copy()
    if compute_inconsistency_formula(final_matrix)>0.3:
        final_matrix=main(consistent_matrix,fixed)
    print(compute_inconsistency_formula(final_matrix))
    return fixed,final_matrix



def gm_method(A):
    n = A.shape[0]
    # geometric mean of each row
    row_gm = np.prod(A, axis=1) ** (1/n)
    # normalize
    w = row_gm / np.sum(row_gm)
    return w


def order_with_ties(Q):
    """
    Returns a list where each item is either an int (single rank)
    or a set of ints (tie group). Example: [0, 1, {2, 3}]
    """
    s = gm_method(Q)
    # bucket indices by score
    by_score = {}
    for i, v in enumerate(s):
        by_score.setdefault(v, []).append(i)

    # sort scores high -> low
    ordered_scores = sorted(by_score.keys(), reverse=True)

    # build order list; singletons as int, ties as set
    out = []
    for v in ordered_scores:
        grp = sorted(by_score[v])
        out.append(grp[0] if len(grp) == 1 else set(grp))
    # print(out,s)
    return out, s

def orders_for_all_solutions(solutions):
    """For each matrix in sols, return (order_with_ties, scores)."""
    results = []
    for Q in solutions:
        ow, sc = order_with_ties(Q)
        results.append({"order": ow, "scores": sc})
    return results

def count_order_repetitions_from_solutions(solutions):
    """
    Count how many times each unique order appears in all solution matrices.
    Input: list of matrices (solutions)
    Output: Counter with order patterns and their counts
    """
    orders = []
    for Q in solutions:
        order, _ = order_with_ties(Q)
        # make the order hashable for counting
        key = tuple(frozenset(x) if isinstance(x, set) else x for x in order)
        orders.append(key)

    counts = Counter(orders)
    # print(counts)
    # sort by highest count first
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_counts





def find_missing_multiple(matrix):
    consistent_matrix=main(matrix,[])
    size=len(consistent_matrix)
    fixed=[]
    miss=[]
    for i in range(size):
        for j in range(i + 1, size):
            if consistent_matrix[i,j]!= "?":
                fixed.append((i,j))
                fixed.append((j,i))
            else:
                
                miss.append((i,j))
                
    n=0
    solutions=[]
    while n<20:
        for (i, j) in miss:
            value=float(random.randint(1, 5))
            consistent_matrix[i,j]=value
            consistent_matrix[j,i]=1/value
        print("cons=",consistent_matrix)
        print(compute_inconsistency_formula(consistent_matrix))
        final_matrix=consistent_matrix.copy()
        if compute_inconsistency_formula(final_matrix)>0.3:
            final_matrix=main(consistent_matrix,fixed)
        print("final=",final_matrix)
        print(compute_inconsistency_formula(final_matrix))
        solutions.append(final_matrix)
        n+=1
    if solutions:
        
        counts = count_order_repetitions_from_solutions(solutions)
        print(counts)
        
    return solutions



pairs=pairs = {(0,1):0.5, (3,4):3, (1,3):2}
            
Q0 = build_matrix(pairs, 5)
find_missing_multiple(Q0)

# matrix = np.array([
#     [1, 2, 5, 9],
#     [0.5, 1, 3, "?"],
#     [0.2, 1/3, 1,  4],
#     [1/9, "?", 0.25, 1]
# ], dtype=object)
# matrix = np.array([
#     [1.000000, 2.812488, 0.5, 2.584059, "?"],
#     [0.355557, 1.000000, 0.338721, 0.841543, "?"],
#     [2, 2.952285, 1.000000, 3.042874, 2.252451],
#     [0.386988, 1.188293, 0.328637, 1.000000, "?"],
#     ["?", "?", 0.443961, "?", 1.000000]
# ], dtype=object)
# b=main(matrix,[(4,2),(2,4)])
# print(b)
# c=main(matrix,[(2,3),(3,2)])
# print(compute_inconsistency_formula(matrix))
# print(c)
# print(compute_inconsistency_formula(c[2]))
# find_missing_multiple(matrix)


# def gm_method(A):
#     n = A.shape[0]
#     # geometric mean of each row
#     row_gm = np.prod(A, axis=1) ** (1/n)
#     # normalize
#     w = row_gm / np.sum(row_gm)
#     return w

# # Example:
# A = np.array([
#     [1,   3,   5],
#     [1/3, 1,   4],
#     [1/5, 1/4, 1]
# ], dtype=float)

# print(gm_method(A))

