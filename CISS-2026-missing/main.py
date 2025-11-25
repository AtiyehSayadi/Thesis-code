import numpy as np
import random
import rules
from collections import Counter
import time
import timeit

priority = ["≻",">","⊃","⊐","≈", "⊏", "⊂", "<", "≺"]
inverse = {"≈": "≈", "⊏": "⊐", "⊐": "⊏", "⊂": "⊃", "⊃": "⊂", "<": ">", ">": "<", "≺": "≻", "≻": "≺"}

RIGHT  = {"<", "≺", "⊂", "⊏"}   # looking right  -> +1
LEFT = {">", "≻", "⊃", "⊐"}   # looking left -> -1


# def compute_inconsistency_matrix(Q):
#     """
#     Computes the inconsistency matrix for a qualitative pairwise comparison matrix Q.
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

    
def build_matrix(pairs, n):
    Q = np.full((n, n), "?", dtype=object)
    np.fill_diagonal(Q, "≈")

    for (i, j), rel in pairs.items():
        # i -= 1
        # j -= 1
        Q[i, j] = rel
        Q[j, i] = inverse[rel]

    return Q




def _next_unknown(Q):
    n = Q.shape[0]
    for i in range(n):
        for j in range(i+1, n):
            if Q[i, j] == "?":
                return i, j
    return None

def _possible(Q, i, j):
    """Allowed values for Q[i,j] from all usable triangles; None => no constraints."""
    n = Q.shape[0]
    allowed = None
    for k in range(n):
        if k in (i, j): 
            continue
        aik, akj = Q[i, k], Q[k, j]
        if aik == "?" or akj == "?":
            continue
        Sj = rules.check_rules(aik, akj)  # set of possible a[i,k] from this triple
        if Sj is None:
            continue
        allowed = Sj if allowed is None else (allowed & Sj)
        if allowed == set():
            return set()
    
    return  allowed                  # could be None when no triangle usable

# def complete_all(Q):
#     sols = []
#     def dfs(A):
#         nxt = _next_unknown(A)
#         if not nxt:
#             sols.append(A); return
#         i, j = nxt
#         cand = _possible(A, i, j)
#         cand = priority if cand is None else sorted(cand, key=priority.index)
#         print(i,j,cand)
#         if not cand:
#             return
#         for r in cand:
#             B = A.copy()
#             B[i, j] = r
#             B[j, i] = inverse[r]
#             dfs(B)
#     dfs(Q.copy())
#     # print (sols)
#     return sols


def complete_all(Q):
    sols = [Q.copy()]     # start with one partial matri
    n=0
    while True:
        new_sols = []
        expanded = False  # flag to see if we filled anything

        for A in sols:
            nxt = _next_unknown(A)
            
            if not nxt:
                # matrix is complete
                new_sols.append(A)
                continue

            expanded = True
            i, j = nxt
            cand = _possible(A, i, j)
            cand = priority if cand is None else sorted(cand, key=priority.index)
            # print(i, j, cand)

            if not cand:
                continue  # contradiction → drop this branch

            for r in cand:
                B = A.copy()
                B[i, j] = r
                B[j, i] = inverse[r]
                # if nxt==(0,4):
                    
                #     print (nxt,B)
                #     n+=1
                #     print(n)
                #     print(i, j, cand)
                new_sols.append(B)

        sols = new_sols

        if not expanded:
            break  # no more "?" found → all matrices complete

    return sols




def global_scores(Q):
    n = Q.shape[0]
    s = [0]*n
    for i in range(n):
        for j in range(n):
            if i == j: 
                continue
            a = Q[i, j]
            if a in LEFT:
                s[i] += 1
            elif a in RIGHT:
                s[i] -= 1
    return s

def order_with_ties(Q):
    """
    Returns a list where each item is either an int (single rank)
    or a set of ints (tie group). Example: [0, 1, {2, 3}]
    """
    s = global_scores(Q)
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



