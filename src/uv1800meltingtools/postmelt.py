# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 14:56:31 2026

@author: alexa
"""

import os
import re
from pathlib import Path

import numpy as np
import pandas as pd


def natural_sort_key(s):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def read_txt(file_path):
    df = pd.read_csv(file_path, header=None)
    df = df.iloc[:, [0, 1]].copy()
    df[0] = pd.to_numeric(df[0], errors="coerce")
    df[1] = pd.to_numeric(df[1], errors="coerce")
    df = df.dropna().reset_index(drop=True)
    return df


def analyze_post_melt(
    directory_path,
    experiment_name,
    concentrations,
    wells=8,
    blanks=1,
    pathlength=1.0,
):
    """
    Process UV1800 post-melt .txt files and generate:
    - MeltWin .prn file
    - Excel summary file
    - MeltR .csv file

    Parameters
    ----------
    directory_path : str or Path
        Folder containing UV1800 .txt files.
    experiment_name : str
        Name used for output files and column headers.
    concentrations : list[float]
        Concentrations used for sample wells.
    wells : int
        Total number of wells/files including blanks.
    blanks : int
        Number of blank wells.
    pathlength : float
        Pathlength used in MeltR output.

    Returns
    -------
    dict
        Paths to generated output files.
    """
    directory_path = Path(directory_path)

    if not directory_path.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory_path}")

    txt_files = sorted(
        [f for f in os.listdir(directory_path) if f.endswith(".txt")],
        key=natural_sort_key,
    )

    if not txt_files:
        raise FileNotFoundError(f"No .txt files found in: {directory_path}")

    headers = (
        ["Temperature"]
        + [f"{experiment_name} {c} uM" for c in concentrations]
        + [f"PBS Blank {i + 1}" for i in range(blanks)]
    )

    all_data = pd.DataFrame()
    all_mw_data = pd.DataFrame()

    for i, filename in enumerate(txt_files):
        file_path = directory_path / filename
        df = read_txt(file_path)

        if i == 0:
            all_data = pd.concat([all_data, df.iloc[:, 0]], axis=1)

        all_data = pd.concat([all_data, df.iloc[:, 1]], axis=1)
        all_mw_data = pd.concat([all_mw_data, df.iloc[:, [0, 1]]], axis=1)

    # Save MeltWin PRN
    prn_path = directory_path / f"{experiment_name}.prn"

    with open(prn_path, "w") as f:
        for row in all_mw_data.values:
            line = " ".join(f"{x:.3f}" for x in row)
            f.write(line + "\n")

    # Main dataframe
    all_data.columns = headers[: all_data.shape[1]]
    df_melt = all_data.copy()

    # Normalize
    norm = df_melt.to_numpy().copy()
    norm[:, 1 : wells + 1] -= norm[0, 1 : wells + 1]

    norm_df = pd.DataFrame(norm, columns=headers[: norm.shape[1]])

    # Blank subtraction
    if blanks == 1:
        blank = norm[:, [-1]]
        blank_sub = norm[:, : wells - blanks + 1] - blank
    else:
        avg_blank = np.mean(norm[:, -blanks:], axis=1, keepdims=True)
        blank_sub = norm[:, : wells - blanks + 1] - avg_blank

    sub_df = pd.DataFrame(blank_sub, columns=headers[: wells - blanks + 1])

    # Save Excel
    empty_cols = pd.DataFrame(columns=["", ""])
    final = pd.concat([df_melt, empty_cols, norm_df, empty_cols, sub_df], axis=1)

    excel_path = directory_path / f"{experiment_name}.xlsx"
    final.to_excel(excel_path, index=False)

    # Save MeltR CSV
    samples = []

    for sample_number, col in enumerate(headers[1 : df_melt.shape[1]], start=1):
        size = df_melt.shape[0]

        sample_df = pd.DataFrame(
            {
                "Sample": sample_number,
                "Pathlength": pathlength,
                "Temperature": df_melt["Temperature"],
                "Absorbance": df_melt[col],
            }
        )

        samples.append(sample_df)

    meltr_df = pd.concat(samples, ignore_index=True)

    meltr_path = directory_path / f"{experiment_name}MeltR.csv"
    meltr_df.to_csv(meltr_path, index=False)

    return {
        "txt_files": txt_files,
        "prn_path": prn_path,
        "excel_path": excel_path,
        "meltr_path": meltr_path,
    }