import numpy as np

# Saaty's Random Index values
RI = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,
    5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
    9: 1.45, 10: 1.49
}

def priority_vector(A):
    """
    Principal eigenvector method.
    Returns normalized priority vector w and lambda_max.
    """
    eigvals, eigvecs = np.linalg.eig(A)
    max_index = np.argmax(eigvals.real)

    lambda_max = eigvals[max_index].real
    w = eigvecs[:, max_index].real

    # make eigenvector positive
    w = np.abs(w)
    w = w / np.sum(w)

    return w, lambda_max


def consistency_ratio(A):
    """
    Calculate Saaty's CI and CR for a reciprocal pairwise comparison matrix.
    """
    A = np.array(A, dtype=float)
    n = A.shape[0]

    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix must be square.")

    if n not in RI:
        raise ValueError("RI value not available for this n.")

    w, lambda_max = priority_vector(A)

    CI = (lambda_max - n) / (n - 1)

    if RI[n] == 0:
        CR = 0.0
    else:
        CR = CI / RI[n]

    return {
        "n": n,
        "lambda_max": lambda_max,
        "CI": CI,
        "CR": CR,
        "priority_vector": w
    }


# Example matrix for n = 4
A4 = np.array([
    [1,       5,       5,       0.111111],
    [0.2,     1,       2,       3       ],
    [0.2,     0.5,     1,       6       ],
    [9,       0.333333,0.166667,1       ]
])

result4 = consistency_ratio(A4)
print("n=4")
print("lambda_max:", result4["lambda_max"])
print("CI:", result4["CI"])
print("CR:", result4["CR"])
print("priority vector:", result4["priority_vector"])


# Example matrix for n = 8
A8 = np.array([
    [1,   3,   5,   7,   9,   3,   5,   7],
    [1/3, 1,   2,   4,   6,   2,   3,   5],
    [1/5, 1/2, 1,   3,   5,   2,   4,   6],
    [1/7, 1/4, 1/3, 1,   3,   1/2, 2,   4],
    [1/9, 1/6, 1/5, 1/3, 1,   1/4, 1/2, 2],
    [1/3, 1/2, 1/2, 2,   4,   1,   3,   5],
    [1/5, 1/3, 1/4, 1/2, 2,   1/3, 1,   3],
    [1/7, 1/5, 1/6, 1/4, 1/2, 1/5, 1/3, 1]
])

result8 = consistency_ratio(A8)
print("\nn=8")
print("lambda_max:", result8["lambda_max"])
print("CI:", result8["CI"])
print("CR:", result8["CR"])
print("priority vector:", result8["priority_vector"])