from utils import delsarte_lp_bound, solve_lrc_z_lp
import math

test_cases = [
    (2, 3, 2, 1, 2, 2, "Binary Repetition Code", "1.0000 (M=2)"),
    (2, 5, 2, 2, 2, 2, "Binary LRC (a=2 Availability)", "2.0000 (M=4)"),
    (3, 8, 3, 2, 2, 3, "Binary LRC (a=2 Availability)", "2.0000 (M=9)"),
    (4, 5, 2, 2, 2, 2, "Binary LRC (a=2 Availability)", "2.0000 (M=16)"),
    (2, 9, 3, 1, 2, 2, "Binary LRC (a=2 Availability)", "3.0000 (M=8)"),
    (2, 14, 4, 2, 2, 2, "Binary LRC (a=2 Availability)", "6.0000 (M=64)"),
    (2, 10, 5, 1, 2, 3, "Binary LRC (a=2 Availability)", "2.0000 (M=4)"),
    (2, 15, 5, 1, 2, 3, "Binary LRC (a=2 Availability)", "3.0000 (M=8)"),
    (2, 6, 3, 1, 2, 3, "Binary LRC (a=2 Availability)", "1.0000 (M=2)"),
    (3, 3, 2, 1, 2, 2, "Ternary Repetition Code", "1.0000 (M=3)"),
    (3, 5, 2, 2, 2, 2, "Ternary LRC (a=2 Availability)", "2.0000 (M=9)"),
    (3, 7, 3, 1, 2, 3, "Ternary LRC (a=2 Availability)", "1.0000 (M=3)"),
    # (a+2)-block LP comparison cases
    (2, 7, 2, 2, 2, 2, "Binary (a+2)-block LP", "3.0000 (M=8)"),
    (2, 7, 3, 2, 2, 2, "Binary (a+2)-block LP", "3.0000 (M=8)"),
    (2, 8, 4, 2, 2, 2, "Binary (a+2)-block LP", "3.0000 (M=8)"),
    (2, 8, 2, 3, 2, 2, "Binary (a+2)-block LP", "4.0000 (M=16)"),
    (2, 8, 3, 3, 2, 2, "Binary (a+2)-block LP", "4.0000 (M=16)"),
    (2, 9, 2, 3, 2, 2, "Binary (a+2)-block LP", "5.0000 (M=32)"),
    (2, 9, 3, 3, 2, 2, "Binary (a+2)-block LP", "5.0000 (M=32)"),
    (2, 9, 4, 3, 2, 2, "Binary (a+2)-block LP", "4.0000 (M=16)"),
    (2, 11, 5, 2, 2, 2, "Binary (a+2)-block LP", "4.0000 (M=16)"),
    (2, 12, 6, 2, 2, 2, "Binary (a+2)-block LP", "4.0000 (M=16)"),
    (3, 7, 2, 2, 2, 2, "Ternary (a+2)-block LP", "3.0000 (M=27)"),
    (3, 7, 3, 2, 2, 2, "Ternary (a+2)-block LP", "3.0000 (M=27)"),
    (3, 7, 4, 2, 2, 2, "Ternary (a+2)-block LP", "3.0000 (M=27)"),
    (3, 8, 4, 2, 2, 2, "Ternary (a+2)-block LP", "3.0000 (M=27)"),
    (3, 8, 5, 2, 2, 2, "Ternary (a+2)-block LP", "3.0000 (M=27)"),
    (3, 9, 4, 2, 2, 2, "Ternary (a+2)-block LP", "4.0000 (M=81)"),
    (3, 9, 5, 2, 2, 2, "Ternary (a+2)-block LP", "3.0000 (M=27)"),
    (4, 7, 2, 2, 2, 2, "Quaternary (a+2)-block LP", "3.0000 (M=64)"),
    (4, 7, 3, 2, 2, 2, "Quaternary (a+2)-block LP", "3.0000 (M=64)"),
    (4, 7, 4, 2, 2, 2, "Quaternary (a+2)-block LP", "3.0000 (M=64)"),
    (4, 8, 4, 2, 2, 2, "Quaternary (a+2)-block LP", "3.0000 (M=64)"),
]

print("\n" + "=" * 95)
print(
    f"{'Remark':<32} | {'q':<2} | {'n':<2} | {'d':<2} | {'r':<2} | {'a':<2} | {'δ':<2} | {'Multiview':<18} | {'Delsarte LP':<12} | {'Paper Target'}"
)
print("=" * 95)

for q, n, d, r, a, delta, remark, expected in test_cases:
    max_k, max_C = solve_lrc_z_lp(q=q, n=n, d=d, r=r, delta=delta, a=a)
    delsarte_C = delsarte_lp_bound(q, n, d)

    if max_k is not None:
        k_str = f"k <= {max_k:.4f} (M<={max_C:.2f})"
    else:
        k_str = "Failed / Infeasible"

    if delsarte_C is not None:
        assert isinstance(delsarte_C, (int, float)) and delsarte_C > 0, "Delsarte LP bound returned a non-positive value."
        delsarte_k = math.log2(delsarte_C) / math.log2(q)
        delsarte_str = f"k <= {delsarte_k:.4f} (M<={delsarte_C:.2f})"
    else:
        delsarte_str = "Failed / Infeasible"

    print(
        f"--> [測試] {remark:<25} | {q:<2} | {n:<2} | {d:<2} | {r:<2} | {a:<2} | {delta:<2} | {k_str:<18} | {delsarte_str} | {expected}"
    )
print("=" * 95)