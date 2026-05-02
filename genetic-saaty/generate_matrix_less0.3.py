import numpy as np
import random
from openpyxl import Workbook

BASE_PATH = "d:/research/code/genetic-saaty/"

N = 8
TARGET_COUNT = 1121
CR_MIN = 0.10
CR_MAX = 0.30

OUTPUT_TXT = BASE_PATH + "random_n8_CR_010_030.txt"
OUTPUT_EXCEL = BASE_PATH + "random_n8_CR_010_030.xlsx"

RI = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,
    5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
    9: 1.45, 10: 1.49
}

SAATY_SCALE = [
    1/9, 1/8, 1/7, 1/6, 1/5, 1/4, 1/3, 1/2,
    1, 2, 3, 4, 5, 6, 7, 8, 9
]


def ahp_metrics(A):
    eigvals, eigvecs = np.linalg.eig(A)
    idx = np.argmax(eigvals.real)

    lambda_max = eigvals[idx].real

    weights = eigvecs[:, idx].real
    weights = np.abs(weights)
    weights = weights / np.sum(weights)

    CI = (lambda_max - A.shape[0]) / (A.shape[0] - 1)
    CR = CI / RI[A.shape[0]]

    return lambda_max, CI, CR, weights


def generate_random_reciprocal_matrix(n):
    A = np.ones((n, n))

    for i in range(n):
        for j in range(i + 1, n):
            value = random.choice(SAATY_SCALE)
            A[i, j] = value
            A[j, i] = 1 / value

    return A


def generate_filtered_matrices():
    matrices = []
    attempts = 0

    while len(matrices) < TARGET_COUNT:
        A = generate_random_reciprocal_matrix(N)
        lambda_max, CI, CR, weights = ahp_metrics(A)

        attempts += 1

        if CR_MIN < CR < CR_MAX:
            matrices.append((A, lambda_max, CI, CR, weights))
            print(f"Accepted {len(matrices)}/{TARGET_COUNT} | CR={CR:.6f}")

    print("Total attempts:", attempts)
    return matrices


def write_txt(results, output_txt):
    with open(output_txt, "w") as f:
        for idx, (A, lambda_max, CI, CR, weights) in enumerate(results, start=1):
            f.write(f"Matrix {idx}:\n")

            for row in A:
                f.write(" ".join(f"{x:.6f}" for x in row) + "\n")

            f.write("\n")


def write_excel(results, output_excel):
    wb = Workbook()
    ws = wb.active
    ws.title = "n8_CR_010_030"

    headers = ["Matrix"]
    headers += [f"A{i}{j}" for i in range(1, N + 1) for j in range(1, N + 1)]
    headers += ["lambda_max", "CI", "CR"]
    headers += [f"W{i}" for i in range(1, N + 1)]

    ws.append(headers)

    for idx, (A, lambda_max, CI, CR, weights) in enumerate(results, start=1):
        row = [idx]
        row += list(A.flatten())
        row += [lambda_max, CI, CR]
        row += list(weights)

        ws.append(row)

    wb.save(output_excel)


def main():
    results = generate_filtered_matrices()

    write_txt(results, OUTPUT_TXT)
    write_excel(results, OUTPUT_EXCEL)

    print("Done.")
    print("TXT saved:", OUTPUT_TXT)
    print("Excel saved:", OUTPUT_EXCEL)


if __name__ == "__main__":
    main()