# UV1800MeltingTools

Tools for calculating oligonucleotide extinction coefficients and concentration ranges for UV–Vis optical melting experiments on the Shimadzu UV-1800.

---

## Overview

This package provides simple utilities for setting up optical melting experiments, including:

- Calculation of nearest-neighbor extinction coefficients for DNA and RNA sequences
- Generation of an evenly spaced concentration series on the log scale based on the Beer–Lambert law
- Designed for use with UV–Vis instruments such as the Shimadzu UV-1800

---

## Usage

### 1. Concentration Series

Generate a log-spaced set of concentrations within an absorbance range.

from uv1800meltingtools.concentration import concentration_series

# Example: epsilon = 592540 M^-1 cm^-1, 5 concentrations
values = concentration_series(592540, 5)

print(values)

---

### 2. Extinction Coefficient Calculation

Calculate the nearest-neighbor extinction coefficient for a DNA or RNA sequence.

from uv1800meltingtools.extinctioncoeff import epsilon_nn

eps = epsilon_nn("ATGC", molecule="DNA")

print(eps)

---

## Scientific Background

### Beer–Lambert Law

The concentration calculations are based on:

A = ε · C · l

where:

- A = absorbance  
- ε = extinction coefficient (M⁻¹ cm⁻¹)  
- C = concentration (M)  
- l = pathlength (cm)

---

### Nearest-Neighbor Method

Extinction coefficients are calculated using the nearest-neighbor model:

ε = 2 × Σ(dinucleotide ε) − Σ(internal base ε)

Values are based on literature parameters (e.g., Tinoco et al., 1989).

---

## Installation

Clone the repository and install locally:

pip install -e .

---

## Requirements

- Python ≥ 3.9  
- numpy  

---

## Author

Alex Evans