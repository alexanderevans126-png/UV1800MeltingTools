# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 14:25:50 2026

@author: alexa

Nearest-neighbor extinction coefficient calculator at 260 nm.

Formula:
epsilon = 2 * sum(all dinucleotide epsilon values)
          - sum(mononucleotide epsilon values of internal bases)
"""

NN_DNA = {
    "AA": 13650, "TT": 8610,
    "AT": 11420, "TA": 11780,
    "CA": 10670, "TG": 9700,
    "GT": 10220, "AC": 10670,
    "CT": 7600, "AG": 12790,
    "GA": 12920, "TC": 8150,
    "CG": 9390, "GC": 9190,
    "GG": 11430, "CC": 7520,
}

NN_RNA = {
    "AA": 13650, "UU": 10110,
    "AU": 12140, "UA": 12520,
    "CA": 10670, "UG": 10400,
    "GU": 10960, "AC": 10670,
    "CU": 8370, "AG": 12790,
    "GA": 12920, "UC": 8900,
    "CG": 9390, "GC": 9190,
    "GG": 11430, "CC": 7520,
}

BASES = {
    "A": 15340,
    "C": 7600,
    "G": 12160,
    "T": 8700,
    "U": 10210,
}


def epsilon_nn(seq: str, molecule: str = "DNA") -> int:
    """
    Calculate nearest-neighbor extinction coefficient for a DNA or RNA sequence.

    Parameters
    ----------
    seq:
        DNA or RNA sequence written 5' to 3'.
    molecule:
        Either "DNA" or "RNA".

    Returns
    -------
    int
        Extinction coefficient in M^-1 cm^-1.
    """
    seq = seq.upper().strip()
    molecule = molecule.upper().strip()

    if len(seq) == 0:
        raise ValueError("Empty sequence")

    if molecule == "DNA":
        nn_values = NN_DNA
    elif molecule == "RNA":
        nn_values = NN_RNA
    else:
        raise ValueError("molecule must be 'DNA' or 'RNA'")

    if len(seq) == 1:
        return BASES[seq]

    dimer_sum = sum(nn_values[seq[i:i + 2]] for i in range(len(seq) - 1))
    internal_sum = sum(BASES[base] for base in seq[1:-1])

    return 2 * dimer_sum - internal_sum