# ----- example -----
if __name__ == "__main__":
    start_time = time.time()
    #pairs = {(0,1):">", (3,4):"⊐", (1,3):"⊂"}
    #pairs={(0,1):">", (1,2):"⊐",(3,4):"≻"} #solutions: 862 Execution time: 4.473 ms ms Execution time: 13.20 milliseconds
    #pairs={(0,1):"<", (2,3):">"} #solutions: 97 Execution time: 0.579 ms Execution time: 2.56 milliseconds
    #pairs={(0,1):">", (1,2):"⊐",(3,4):"≻", (4,5):"⊂", (5,6):">", (6,7):"≈"}  # solutions: 5078385  Execution time: 174955.59 milliseconds Execution time: 114950.273 ms
    #pairs={(0,1):">", (1,2):"⊂",(3,4):"≻", (4,5):"≻", (5,6):">", (6,7):"≈"} #solutions: 59749  Execution time: 2689.263 ms Execution time: 3266.85 milliseconds
    #pairs={(0,1):">"}  #solutions: 22   Execution time: 0.080 ms   Execution time: 1.45 milliseconds
    #pairs={(0,1):">", (1,2):"⊐",(2,3):">",(3,4):"≻", (5,6):"<"} #solutions: 5270 Execution time: 165.25 milliseconds Execution time: 139.930 ms
    #pairs={(0,1):">", (1,2):"⊂", (3,4):"≻",(4,5):"≻"} #solutions: 3487 Execution time: 72.110 ms Execution time: 91.76 milliseconds
    #pairs={(0,1):">", (1,2):"⊂",(3,4):"≻", (4,5):"≻", (5,6):">", (6,7):"≈", (7,8):"<"} #solutions:2863763    Execution time: 274887.01  milliseconds
    #pairs={(0,1):">", (1,2):"⊂",(3,4):"≻", (4,5):"≻", (5,6):">", (6,7):"≈", (7,8):"<", (8,9):"⊏"} #solutions:    Execution time:  milliseconds
    #pairs={(0,1):">", (1,2):"⊂",(3,4):"≻", (4,5):"≻", (5,6):">", (6,7):"≈", (7,8):"<", (8,9):"⊏", (9,10):"⊐"} #solutions:    Execution time:  milliseconds
    #pairs={(0,1):">", (1,2):"⊂",(3,4):"≻", (4,5):"≻", (5,6):">", (6,7):"≈", (7,8):"<", (8,9):"⊏", (9,10):"⊐", (10,11):"≈"} #solutions:    Execution time:  milliseconds
    Q0 = build_matrix(pairs, 10) 
    print(Q0)
    solutions = complete_all(Q0)
    print("solutions:", len(solutions))
    # print(solutions)
    if solutions:
        # print(compute_inconsistency_matrix(solutions[0]))
        # res = orders_for_all_solutions(solutions)
        counts = count_order_repetitions_from_solutions(solutions)
        print("count=",counts)
        # for k, r in enumerate(res):  # show first few
        #     print(f"\nSolution #{k+1}")
        #     print("Scores:", r["scores"])
        #     print("Order :", r["order"]) 
            
        #     print(solutions[858])
        end_time = time.time()     # <-- end timer
        total_elapsed = (end_time - start_time) * 1000
        print(f"Execution time: {total_elapsed:.2f} ms")
        # elapsed = timeit.timeit(lambda: complete_all(Q0), number=1)
        # #elapsed = timeit.timeit(lambda: count_order_repetitions_from_solutions(solutions), number=1)
        # print(f"Execution time: {elapsed * 1000:.3f} ms")







# pairs = {(0, 1): ">", (3, 4): "⊐", (1,3): "⊂"}  # 1-based indexes
# Q = build_matrix(pairs,5)     # infer n=5
# print(Q)


# Q = np.array([
#     ["≈", ">", "<"],
#     ["<", "≈", ">"],
#     [">", "<", "≈"]
# ], dtype=object)

# order, scores = order_with_ties(Q)
# print("Scores1:", scores)
# print("Order 1:", order)