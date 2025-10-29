import numpy as np
import random
import rules

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


# def adjust_matrix(Q):
#     priority = ["≈", "⊏", "⊂", "<", "≺"]
#     inverse = {"≈": "≈","⊏": "⊐", "⊐": "⊏", "⊂": "⊃", "⊃": "⊂", "<": ">", ">": "<", "≺": "≻", "≻": "≺"}
#     inconsistency_matrix=compute_inconsistency_matrix(Q)
#     max_violation = np.max(inconsistency_matrix)
#     # if max_violation == 0:
#     #     return Q
#     while max_violation !=0:
#         i, j = random.choice([(i, j) for i in range(len(Q)) for j in range(len(Q)) 
#                         if inconsistency_matrix[i, j] == max_violation and Q[i, j] != "≈" and Q[i, j] in priority])
#         idx = priority.index(Q[i, j])
#         if idx > 0:
#             Q[i, j] = priority[idx - 1]
#             Q[j, i] = inverse[priority[idx - 1]]
#         print(Q)
#         inconsistency_matrix=compute_inconsistency_matrix(Q)
#         print (inconsistency_matrix) 
#         max_violation = np.max(inconsistency_matrix)
    
#     return Q



def adjust_matrix(Q):
    priority = ["≈", "⊏", "⊂", "<", "≺"]
    inverse = {"≈": "≈", "⊏": "⊐", "⊐": "⊏", "⊂": "⊃", "⊃": "⊂", "<": ">", ">": "<", "≺": "≻", "≻": "≺"}
    
    inconsistency_matrix = compute_inconsistency_matrix(Q)
    max_violation = np.max(inconsistency_matrix)
    generation_number=0
    
    while max_violation != 0:
        candidates = []
        while not candidates and max_violation > 0:
            candidates = [(i, j) for i in range(len(Q)) for j in range(len(Q)) 
                          if inconsistency_matrix[i, j] == max_violation and Q[i, j] in priority and Q[i, j] != "≈"]
            if not candidates:
                max_violation = max((v for row in inconsistency_matrix for v in row if v < max_violation), default=0)
        
        
        i, j = random.choice(candidates)
        idx = priority.index(Q[i, j])
        
        if Q[i, j] == "≈":
            next_max_violation = max(v for row in inconsistency_matrix for v in row if v < max_violation)
            max_violation = next_max_violation
        
        if idx > 0:
            Q[i, j] = priority[idx - 1]
            Q[j, i] = inverse[priority[idx - 1]]
        
        inconsistency_matrix = compute_inconsistency_matrix(Q)
        # print(Q)
        # print(inconsistency_matrix)
        max_violation = np.max(inconsistency_matrix)
        generation_number +=1
    # print(Q)
    return Q,generation_number
# Example usage
# Q_example = np.array([
#     ["≈", "⊏", "⊂", "⊂"],
#     ["⊐", "≈", "≺", "≺"],
#     ["⊃", "≻", "≈", ">"],
#     ["⊃", "≻", "<", "≈"]
# ])

# inconsistency_matrix = compute_inconsistency_matrix(Q_example)
# print(inconsistency_matrix)
# Q_example = np.array([
#     ["≈", "⊏", "⊂"],
#     ["⊐", "≈", "<"],
#     ["⊃", "≺", "≈"]
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
# # matrix =np.array( [
# #     ["≈", "≻", "≺", "⊂", "⊐"],
# #     ["≺", "≈", "≺", "⊃", ">"],
# #     ["≻", "≻", "≈", "≻", "⊏"],
# #     ["⊃", "⊂", "≺", "≈", "≺"],
# #     ["⊏", "<", "⊐", "≻", "≈"]
# # ])

# inconsistency_matrix = compute_inconsistency_matrix(Q_example)
# print(inconsistency_matrix)
# Q_adjusted = adjust_matrix(Q_example)
# print(Q_adjusted)
# print(compute_inconsistency_matrix(Q_adjusted))
