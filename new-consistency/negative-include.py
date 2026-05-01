import sys
sys.stdout.reconfigure(encoding="utf-8")
# Simple additive model for all compositions of i and j

# Relation symbols
REL_POS = {  # positive
    1: "≈", 2: "⊏", 3: "⊂", 4: "<", 5: "≺"
}
REL_NEG = {  # negative (opposites)
    -1: "≈", -2: "⊐", -3: "⊃", -4: ">", -5: "≻"
}

# Allowed i, j, k values (no 0)
IDX_DOMAIN = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]

# Linear strength function:
# strn(1) = 0, strn(2) = 1, ..., strn(5) = 4
# strn(-i) = -strn(i)
def strn(i):
    s = abs(i) - 1
    if i > 0:
        return s
    else:
        return -s

# Margin (constant for all i, j)
MARGIN = 1.0

def mrg(i, j):
    return MARGIN

# Map strength -> list of indices that have that strength
S_TO_I = {}
for i in IDX_DOMAIN:
    s = strn(i)
    if s not in S_TO_I:
        S_TO_I[s] = []
    S_TO_I[s].append(i)

# Strength range (should be -4..4 for this scale)
MIN_S = min(S_TO_I.keys())
MAX_S = max(S_TO_I.keys())

def rel_symbol(i):
    """Return relation symbol (positive or negative)."""
    if i > 0:
        return REL_POS[i]
    else:
        return REL_NEG[i]

def canonicalize_zero(k_list):
    """If we have both +1 and -1, keep only +1 (≈)."""
    k_list = sorted(set(k_list))
    if 1 in k_list and -1 in k_list:
        k_list.remove(-1)
    return k_list

def allowed_k_for(i, j):
    """
    Additive model:
      strn(j) - mrg(i,j) <= strn(i) + strn(k) <= strn(j) + mrg(i,j)

    We solve this for strn(k), check bounds, and:
      - if both bounds are outside [-4,4]  -> illegal
      - else clamp to [-4,4] and find all k with strengths in the interval
    """
    margin = mrg(i, j)

    # Inequalities for strn(i) + strn(k)
    L = strn(j) - margin
    U = strn(j) + margin

    # Now for strn(k):
    L_k = L - strn(i)
    U_k = U - strn(i)

    # ---- NEW PART: check if BOTH bounds are out of range ----
    lower_out = (L_k < MIN_S) or (L_k > MAX_S)
    upper_out = (U_k < MIN_S) or (U_k > MAX_S)

    if lower_out and upper_out:
        # both bounds are outside [-4,4] -> illegal combination
        return [], (L_k, U_k), True

    # ---- otherwise, clamp to scale support ----
    cl_L_k = max(L_k, MIN_S)
    cl_U_k = min(U_k, MAX_S)

    # If clamped interval is empty, still illegal
    if cl_L_k > cl_U_k:
        return [], (L_k, U_k), True

    # Collect all k whose strength lies in [cl_L_k, cl_U_k]
    k_list = []
    for s_val, indices in S_TO_I.items():
        if cl_L_k <= s_val <= cl_U_k:
            k_list.extend(indices)

    k_list = canonicalize_zero(k_list)
    return k_list, (L_k, U_k), False

def rule_text(i, j, k_list, illegal):
    """Pretty-print a rule like: a R_i b ∧ a R_j c ⇒ b R_k c ..."""
    lhs = f"a {rel_symbol(i)} b  ∧  a {rel_symbol(j)} c"
    if illegal or not k_list:
        return f"{lhs}  ⇒  illegal"
    rhs_parts = [f"b {rel_symbol(k)} c" for k in sorted(k_list, key=lambda x: (strn(x), x))]
    rhs = " ∨ ".join(rhs_parts)
    return f"{lhs}  ⇒  {rhs}"

if __name__ == "__main__":
    # Generate rules for ALL compositions (i, j)
    for i in IDX_DOMAIN:
        for j in IDX_DOMAIN:
            k_list, bounds, illegal = allowed_k_for(i, j)
            print(rule_text(i, j, k_list, illegal))
            # If you also want to see numeric bounds, uncomment:
            # print("   bounds for strn(k):", bounds, " illegal:", illegal)

# if __name__ == "__main__":
#     # Open results.txt in UTF-8 and write all rules there
#     with open("results.txt", "w", encoding="utf-8") as f:
#         for i in IDX_DOMAIN:
#             for j in IDX_DOMAIN:
#                 k_list, bounds, illegal = allowed_k_for(i, j)
#                 line = rule_text(i, j, k_list, illegal)
#                 print(line, file=f)

#     print("Done. Rules saved to results.txt")
