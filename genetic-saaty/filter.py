import re
import numpy as np
from openpyxl import Workbook

BASE_PATH = "d:/research/code/genetic-saaty/"

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
            matrices.append(np.array(nums).reshape(n, n))

    return matrices


def ahp_metrics(A):
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


def filter_matrices(matrices):
    filtered = []

    for A in matrices:
        lambda_max, CI, CR, weights = ahp_metrics(A)

        if 0.10 < CR < 0.80:
            filtered.append((A, lambda_max, CI, CR, weights))

    return filtered


def write_txt(filtered, output_txt):
    with open(output_txt, "w") as f:
        for idx, (A, lambda_max, CI, CR, weights) in enumerate(filtered, start=1):
            f.write(f"Matrix {idx}:\n")

            for row in A:
                f.write(" ".join(f"{x:.6f}" for x in row) + "\n")
            f.write("\n")

            


def write_excel(filtered_n4, filtered_n8, output_excel):
    wb = Workbook()
    wb.remove(wb.active)

    for sheet_name, filtered, n in [
        ("n4_filtered", filtered_n4, 4),
        ("n8_filtered", filtered_n8, 8)
    ]:
        ws = wb.create_sheet(sheet_name)

        headers = ["Matrix"]
        headers += [f"A{i}{j}" for i in range(1, n + 1) for j in range(1, n + 1)]
        headers += ["lambda_max", "CI", "CR"]
        headers += [f"W{i}" for i in range(1, n + 1)]

        ws.append(headers)

        for idx, (A, lambda_max, CI, CR, weights) in enumerate(filtered, start=1):
            row = [idx]
            row += list(A.flatten())
            row += [lambda_max, CI, CR]
            row += list(weights)

            ws.append(row)

    wb.save(output_excel)


def main():
    n4_txt = BASE_PATH + "10000_scale9_size4.txt"
    n8_txt = BASE_PATH + "10000_scale9_size8.txt"

    matrices_n4 = read_matrices_from_txt(n4_txt, 4)
    matrices_n8 = read_matrices_from_txt(n8_txt, 8)

    filtered_n4 = filter_matrices(matrices_n4)
    filtered_n8 = filter_matrices(matrices_n8)

    write_txt(filtered_n4, BASE_PATH + "filtered_n4_CR_010_080.txt")
    write_txt(filtered_n8, BASE_PATH + "filtered_n8_CR_010_080.txt")

    write_excel(
        filtered_n4,
        filtered_n8,
        BASE_PATH + "filtered_matrices_CR_010_080.xlsx"
    )

    print("Done.")
    print("Original n=4:", len(matrices_n4))
    print("Filtered n=4:", len(filtered_n4))
    print("Original n=8:", len(matrices_n8))
    print("Filtered n=8:", len(filtered_n8))


if __name__ == "__main__":
    main()