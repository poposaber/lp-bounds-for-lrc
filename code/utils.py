import math
from itertools import product
from scipy.optimize import linprog
from typing import cast, Tuple, Optional
from scipy.special import comb
import cvxpy as cp

def krawtchouk(k, x, n, q=2):
    """計算一維 Krawtchouk 多項式 K_k(x; n)"""
    val = 0
    for j in range(k + 1):
        val += ((-1)**j) * ((q - 1)**(k - j)) * comb(x, j, exact=True) * comb(n - x, k - j, exact=True)
    return val

def singleton_bound(n, d):
    """Computes the Singleton Bound"""
    return 2**(n - d + 1)

def hamming_bound(n, d):
    """Computes the Hamming (Sphere-Packing) Bound"""
    t = (d - 1) // 2
    sphere_volume = sum(math.comb(n, i) for i in range(t + 1))
    return (2**n) // sphere_volume

def plotkin_bound(n, d):
    """Computes the Plotkin Bound if applicable"""
    # Plotkin bound applies when 2d > n
    if 2 * d > n:
        return (2 * d) // (2 * d - n)
    elif 2 * d == n:
        return 2 * n
    return "N/A"

def delsarte_lp_bound(q, n, d, print_solution=False):
    """Solves the Delsarte Linear Programming Bound"""
    # Variables: A_1, A_2, ..., A_n (A_0 is fixed to 1)
    # Objective: Maximize 1 + sum(A_i) -> Minimize -sum(A_i)
    c = [-1.0] * n
    
    # Bounds: A_i >= 0 for all i
    # Also enforce A_i = 0 for 0 < i < d
    x_bounds = []
    for i in range(1, n + 1):
        if i < d:
            x_bounds.append((0, 0))
        else:
            x_bounds.append((0, None))
            
    # Dual constraints based on Krawtchouk polynomials
    # Constraints: A^\perp_k = K_k(0) + sum_{i=1}^n A_i * K_k(i) >= 0
    # Since K_k(0) = (q - 1)^k * comb(n, k), this means:
    # - sum_{i=1}^n A_i * K_k(i) <= (q - 1)^k * comb(n, k)
    A_ub = []
    b_ub = []
    
    for k in range(1, n + 1):
        row = []
        for i in range(1, n + 1):
            row.append(-float(krawtchouk(k, i, n, q)))
        A_ub.append(row)
        b_ub.append(float((q - 1) ** k * math.comb(n, k)))
        
    # Solve the LP
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=x_bounds, method='highs')
    
    if res.success:
        # Maximum size is 1 + sum(A_i)
        if print_solution:
            print(f"Optimal A_i values: {[float(a) for a in res.x]}")
        return math.floor(1.0 - res.fun)
    else:
        return "Failed to optimize"  

