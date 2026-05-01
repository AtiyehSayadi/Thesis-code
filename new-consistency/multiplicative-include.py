# ------------------------------------------------------------
# Multiplicative (geometric) model for all compositions of i, j
# ------------------------------------------------------------

# Relation symbols
REL_POS = {
    1: "≈", 2: "⊏", 3: "⊂", 4: "<", 5: "≺"
}
REL_NEG = {
    -1: "≈", -2: "⊐", -3: "⊃", -4: ">", -5: "≻"
}

# All allowed indices
IDX_DOMAIN = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]


def rel_symbol(i):
    return REL_POS[i] if i > 0 else REL_NEG[i]


# ------------------------------------------------------------
# 1. Multiplicative scale (from the paper)
#    strn(1)=1, strn(i)=α^(i-1), strn(-i)=1/strn(i)
# ------------------------------------------------------------

ALPHA = 2.0   # You may change this (paper uses values around 1.11, 1.29, etc.)


def strn_mult(i):
    """Geometric strength used in Eq. (6)–(7)."""
    power = abs(i) - 1
    base = ALPHA ** power
    return base if i > 0 else 1.0 / base


# Margin for multiplicative model (constant α in the paper)
def mrg_mult(i, j):
    return ALPHA


# Precompute strengths and allowed minimum/maximum values
S_MULT = {idx: strn_mult(idx) for idx in IDX_DOMAIN}
MIN_S = min(S_MULT.values())     # e.g. 1/16 when α=2
MAX_S = max(S_MULT.values())     # e.g. 16   when α=2


# ------------------------------------------------------------
# 2. Solve Equation (6) and (7) for k, without 1 ≤ i < j
# ------------------------------------------------------------

def allowed_k_multiplicative(i, j):
    """
    Equation (6) for i != j:
       strn(j)/α <= strn(i)*strn(k) <= strn(j)*α

    Equation (7) for i == j:
       1/α <= strn(k) <= α

    The bounds are clamped to [MIN_S, MAX_S].
    If BOTH original bounds are out of range, the combination is illegal.
    """

    margin = mrg_mult(i, j)

    if i == j:
        # Equation (7)
        L_k = 1.0 / margin
        U_k = margin
    else:
        # Equation (6)
        s_i = S_MULT[i]
        s_j = S_MULT[j]
        L_prod = s_j / margin
        U_prod = s_j * margin
        L_k = L_prod / s_i
        U_k = U_prod / s_i

    # Check “both bounds outside range” → illegal
    lower_out = (L_k < MIN_S) or (L_k > MAX_S)
    upper_out = (U_k < MIN_S) or (U_k > MAX_S)
    if lower_out and upper_out:
        return [], (L_k, U_k), True

    # Clamp to allowed geometric scale
    cl_L_k = max(L_k, MIN_S)
    cl_U_k = min(U_k, MAX_S)

    # Empty interval → illegal
    if cl_L_k > cl_U_k:
        return [], (L_k, U_k), True

    # Collect all k whose strength lies in [cl_L_k, cl_U_k]
    k_list = []
    for idx, strength in S_MULT.items():
        if cl_L_k <= strength <= cl_U_k:
            k_list.append(idx)

    return unique_relations(sorted(set(k_list))), (L_k, U_k), False


# ------------------------------------------------------------
# 3. Rule text
# ------------------------------------------------------------
def unique_relations(k_list):
    """Remove duplicates when different k map to the same relation symbol."""
    seen = set()
    result = []
    for k in k_list:
        sym = rel_symbol(k)
        if sym not in seen:
            seen.add(sym)
            result.append(k)
    return result

def rule_text(i, j, k_list, illegal):
    lhs = f"a {rel_symbol(i)} b  ∧  a {rel_symbol(j)} c"
    if illegal or not k_list:
        return f"{lhs} ⇒ illegal"
    rhs = " ∨ ".join(f"b {rel_symbol(k)} c" for k in k_list)
    return f"{lhs} ⇒ {rhs}"


# ------------------------------------------------------------
# 4. MAIN: write all multiplicative rules to UTF-8 file
# ------------------------------------------------------------

if __name__ == "__main__":
    with open(r"d:\research\code\new-consistency\results_multiplicative.txt", "w", encoding="utf-8") as f:
        for i in IDX_DOMAIN:
            for j in IDX_DOMAIN:
                k_list, bounds, illegal = allowed_k_multiplicative(i, j)
                print(rule_text(i, j, k_list, illegal), file=f)

    print("Done. Multiplicative rules saved to results_multiplicative.txt")
