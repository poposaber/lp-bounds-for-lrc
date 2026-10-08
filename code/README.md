# Code of Implementation for Upper Bounds

This folder contains the computational implementation used to evaluate LP-based upper bounds for locally recoverable codes.

## Introduction

The code studies how linear programming formulations can be used to bound the maximum size of a code under locality and availability constraints. In particular, the implementation solves a generalized LP problem based on block-distance distributions and compares the resulting numerical bounds against classical code bounds.

## Files

- `utils.py` — core numerical routines and helper functions.
- `lrc_lp_bound.py` — batch evaluation of representative LRC test cases.
- `bound_compare.py` — comparison with classical bounds and known code sizes.

## Main Functions

In `utils.py`:

- `krawtchouk(k, x, n, q=2)` computes the Krawtchouk polynomial values used in the LP formulations.
- `singleton_bound(n, d)` returns the Singleton bound.
- `hamming_bound(n, d)` returns the Hamming bound.
- `plotkin_bound(n, d)` returns the Plotkin bound when applicable.
- `delsarte_lp_bound(q, n, d, print_solution=False)` solves the Delsarte LP relaxation for codes with distance `d`.
- `solve_lrc_z_lp(q, n, d, r, delta, a)` solves the generalized availability LP used for the LRC setting.

## How to Use

Run the scripts directly with Python:

```bash
cd code
py -3 lrc_lp_bound.py
py -3 bound_compare.py
```

You can also import functions from `utils.py` in your own experiments:

```python
from utils import solve_lrc_z_lp, delsarte_lp_bound

max_k, max_C = solve_lrc_z_lp(q=2, n=10, d=5, r=1, delta=2, a=3)
print(max_k, max_C)
print(delsarte_lp_bound(2, 10, 5))
```

## Expected Behavior

The scripts print a table of parameter choices and the corresponding upper bounds. Typical output includes the code parameters `(q, n, d, r, a, delta)` and computed bound values, such as comparisons between the multiview LP bound and Delsarte's LP bound for a given code family.

## Dependencies

This code relies on:

- `scipy`
- `cvxpy`

Install them using:

```bash
py -3 -m pip install scipy cvxpy
```

## Notes

- The implementation is research-oriented and intended for exploration of bound behavior under various parameters.
- The LP formulation is computationally heavier than classical bound calculations, especially for larger values of `n`, `a`, and `delta`.
- The equations and optimization structure are designed to reflect multi-view block distance distributions for LRCs with availability constraints.