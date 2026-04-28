# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 14:24:00 2026

@author: alexa

Concentration calculator using Beer-Lambert law.

A = epsilon * concentration * pathlength
concentration = A / (epsilon * pathlength)
"""

import numpy as np


def concentration_limits(
    epsilon: float,
    pathlength: float = 1.0,
    low_absorbance: float = 0.4,
    high_absorbance: float = 1.8,
) -> tuple[float, float]:
    """
    Calculate low and high concentration limits in M.
    """
    low_conc = low_absorbance / (epsilon * pathlength)
    high_conc = high_absorbance / (epsilon * pathlength)

    return low_conc, high_conc


def concentration_series(
    epsilon: float,
    num_concentrations: int,
    pathlength: float = 1.0,
    low_absorbance: float = 0.4,
    high_absorbance: float = 1.8,
) -> list[float]:
    """
    Calculate log-spaced concentration values in uM.
    """
    low_conc, high_conc = concentration_limits(
        epsilon=epsilon,
        pathlength=pathlength,
        low_absorbance=low_absorbance,
        high_absorbance=high_absorbance,
    )

    low_log = np.log10(low_conc)
    high_log = np.log10(high_conc)

    log_conc = np.linspace(low_log, high_log, num_concentrations)

    concentrations_um = [(10 ** value) * 1_000_000 for value in log_conc]

    return [round(float(value), 3) for value in concentrations_um]