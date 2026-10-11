# Multi-View Block Distance Distributions and Linear Programming Bounds for Locally Recoverable Codes

This repository contains the source code and supporting materials for the study of upper bounds on the size of locally recoverable codes (LRCs) using multi-view block distance distributions and linear programming (LP) formulations.

The project focuses on numerical experiments and bound computations for q-ary LRCs with availability, comparing generalized LP-based upper bounds against classical bounds such as the Singleton, Hamming, Plotkin, and Delsarte bounds.

## Overview

Locally recoverable codes are designed so that individual erased code symbols can be repaired by accessing only a small subset of coordinates. In the presence of availability constraints, the distance distribution and block-structure of the code become highly relevant for deriving tighter upper bounds.

This repository implements the computational framework used to study those bounds and to evaluate specific parameter choices numerically.

## Structure of This Repository

- `code/` — Python implementation of the LP-based bound calculations and comparison scripts.
- `paper/` — PDF copy of our paper on ArXiv.
- `slide/` — slides for presenting the work.

## Requirements

- Python 3.10 or newer
- `scipy`
- `cvxpy`

Install dependencies with:

```bash
py -3 -m pip install scipy cvxpy
```

## Quick Start

From the repository root:

```bash
cd code
py -3 lrc_lp_bound.py
py -3 bound_compare.py
```

These scripts evaluate representative parameter sets and print the resulting LP-based bounds alongside classical bounds and known benchmark values.

## Core Implementation

The implementation in `code/utils.py` includes:

- `solve_lrc_z_lp(q, n, d, r, delta, a)` — solves the generalized availability LP formulation using multi-view block mass variables.
- `delsarte_lp_bound(q, n, d)` — computes the Delsarte linear programming bound.
- `singleton_bound(n, d)` — singleton bound.
- `hamming_bound(n, d)` — Hamming bound.
- `plotkin_bound(n, d)` — Plotkin bound.

The script `code/lrc_lp_bound.py` runs a suite of test cases for LRC parameter choices, while `code/bound_compare.py` compares the LP bound with classic coding-theory bounds for selected examples.

## Parameters

The main LP routine is parameterized by:

- `q` — alphabet size,
- `n` — code length,
- `d` — minimum distance,
- `r` — local repair parameter,
- `delta` — local distance threshold,
- `a` — availability parameter.

These parameters correspond to the structural assumptions used in the bound derivation.

## Notes

This code is intended for research and numerical experimentation rather than production deployment. It is best suited for reproducing the computational examples in the corresponding paper and exploring related parameter regimes.