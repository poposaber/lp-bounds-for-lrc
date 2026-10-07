from utils import delsarte_lp_bound, hamming_bound, plotkin_bound, singleton_bound

# Database of known optimal sizes A(n, d) for the requested examples
known_examples = {
    (5, 3): "4 (e.g., Repetition extended / Hamming subcode)",
    (6, 3): "8 (e.g., Punctured Hamming code)",
    (7, 3): "16 (The [7, 4, 3] Hamming Code)",
    (7, 4): "8 (The [7, 3, 4] Simplex Code)",
    (8, 4): "16 (The [8, 4, 4] Extended Hamming Code)",
    (9, 4): "20 (The Best Code / Nonlinear)",
    (10, 4): "40 (The Best Code / Nonlinear)", 
    (11, 4): "72 (The Best Code / Nonlinear)",
    (12, 4): "144",
    (13, 4): "256",
}

examples = [(5, 3), (7, 4), (9, 4), (11, 4), (13, 4)]

print(f"{'n':<4}{'d':<4}{'LP Bound':<12}{'Hamming':<10}{'Plotkin':<10}{'Singleton':<12}{'Known A(n,d)'}")
print("-" * 90)
for n, d in examples:
    lp = delsarte_lp_bound(2, n, d)
    ham = hamming_bound(n, d)
    plot = plotkin_bound(n, d)
    sing = singleton_bound(n, d)
    known = known_examples.get((n, d), "Unknown")
    print(f"{n:<4}{d:<4}{lp:<12}{ham:<10}{plot:<10}{sing:<12}{known}")