def solve_lrc_z_lp(
    q: int, n: int, d: int, r: int, delta: int, a: int
) -> Tuple[Optional[float], Optional[float]]:
    """Solve the generalized availability LP using four-block masses Z."""
    R_0 = min(n, r + delta - 1)

    valid_t_tuples = []
    for t_tuple in product(range(delta, R_0 + 1), repeat=a):
        u_t = 1 + sum(t_h - 1 for t_h in t_tuple)
        if u_t <= n:
            valid_t_tuples.append(t_tuple)

    valid_keys = []
    for t_tuple in valid_t_tuples:
        u_t = 1 + sum(t_h - 1 for t_h in t_tuple)
        outside_len = n - u_t
        for j_tuple in product(*(range(t_h) for t_h in t_tuple)):
            for c in range(outside_len + 1):
                for b in (0, 1):
                    ell = sum(j_tuple) + c + b
                    if any(1 <= j_h + b < delta for j_h in j_tuple):
                        continue
                    if 0 < ell < d:
                        continue
                    valid_keys.append((t_tuple, j_tuple, c, b))

    Z = {
        key: cp.Variable(nonneg=True, name=f"Z_{key}")
        for key in valid_keys
    }
    constraints = []

    zero_keys = [
        key
        for key in valid_keys
        if all(j == 0 for j in key[1]) and key[2] == 0 and key[3] == 0
    ]
    if zero_keys:
        constraints.append(cp.sum([Z[key] for key in zero_keys]) == 1)

    ell_by_key = {
        key: sum(key[1]) + key[2] + key[3]
        for key in valid_keys
    }
    A_l_expr = {}
    for ell in range(n + 1):
        ell_keys = [key for key in valid_keys if ell_by_key[key] == ell]
        A_l_expr[ell] = cp.sum([Z[key] for key in ell_keys]) if ell_keys else 0

    for ell in range(1, n + 1):
        b1_keys = [
            key
            for key in valid_keys
            if ell_by_key[key] == ell and key[3] == 1
        ]
        if b1_keys:
            constraints.append(
                (ell / n) * A_l_expr[ell] == cp.sum([Z[key] for key in b1_keys])
            )
        elif not isinstance(A_l_expr[ell], (int, float)):
            constraints.append(A_l_expr[ell] == 0)

    for t_tuple in valid_t_tuples:
        u_t = 1 + sum(t_h - 1 for t_h in t_tuple)
        outside_len = n - u_t
        t_keys = [key for key in valid_keys if key[0] == t_tuple]
        for p_tuple in product(*(range(t_h) for t_h in t_tuple)):
            for v in range(outside_len + 1):
                for e in (0, 1):
                    fourier_sum = []
                    for key in t_keys:
                        _, j_tuple, c, b = key
                        coeff = krawtchouk(e, b, 1, q)
                        for h in range(a):
                            coeff *= krawtchouk(
                                p_tuple[h], j_tuple[h], t_tuple[h] - 1, q
                            )
                        coeff *= krawtchouk(v, c, outside_len, q)
                        fourier_sum.append(coeff * Z[key])
                    if fourier_sum:
                        constraints.append(cp.sum(fourier_sum) >= 0)

    for h in range(a):
        for t_h in range(delta, R_0 + 1):
            x_h_zero_keys = [
                key
                for key in valid_keys
                if key[0][h] == t_h and key[1][h] == 0 and key[3] == 0
            ]
            m_h_keys = [key for key in valid_keys if key[0][h] == t_h]
            x_h_zero = cp.sum([Z[key] for key in x_h_zero_keys]) if x_h_zero_keys else 0
            m_h = cp.sum([Z[key] for key in m_h_keys]) if m_h_keys else 0
            if not isinstance(m_h, (int, float)):
                constraints.append((q**t_h) * x_h_zero >= (q ** (delta - 1)) * m_h)

        all_x_h_zero_keys = [
            key for key in valid_keys if key[1][h] == 0 and key[3] == 0
        ]
        if all_x_h_zero_keys:
            constraints.append(cp.sum([Z[key] for key in all_x_h_zero_keys]) >= 1)

    for t_tuple in valid_t_tuples:
        u_t = 1 + sum(t_h - 1 for t_h in t_tuple)
        zero_j_b_keys = [
            key
            for key in valid_keys
            if key[0] == t_tuple
            and all(j == 0 for j in key[1])
            and key[3] == 0
        ]
        all_t_keys = [key for key in valid_keys if key[0] == t_tuple]
        X_t_zero = cp.sum([Z[key] for key in zero_j_b_keys]) if zero_j_b_keys else 0
        m_t = cp.sum([Z[key] for key in all_t_keys]) if all_t_keys else 0
        if not isinstance(m_t, (int, float)):
            constraints.append((q**u_t) * X_t_zero >= (q ** (delta - 1)) * m_t)

    X_0_0_keys = [
        key for key in valid_keys if all(j == 0 for j in key[1]) and key[3] == 0
    ]
    if X_0_0_keys:
        constraints.append(cp.sum([Z[key] for key in X_0_0_keys]) >= 1)

    objective = cp.Maximize(cp.sum(list(Z.values())))
    prob = cp.Problem(objective, constraints)
    prob.solve(solver=cp.SCIPY, scipy_options={"method": "highs"})

    if prob.status in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE]:
        max_C = cast(float, prob.value)
        max_k = math.log2(max_C) / math.log2(q)
        return max_k, max_C
    return None, None