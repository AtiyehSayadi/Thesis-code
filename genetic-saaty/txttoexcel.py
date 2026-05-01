import re
import numpy as np
import pandas as pd

RI = {
    1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,
    5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
    9: 1.45, 10: 1.49
}

def read_matrices_from_txt(file_path, n):
    with open(file_path, "r") as f:
        text = f.read()

    blocks = re.split(r"Matrix\s+\d+:", text)
    matrices = []

    for block in blocks:
        nums = re.findall(r"[-+]?\d*\.\d+|\d+", block)
        nums = [float(x) for x in nums]

        if len(nums) == n * n:
            A = np.array(nums).reshape(n, n)
            matrices.append(A)

    return matrices


def ahp_calculations(A):
    n = A.shape[0]

    eigvals, eigvecs = np.linalg.eig(A)
    idx = np.argmax(eigvals.real)

    lambda_max = eigvals[idx].real
    weights = eigvecs[:, idx].real
    weights = np.abs(weights)
    weights = weights / weights.sum()

    CI = (lambda_max - n) / (n - 1)
    CR = CI / RI[n]

    return lambda_max, CI, CR, weights


def build_excel_table(matrices, n):
    rows = []

    matrix_cols = [f"A{i}{j}" for i in range(1, n + 1) for j in range(1, n + 1)]
    weight_cols = [f"W{i}" for i in range(1, n + 1)]

    for k, A in enumerate(matrices, start=1):
        lambda_max, CI, CR, weights = ahp_calculations(A)

        row = {"Matrix": k}

        flat_values = A.flatten()
        for col, val in zip(matrix_cols, flat_values):
            row[col] = val

        row["lambda_max"] = lambda_max
        row["CI"] = CI
        row["CR"] = CR

        for col, val in zip(weight_cols, weights):
            row[col] = val

        row["Acceptable_CR"] = "Yes" if CR < 0.10 else "No"

        rows.append(row)

    return pd.DataFrame(rows)


def create_excel_file(n4_txt, n8_txt, output_file):
    matrices_n4 = read_matrices_from_txt(n4_txt, 4)
    matrices_n8 = read_matrices_from_txt(n8_txt, 8)

    df_n4 = build_excel_table(matrices_n4, 4)
    df_n8 = build_excel_table(matrices_n8, 8)

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df_n4.to_excel(writer, sheet_name="n4", index=False)
        df_n8.to_excel(writer, sheet_name="n8", index=False)

    print("Excel file created:", output_file)
    print("n=4 matrices:", len(df_n4))
    print("n=8 matrices:", len(df_n8))


create_excel_file(
    n4_txt="d:/research/code/genetic-saaty/10000_scale9_size4.txt",
    n8_txt="d:/research/code/genetic-saaty/10000_scale9_size8.txt",
    output_file="d:/research/code/genetic-saaty/Matrices_with_AHP_results.xlsx"
)