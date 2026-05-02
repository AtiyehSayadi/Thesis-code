import re
import numpy as np
from openpyxl import Workbook
from main_gp import main

BASE_PATH = "d:/research/code/genetic-saaty/"

INPUT_FILE = BASE_PATH + "random_n8_CR_010_030.txt"
OUTPUT_TXT = BASE_PATH + "ga_reduced_n8_010_030_matrices.txt"
OUTPUT_EXCEL = BASE_PATH + "ga_reduced_n8_010_030_matrices.xlsx"

RI = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,
    5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
    9: 1.45, 10: 1.49
}


def read_matrices_from_txt(file_path, n=8):
    with open(file_path, "r") as f:
        text = f.read()

    blocks = re.split(r"Matrix\s+\d+:", text)
    matrices = []

    for block in blocks:
        nums = re.findall(r"[-+]?\d*\.\d+|\d+", block)
        nums = [float(x) for x in nums]

        if len(nums) == n * n:
            matrices.append(np.array(nums).reshape(n, n))

    return matrices


def ahp_metrics(A):
    n = A.shape[0]

    eigvals, eigvecs = np.linalg.eig(A)
    idx = np.argmax(eigvals.real)

    lambda_max = eigvals[idx].real

    weights = eigvecs[:, idx].real
    weights = np.abs(weights)
    weights = weights / np.sum(weights)

    CI = (lambda_max - n) / (n - 1)
    CR = CI / RI[n]

    return lambda_max, CI, CR, weights


def write_txt(matrices, output_file):
    with open(output_file, "w") as f:
        for idx, A in enumerate(matrices, start=1):
            f.write(f"Matrix {idx}:\n")

            for row in A:
                f.write(" ".join(f"{x:.6f}" for x in row) + "\n")

            f.write("\n")


def write_excel(matrices, output_file, n=8):
    wb = Workbook()
    ws = wb.active
    ws.title = "GA_Reduced_n8"

    headers = ["Matrix"]
    headers += [f"A{i}{j}" for i in range(1, n + 1) for j in range(1, n + 1)]
    headers += ["lambda_max", "CI", "CR"]
    headers += [f"W{i}" for i in range(1, n + 1)]
    headers += ["Generations"] 

    ws.append(headers)

    for idx, (A, generations) in enumerate(matrices, start=1):
        lambda_max, CI, CR, weights = ahp_metrics(A)

        row = [idx]
        row += list(A.flatten())
        row += [lambda_max, CI, CR]
        row += list(weights)
        row += [generations]
        ws.append(row)

    wb.save(output_file)


def process_all():
    original_matrices = read_matrices_from_txt(INPUT_FILE, n=8)

    reduced_matrices = []

    for i, A in enumerate(original_matrices, start=1):
        print(f"Processing matrix {i}/{len(original_matrices)}")

        best_min, generations, best_matrix = main(A)
        reduced_matrices.append((best_matrix, generations))

    write_txt([A for A, _ in reduced_matrices], OUTPUT_TXT)
    write_excel(reduced_matrices, OUTPUT_EXCEL, n=8)

    print("Done.")
    print("Reduced matrices saved to:")
    print(OUTPUT_TXT)
    print(OUTPUT_EXCEL)


if __name__ == "__main__":
    process_all()